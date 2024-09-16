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
RUN apt install -y git graphviz wget bzip2 python3 python3-pip imagemagick curl protobuf-compiler mc

# Install the version 1.76.0 of the Rust toolchain
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s  -- -y --default-toolchain=1.76.0
ENV PATH="/root/.cargo/bin:$PATH"
# Install svgbob
RUN cargo install svgbob_cli
RUN cp /root/.cargo/bin/svgbob_cli /usr/local/bin

# Forced version of pillow as with version 10 the build fails
RUN python3 -m pip install --upgrade pip setuptools seqdiag blockdiag actdiag nwdiag convert racks opc-diag pillow==9.5.0

# Install vg2svg for rendering vega diagrams
#ENV NODE_VERSION=18.20.4
#RUN curl --silent -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
#RUN /root/.nvm/install.sh
#ENV PATH=/root/.nvm/versions/node/v$NODE_VERSION/bin:$PATH
#RUN npm install --no-audit vega

#RUN wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
#RUN bunzip2 phantomjs-2.1.1-linux-x86_64.tar.bz2
#RUN tar -xvf phantomjs-2.1.1-linux-x86_64.tar

# Install ERD
#RUN cabal v2-update && cabal v2-install erd

# Required for running on Windows systems
RUN apt install -y dos2unix

# Change the working directory (where commands are executed) into the new "ws" directory
WORKDIR /ws