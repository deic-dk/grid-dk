# Staff meeting 8/9-2009

Minutes by Frederik

Present: Frederik, Jost,Jonas (Benjamin is on vacation)

# ARC-MiG integration

This meeting was held specifically to discuss the direction to take for the ARC integration in the MiG portal that Jost is working on.

Jost had produced a <a href="http://code.google.com/p/grid-dk/source/browse/trunk/braindumps/MiGResourceARC.tex">writeup</a> of the issues.

We decided to initially go with Jost's option 1 - i.e. simply allow a user to choose from the web interface whether he wants to submit to ARC or to MiG. When submitting to ARC, the job will then go to where ever the ARC client library chooses. The decision will depend on the RTE dependencies (a) of the job and potentially on the user's VO membership - i.e. his rights on the resources.

Later on we will consider extending this to:

1) allowing the user to explicitly choose both MiG and ARC resources.

2) extend MiG to be able to schedule jobs on ARC resources - by implementing a proxy service, running on the MiG server host, that regularly queries the ARC resources for information on load, RTEs, etc. It should be possible to model this service on the corresponding service that MiG employs for PBS resources (running on the PBS frontend).

a: The list of available ARC RTEs will have been collected from all of the ARC resources.

# Layout and usability improvements of the portal

A number of improvements suggested by Frederik were discussed. It was decided that Jost will try and find the HTML/JS savvy manpower on DIKU. If this fails, we will decide who of us will do it.

The discussion was based on the email exchange pasted below for reference.

-----------

> > Below is a list of
> > some proposals - we can discuss next week.

Right, please keep in mind that most pages require the user auth.

I've commented a bit on your proposals below, and we can discuss them in
further detail tomorrow.

> > - https://portal.grid.dk/ should take me to the dashboard, not the
> > "submit job" page

Done, this has been the default redirect in /index.html for a while, but
just wasn't updated on grid.dk

> > - the top banner should go away and instead there should just be a
> > "grid.dk" headline at the top of the navigation bar
> > 
> > - "MiG" and "minimum intrusion grid" should be removed from the text on
> > the dashboard and everywhere else

Cosmetic changes can be done either with a custom CSS for grid.dk or
through code changes.
Experiments with CSS are possible directly with the personal css field
on the Settings page, and a global css file can easily be installed if
that is the way we choose. Otherwise we need to patch
mig/shared/html.py, which should be relatively simple, too. Either way
the changes will likely be welcome 'upstream' if made in a flexible way.

> > - the "submit job" page should default to the new form interface (where
> > is it?)

The default was set to textui in the MiGserver.conf:
[SETTINGS]
submitui = textarea fields
(which defines available interfaces and uses the first one as default)

I've swapped the order now, but it is still possible for each user to
override this in SUBMITUI on the Settings page.

Btw, we would also like a user friendly backend to the submit form,
which delivers an unformatted output object text ATM: This change is
already planned 'upstream'.

> > - on the form interface ::RUNTIMEENVIRONMENT:: should be filled in by
> > selecting in a drop-down box

Already there but only possible to select anything now that I added a
runtime environment.

> > - the files page should be simplified: less text, "File view options",
> > "Create directory", "Upload file" should be small links with popups,
> > "Edit file" should be available from the right-click menu - yes this
> > requires some AJAX gymnastics

Good idea. I looked a bit at the Trac code view module which shows file
and dir entries in a sensible way with dirs above files and each one
with a MIME icon and such. Perhaps we can get some inspiration from the
code:
http://trac.edgewall.org/browser/trunk/trac/versioncontrol/web_ui/browser.py

The general layout could surely be improved and enhanced with some AJAX.
I don't mind giving it a shot but I know from experience that it takes
(at least me) ages to build and polish such interfaces. As you know my
graphical design skills are quite limited, too.

> > - VGrids should be called VOs

Possible, but more intrusive changes required in multiple files, I
guess. Quite a few different file hits in a VGrid grep on the code.

> > - Resources should be removed from the navigation bar for normal users -
> > we will create an administration portal section available only for
> > members of an admin VO

Ehm, all users are potential resource owners due to the sandbox support
(SSS and Java VM resources) and there is really no such thing as admin
VOs in MiG.
It is easy to modify the navigation menu with a patch to html.py as
above, however.

> > - Downloads should be removed from the navigation bar. Instead we will
> > make an extended documentation section with links to MiG scripts and
> > other scripts and utilities

Easy to remove, but more work to maintain the downloads elsewhere. A
compromise could be to remove the nav item and include the same link on
an external doc page, but access still requires a MiG account on the
server, then.

> > - Runtime Envs: too much text - put a link to a relevant section of the
> > documentation instead

Requires a patch to the RE content provider module: possible but harder
to maintain.

> > I don't know how configurable the MiG portal is - to accommodate the
> > above we may have to fork it.

Apart from CSS layout, most changes require patching of one or more
source files, as my comments above indicate.
In most cases I think we will be best of by proposing flexible solutions
to be included in the MiG code trunk.