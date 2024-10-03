# How To Do Basic Stuff

This documents some of the simple stuff that you may need to do to get
started. Some day, we should write real docs! But today is not that day.

## Creating a new presentation

To create a new presentation, `cd` into the directory that you'd like
your presentation to get created under.

`cd Apache/ComDev`

And then run:

`mvn archetype:generate -DarchetypeGroupId=org.apache.training -DarchetypeArtifactId=content-archetype -DarchetypeVersion=1.3.0`

This will give you a list of questions to answer in order to create the
new presentation:

  Define value for property 'groupID': org.apache.training.content
  Define value for property 'artifactID': training-content-HowToDoStuff
  Define value for property 'version' 1.0.0-SNAPSHOT: :
  Define value for property 'package' org.apache: :
  Confirm properties configuration:
  apacheTrainingToolsVersion: 1.3.0
  groupID: org.apache.training.content
  artifactId: training-content-HowToDoStuff
  version 1.0.0-SNAPSHOT
  package: org.apache
  Y: :

In practice, you'll have to answer the first two questions (`groupID` and
`articactID`) and just hit enter for the others. Answer Y at the end to
start the generation process.

Update the file `pom.xml` to set the presentation's name and
description.

Edit your content in the file `src/main/asciidoc/index.adoc` to create
your content.

Rebuild your presentation by going to the top level directory of the
repository and running `mvn package`.

## Adding your presentation to the Apache Training (incubating) Website

The website of the Apache Training project is built by the module in the directory `site`.

There are two steps that need to be done here, in order to deploy your presentation:

- Add the maven coordinates of your presentation to the `pom.xml` in two locations:
  - As a `dependency` (This ensures maven builds the presentation before trying to use it)
  - As an `artifactItem` inside the `copy-presentations` section (This tells maven to take the war of the presentation module and to unpack it into the output of the website module)

Please be sure to pay attention to the `outputDirectory` element of the `artifactItem`, as this defines where maven will copy the resources. In general, following the naming of the other presentations, that somewhat reflect the directory structure of the modules, makes sense.

Now your presentation would be available on the page, but not yet added to the navigation menu. 
In order to add it to that, you need to do one last step:

- Edit the file `src/site/site.xml` and add an `item` element to the correct place. 

Simply follow the convention of the other presentations and be sure to use the correct path.

As soon as you commit and push your changes, Jenkins will checkout these changes, build your and all other presentations and then update the website.
There should be no other step needed.
