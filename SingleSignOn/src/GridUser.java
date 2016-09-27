import java.util.Hashtable;
import java.util.Enumeration;

import edu.stanford.ejalbert.BrowserLauncher;

class GridUser{
	final String CREATE_USER_URL = "https://portal.grid.dk:8443/"/*serverUrl*/+"cgi-bin/autocreate.py";
	BrowserLauncher browser;
	 
	 
	public GridUser(){}
     
	/*
     * Creates a grid user account by constructing a url string and making a https call to the grid.dk server. Open the browser too.
     */ 
	public boolean create(Hashtable attributes, String proxyStr){
    	String url = CREATE_USER_URL;
    	String urlParams = "?";
    	String country = "na";
    	String org = "na";
    	String email = "na";
    	String DN = "";
    	
        for (Enumeration<String> e = attributes.keys() ; e.hasMoreElements() ;) {
        	String key = e.nextElement();
        	DN += "/"+key+"="+attributes.get(key); 
 		}
	  	
	  	// grid.dk's create user method requires fields CN, DN, email, org, country     	    	
    	urlParams += "cert_id="+DN;	// cert_id is the DN
    	urlParams += "&cert_name="+attributes.get("CN"); // cert_name is the CN
    	
    	if (attributes.containsKey("C") && attributes.get("C")!="")
			country = (String) attributes.get("C");
		urlParams += "&country="+country;
    	    	
    	if (attributes.containsKey("O")&& attributes.get("O")!="")
    		org = (String) attributes.get("O");
    	urlParams += "&org="+org;
    	
    	if (attributes.containsKey("email")&& attributes.get("email")!="")
			email = (String) attributes.get("email");
		urlParams += "&email="+email;
       
	   	urlParams += "&proxy_upload="+proxyStr;
    	   	
    	url += urlParams;
    	System.out.println(url);
       	url = url.replace(" ","%20"); // encode spaces
		boolean newWindow = true;
		
		try{
			BrowserLauncher browser = new BrowserLauncher();	
    		browser.setNewWindowPolicy(newWindow);
			browser.openURLinBrowser(url); // we don't need oauth authentication since we have a cert in the browser at this point
		}catch(Exception e){
			e.printStackTrace(System.out);
			System.exit(-1);
			}
    	return true;
    }
	
	
	
	
	
	
	
	
	
	
	
	
	}
