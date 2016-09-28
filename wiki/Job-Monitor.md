# The job monitor

# Job monitoring

The status of the jobs can be viewed under <a href="https://portal.grid.dk/cgi-bin/jobman.py">Job monitor</a>. On this page, all the jobs submitted by the user are listed. Each job is shown by a row containing a "JobID" given by the grid-dk server, a status and a date. The date field shows the time when the job was submitted.

![](images/jobmon_cut1.jpg | width=1000)

The status field indicates what is currently happening with the job. Here is typical example 

  1. After starting the job it will go into "QUEUED" status.
  1. When a suitable grid resource host has presented itself, it will be handed the job and the status will change to "EXECUTING".
  1. When the job is done executing it will be given the status "FINISHED".

## Job management

A job can be controlled by right-clicking on it. This enables the user to cancel or resubmit a running job. 

![](images/jobmon_cut2.jpg | width=1000)

From the right-click menu under "raw description" it is possible to see the .mRSL file that was used to submit the job. The menu items "Output Files" and "Status Files" shows the output files and status files of a finished job. In fact, a job need not be finished before the status files can be viewed. The "live output" option enables the user to retrieve temporary status files of an executing job. 


## Status files

In addition to the user specified output files, each job produces a set of system files called the status files. These files include the standard output and standard error print outs of the grid resource process. Standard output and standard error can be very helpful in monitoring the grid job. When choosing the right-click option "Status Files" mentioned
previously, the file manager will be opened showing the files.

![](images/jobmon_cut3.jpg | width=600)