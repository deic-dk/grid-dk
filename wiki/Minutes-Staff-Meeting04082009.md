# Staff meeting 4/8-2009

Minutes by Jost

Present: Frederik, Jost, Benjamin (Jonas: vacation)

## Reports

### Benjamin

	 continued on user login application
	 (reduced no. of clicks, slightly changed the workflow)
	 -key file, cert. file and p12 package are generated 
	  major issue: automatically importing the p12 
	       we could use a local webserver, if there is no
	       better way to do it
	  problem 2: the p12 seems to need a password in java
  	       either find a way around it (still the browser
	       import will ask for a password), or the user
	       needs to provide another password.

### Jost

	 ARC backend in progress, mockup demonstrated.
	 The MiG web part is used to drive an ARC system 
	 through the arclib python bindings.

	 Our goal for the prototype is basic job submission and 
	 tracking facilities. For now, this is a completely 
	 separate system, which only provides MiG Look&Feel.

	 In the end system, the ARC part should consist of resources
	 and the MiG server submits jobs on behalf of the user.
	 A decision about which systems to use could be taken on 
	 the basis of a certificate inspection.

### Jonas

	 is on vacation for 2 weeks. Copy from his mail:
	 <br>> Apart from enabling the user import from VOMS cron job on
	 <br>> grid.dk, I've been busy dist upgrading and migrating MiG
	 <br>> servers lately.

## Internal deadline

	 we should have a working frontend integrating both MiG and
	 ARC, including login solution, by the end of August.

	 Tentatively planning a demonstration session with guests
	 in the 2nd week of September...

## Vacation info

Jonas is on vacation, will surely be back for the next meeting

Benjamin will go on vacation from August 24 to September 9.

Jost will attend EuroPar from August 24 to August 29, and probably be off work single days in the first week of September.