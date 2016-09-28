# Staff meeting 6/4-2010

This is a just a collection of topics for the next meeting. It should be modified to actual meeting minutes after the meeting :-)

Minutes by ?

Status and planning meeting at NBI.

Attending: ?


# Open questions about certificate procedure for new users

At last meeting we briefly discussed certificate procedures and more or less made a priority list:
1. use DanID, NorduGRID or MiG cert if available
2a. use SSO to get short lived certificate
2b. request certificate from existing CA

2a is pending external factors so we are stuck with 2b for now.

Benjamin wrote a wiki page on the topic of certificates in grid.dk context. The current instructions there for users without a certificate is to use the cert request page on *portal*. However, ~~this page does not send the request to anyone and even if it did~~,,(sending mails is now fixed, was a configuration error and particularity in MiG code),, we don't have a matching CA setup to handle the requests. Do we want to use the portal request page or should we point users to the dk.migrid.org request page?

If we don't want to explicitly mix up MiG servers, it may still be possible to frame the dk.migrid.org request page to make it look like pure portal communication. We could even just send the actual request to the request backend there with JQuery or something.

Using the portal request page requires manual forwarding of the data to dk.migrid.org or running our own grid.dk CA e.g. using the ca-scripts from MiG.


# RTE matching in jobs

The RuntimeEnvironments wiki page should be updated to use the new viewres page to find suitable resources for a given runtime environment once the feature gets included on portal. In trunk and on dk.migrid.org the Resources page now includes a link to view all public resource details including the provided RTEs. This allows the user to find any suitable resources before submitting jobs and thus make sure they will eventually get executed.