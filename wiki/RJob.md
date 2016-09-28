# How to run an R job for statistical computing.

# Running an R job on the grid.dk web portal

R is an open source statistical computing application that is used in a wide range of research areas. Running an R program from the command line is done by typing
```
 $R <my_rprogram.R --args dataset.txt > results.txt
```

where `R` is the R binary, `my_rprogram.R` is our program and `dataset.txt` contains the data we want to process. The output is then redirected to the result file `result.txt`.  

To run an R job on grid.dk resources, we go to the <a href="https://grid.dk/cgi-bin/submitjob.py">submit job page</a> and fill out the fields as follows.

## Command, input and output files

![](images/simple_job_r.png)

## Runtime environment

![](images/simple_job_r_RE.png)

## Submitting the job

After filling out the fields, click the "submit job" button. Your job will now be executed on grid.dk resources.

## mRSL script

As a note to users who want to use scripts, the .mRSL script corresponding to the above should look like this:

```
::EXECUTE::
$R <myrprogram.R --args dataset.txt > results.txt

::INPUTFILES::
my_rprogram.R
dataset.txt

::OUTPUTFILES::
results.txt

::RUNTIMEENVIRONMENT::
R-2.13.1
```