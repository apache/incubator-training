# How To Do Basic Stuff

This documents some of the simple stuff that you may need to do to get
started. Some day, we should write real docs! But today is not that day.

## Creating a new presentation

To create a new presentation, `cd` into the directory that you'd like
your presentation to get created under.

`cd Apache/ComDev`

And then run:

`mvn archetype:generate -DarchetypeGroupId=org.apache.training -DarchetypeArtifactId=content-archetype -DarchetypeVersion=1.3.0-SNAPSHOT`

This will give you a list of questions to answer in order to create the
new presentation:

  Define value for property 'groupID': org.apache.training.presentations
  Define value for property 'artifactID': HowToDoStuff
  Define value for property 'version' 1.0-SNAPSHOT: :
  Define value for property 'package' org.apache: :
  Confirm properties configuration:
  apacheTrainingToolsVersion: 1.3.0-SNAPSHOT
  groupID: org.apache.training.presentations
  artifactId: HowToDoStuff
  version 1.0-SNAPSHOT
  package: org.apache
  Y: :

In practice you'll have to answer the first two questions (`groupID` and
`articactID`) and just hit enter for the others. Answer Y at the end to
start the generation process.

Once this completes, you'll have the starter presentation. You may need
to copy the directory `src/theme` from another presentation to get the
starter CSS file(s).

Update the file `pom.xml` to set the presentation's name and
description.

Edit your content in the file `src/main/asciidoc/index.adoc` to create
your content.

Rebuild your presentation by going to the top level directory of the
repository and running `mvn install`.


