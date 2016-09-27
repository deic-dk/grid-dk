/*
 *      HandleCert.java
 *      
 *      Copyright 2009 Benjamin <benjamin@benjamin-laptop>
 *      
 *      This program is free software; you can redistribute it and/or modify
 *      it under the terms of the GNU General Public License as published by
 *      the Free Software Foundation; either version 2 of the License, or
 *      (at your option) any later version.
 *      
 *      This program is distributed in the hope that it will be useful,
 *      but WITHOUT ANY WARRANTY; without even the implied warranty of
 *      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *      GNU General Public License for more details.
 *      
 *      You should have received a copy of the GNU General Public License
 *      along with this program; if not, write to the Free Software
 *      Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 *      MA 02110-1301, USA.
 */

import java.io.*;
import java.security.*; 
import java.security.cert.*; 
import java.io.FileOutputStream;
import java.security.KeyStore;
import java.security.PrivateKey;
import java.security.Security;
import java.security.cert.X509Certificate;

import org.bouncycastle.jce.provider.BouncyCastleProvider;
import org.bouncycastle.openssl.PEMWriter;

import org.globus.gsi.bc.BouncyCastleCertProcessingFactory;
import org.globus.gsi.GlobusCredential;

class HandleCert {
	final String BEGIN_CERT_TOKEN = "-----BEGIN CERTIFICATE-----";
	final String END_CERT_TOKEN = "-----END CERTIFICATE-----";
	String certname = "cert.crt";
	String keyname = "key.pem";
	String certp12 = "cert.p12";

	public HandleCert(){
		}
		
	/*
	 * Removes the begin/end certificate tags
	 */ 
	public String filterCertStr(String rawText){
		String certStr = "";
		certStr = rawText.split(BEGIN_CERT_TOKEN)[1];
		certStr = certStr.split(END_CERT_TOKEN)[0];
		certStr = BEGIN_CERT_TOKEN +"\n"+certStr+"\n"+END_CERT_TOKEN;
		return certStr;
		
		}
  
  	/*
  	 * Converts the certificate string into X509Certificate object
  	 */ 
   	public X509Certificate parseCertificate(String certStr){
		X509Certificate cert = null;
		try{
			ByteArrayInputStream bais = new ByteArrayInputStream(certStr.getBytes()); 
			CertificateFactory cf = CertificateFactory.getInstance("X.509");
  			cert = (X509Certificate) cf.generateCertificate(bais);	
		}catch(Exception e){
			System.err.println(e.toString());
			System.exit(1);
	 	}	
		return cert;
	}
  
  
  	/*
  	 * Writes private key and certificate to files
  	 */
   	public X509Certificate parseAndExportCertificate(String rawCertStr, String folder, String namep12, KeyPair kp, String keyStorePasswd){
  		String certStr = filterCertStr(rawCertStr);
		X509Certificate cert = parseCertificate(certStr);
		
		String keyname = "key.pem";
	    if (!namep12.endsWith(".p12")){
	    	certname = namep12+".crt";
	    	namep12+=".p12";
		}
		else{
			certname = namep12.substring(0,namep12.length()-4)+".crt";
			}
	    
	    writeCertToFile(cert, folder+namep12, kp, keyStorePasswd);
		writeToFile(folder+keyname, kp.getPrivate());
		writeToFile(folder+certname, cert);
		return cert;
  		}
  
  
  	/*
  	 * Write object to file
  	 */
  	public void writeToFile(String filename,Object o){
  		try{	
			FileWriter fWrt = new FileWriter(filename);
			PEMWriter pemWrt = new PEMWriter(fWrt);
			pemWrt.writeObject(o);
			pemWrt.close();
			fWrt.close();
			System.out.println("Wrote to file "+filename);
			}
		catch(IOException e){
			e.printStackTrace(System.out);//.println(e.toString());
			System.exit(1);
		}catch(Exception e){
			e.printStackTrace(System.out);//System.out.println(e.toString());
			System.exit(1);
			}
  		}
  
  /*
   * Saves the certificate as a .p12 file
   */
  	public void writeCertToFile(X509Certificate crt, String filepath, KeyPair kp, String passwd){
	    try{
			KeyStore ks = KeyStore.getInstance ("PKCS12");
			// for security, KeyStore wants certificate password as char[]
			char[] password = passwd.toCharArray();
			ks.load(null,null);
			X509Certificate[] certChain = new X509Certificate[1];
			certChain[0] = crt;
			PrivateKey privKey = kp.getPrivate();
			ks.setKeyEntry("thekey",privKey, password,certChain);
			FileOutputStream fos = new FileOutputStream(filepath);
			ks.store(fos, password);
			fos.close();
			System.out.println("Wrote to file "+filepath);
		}
		catch(IOException e){
				e.printStackTrace(System.out);
				System.exit(1);
			}catch(CertificateException e){
				e.printStackTrace(System.out);
				System.exit(1);
			}catch(Exception e){
				e.printStackTrace(System.out);
				System.exit(1);
			}
		}


		/*
		 * Creates a proxy from the certificate and private key. Saves it to file and returns it as a string.
		 */ 
    public String createProxyCert(X509Certificate cert, KeyPair kp, int keyLength, String proxyFilename){
     	//String proxyFilename = saveCertDir+"proxycert.crt";
     	int proxyLifetimeInSeconds = 11*24*60*60;
    	String proxyCertStr = "";
    	try{
    		BouncyCastleCertProcessingFactory proxyFactory = BouncyCastleCertProcessingFactory.getDefault(); 
    	
     	 	PrivateKey userKey = kp.getPrivate(); 
      		GlobusCredential proxyCert = proxyFactory.createCredential(new X509Certificate[]{cert}, userKey, keyLength, proxyLifetimeInSeconds, org.globus.gsi.GSIConstants.DELEGATION_FULL);//, (org.globus.gsi.proxy.ext.ProxyCertInfo) null);
    	
    		ByteArrayOutputStream out = new ByteArrayOutputStream();
			proxyCert.save(out);
			proxyCertStr = out.toString();
			out.close();
			System.out.println("Wrote to file "+proxyFilename);
			}catch(Exception e){
				e.printStackTrace(System.out);
				System.exit(-1);
			}
		
		return proxyCertStr;	
    	}




	public String getCertp12Name(){
		return certp12;
		}


	public static void main (String args[]) throws Exception{		
		
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
	
	    Security.addProvider(new BouncyCastleProvider());	


	HandleCert hc = new HandleCert();
	/*String certStr = hc.filterCertStr(certText);
	X509Certificate cert = hc.parseCertificate(certStr);
	KeyPair kp = hc.generateKeys();
	X509Certificate crt = (X509Certificate) hc.createMasterCert(kp.getPublic(),kp.getPrivate());
	//System.out.println(certstr);
	String filename = "SLCS.crt"; 
	hc.writeCertToFile(crt, filename, kp);	*/
				
	}
}
