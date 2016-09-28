# Collection of ToDos for internal use

# How to use this

Comment on every item in the part labeled "Main List" in free text, adding information or suggesting variants.
Once an item is finished, move it to the "Done List", and cleaned up to leave only the interesting parts.

Bigger development could be documented in separate Wiki pages, and eventually be moved to the migrid wiki if appropriate.

# Main List

### Small bits to improve in MiG

 - VGrid creation page sez "vgrid" (modify success case only)
     and maybe add file manager links to public/private/files space.

 - VGrid member "view" page (?)
   - should have a LOD between VGrid list/overview and single pages

 - hide dot files? especially .vnc`*`, .ngjobs and .proxy
   - maybe not, the user might want them explicitly for some reason

 - inconsistent sorting (upper/lower case) in file manager
     (seen in Brian's screenshots)

 - cron import currently fails with ssl certificate error
    Reason unclear, but POSTPONED. Not crucial for us now.

 - ARC support in practice:
  - Switch to using ":" as the separator for ARC queues.
   - Affected files: mrsltoxrsl, safeinput, arcresources (imported in resman)
  - job cleanup (from .ngjobs) for finished/failed jobs
   - Jobs are usually cleaned up after finishing. Only in case of errors, they are not.
  - *Future work*: use MiG Server certificate proxy if no user proxy available.
 - statistics/logging
  - Redo entire statistics based on the new postgreSQL SGAS (switch when?)
   - Started. Evaluation of setup and basics, then passed on to Jesper.
  - logging ARC job URs to our SGAS instance: need to determine which jobs were issued from the grid.dk server

 - Slides from DCSC user meeting should be stored for other occasions, point out different grid access ways.

-----------------------------------------------------------

# Done List

  - ARC support, choosing target queues for ARC
    affected: arcresources.py json queue information; resman.py showing ARC infos; submit.py; mrsltoxrsl.py; 

    - Format of target resource currently `queue / cluster`, valid FQDN  do not use `/`).
     Should be changed to use a colon.

  - ARC tests (for future work):
    - can access steno based on "dcsc.dk" membership, works with server certificate proxy.
    - Should also accept MiG CA signed certificates. DONE and does not.
    - Submission with proxy signed by MiG server cert. DONE, works.

  - make help link/text for VGrid management, explaining deletion
    VGrid page should have help link, and hint to possible *deletion*