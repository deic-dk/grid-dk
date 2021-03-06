/*
 * myJFrame.java
 *
 * Created on 29. juni 2009, 11:21
 */

//package myTestGUI;

/**
 *
 * @author  benjamin
 */
import java.lang.ProcessBuilder;
import java.util.Hashtable;
import java.awt.Cursor;

import java.io.File;
import javax.swing.SwingWorker;
import javax.swing.JOptionPane;
import javax.swing.JFileChooser;

public class ConfusaUI extends javax.swing.JFrame {
    OAuthSession oas;
    ConfusaSLCSApp confusa;
    /** Creates new form myJFrame */
    public ConfusaUI() {
        initComponents();
        oas = new OAuthSession();
    }
    
    /** This method is called from within the constructor to
     * initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is
     * always regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        saveCertOption = new javax.swing.JOptionPane();
        jFileChooser1 = new javax.swing.JFileChooser();
        downloadCertButton = new javax.swing.JButton();
        jScrollPane1 = new javax.swing.JScrollPane();
        jTextArea1 = new javax.swing.JTextArea();
        logInButton = new javax.swing.JButton();
        jLabel1 = new javax.swing.JLabel();
        jScrollPane2 = new javax.swing.JScrollPane();
        StatusPane = new javax.swing.JTextPane();
        jLabel2 = new javax.swing.JLabel();
        jSeparator1 = new javax.swing.JSeparator();
        goToGriddk = new javax.swing.JButton();

        saveCertOption.setMessageType(1);
        saveCertOption.setOptionType(0);

        jFileChooser1.setCurrentDirectory(null);
        jFileChooser1.setDialogTitle("Save certificate");
        jFileChooser1.setDialogType(javax.swing.JFileChooser.SAVE_DIALOG);
        jFileChooser1.setFileFilter(null);
        jFileChooser1.setSelectedFile(new java.io.File("/home/benjamin/cert.p12"));

        setDefaultCloseOperation(javax.swing.WindowConstants.EXIT_ON_CLOSE);
        setTitle("Confusa SLCS");
        setAlwaysOnTop(true);
        setCursor(new java.awt.Cursor(java.awt.Cursor.DEFAULT_CURSOR));

        downloadCertButton.setText("Download certificate");
        downloadCertButton.setEnabled(false);
        downloadCertButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                downloadCertButtonActionPerformed(evt);
            }
        });

        jTextArea1.setColumns(20);
        jTextArea1.setEditable(false);
        jTextArea1.setFont(new java.awt.Font("DejaVu Sans", 0, 12));
        jTextArea1.setLineWrap(true);
        jTextArea1.setRows(5);
        jTextArea1.setText("For access to the grid service you need a trusted certificate. Confusa SLCS provides such certificates to authorized users. Please follow the these instructions:\n\n\n1. Install the CA certificate to make your browser trust the confusa server.\n\n2. Click the \"Log in\" button to log in at your identity provider.\n\n3.  When logged in, click \"Download certficate\". \n\n4. When the certificate has been saved, import it to your browser.\n\n5. Click \"Go to grid.dk\" to open the grid web portal.\n");
        jTextArea1.setWrapStyleWord(true);
        jScrollPane1.setViewportView(jTextArea1);

        logInButton.setText("Log in");
        logInButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                logInButtonActionPerformed(evt);
            }
        });

        jLabel1.setFont(new java.awt.Font("DejaVu Sans", 0, 16));
        jLabel1.setHorizontalAlignment(javax.swing.SwingConstants.CENTER);
        jLabel1.setText("Short Lived Credential Service");

        StatusPane.setEditable(false);
        StatusPane.setText("Install the server CA certificate.\n\nThen click \"Log in\" to begin...   ");
        StatusPane.setOpaque(false);
        jScrollPane2.setViewportView(StatusPane);
        StatusPane.getAccessibleContext().setAccessibleName("");

        jLabel2.setText("Status");

        goToGriddk.setText("Go to grid.dk");
        goToGriddk.setEnabled(false);
        goToGriddk.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                goToGriddkActionPerformed(evt);
            }
        });

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(getContentPane());
        getContentPane().setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addComponent(jScrollPane1, javax.swing.GroupLayout.DEFAULT_SIZE, 385, Short.MAX_VALUE)
                .addContainerGap())
            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                .addGap(117, 117, 117)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.CENTER)
                    .addComponent(logInButton, javax.swing.GroupLayout.DEFAULT_SIZE, 177, Short.MAX_VALUE)
                    .addComponent(downloadCertButton, javax.swing.GroupLayout.DEFAULT_SIZE, 177, Short.MAX_VALUE)
                    .addComponent(goToGriddk, javax.swing.GroupLayout.DEFAULT_SIZE, 177, Short.MAX_VALUE))
                .addGap(115, 115, 115))
            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                .addContainerGap(183, Short.MAX_VALUE)
                .addComponent(jLabel2)
                .addGap(184, 184, 184))
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addComponent(jScrollPane2, javax.swing.GroupLayout.DEFAULT_SIZE, 385, Short.MAX_VALUE)
                .addContainerGap())
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addComponent(jSeparator1, javax.swing.GroupLayout.DEFAULT_SIZE, 385, Short.MAX_VALUE)
                .addContainerGap())
            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                .addContainerGap(97, Short.MAX_VALUE)
                .addComponent(jLabel1)
                .addGap(81, 81, 81))
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addComponent(jLabel1, javax.swing.GroupLayout.PREFERRED_SIZE, 19, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addGap(12, 12, 12)
                .addComponent(jScrollPane1, javax.swing.GroupLayout.PREFERRED_SIZE, 242, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(logInButton)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(downloadCertButton)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(goToGriddk)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                .addComponent(jSeparator1, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jLabel2)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jScrollPane2, javax.swing.GroupLayout.DEFAULT_SIZE, 180, Short.MAX_VALUE)
                .addContainerGap())
        );

        pack();
    }// </editor-fold>//GEN-END:initComponents

    
/*
 * Starts a OAutherWorker thread that handles authentication. 
 */ 
private void logInButtonActionPerformed(java.awt.event.ActionEvent evt) {                                                
                                                                    
    try{
        OAuthWorker worker = new OAuthWorker();
        worker.execute();
    }catch(Exception e){
        e.printStackTrace(System.out);
    }
}    
   
/*
 * Starts a ConfusaWorker thread that handles certificate retrieval. 
 */ 
private void downloadCertButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_downloadCertButtonActionPerformed
//GEN-LAST:event_downloadCertButtonActionPerformed
    try{
        ConfusaWorker worker = new ConfusaWorker();
        worker.execute();
    }
    catch(Exception e){
        e.printStackTrace(System.out);
        StatusPane.setText("Authentication failed. Please login.");
    }
}


/*
 * Starts a worker thread that creates a grid.dk user and launches the browser. 
 */ 
private void goToGriddkActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_goToGriddkActionPerformed
//GEN-LAST:event_goToGriddkActionPerformed
    SwingWorker worker = new SwingWorker<Boolean, String>(){
    @Override
    public Boolean doInBackground(){
       GridUser newUser = new GridUser();
       Hashtable attributes = confusa.getAttributes();
       String proxycertStr = confusa.getProxyCertStr();
       boolean success = newUser.create(attributes,proxycertStr);
       if(success){
           String message = "Congratulations, you now have access to the grid.dk web portal.";
           saveCertOption.showMessageDialog(ConfusaUI.this, message, "Done", JOptionPane.INFORMATION_MESSAGE);
           System.exit(0);

       }
    return success;
    }
    
    @Override
    public void done() {
    }                                          
    };
    worker.execute();
}

/****************
 **** WORKERS**** 
 */

class OAuthWorker extends SwingWorker<Boolean, String>{
/*
 * Thread that handles the authentication part. Launched when the "Log In"-button is clicked.
 */     
    public OAuthWorker(){}
      
    /*
     * Manages the OAuth login procedure
     */
    @Override
    public Boolean doInBackground() {
        
        StatusPane.setText("Please log in...");
        Boolean success = false;
        ConfusaUI.this.setCursor(Cursor.getPredefinedCursor(Cursor.WAIT_CURSOR));
        try{
            oas.startAuthenticationAndLaunchBrowser(); // Starts the oauth handshake. Launches a browser for login.
            ConfusaUI.this.setCursor(Cursor.getDefaultCursor());
        
            String message = "";
            Boolean loggedIn = false;
            int tries = 3;
            while(!loggedIn){
                message = "Please log in through your web browser before proceeding.";
                Object[] options = {"I am logged in"};
                saveCertOption.showOptionDialog(ConfusaUI.this, message, "Please log in...", JOptionPane.DEFAULT_OPTION, JOptionPane.INFORMATION_MESSAGE,null, options, options[0]);
                ConfusaUI.this.setCursor(Cursor.getPredefinedCursor(Cursor.WAIT_CURSOR));
                loggedIn = oas.completeAuthentication(); // When login is successful this will complete the handshake and download the access token
                ConfusaUI.this.setCursor(Cursor.getDefaultCursor());
           
                if (!loggedIn){
                    tries--;
                    message = "Authentication failed. You are not properly logged in. Please log in...";
                    JOptionPane.showMessageDialog(ConfusaUI.this, message, "Error", JOptionPane.ERROR_MESSAGE);
                //return false;
                }
                if (tries==0)
                    return false;
            }
            message = "Login successful";
            saveCertOption.showMessageDialog(ConfusaUI.this, message, "Login complete",JOptionPane.INFORMATION_MESSAGE);
        
            success = true;
            StatusPane.setText("Your are logged in. Press \"Download certificate.\" to retrieve a signed certificate.");
            logInButton.setEnabled(false);
            downloadCertButton.setEnabled(true);
        }catch(Exception e){
            e.printStackTrace(System.out);
            StatusPane.setText("Problems starting authentication.");
        }
        
       return success; 
    }

    @Override
    public void done() {
    }
}


class ConfusaWorker extends SwingWorker<Boolean,String>{
/*
 * This thread handles communication with the Confusa server to download the certificate.
 */
    Boolean success = false;
    String message = "";
    String certPath = "";
    public ConfusaWorker(){}

    
    /*
     * Generates CSR, retrieves the signed certificate and saves to disk. 
     */
    @Override
    public Boolean doInBackground(){
        
        ConfusaUI.this.setCursor(Cursor.getPredefinedCursor(Cursor.WAIT_CURSOR));
        StatusPane.setText("Downloading certificate."); 
       
        confusa = new ConfusaSLCSApp(oas);	
    
    	confusa.uploadCsr(); // Generate a certificate request and upload it to the Confusa server
	confusa.approveCsr();	// Approve and sign the request
	String certReply = confusa.downloadCertificate(); // Download the signed certificate
        certPath = confusa.getCertPath()+".p12";
        message = "Save certificate to "+certPath+"?";
        
        ConfusaUI.this.setCursor(Cursor.getDefaultCursor());
        int choice = saveCertOption.showConfirmDialog(ConfusaUI.this, message, "Save certificate to disk",JOptionPane.YES_NO_OPTION);// aComponent);
        if(choice == JOptionPane.NO_OPTION){
            int returnVal = jFileChooser1.showOpenDialog(ConfusaUI.this);
            if(returnVal != JFileChooser.APPROVE_OPTION)
                return false;
            File file = jFileChooser1.getSelectedFile();
            String folder = file.getParentFile().getAbsolutePath()+System.getProperty("file.separator");
            String name = file.getName();
            confusa.setCertName(name);
            confusa.setCertDir(folder);
            certPath= folder+name;
        }
        if((new File(certPath)).exists()){
            message = certPath+" already exists. Overwrite?";
            choice = saveCertOption.showConfirmDialog(ConfusaUI.this, message, "File already exists",JOptionPane.YES_NO_OPTION);// aComponent);
            if(choice == JOptionPane.NO_OPTION){
                int returnVal = jFileChooser1.showOpenDialog(ConfusaUI.this);// aComponent);
                if(returnVal != JFileChooser.APPROVE_OPTION)
                    return false;
                File file = jFileChooser1.getSelectedFile();
                String folder = file.getParentFile().getAbsolutePath()+System.getProperty("file.separator");
                String name = file.getName();
                confusa.setCertName(name);
                confusa.setCertDir(folder);
                certPath= folder+name;
             }
        }
        ConfusaUI.this.setCursor(Cursor.getPredefinedCursor(Cursor.WAIT_CURSOR));
        
        String pass = "";
        while(pass.trim().length()==0)
            pass = saveCertOption.showInputDialog("Please choose a password used when importing the certificate to your browser.");
        
	StatusPane.setText("Saving certificate.");
	confusa.saveCertificate(certReply, pass);
        
        StatusPane.setText("Certificate downloaded to "+certPath);
        goToGriddk.setEnabled(true);
        downloadCertButton.setEnabled(false);
        logInButton.setEnabled(false);
        success = true;
        return true;
    }
    
    /*
     * Implicitly called when doInBackground() is complete. If the local OS is windows, executing the p.12 certificate file will start the cert wizard.
     */
    @Override
    public void done(){
        ConfusaUI.this.setCursor(Cursor.getDefaultCursor());
        if(success){
            message = "Certificate saved";
            JOptionPane.showMessageDialog(ConfusaUI.this, message,"Finished", JOptionPane.INFORMATION_MESSAGE);
        
                if(System.getProperty("os.name").startsWith("Windows")){
                    Boolean openFileSuccess = false;
                    try{
                        ProcessBuilder pb = new ProcessBuilder("explorer",certPath);
                        Process p = pb.start();
                        p.waitFor();
                        openFileSuccess = true;
                    }catch(Exception e){
                        e.printStackTrace(System.out);
                    }
            
                    if(!openFileSuccess){
                        message = "Could not open the file. Please install the certificate manually";
                        JOptionPane.showMessageDialog(ConfusaUI.this, message, "Error", JOptionPane.ERROR_MESSAGE);
                    }
            }
        
        StatusPane.setText("Import the certificate (.p12 format) to your web browser. \n\n"+
        "Example (Firefox) : Preferences->Advanced->View Certificates->Import...\n\n"
        );
        
        }else{ // did not save cert
                message = "No certificate was saved";
                JOptionPane.showMessageDialog(ConfusaUI.this, message,"Finished", JOptionPane.INFORMATION_MESSAGE);
            }
        }
    }

    /**
     * @param args the command line arguments
     */
    public static void main(String args[]) {
        java.awt.EventQueue.invokeLater(new Runnable() {
            public void run() {
                new ConfusaUI().setVisible(true);
            }
        });
    }
    
    // Variables declaration - do not modify//GEN-BEGIN:variables
    public javax.swing.JTextPane StatusPane;
    private javax.swing.JButton downloadCertButton;
    private javax.swing.JButton goToGriddk;
    private javax.swing.JFileChooser jFileChooser1;
    private javax.swing.JLabel jLabel1;
    private javax.swing.JLabel jLabel2;
    private javax.swing.JScrollPane jScrollPane1;
    private javax.swing.JScrollPane jScrollPane2;
    private javax.swing.JSeparator jSeparator1;
    private javax.swing.JTextArea jTextArea1;
    private javax.swing.JButton logInButton;
    private javax.swing.JOptionPane saveCertOption;
    // End of variables declaration//GEN-END:variables
    
}
