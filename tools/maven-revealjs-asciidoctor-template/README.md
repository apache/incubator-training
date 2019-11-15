<!--

  Licensed to the Apache Software Foundation (ASF) under one or more
  contributor license agreements.  See the NOTICE file distributed with
  this work for additional information regarding copyright ownership.
  The ASF licenses this file to You under the Apache License, Version 2.0
  (the "License"); you may not use this file except in compliance with
  the License.  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

-->

# Example presentation with Reveal.JS and Asciidoctor

This directory contains a template project demonstrating:

* creating slides from human-readable markup using [Asciidoctor](https://asciidoctor.org/),
* presented in a web browser using [Reveal.JS](https://revealjs.com) instead of proprietary presentation software, and 
* built and optionally served using [maven](https://maven.apache.org/). 

Notably, this template shows off many of the diagramming tools that can be used with
asciidoctor, including:  

* [PlantUML](http://plantuml.com/) <!-- and [Mermaid](https://mermaidjs.github.io/) --> for generating UML diagrams, 
* [Svgbob](https://github.com/ivanceras/svgbob) and [ditaa](http://ditaa.sourceforge.net/) for generating diagrams from ASCII art,
* [Graphviz](http://www.graphviz.org/) for general graph visualization diagrams,
* [erd](https://github.com/BurntSushi/erd) for entity-relational diagrams,
* [blockdiag](http://blockdiag.com/en/) and its family of tools for network, sequence, rack diagrams, etc., 
* [Syntrax](https://kevinpt.github.io/syntrax/) for railroad diagrams, and  
* [Vega](https://vega.github.io/vega/) for interactive data visualizations.

## Building the presentation

Images are generated using the asciidoctor-diagram project, which integrates [many external tools](https://github.com/asciidoctor/asciidoctor-diagram#specifying-diagram-generator-paths).  Not all presentations will use every tool, but you may need to install some additional software.  

### Installing the diagramming tools 

There are example installation scripts for [Mac](./install-deps-mac.sh) and [linux](./install-deps-centos.sh).
  
With the external tools installed (or if your presentation doesn't use images that require external tools), building is as simple as:

    mvn clean package

### Using the diagramming tools inside docker 

Alternatively, you can use a docker image containing all of the necessary tools:

    # Build the docker image (once).  Takes about 20 minutes.
    cd incubator-training/tools
    docker image build --build-arg USER_ID=$(id -u ${USER}) \
      --build-arg GROUP_ID=$(id -g ${USER}) -t training-build .
    
    # Build the presentation inside the docker image.
    cd incubator-training/tools/maven-revealjs-asciidoctor-template
    docker run -it --rm --volume $HOME/.m2:/home/docker-user/.m2 \
      --volume $PWD:/opt/workdir training-build:latest

* Passing the `USER_ID` and `GROUP_ID` is useful to build presentations with the same user and permissions inside the docker container.
* The `--volume $HOME/.m2:/home/docker-user/.m2` is optional.  Using your local maven `.m2` can significantly speed up the build.

## Running the presentation

The presentation is generated in `target/generated-slides`.  Even if it is possible to run the presentation directly from this directory, some JavaScript extensions don't work in this case. It is highly recommended to run the presentation from a webserver. 

In order to start a local web server serving the presentation, execute the following command:

    mvn jetty:run-exploded
    
As soon as that's done, just point your browser to **[http://localhost:8080/](http://localhost:8080/)**.

You can run the same jetty webserver in a docker container.  This can be useful if you want to run multiple presentations using dfferent ports. 

    docker run -it --rm --publish 58080:8080/tcp \
        --volume $HOME/.m2:/home/docker-user/.m2 \
        --volume $PWD:/opt/workdir training-build:latest \
        -c "mvn jetty:run-exploded"


Alternatively, you can upload or serve the pages using any web server:

    # Demonstrates serving a directory with the Apache HTTP Server
    docker run -d --publish 58080:80 \
         --volume $PWD/target/generated-slides/:/usr/local/apache2/htdocs/:ro \
         httpd:2.4

## Generating PDF versions

In order to generate a PDF version of the presentation just add `?print-pdf` to the url. (Keep in mind, that you have to add it before any `#blahblah`)

The following link should do the trick:

    http://localhost:8080/?print-pdf
    
As soon as that's loaded, just use the normal `print` functionality of the browser and `print as PDF`.

# Implementation details
- Currently it seems as if the system can't detect the 'docinfo' files, so we have to replace the `document.html.slim` file from `asciidoctor-reveal.js` with an updated one, that adds some additional js and css references. This template is located in `libs/docinfo-hack`.
- In order to use the preview of the IntelliJ asciidoctor plugin, you need to set an attribute in the plugin settings: `imagesdir` = `../resources/images`
- The template is adjusted to use the fontfabric [**Panton** font](https://www.fontfabric.com/fonts/panton/), so be sure to have that installed on your presentation machine.
- Any css adjustments can go to `src/main/theme/cc.css` as this is automatically embedded into the themes directory.


<!-- These need to be re-integrated into the presentation and installation scripts.

## Installing third party software:

### Mermaid

    npm install mermaid.cli
    
This will install mermaid under `node_modules/.bin/mmdc`.

### PhantomJS

https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-macosx.zip
-->