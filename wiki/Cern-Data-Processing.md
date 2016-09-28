# CERN data processing

# Introduction

<img src="http://www.atlas.ch/photos/atlas_photos/selected-photos/full-detector/0803012_01-A4-at-144-dpi.jpg" width="612"/>

The ATLAS detector is one of 4 very large detectors at the Large Hadron Collider at CERN, Geneva. It detects particles and radiation resulting from the collision of two protons at near light speed. The collected data is stored in data files, each of which contain a number of so-called events.

Each of the 303 jobs of the current example, uses ATLAS software to process a data file of ~120 MB, extracting information relevant for the end-analysis, and produces an output file of ~16 MB.

At the end, these files can be further analyzed to produce the final plots.

This example illustrates the use of the {{{GridPilot}}} GUI when running large amounts of jobs that need data from international grid storage resources, such as those hosting ATLAS data.

# Installing {{{GridPilot}}}

Installers for all common platforms are provided on the [GridPilot download page](http://www.gridfactory.org/download/).

An introduction to {{{GridPilot}}} for ATLAS physicists can be found in the paper [ATLAS data processing with GridPilot on NorduGrid and WLCG](http://cdsweb.cern.ch/record/1359226?ln=en).

# Configuring {{{GridPilot}}} to submit to DCSC resources

When running {{{GridPilot}}} for the first time, you'll be asked a series of questions. On most panes, you can simply click "OK", but on the computing systems pane, you should remember to enable "**NG**", which is the {{{NorduGrid}}}/ARC plugin, set your submission cluster to "**gateway01.dcsc.ku.dk**" and your virtual organization to "**ATLAS**".

Notice that you cannot run the application if you're not member of the ATLAS virtual organization, i.e. if you're not an ATLAS physicist. If you're not an ATLAS member, setting your virtual organization to ATLAS will have no effect.

# Importing the example application

 - choose {{{Import application(s)}}} from the {{{File}}} menu
 - navigate to the folder {{{/apps/high_energy_physics/atlas_d3pd_boildown}}}
 - click {{{OK}}}

# Running the example

Select the new application and click  {{{Run}}}.

Runs of the application are [described in detail](http://www.gridfactory.org/2010/12/22/cernatlas-n-tuple-boildown-on-nordugrid-wlcg-and-gridfactory/) on the {{{GridPilot}}} web site.