# How to run a python job

# Running a Python job

Python is a popular scripting language known for its simple syntax and readability. To run a python job on grid.dk we need to upload the python file and specify that we need a python runtime environment.

### Command

The file `myprog.py` contains the code we want to run. In the **Execute commands** field we write the command to execute the file.

```
$PYTHON myprog.py
```

`$PYTHON` is an environment variable on the resource that points to Python.

### Input file

After uploading the python file to our home directory we write it in the **Input Files** field.

```
myprog.py
```

In the submit <a href="https://portal.grid.dk/cgi-bin/submitjob.py">job user interface</a> it would look like this.

![](images/simple_job_python.jpg)

### Runtime Environment

Since we are using python we specify that we need it as runtime environment on the resource. Choose any of the available Python versions:

![](images/refmatch_selectRE.jpg)

### Submitting the job

Now click "submit job".


## User script

If using a the MiG CLI or API, the .mRSL file to submit the job would look like this:

```
::EXECUTE::
$PYTHON myprog.py

::INPUTFILES::
myprog.py

::RUNTIMEENVIRONMENT::
PYTHON-2-1.0

```