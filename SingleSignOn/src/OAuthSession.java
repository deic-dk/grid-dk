import java.security.*;
import java.io.*;
import java.util.Hashtable;
import java.net.URISyntaxException;
import java.io.IOException;
import java.security.cert.*;

import javax.net.ssl.*;

import edu.stanford.ejalbert.BrowserLauncher;
import net.oauth.OAuthException;
import org.bouncycastle.openssl.PEMWriter;

class OAuthSession {
	/* 
	 * This class establishes an Oauth SSL session to a simplesaml/oauth server. 
	 * Intended to easy ouath communication by hidding a oauth specific url parameters.
	 * The ouath protocol is: 1. get request token 2. authorize 3. get accesstoken 4. use accesstoken
	 */  
	 
    final String GRID_DK = "portal.grid.dk";
	final String USER_INFO_URL = "https://portal.grid.dk/simplesaml/module.php/oauth/getUserInfo.php";
   	final String SYS_TMP_DIR = System.getProperty("java.io.tmpdir"); 
	final String FILE_SEP = System.getProperty("file.separator");
	
   	Hashtable userData;
	OAuthHelperApp oauthSession = null;
	public BrowserLauncher browser;

	/*
	 * The constructor implicitly downloads the grid.dk certificates certificate and imports it to java trust store.
	 * Uses the OauthHelperApp to perform lower level Oauth communication.
	 */ 
	public OAuthSession(){
	   	try{
 			browser = new BrowserLauncher();
			X509Certificate[] certs = retrieveServerCertificate(GRID_DK);
			importCerts(certs);
    		installTrustedCert(certs[1]);
    		oauthSession = new OAuthHelperApp();
    	
   		}catch(Exception e){
			e.printStackTrace(System.out);
			System.exit(1);
		}
	}
	
	
	/*
	 *  Creates a SSL connection to the server and retrieves its certificate chain 
	 */ 
	private X509Certificate[] retrieveServerCertificate(String serverUrl){
		int SSL_PORT = 443;
		// Create a trust manager that does not validate certificate chains
    	TrustManager[] trustAllCerts = new TrustManager[]{
        new X509TrustManager() {
            public java.security.cert.X509Certificate[] getAcceptedIssuers() {
                return null;
            }
            public void checkClientTrusted(
                java.security.cert.X509Certificate[] certs, String authType) {
            }
            public void checkServerTrusted(
                java.security.cert.X509Certificate[] certs, String authType) {
            }
        }
    };
    X509Certificate[] serverCerts = null;
    X509Certificate cert = null; 
    // Install the all-trusting trust manager
    try {
        SSLContext sc = SSLContext.getInstance("TLSv1");
        System.out.println(sc.getProvider().toString());
        
        sc.init(null, trustAllCerts, new java.security.SecureRandom());
        HttpsURLConnection.setDefaultSSLSocketFactory(sc.getSocketFactory());
        

        SSLSocketFactory factory = HttpsURLConnection.getDefaultSSLSocketFactory();
        SSLSocket socket = (SSLSocket)factory.createSocket(serverUrl,SSL_PORT);
       
        // Connect to the server
        socket.startHandshake();
        // Retrieve the server's certificate chain
        serverCerts = (X509Certificate[])
        socket.getSession().getPeerCertificates();
        
        // Close the socket
        socket.close();
        
    } catch (Exception e) {
    	e.printStackTrace(System.out);
    	System.exit(0);
       }
    
    return serverCerts;

    }
	
	/*
	 * Creates a local truststore file and imports the servers certificate. 
	 * This is necessary for SSL communication in java.
	 */
	private void importCerts(X509Certificate[] certs){
		FileOutputStream fos = null;
		
		String filename = SYS_TMP_DIR+FILE_SEP+"truststore.keystore";
        try{
        	KeyStore trustStore = KeyStore.getInstance(KeyStore.getDefaultType());        
    		fos = new FileOutputStream(filename);
    	   	char[] pass = "nopass".toCharArray();
          	trustStore.load(null,null);
           	for (int i = 0; i < certs.length; i++)
           		trustStore.setCertificateEntry("cert"+i, certs[i]); 
           	trustStore.store(fos,pass);
            fos.close();
        		
        	}catch (Exception e) {
    			e.printStackTrace(System.out);
    			System.exit(0);
   			}
        	System.setProperty("javax.net.ssl.trustStore",filename);
   			System.setProperty("javax.net.ssl.trustStorePassword","nopass");
		}
	
    /* Save the CA's certificate to a file and opens it in the web browser to
     * install it.
     */ 
    public void installTrustedCert(X509Certificate cert){
    	String tempDir = SYS_TMP_DIR;
    	if (!tempDir.endsWith(FILE_SEP)){
    		tempDir += FILE_SEP;
    		}
    	String trustedCert = tempDir+"trusted.crt";
    	writeToFile(trustedCert, cert);
    	
    	browser.setNewWindowPolicy(false);
    	browser.openURLinBrowser("file://"+trustedCert);
		
    	}
    
    /*
     * Starts the ouath session by getting a request token from the simplesaml server and 
     * launching a web browser for authentication.
     */
    public void startAuthenticationAndLaunchBrowser(){
    	try{	
    		requestToken();
    		String url = authorize();
    		browser.setNewWindowPolicy(false);
    		browser.openURLinBrowser(url);
		}catch(javax.net.ssl.SSLHandshakeException e){
			e.printStackTrace(System.out);
			System.exit(0);
		}catch(Exception e){
			e.printStackTrace(System.out);
			System.exit(0);
		}
    }
    
        	
    /*
     * This method complete the oauth session creation after authentication by 
     * requesting an access token used to communicate with the simplesaml server. 
     * Finally the servers identity info about the user is retrieved.
     */	
    public boolean completeAuthentication(){
    	int attempts = 0;
    	final int maxAttempts = 1;
    	boolean success = false;
    	while(true){
			try{
				if(retrieveAccessToken())
					success = true;
				}catch(OAuthException e){
				System.err.println(e.toString() + " User not authenticated yet.");
				if(attempts++==maxAttempts){
					System.err.println("Max attempts reached.");
					break;
					}
				try{	
					Thread.currentThread().sleep(1000);	
				}catch(java.lang.InterruptedException ie){
					ie.printStackTrace(System.out);
				}
			
				continue;
			}
			if(success){
				String datastr = openUrl(USER_INFO_URL);
    			userData = parseUserData(datastr);
			}
      		break;
		}
    	return success;
	}
    	            
	/*
	 * Command line oauth session scheme. Deprecated. 
	 */
    public void authenticate(){
    	try{
    	startAuthenticationAndLaunchBrowser();
    	System.out.print("When logged in press any key to continue...");
		
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		while(true){
			String input = br.readLine();
			if(input != null)
				break;
		}
    	retrieveAccessToken();
    	String datastr = openUrl(USER_INFO_URL);
    	userData = parseUserData(datastr);
   	} catch(Exception e){
			e.printStackTrace(System.out);
			System.exit(1);
		}
   	}        
            
            
    /*
     * Uses the aouth helper class to start an oauth session by requesting a token.
     */ 
    private void requestToken() throws IOException, OAuthException,URISyntaxException {
		try{
			oauthSession.execute("request");
		}
		catch(javax.net.ssl.SSLHandshakeException e){
			e.printStackTrace(System.out);
			return;
			}
	}

	/*
 	* Requests the server to authenticate the token. Returns a url of the specified IdP 
 	* for user login.
 	*/
 	private String authorize(){
		String authorizeUrl = "";
		try{
			authorizeUrl = oauthSession.execute("authorize");
				
		}catch(OAuthException e){
			e.printStackTrace(System.out);
		}catch(IOException e){
			e.printStackTrace(System.out);
		}catch(URISyntaxException e){
			e.printStackTrace(System.out);
		}
		return authorizeUrl;
	}
	
	/*
	 * Retrieves an access token to complete the oauth session.
	 */
	private boolean retrieveAccessToken() throws OAuthException{
		boolean success = false;
		try{
		
		String token = oauthSession.execute("access");
		if (!token.equals(""))
			 success = true;
			 
		 }catch(IOException e){
			e.printStackTrace(System.out);
			System.exit(1);
		}catch(URISyntaxException e){
			e.printStackTrace(System.out);
			System.exit(1);
		}  

		return success;
		} 
		
		
	/*
	 * Creates a hashtable with info from the data string retrieved via oauth's getUserInfo()
	 */	
	private Hashtable parseUserData(String data){
		// example : {"eduPersonPrincipalName":["benji@rnd.feide.no"],"mail":["bsedoc@yahoo.com"],
		// "uid":["benji"],"sn":["Benjamin Sedoc"],"cn":["Benjamin Sedoc"],
		// "eduPersonTargetedID":["e82a0210072a882a5694e50d08c489ede9951b9c"]}
	
		Hashtable userInfo = new Hashtable();
		// remove the '"'s and the '"[' from the both ends of the key and the value 
		data = data.replaceAll("[]\"]","").replace("[","").replace("{", "").replace("}","");
		

		String[] tokens = data.split(",");
		for (int i = 0; i < tokens.length-1; i++){
			String[] fields = tokens[i].split(":");
			fields[1].replaceAll("\"", "");
			userInfo.put(fields[0].trim(),fields[1].trim());
		}
		return userInfo;
	}
    
    /*
     * Make a http get request through the oauthhelper
     */
    	public String openUrl(String url){
			String response = "";
			System.out.println("Opening url :  "+url);
			try {
			response = oauthSession.execute(url);
				
			}catch(Exception e){
			e.printStackTrace(System.out);
			System.exit(1);
		}
		
		return response;
			
		}
  
    /*
     * Writes object to file
     */ 
    private void writeToFile(String filename,Object o){
  		try{	
    	FileWriter fWrt = new FileWriter(filename);
    	   		
   		PEMWriter pemWrt = new PEMWriter(fWrt);
		pemWrt.writeObject(o);
		pemWrt.close();
    	fWrt.close();
    	
    	System.out.println("Wrote to file "+filename);
		}
		catch(IOException e){
			e.printStackTrace(System.out);
			System.exit(1);
		}catch(Exception e){
			e.printStackTrace(System.out);
			System.exit(1);
			}
  		}

  
  	public Hashtable getUserData(){
  		return userData;
  		}
    
    
    public static void main(String[] args){
    	OAuthSession oas = new OAuthSession();	
    	oas.authenticate();
  		//oas.SLCS();
  		/*String testdata =  "{\"eduPersonPrincipalName\":[\"benji@rnd.feide.no\"],\"mail\":[\"bsedoc@yahoo.com\"], \"uid\":[\"benji\"],\"sn\":[\"Benjamin Sedoc\"],\"cn\":[\"Benjamin Sedoc\"], \"eduPersonTargetedID\":[\"e82a0210072a882a5694e50d08c489ede9951b9c\"]}";
  		
  		Hashtable dict = gc.parseUserData(testdata);
  		System.out.println("-------------\n"+gc.createFullDN(dict));*/
  		
  		
  		
  	}
}
