# How to import a certificate

# Introduction

Importing a certificate in your browser's key store means that when a website like [https://portal.grid.dk/](https://portal.grid.dk/) asks for authentication, the browser will present your certificate. For certificates from the Terena Certificate Service, importing is done automatically when you click "Install to keystore", for other certificates see below.

# How to import a certificate manually

Here we show how to import a certificate in Firefox, Chrome and Internet Explorer. It is assumed that you have already have a valid certificate. If not, please go to the <a href="http://code.google.com/p/grid-dk/wiki/AuthenticationAndAuthorization">getting started page</a>. 

## Firefox

In your Firefox window go to the "Edit" tab menu and select "Preferences". Inside the preferences panel, choose the "Advanced" tab and click "View Certificates". Here you can import a certificate by clicking "Import" and selecting your certificate file (**cert.p12**). Please note that you may have to select the "Your Certificates" tab first if the Certificate Manager opens up with another tab active.

![](images/import_cert_help_firefox.jpg | width=400)


## Internet Explorer

If you are using Internet Explorer 8 or later, it will use a central MS Windows certificate database to find your certificate. To install the certificate in Windows, just open the certificate file (**cert.p12**) with your file explorer. This will launch an import certificate wizard.

![](images/import_cert_help_ie.jpg | width=400)

## Chrome

In your Chrome (or Chromium) window click the wrench button at the top right to open the menu and select "Preferences". Inside the preferences panel, choose the "Under the Hood" section and click "Manage Certificates". Here you can import a certificate by clicking "Import" and selecting your certificate file (**cert.p12**).
Please note that you may have to select the "Your Certificates" tab first if the Certificate Manager opens up with another tab active.

![](images/import_cert_help_chrome.jpg | width=400)