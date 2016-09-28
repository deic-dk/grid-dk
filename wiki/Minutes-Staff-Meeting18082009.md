# Staff meeting 18/8-2009

Minutes by Frederik

Present: Frederik, Jost, Benjamin,Jonas

## Reports

### Benjamin

 - Continued work on user login application.
 - Problems with automatically importing p12 file in browser persist - considering giving up and just popping up some short instructions to the user.
### Jost

 - ARC backend demoed - jobs submitted to benedict.
 - Will now stop working in a MiG branch and instead do a proper integration of ARC in MiG.
  - ARC will be a remote resource on par with PBS.
  - Jonas will contribute.
  - A MiG runtime environment will be created for ARC, where MiG pre- and post-processing hooks can be encapsulated. (On the ARC resources, the runtime script is called with argument 0 on the ARC front-end before the job is submitted to PBS, with argument 1 on the worker node and with argument 2 on the ARC front-end after the job has finished.)
  - Jobs can be copied back to the MiG server via HTTPS. The ARC front-end uses the user grid proxy for this.
  - This means that we must switch on proxy support on the Apache server.
```
     RFC 3820 client proxy certificates are supported with OpenSSL>=0.9.8. To have
     OpenSSL accept them, the following should be added to /etc/sysconfig/httpd,
     /etc/init.d/httpd or an equivalent file:
 
     export OPENSSL_ALLOW_PROXY_CERTS=2
```
 - The ARC integration work will also entail integration of ARC runtime environments in the MiG web interface.
 - Work on accounting/reporting will continue in collaboration with NDGF.

## =Jonas

 - Was on vacation. Nothing to report.