# Molecular docking on grid.dk

<!-- No auto-Table of Contents support! -->

# Introduction

Molecular docking is a method used in the area of drug design research. The basic theory of drug design is that a medical drug can be constructed from ligand molecules that are known to affect a given target molecule. A virtual molecular docking experiment simulates the interaction between a target and a ligand. If the ligand can "dock" in a structural cavity of the target molecule, there is a chance that this will affect its biological behavior. Since the pool of ligand candidates is often enormous, this presents a large computational problem. Because each docking simulation is an independent process, the problem is well-suited for grid computing where we can execute several jobs in parallel.

# Files of this example

The files of this example can be downloaded [here](code_examples/moldocking/moldocking.zip).

# Molecular docking on grid.dk

A basic grid computing technique is to fragment our workload into several independent jobs that can be executed in parallel on the grid resources. A simple way to fragment a molecular docking procedure is to use a different ligand molecule for each job. Hereby we can dock multiple ligands to the same target molecule in parallel.

![](images/refmatch_simple_grid_method.jpg | width=400)

## Docking software

To do grid molecular docking on grid.dk, we first need an application that can perform molecular docking. The Molegro Virtual Docker (MVD) is such an application. It can be downloaded for most of the common operating systems(Linux, MAC, MS Windows) from <a href="http://www.molegro.com/">www.molegro.com</a>.

<img src="http://www.molegro.com/images/mvdbox-small.png"><img>

The settings and parameters of the docking procedure are included in a ".mvdscript" file that we input to the mvd docking application. A molecular docking procedure is executed with the command:

```
mvd script.mvdscript -nogui
```

As mentioned, the file [`script.mvdscript`](code_examples/moldocking/script.mvdscript) contains a number of execution settings along with paths to the molecule files. For each docking procedure we need a target molecule and at least one ligand to dock. The `-nogui` flag specifies that we want to run in command-line mode. 

## Creating a grid.dk molecular docking job

To run a molecular docking job on a grid resource, we must first upload the input files, an MVD input script and some molecule files, to the grid.dk server. This can be done with the <a href="https://portal.grid.dk/cgi-bin/fileman.py">file manager</a>. Since Molegro is proprietary software, we must also upload a valid Molegro license. A trial license can be obtained from <a href="http://www.molegro.com/">www.molegro.com</a>

Our grid job gathers the output files in a tar file `output.tar` after executing the actual docking job.

After uploading the input files, a virtual docking job can be submitted on the [Submit Job](https://portal.grid.dk/cgi-bin/submitjob.py?template_path=../job_templates/moldocking.mRSL) page: 

![](images/moldock_gridjob_cut1.png)

It is important to specify that we require the Molegro runtime environment to be installed on the computing resource:

![](images/moldock_gridjob_cut2.png)

## Running multiple jobs

When creating a grid application we usually want to submit several jobs at a time. This conveniently done in a Python script. Our script uses the MiG API provided by the [miglib.py](code_examples/refmatch/miglib.py) module to communicate with the grid.dk server. Our example grid molecular docking script, [grid_moldocking.py](code_examples/moldocking/grid_moldocking.py), uploads our input files, generates job descriptions and then submits a couple of jobs.  

## Job monitoring and output retrieval

After submitting, we can follow the progress of the jobs on the [Job Monitor](https://portal.grid.dk/cgi-bin/jobman.py):

![](images/moldock_jobmon.jpg)

When a job has finished we can locate and download the output file with the [File Manager](https://portal.grid.dk/cgi-bin/fileman.py):

![](images/moldock_fileman.jpg)