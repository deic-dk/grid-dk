This folder contains view definitions for couchdb-sgas-experimental, 
intended for the grid.dk statistics. 

Generating and uploading the view definitions:

Views are canonical, using identical value output (a triple of 
count,wall-duration,charge) and one and the same reduce function,
which sums up the three components. 
We currently use statistics views for month, week, and day view, 
groupable per user (global user id) or per machine (host).

The actual view definitions are generated from the map function
definitions, by adding a standard reduce and some more json fields
(doc.ID, language..), here done using a small tool program (Haskell).

jost@ibm-jost:$ runhaskell writeViewFile.hs week
jost@ibm-jost:$ runhaskell writeViewFile.hs day
jost@ibm-jost:$ runhaskell writeViewFile.hs month 
jost@ibm-jost:$ 

Format of the file containing the map functions: 

* The file name given to the haskell script defines the name of the
  view file (design document).

* The file starts with one line containing only the name of the view
  (thus, only one word) to be defined using a map function which
  follows.  After the map function definition is finished (indicated
  by a closing brace '}' and a newline, more such definitions may follow. 

Passing a wrong format may lead to obscure other errors, don't expect 
any checks. The tool does not thoroughly parse the definitions, but only 
matches opening and closing braces ("{...}"). For instance, empty lines
between view definitions are not ignored, but a syntax error.


The views are then uploaded to the couchdb, in our case using curl. Here, 
we assume couch is running on the local machine, the database is called 
"usagerecords", and we use the (non-standard) port 15984 (standard for 
couchdb is 5984).

jost@ibm-jost:$ curl --upload-file month.view http://localhost:15984/usagerecords/_design/month 
{"ok":true,"id":"_design/month","rev":"3-5395d0e6d57bab0ddb1ceb1984584806"}

jost@ibm-jost:$ curl --upload-file week.view http://localhost:15984/usagerecords/_design/week
{"ok":true,"id":"_design/week","rev":"1-de2513da69773cbc935d5d69d4944cd6"}

jost@ibm-jost:$ curl --upload-file day.view http://localhost:15984/usagerecords/_design/day
{"ok":true,"id":"_design/day","rev":"1-8bb53f81a755ae1671161692e5d32123"}
jost@ibm-jost:$ 

After uploading, it might make sense to trigger the views using
curl. They will be generated and cached on the DB server.

jost@ibm-jost:$curl http://localhost:15984/usagerecords/_design/week/_view/<one of the views>

