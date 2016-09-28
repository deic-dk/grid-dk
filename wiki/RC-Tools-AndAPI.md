# grid.dk scripts

# ARC command-line tools

This section presents more advanced options for submitting jobs to DCSC sandbox resources. Notice that when submitting jobs with ARC, you submit to an ARC server running at the computing resource and the grid.dk server is not involved.

If you're comfortable with the Linux command line and basic scripting, the ARC command-line can be useful for managing multiple jobs.

Requirements:

  - a grid.dk user certificate

## Download

The ARC client distribution (command-line tools) is available for most modern platforms, including Mac OS X, Windows and major Linux distributions from

http://download.nordugrid.org/

## Job submission, monitoring and retrieval

As mentioned, with ARC, you submit directly to an ARC server, like e.g.

```
arcsub -c gateway01.dcsc.ku.dk -f my_job.xrsl
```

This will return a job identifier. The job can then be monitored by

```
arcstat my_identifier
```

Once the job has finished, its output files can be retrieved with

```
arcget my_identifier
```

Jobs can also be monitored via the [NorduGrid monitor page](http://www.nordugrid.org/monitor)

## More information

For more information please visit  http://www.nordugrid.org/