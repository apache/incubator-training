#  Licensed to the Apache Software Foundation (ASF) under one or more
#  contributor license agreements.  See the NOTICE file distributed with
#  this work for additional information regarding copyright ownership.
#  The ASF licenses this file to You under the Apache License, Version 2.0
#  (the "License"); you may not use this file except in compliance with
#  the License.  You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

##########################################################################################
# Build Apache Training
##########################################################################################

# Fixed version of this in order to have a fixed JDK version
FROM azul/zulu-openjdk:21 as build

# Install some stuff we need to run the build
RUN apt update -y
RUN apt install -y git graphviz nodejs npm wget bzip2 python3 python3-pip cargo
RUN python3 -m pip install --upgrade pip setuptools seqdiag blockdiag actdiag nwdiag convert racks opc-diag
#RUN npm install vega pango
RUN wget -qO- https://get.haskellstack.org/ | sh
RUN wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
RUN bunzip2 phantomjs-2.1.1-linux-x86_64.tar.bz2
RUN tar -xvf phantomjs-2.1.1-linux-x86_64.tar

# Required for running on Windows systems
RUN apt install -y dos2unix

# Change the working directory (where commands are executed) into the new "ws" directory
WORKDIR /ws