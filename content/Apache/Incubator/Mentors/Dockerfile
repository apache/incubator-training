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
RUN python3 -m pip install --upgrade pip setuptools==57.5.0 seqdiag blockdiag actdiag nwdiag convert racks opc-diag pillow==9.5.0

#ENV CONDA_DIR /opt/conda
#RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh -O /root/miniconda.sh
#RUN sh /root/miniconda.sh -b -p $CONDA_DIR
#ENV PATH=$CONDA_DIR/bin:$PATH
#RUN conda update -y conda
#RUN rm /root/miniconda.sh
#RUN wget --quiet https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-arm64.sh -O /root/miniconda.sh && sh /root/miniconda.sh -b -p /opt/conda
#ENV PATH=$CONDA_DIR/bin:$PATH

# Install vg2svg for rendering vega diagrams
# NOTE: Installing vega-cli doesn't seem to work as dependencies are not available for arm64 (silicon)
ENV NODE_VERSION=18.20.4
RUN curl --silent -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
RUN /root/.nvm/install.sh
ENV PATH=/root/.nvm/versions/node/v$NODE_VERSION/bin:$PATH
#RUN npm install --no-audit vega

#RUN wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
#RUN bunzip2 phantomjs-2.1.1-linux-x86_64.tar.bz2
#RUN tar -xvf phantomjs-2.1.1-linux-x86_64.tar

# Install ERD
RUN apt install -y golang
ENV PATH=/root/go/bin:$PATH
RUN go install github.com/kaishuu0123/erd-go@v1.4.6

# Install Syntrax
# https://kevinpt.github.io/syntrax/
# Problem is, that newer versions of python don't have use_2to3
#RUN apt install -y libcairo2-dev pkg-config python3-dev python3-gi python3-gi-cairo gir1.2-gtk-4.0
RUN apt install -y libcairo2-dev pkg-config python3-dev python3-gi gir1.2-gtk-4.0
RUN python3 -m pip install --upgrade pycairo pango syntrax
# For some reason, if we install this before the python stuff, it doesn't work
RUN apt install -y python3-gi-cairo

# Install Mermaid
# Mermaid seems to have issues with Apple Silicon
#RUN apt install -y nodejs npm
RUN npm install -g @mermaid-js/mermaid-cli

# Required for running on Windows systems
RUN apt install -y dos2unix

# Change the working directory (where commands are executed) into the new "ws" directory
WORKDIR /ws