# Staff meeting 21/7-2009

Minutes by Jonas

Jost is on vacation, so only Benjamin, Jonas and Frederik attended.

Benjamin demoed web start app to provide login and cert generation using confusa
 - still needs automatic exporting of key and p12 cert in some default location.
 - probably should add a note about this writing in text
 - merge generation into login button
 - add logout button to auto clean up certificate and key
 - so interface is just login and logout button with key and cert hidden underneath

For the entire end solution login process to work we also need:
 - MiG cert error page should be modified to redirect or link to webstart app
 - auto add all users with a valid (even just generated) cert as MiG users
 - add all users to unprivileged VO (Generic) immediately so that they can get started (this happens automatically with Generic VGrid)
 - access control is only applied when assigning unknown users to VOs

In production on portal.grid.dk: users should be redirected/proxied to login on WAYF and sent back to web start app after login (investigate redirect back support)
Benjamin will try to simplify the work flow as much as possible in order for user login to require a minimal effort.
Jonas will investigate the possibilities of auto adding new users with a validated certificate.

Portal MiG server status:
 - runs as apache with latest svn version after many problems with user separation and permissions
 - still problems with cert extraction on sign up page of portal server:
  - check that SSL cert env vars are available (os.environ), check apache conf
 - Still need to import users from VOMS and add to DCSC VGrid in cron job
 - Existing Aalborg resource did not work as they shut down the corresponding back end queue (Sister @ benedict)
 - New Aalborg resource (Brother @ benedict) seems to work but only minimally tested
 - Job submit interface is cleaned up and now supports a simplified field version where job descriptions are entered or selected from drop down as appropriate
 - WSGI interface is fully functional and could be used to separate apache and MiG users if mod_wsgi is available.

We will all continue with other active tasks as usual, too.

Benjamin is going on vacation for three weeks at the end of August and so am I (Jonas) for two weeks at the beginning of August.