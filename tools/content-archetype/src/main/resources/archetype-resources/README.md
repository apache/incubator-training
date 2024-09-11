<!--

  Licensed to the Apache Software Foundation (ASF) under one or more
  contributor license agreements.  See the NOTICE file distributed with
  this work for additional information regarding copyright ownership.
  The ASF licenses this file to You under the Apache License, Version 2.0
  (the "License"); you may not use this file except in compliance with
  the License.  You may obtain a copy of the License at

      https://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

-->

# Presentation with Reveal.JS and AsciiDoctor

Remarks:
- In order to use the preview of the IntelliJ asciidoctor plugin, you need to set an attribute in the plugin settings: `imagesdir` = `../resources/images`
- In order to generate the diagrams, GraphVIS needs to be installed locally. Get it from: http://www.graphviz.org/
- Any css adjustments can go to `src/main/theme/apache.css` as this is automatically embedded into the themes directory.

## Building the presentation

By running the following command, you can generate the presentation:

    mvn package
   
## Running the presentation

In order to show the presentation, go into the `target` directory and look for a directory named {artifactId}-{version}.
This direcotry contains an `index.html` file.

Simply open this in any browser of your choice.

## Generating PDF versions

In order to generate a PDF version of the presentation just add `?print-pdf` to the url. (Keep in mind, that you have to add it before any `#blahblah`)

The following link should do the trick:

    http:///{someFilePath}/?print-pdf
    
As soon as that's loaded, the presentation will look a bit odd. Now just use the normal `print` functionality of the browser and select `print as PDF`.

## Installing third party software:

### Mermaid

    npm install mermaid.cli
    
This will install mermaid under `node_modules/.bin/mmdc`.

### PhantomJS

https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-macosx.zip
