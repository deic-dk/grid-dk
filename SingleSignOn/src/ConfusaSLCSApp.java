import java.security.*;
import java.io.*;
import java.util.ArrayList;
import java.util.Hashtable;
import java.util.Enumeration;
import java.security.cert.X509Certificate;
import java.security.PrivateKey;
import java.security.KeyPairGenerator;
import java.util.Scanner;
import java.util.Arrays;

import org.bouncycastle.jce.*;
import org.bouncycastle.openssl.PEMWriter;
import org.bouncycastle.jce.provider.*;
import org.bouncycastle.util.encoders.Base64;
import org.mozilla.jss.CryptoManager;
import org.mozilla.jss.crypto.*;


public class ConfusaSLCSApp {
/*
 * Handles communication with the counfusa server for obtain a signed certificate.
 */

	final String SERVER_URL = "https://portal.grid.dk/";
	final String UPLOAD_PAGE = "confusa/key_upload.php";
	final String APPROVE_PAGE = "confusa/index.php";
	final String DOWNLOAD_PAGE = "confusa/key_download.php";
	
	final int SLCS_LIFETIME = 11; // 11 days until expired

 	final int KEY_LENGTH = 2048; // number bits in the generated keys

	final String HOME_DIR = System.getProperty("user.home");
	final String FILE_SEP = System.getProperty("file.separator");
	final String DEFAULT_SUBDIR = ".globus"+FILE_SEP;
	
	String saveCertDir = HOME_DIR+FILE_SEP+DEFAULT_SUBDIR; // the default save destination
    
    String[] CONFUSA_DN_FIELDS = new String[]{"C","O","OU","CN"}; // confusa's DN fields in fixed order
    
    String authenticationToken = "";
	Hashtable myData;
	String commonName = "";

	KeyPair keypair;
    PKCS10CertificationRequest csr; 
	OAuthSession myOAuthSession = null;
	String certname = "cert";
	String proxyFilename = "proxycert.crt";
	String proxyCertStr = "";
	X509Certificate certificate = null;
	Hashtable attributes = null; // will contain the cert attributes
	
	
	/*
	 * Confusa class constructor. Imports an oauth object to be used when communicating with the server. Also loads user data from the simplesaml/oauth server.
	 */
    public ConfusaSLCSApp(OAuthSession oauth){
    	myOAuthSession = oauth;
    	myData = myOAuthSession.getUserData();
    	setCertAttributes(myData);
    	}
   
   public void SLCS(String passwd){

		try{
			uploadCsr();
			approveCsr();	
			String certReply = downloadCertificate();
			saveCertificate(certReply, passwd);
			}
		catch(Exception e){
			e.printStackTrace(System.out);
			System.exit(1);
			}
	}

	/*
	 * Parses and stores the stores the certificate string to files. Also creates a proxy certificate.
	 */ 
	public void saveCertificate(String certStr, String keyStorePasswd){
		HandleCert certHandler = new HandleCert();
		File handle = new File(saveCertDir);
		if (!handle.exists()){
			handle.mkdir();			
			}
		certificate = certHandler.parseAndExportCertificate(certStr,saveCertDir, certname, keypair, keyStorePasswd);
		proxyCertStr = certHandler.createProxyCert(certificate,keypair,KEY_LENGTH, saveCertDir+proxyFilename);
		}    


	/*
	 * Generates a keypair and a CSR. The CSR is uploaded to the confusa server 64bit-encoded along with an authentication
	 * token made from a sha1hashed public key.
	 */ 
	public void uploadCsr(){
		try{
			String DN = getDN();
			BouncyCastleProvider bcprov = new BouncyCastleProvider();
			Security.addProvider(bcprov);	
		
			System.setProperty("line.separator","\n"); // necessary in windows XP
			keypair = generateKeys();
			
			csr = generateCSR(keypair, DN);
			// write the CSR to a string
			StringWriter strWrt = new StringWriter();
			PEMWriter pemWrt = new PEMWriter(strWrt);
			pemWrt.writeObject(csr);
			pemWrt.close();
			String csrStr = strWrt.toString();
			
			// write public key to a string
			strWrt = new StringWriter();
			pemWrt = new PEMWriter(strWrt);
			pemWrt.writeObject(csr.getPublicKey());
			pemWrt.close();
			String pubKeyStr = strWrt.toString();
				
			// create the authentication token: sha1 of pubkey
			byte[] digest = sha1Digest(pubKeyStr.getBytes());
			authenticationToken = convertToHex(digest);
			 
			// create base64 hash value of the csr
			byte[] CSRb64Bytes = base64Encode(csrStr.getBytes());
			String CSRb64 = new String(CSRb64Bytes);
			
			// create the url for uploading the csr
			String auth_name = "inspect_csr="; // difference between confusa versions (git DL) which use "auth_key=";
			String postStr = "?"+auth_name+authenticationToken+"&remote_csr="+CSRb64;
			String uploadUrl = SERVER_URL+UPLOAD_PAGE+postStr;
			myOAuthSession.openUrl(uploadUrl);
			
		}catch(Exception e){
			System.out.println(e.toString());
			e.printStackTrace(System.out);
			System.exit(0);
		}	
	}

	/*
	 * Request confusa server to approve and sign the uploaded CSR
	 */
	public void approveCsr(){
		// create the url for approving the csr
		String approveUrl = SERVER_URL+APPROVE_PAGE+"?auth_token="+authenticationToken; 
		myOAuthSession.openUrl(approveUrl);
	}


	/*
	 * If downloads the signed certificate from the confusa server
	 */ 
	public String downloadCertificate(){
		byte[] CNb64Bytes = base64Encode(commonName.getBytes()); 
		String CNb64 = new String(CNb64Bytes); // the confusa server wants the CN 64 bit encoded
		// inspect_csr
		String downloadUrl= SERVER_URL+DOWNLOAD_PAGE+"?inspect_csr="+authenticationToken+"&common_name="+CNb64;
		return myOAuthSession.openUrl(downloadUrl);
	}

/*
 *	Generates a keypair of KEY_LENGTH bits
 */ 
    private KeyPair generateKeys() throws java.security.NoSuchAlgorithmException, java.security.NoSuchProviderException{
	
		KeyPairGenerator keyGen = KeyPairGenerator.getInstance("RSA", "BC");
		SecureRandom random = SecureRandom.getInstance("SHA1PRNG", "SUN");
		keyGen.initialize(KEY_LENGTH, random);
		KeyPair pair = keyGen.generateKeyPair();
	
		return pair;
    }
    
    /*
     * Generates a CSR to be shipped to the confusa server
     */ 
    private PKCS10CertificationRequest generateCSR (KeyPair pair, String DN){
   		PKCS10CertificationRequest csr = null;
    	try{
			csr = new PKCS10CertificationRequest(
    		"SHA256withRSA",
    		new X509Principal(DN),
    		pair.getPublic(),
    		null,
    		pair.getPrivate());
    	} catch(Exception e){
    		e.printStackTrace(System.out);
    		System.exit(1);
    	}
    	return csr;
    	}
    
	/*
	 * Returns a 64 bit encoding of the data
	 */ 
	private byte[] base64Encode(byte[] data){
		Base64 b64encoder = new Base64();
		byte[] b64data = b64encoder.encode(data);
		return b64data;
		}

	/*
	 * Makes a sha1sum of the data
	 */ 
	private byte[] sha1Digest(byte[] data) throws NoSuchAlgorithmException, IOException {
	    MessageDigest md = MessageDigest.getInstance("SHA1");
  		md.update(data);
		byte[] digest = md.digest();
		return digest;
	}

	/*
	 * Converts the the byte data to a hex string
	 */ 
	private static String convertToHex(byte[] data) {
        StringBuffer buf = new StringBuffer();
        for (int i = 0; i < data.length; i++) {
        	int halfbyte = (data[i] >>> 4) & 0x0F;
        	int two_halfs = 0;
        	do {
	            if ((0 <= halfbyte) && (halfbyte <= 9))
	                buf.append((char) ('0' + halfbyte));
	            else
	            	buf.append((char) ('a' + (halfbyte - 10)));
	            halfbyte = data[i] & 0x0F;
        	} while(two_halfs++ < 1);
        }
        return buf.toString();
    }
    
	/*
     * Sets the certificate attributes from the user information provided by the idP via simplesaml/oauth. Also returns the full DN for convenience.
     */
    private void setCertAttributes(Hashtable userInfo){
    	attributes = new Hashtable<String,String>();
    	commonName = userInfo.get(new String("cn"))+ " "+userInfo.get(new String("eduPersonPrincipalName")); // this is how confusa constructs the CN for some reason (see person.php).
		attributes.put("CN",commonName);
				
		if (userInfo.containsKey("org"))
			attributes.put("O", (String) userInfo.get("org"));
		
		if (userInfo.containsKey("orgUnit"))
			attributes.put("OU", (String) userInfo.get("orgUnit"));
		
		if (userInfo.containsKey(new String("country")))
			attributes.put("C", userInfo.get(new String("country")));
    	
    	if (userInfo.containsKey("state"))
			attributes.put("ST", userInfo.get(new String("state")));
    	
    	if (userInfo.containsKey("email"))
			attributes.put("EmailAddress", userInfo.get(new String("email"))); 
    	 
    	}
       
	/*
	 * Composes a DN that is accepted by Confusa.
	 * 
     * See confusa file cert_manager.php->match_dn()
	 * Fields must match simplesaml IdP data from oauth login, but Confusa only checks for CN, O, OU and C, so the DN cannot contain mail, state etc. so far.
	 * The DN must match the one composed by confusa's person.php->get_complete_dn() which only uses attributes C,O,CN.
	 */
	private String getDN(){
		ArrayList confusaFields = new ArrayList(Arrays.asList(CONFUSA_DN_FIELDS));
		String DN = "";
    	 
    	for (Enumeration<String> e = attributes.keys() ; e.hasMoreElements() ;) {
			String key = e.nextElement();
            if(confusaFields.contains(key))
            	DN += key+"="+attributes.get(key)+","; 
      	}
    	DN = DN.substring(0,DN.length()-1); 
    	System.out.println(DN); 
    	return DN;      
	}
    
    
    public Hashtable getAttributes(){
    	return attributes;
    	}
    
    
    
    public String getProxyCertStr(){
    	return proxyCertStr;
    	
    	}
    
    public void certtest(X509Certificate cert, PrivateKey pKey){
   	try {
		//KeyStore ks = KeyStore.getInstance("Windows-ROOT");//, sun.security.mscapi.SunMSCAPI);
		KeyStore ks = KeyStore.getInstance("Windows-MY");//, sun.security.mscapi.SunMSCAPI);

	ks.load(null, null) ;
	//ks.setCertificateEntry("mittestcert",cert);
	ks.setKeyEntry("mytestcert",pKey.getEncoded(),new X509Certificate[]{cert});
	
	java.util.Enumeration en = ks.aliases();
	

	//ks.setKeyEntry("thekey",privKey, password,certChain);
	//ks.setCertEntry("mittestcert",cert);
	ks.store(null,null);
	while (en.hasMoreElements()) {
		String aliasKey = (String)en.nextElement() ;
		X509Certificate c = (X509Certificate) ks.getCertificate(aliasKey) ;
		System.out.println("---> alias : " + aliasKey) ;
//		System.out.println("    Certificat : " + c.toString() ) ;
 
		if (aliasKey.equals("myKey") ) {
		      PrivateKey key = (PrivateKey)ks.getKey(aliasKey, "monPassword".toCharArray());
		      X509Certificate[] chain = (X509Certificate[]) ks.getCertificateChain(aliasKey);
		}
	}
 
} catch (Exception ioe) {
	System.err.println(ioe.getMessage());
}
    	
    	}
    

	public void mozcerttest(){
		
		try {
			
			String dbdir = "/home/benjamin/.mozilla/firefox/jt6uro1c.default";
             CryptoManager.initialize(dbdir);
             CryptoManager cm = CryptoManager.getInstance();
             
             X509Certificate[] certs = (X509Certificate[]) cm.getCACerts();
             
             //added verbose option to limited the output of the tinderbox
             // and nightly QA.
             
             System.out.println("Number of CA certs: " + certs.length);
             System.out.println("use option \"verbose\" if you want the CA " +
                 "certs printed out");
             //if (args.length == 2 && args[1].equalsIgnoreCase("verbose")) {
                 for(int i=0; i < certs.length; ++i ) {
                     System.out.println(certs[i].getSubjectDN().toString());
                     InternalCertificate ic = (InternalCertificate) certs[i];
                     System.out.println("SSL: " + ic.getSSLTrust() + 
                         ", Email: " + ic.getEmailTrust() + 
                         ", Object Signing: " + ic.getObjectSigningTrust());
               //  }
             }
             
         } catch(Throwable e) {
             e.printStackTrace();
             System.exit(1);
         }

		}    
    
    public String getCertDir(){
    	return saveCertDir;
    	}
    	
    	
    public String getCertName(){
    	return certname;
    	}
    	
    	
    public void setCertDir(String dir){
    	saveCertDir = dir;
    	}
    	
    	
    public void setCertName(String name){
    	certname=name;
    	}
    	
    	
    public String getCertPath(){
    	return saveCertDir+certname;
    	
    	}	

  
    
    public static void main(String[] args) throws Exception{ 
    	OAuthSession oas = new OAuthSession();
    	//oas.startAuthenticationAndLaunchBrowser();
    	//oas.completeAuthentication();
    	//oas.authenticate();
    	
    	
    			String certText = " -----BEGIN CERTIFICATE-----"+ 
"MIIEMTCCAxmgAwIBAgIBADANBgkqhkiG9w0BAQUFADCBhTELMAkGA1UEBhMCREsx"+
"DDAKBgNVBAgTA0NQSDEMMAoGA1UEBxMDQ1BIMQswCQYDVQQKEwJrdTENMAsGA1UE"+
"CxMEZGlrdTEbMBkGA1UEAxMSYmVuamFtaW4gdGVzdCBjZXJ0MSEwHwYJKoZIhvcN"+
"AQkBFhJic2Vkb2Nub3RAaG9tZS5jb20wHhcNMDkwNjI0MTIwMDA1WhcNMDkwNzA1"+
"MTIwMDA1WjBCMQkwBwYDVQQGEwAxCTAHBgNVBAoMADEqMCgGA1UEAwwhQmVuamFt"+
"aW4gU2Vkb2MgYmVuamlAcm5kLmZlaWRlLm5vMIIBIjANBgkqhkiG9w0BAQEFAAOC"+
"AQ8AMIIBCgKCAQEAkG5iTutuzw/2h113a/iVE/Or4LP0BVJhwII/SfeG/PPOH59j"+
"33r0J6WEXI1As5bodbMdgMun9+sI21SgaZKCbfWSVuZZ+YeagiwltXIdG2Zr8qc7"+
"WLYs54j477AKsKVpeHQtB4gKIladQFl6wMVRGUndJZYTJ2YzUGyvieXRqvoBBvai"+
"XdFLaJftkVfP9TmiU1HOfXdL/+9FY5pTTkZEKcjjBHGFeVo7QUe2/+BTQbLYaAGy"+
"roRdhY3VSeJVwMQk4SubBAPQZzp7Q4SRc53JJG8t7vv5DolOtuIRJYUQVSSiSNH5"+
"H8U7ycJ7Fos2I3L31kNPO7G2TUV3t5X32O0ZNQIDAQABo4HtMIHqMB0GA1UdDgQW"+
"BBSdALZ+6sYgzzjA/d1wgwIBM+v3fjCBugYDVR0jBIGyMIGvgBQgW5dnSYG7fYsa"+
"INeLhwG6zoVqrKGBi6SBiDCBhTELMAkGA1UEBhMCREsxDDAKBgNVBAgTA0NQSDEM"+
"MAoGA1UEBxMDQ1BIMQswCQYDVQQKEwJrdTENMAsGA1UECxMEZGlrdTEbMBkGA1UE"+
"AxMSYmVuamFtaW4gdGVzdCBjZXJ0MSEwHwYJKoZIhvcNAQkBFhJic2Vkb2Nub3RA"+
"aG9tZS5jb22CCQDyJQJf3qgF1jAMBgNVHRMEBTADAQH/MA0GCSqGSIb3DQEBBQUA"+
"A4IBAQBgQM23MO8Fcc9x/ZzWUrAZ8h0hZ43Gh1t+tRXBmrccCUUaxwAhzeaH6nqX"+
"wJv6kmt6rD/5cLxhkCKTGD+ZM9b7UrJk3mYlK6fvsZyhyxY9BjgqdlWxuhDy/k+I"+
"+P72ZRkeU2qCz4W3ehCg0LoS+vdZeqNpWXDmk0TE0qUPYsZiFV+8ITcm2miCq2DX"+
"P8bpiwXH7/FCJea6PevmEWzg8JyaDhfvsDnmotKmi8zT9uOWHhX0k7NsycJomBYw"+
"9DCdknsCHikrosM53mvMhnx2zPpMUnZP+mg+nyt+gFc71hWSNrJ9oCGuareAoEVT"+
"+6B066WzHlAe7chufSBcSq0wDhc6"+
"-----END CERTIFICATE-----"+
"2009 Jun 24 14:00:05 (Confusa) notice: Sending certificate with hash 8ab05b7acf3d08483980af6aec051aaf822c0984 and auth-token 8ab05b7acf3d08483980af6aec051aaf822c0984 to user from ip 192.38.109.188"+
"<BR>";
	
	//String certpath = "/home/benjamin/Dokumenter/Benjamin_Richardt_Thomas_Sedoc-certs/Benjamin_Sedoc-certs/cert.pem";
	
	
			
	
	String certpath = System.getProperty("user.home")+"/.globus/cert.crt";
	String keypath = System.getProperty("user.home")+"/.globus/key.pem";
	Scanner scanner = 
      new Scanner(new File(certpath)).useDelimiter("\\Z");
    String contents = scanner.next();
    scanner = 
      new Scanner(new File(keypath)).useDelimiter("\\Z");
    
    String keycontents = scanner.next();
    keycontents= keycontents.replace("-----BEGIN RSA PRIVATE KEY-----","");
    keycontents= keycontents.replace("-----END RSA PRIVATE KEY-----","");
    
    
    
    System.out.println(keycontents);

    scanner.close();
    byte[] key = Base64.decode(keycontents.getBytes());

    
    java.security.KeyFactory keyFactory = java.security.KeyFactory.getInstance("RSA");
	java.security.spec.PKCS8EncodedKeySpec privateKeySpec=new java.security.spec.PKCS8EncodedKeySpec(key);
    byte[] PKCSencoded=privateKeySpec.getEncoded();
    //PrivateKey privateKey = keyFactory.generatePrivate(privateKeySpec);


	System.setProperty("java.library.path","lib/jss4.jar");
	
	HandleCert hc = new HandleCert();
	String certStr = hc.filterCertStr(contents);
	X509Certificate cert = hc.parseCertificate(certStr);
    Security.addProvider(new BouncyCastleProvider());	
	ConfusaSLCSApp confusa = new ConfusaSLCSApp(oas);	
    //KeyPair kp = confusa.generateKeys();
    //confusa.createProxyCert(cert, kp);
    String certfile = "cert.pem";
    String pass = "grid";
  	//confusa.certtest(cert, privateKey);
  	//confusa.mozcerttest();
  	
  	//confusa.SLCS(pass);
  		/*String testdata =  "{\"eduPersonPrincipalName\":[\"benji@rnd.feide.no\"],\"mail\":[\"bsedoc@yahoo.com\"], \"uid\":[\"benji\"],\"sn\":[\"Benjamin Sedoc\"],\"cn\":[\"Benjamin Sedoc\"], \"eduPersonTargetedID\":[\"e82a0210072a882a5694e50d08c489ede9951b9c\"]}";
  		
  		Hashtable dict = gc.parseUserData(testdata);
  		System.out.println("-------------\n"+gc.createFullDN(dict));*/
  	}
}
