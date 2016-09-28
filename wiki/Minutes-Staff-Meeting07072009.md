# Staff meeting 7/7-2009

Minutes by Jonas

Jost discovered lunarc uses arc library, arclib, that may be used for our purposes as well. There's a python wrapper available that is used in production. We'll have to see if that means general stability.

Jost will remove the the toy certificate access now we have benedict access. Move benedict resources to new DCSC vgrid.

Jost researched lunarc and considers possibly using the interface as frontend to MiG files.

MiG unique DN issue fixed now.
 - external cert can now join - there's a bug in DN extraction on some browsers though.
 - import users works to pull VOMS users is ready and a cron job is prepared. It just needs to be applied and change to a NG server certificate without a passphrase.
 - importuser should add users to corresponding VGrid.
 - we should consider a resource to/from VO mapping for vgrid membership.
 - for now we postpone the task of synchronizing additional VGrids back to VOMS.

Jost reported on SGAS status: there is still discussions about e.g. the database format. 
 - Henrik is working on another project at the moment so SGAS development may slow down.
 - Jost will investigate possibility of using VGrids to control access to on-demand statistics for each vgrid reusing the vgrid monitor approach.

Frederik will investigate status of MiG CA support in NDGF VOMS.

Jost and Jonas will investigate a uid/gid solutions on grid.dk . Perhaps just running everything as apache.