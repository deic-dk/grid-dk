# Runtime Environments

# Runtime Environments

In order to execute a user program on a grid resource it is necessary that all the software dependencies are met. For instance, if the user wants to execute python code, python should be installed at the resource. The runtime environment of a grid resource defines what software is available and can be used in a job.

## Runtime environment overview

When submitting jobs, it is important to be aware of the runtime environment on the resources. A resource is always tied to a virtual organization, so to see the runtime environment on the resources of a given virtual organization we use the virtual organizations page found under <a href="https://portal.grid.dk/cgi-bin/vgridadmin.py"> Virtual Orgs</a> in the left-side menu. On the table of virtual organizations the resource monitor for each is found using the <a href="https://portal.grid.dk/cgi-bin/showvgridmonitor.py?vgrid_name=Generic">Private</a> link in "Monitor" column.

![](images/virt_org_monitor_link.jpg | width=900)


On the top of the virtual organization monitor page there is a summary containing statistics along with a list of applications on the right. The list of entries under the **Runtimeenvironment** column shows which applications are installed on the resources of the virtual organization.

![](images/vo_monitor_RE_cut.jpg | width=900)


## Specifying a runtime environent

When submitting a job it is necessary to specify which runtime environment is required at the resource. This is done by selecting the correct environments in Runtime Environments field of the <a href="https://portal.grid.dk/cgi-bin/submitjob.py">Submit job</a> page.

![](images/jobsubmit_choosing_RE_cut.jpg | width=200)

## Setting up a runtime environment

For an explanation of how to setup your own runtime environment, information is available <a href="http://code.google.com/p/migrid/wiki/SettingUpRuntimeEnvironments">here</a>