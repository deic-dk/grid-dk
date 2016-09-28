# Staff meeting 9/2-2010

Minutes by Frederik

Status and planning meeting at NBI.

Attending: Frederik, Jost, Benjamin, Jonas


## Information from Frederik

WAYF/Terena integration dropped for now; moving on with standard grid
certificates from either Jonas, Anders or TDC.

## Overall plan for February/March

  - Extend our library of runtime environments and and documented use
cases. Start with Benjamin's 3 use cases and consider common ones like
BLAST, Gaussian and Dalton.
  - Documentation on the Wiki (all)
  - Usability of the portal (Jonas, Jost - see below).


Once this is in place:

  - Statistics (Jost)
  - File serving

## Portal improvements

### Navigation bar

Responsibility: Jost

  - hovers
  - Move "Files " one up
  - Move "Resources" one up
  - Move "Runtime Envs" to top
  - Remove "Shell" - allow reenabling in preferences
  - "VGrids" -> "Virtual Organizations" or "Grids" or "Virtual orgs"
  - "Jobs" -> "Job Monitor"
  - Remove "Downloads" - put a link on the Wiki
  - Add "Statistics" item
  - Add "Documentation" item

### Dashboard

Responsibility: Jonas

  - Remove "Personal Settings" section (configurable)
  - "Status" -> "Your status": table, include disk space used on our server
  - "Resource status": no. of resources that are alive with number of nodes on each

### Runtime environments

Responsibility: Jost

  - Move the documentation to the Wiki

Responsibility: Jonas

  - Details: "Environments" --> "Environment variables set by this runtime
environment", add $, move up, perhaps add 'example' field

### Files

Responsibility: Jonas

  - hovers on "system" folders/links

Responsibility: negotiate!

 - Bonus task: Add busy markers while loading jobs with json from server

### Submit job

Responsibility: Jonas

  - Target Resources empty!?

Responsibility: Jost

  - "Upload file" ?
  - Bonus task: polish with AJAX foldable items, file selectors, etc

### Job monitor

Responsibility: negotiate!

 - Bonus task: Add busy markers while loading jobs with json from server

### Resources

Responsibility: Jonas

  - Remove sandbox and one-click stuff (configurable)
  - List all known resources; those that one can administer should have an
"Administer" link

### Virtual organizations

Responsibility: Jost (support from Jonas if needed for URL ops)

  - Replace with a list of all VOs:
   - those that one is a member of should have a check in a column "member"
   - implement "leave a VO"
   - those that one can administer should have an "Administer" link
  - "Administrate": checkbox: "Get member list from URL"
  - "Administrate": checkbox: "Auto load member list from URL" (cron hook)
  - Remove statistics link

Responsibility: negotiate!

  - Bonus task: polish with AJAX sortable columns etc

### Statistics

Responsibility: Jost

  - 4 sections:
   - "My statistics": CPU usage per resource, usage of RTEs
   - "VO statistics" : CPU usage per resource, per user, usage of RTEs
   - "Resource statistics" : CPU usage per VO, per user, usage of RTEs
   - "Global statistics" : CPU usage per resource, per VO, per user

### Settings

Responsibility: Jonas

  - Do we want all those IMs? (make supported notifications configurable)

### Documentation

Responsibility: Jost

  - A bit of text and a link to the Wiki