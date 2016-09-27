/*
 * Copyright 2008 Netflix, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

//package net.oauth.example.cmdline;

import java.util.Map;
import java.util.List;
import java.util.ArrayList;
import java.util.Iterator;
import java.io.IOException;
import java.net.URISyntaxException;
import java.util.Hashtable;

import net.oauth.client.httpclient4.HttpClient4;
import net.oauth.client.OAuthClient;
import net.oauth.OAuthServiceProvider;
import net.oauth.OAuthConsumer;
import net.oauth.OAuthAccessor;
import net.oauth.OAuth;
import net.oauth.OAuthMessage;
import net.oauth.OAuthException;


// See the readme.txt and manpage.txt for more information

public class OAuthHelperApp {
	/*
	 * This is a simple rewrite of the OauthHelper class. Customized to stay in memory in stead
	 * of using property files on disk.
	 */ 
    private Hashtable props;
    //private File propFile;
	String requestUrl= "https://portal.grid.dk/simplesaml/module.php/oauth/requestToken.php";
	String authorizationUrl="https://portal.grid.dk/simplesaml/module.php/oauth/authorize.php";
	String accessUrl= "https://portal.grid.dk/simplesaml/module.php/oauth/accessToken.php";
	String callbackUrl = "https://portal.grid.dk";
	String consumerKey = "key";
	String consumerSecret = "secret";
	String appName = "confusa";

    public static void main(String[] argv) throws Exception {
        if ("help".equals(argv[0])) {
            System.err.println("Please see the readme.txt");
            return;
        } else {
            if (argv.length < 2 && (!"help".equals(argv[0]))){
                System.err.println(
                            "OAuthHelper [help | <properties> [<operation> | <url>]]");
                return;
            }
        }
        new OAuthHelperApp().execute(argv[1]);
    }


    public OAuthHelperApp() throws IOException {
        //props = new Properties();
        props = new Hashtable();
        //propFile = new File(fileName);
        //props.load(new FileInputStream(propFile));
    }

    private OAuthAccessor createOAuthAccessor(){
        //String consumerKey = props.getProperty("consumerKey");
        //String consumerKey = props.get("consumerKey").toString();
        //String callbackUrl = null;
        //String callbackUrl = "http://www.grid.dk";
        //String consumerSecret = props.getProperty("consumerSecret");
		//String consumerSecret = props.get("consumerSecret").toString();

        //String reqUrl = props.getProperty("requestUrl");
        //String reqUrl = props.get("requestUrl").toString();
        
        //String authzUrl = props.getProperty("authorizationUrl");
        //String authzUrl = props.get("authorizationUrl").toString();
               
        //String accessUrl = props.getProperty("accessUrl");
        //String accessUrl = props.get("accessUrl").toString();

        OAuthServiceProvider provider
                = new OAuthServiceProvider(requestUrl, authorizationUrl, accessUrl);
                
        OAuthConsumer consumer
                = new OAuthConsumer(callbackUrl, consumerKey,
                consumerSecret, provider);
        return new OAuthAccessor(consumer);
    }

   /* private void updateProperties(String msg) throws IOException {
        props.store(new FileOutputStream(propFile), msg);
    }
*/
    private OAuthMessage sendRequest(Map map, String url) throws IOException,
            URISyntaxException, OAuthException
    {
        List<Map.Entry> params = new ArrayList<Map.Entry>();
        Iterator it = map.entrySet().iterator();
        while (it.hasNext()) {
            Map.Entry p = (Map.Entry) it.next();
            params.add(new OAuth.Parameter((String)p.getKey(),
                    (String)p.getValue()));
        }
        OAuthAccessor accessor = createOAuthAccessor();
        //accessor.tokenSecret = props.getProperty("tokenSecret");
        accessor.tokenSecret = props.get("tokenSecret").toString();
        
        OAuthClient client = new OAuthClient(new HttpClient4());
        System.out.println(accessor.toString()+", "+url+", "+params.toString());
        return client.invoke(accessor, "GET",  url, params);
    }

    public String execute(String operation) throws IOException, OAuthException,
            URISyntaxException
    {
        if ("request".equals(operation)){
     		//Security.addProvider(new BouncyCastleProvider());
     		//String truststore = "file:///home/benjamin/Dokumenter/grid-dk/SingleSignOnApplet/myTrustStore";	
			//System.setProperty("javax.net.ssl.trustStore","susanstore");
   			//System.setProperty("javax.net.ssl.trustStorePassword","ab987c");
    		
    //System.setProperty("java.protocol.handler.pkgs", "com.sun.net.ssl.internal.www.protocol");
 	//Security.addProvider(new com.sun.net.ssl.internal.ssl.Provider());
        	
            OAuthAccessor accessor = createOAuthAccessor();
           // HttpClient4 hc4 = new HttpClient4();
            //HttpClient hc = hc4.get
            /*KeyStore trustStore  = KeyStore.getInstance(KeyStore.getDefaultType());        
        	FileInputStream instream = new FileInputStream(new File("my.keystore")); 
        	try {
            	trustStore.load(instream, "nopassword".toCharArray());
        	} finally {
            	instream.close();
        	}
        
        	SSLSocketFactory socketFactory = new SSLSocketFactory(trustStore);
        	Scheme sch = new Scheme("https", socketFactory, 443);
        	//httpclient.getConnectionManager().getSchemeRegistry().register(sch);

*/
            //httpClient.setAuthenticationPreemptive(false);
            
            
	    OAuthClient client = new OAuthClient(new HttpClient4());
            client.getRequestToken(accessor);

            //props.setProperty("requestToken", accessor.requestToken);
            //props.setProperty("tokenSecret", accessor.tokenSecret);
			props.put("requestToken", accessor.requestToken);
            props.put("tokenSecret", accessor.tokenSecret);

            //updateProperties("Last action: added requestToken");
            //System.out.println(propFile.getCanonicalPath() + " updated");
            System.out.println("Request token: "+accessor.requestToken);
            return accessor.requestToken;
        }
        else if ("access".equals(operation))
        {
            //Properties paramProps = new Properties();
            Hashtable paramProps = new Hashtable();
            
            //paramProps.setProperty("oauth_token", props.getProperty("requestToken"));
			paramProps.put("oauth_token", props.get("requestToken").toString());
			OAuthMessage response = sendRequest(paramProps, accessUrl);
            
            //props.setProperty("accessToken",response.getParameter("oauth_token"));
            props.put("accessToken",response.getParameter("oauth_token"));
            //props.setProperty("tokenSecret", response.getParameter("oauth_token_secret"));
            props.put("tokenSecret", response.getParameter("oauth_token_secret"));
            
            //props.setProperty("userId", response.getParameter("user_id"));


            //updateProperties("Last action: added accessToken");
            //System.out.println(propFile.getCanonicalPath() + " updated");
            System.out.println("got access token");
            return response.getParameter("oauth_token");
        }
        else if ("authorize".equals(operation))
        {
            // just print the redirect
            //Properties paramProps = new Properties();
            Hashtable paramProps = new Hashtable();
            
            //paramProps.setProperty("application_name", props.getProperty("appName"));
            //paramProps.setProperty("oauth_token", props.getProperty("requestToken"));
			paramProps.put("application_name", appName);
			paramProps.put("oauth_token", props.get("requestToken"));
			paramProps.put("oauth_callback", callbackUrl);

            OAuthAccessor accessor = createOAuthAccessor();

            OAuthMessage response = sendRequest(paramProps,
                accessor.consumer.serviceProvider.userAuthorizationURL);

            System.out.println("Paste this in a browser:");
            System.out.println(response.URL);
            return response.URL;
            
        } else {
            // access the resource
            //Properties paramProps = new Properties();
            Hashtable paramProps = new Hashtable();
            
            //paramProps.setProperty("oauth_token", props.getProperty("accessToken"));

            paramProps.put("oauth_token", props.get("accessToken"));

            OAuthMessage response = sendRequest(paramProps, operation);
            String reply = response.readBodyAsString();
            System.out.println(reply);
            return reply;
        }
    }
}
