# Feature extraction of medical images

# Introduction

<img src="http://www.gridfactory.org/files/2011/03/000498643000042dcm_small.png">

An enormous amount of medical images are produced at hospitals worldwide. Just at e.g. the radiology department of the Geneva University Hospitals, over 70'000 images are produced daily. To facilitate the analysis of such a huge amount of medical image data, content based information retrieval (CBIR) can be useful: In a CPU-intensive process called indexing, features are extracted from the images. Based on these features, images can be compared with each other in an automatized fashion.

This example illustrates the use of the {{{GridPilot}}} GUI to run such image extraction on a large number of images.

## Installing {{{GridPilot}}}

Installers for all common platforms are provided on the [GridPilot download page](http://www.gridfactory.org/download/).

## Configuring {{{GridPilot}}} to submit to DCSC resources

When running {{{GridPilot}}} for the first time, you'll be asked a series of questions. On most panes, you can simply click "OK", but on the computing systems pane, you should remember to enable "**NG**", which is the {{{NorduGrid}}}/ARC plugin and set your submission cluster to "**gateway01.dcsc.ku.dk**".

# Importing the example application

 - choose {{{Import application(s)}}} from the {{{File}}} menu
 - navigate to the folder {{{/apps/biomed/medgift_image_feature_extraction}}}
 - click {{{OK}}}

# Running the application

Select the new application and click  {{{Run}}}.

Runs of the application are [described in detail](http://www.gridfactory.org/2011/03/12/feature-extraction-of-medical-images/) on the {{{GridPilot}}} web site.