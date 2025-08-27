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

# --- Versions in one place ---
ARG RUST_TOOLCHAIN=1.89.0
ARG SVGBOB_VERSION=0.7.6
ARG NODE_VERSION=22.18.0
ARG NVM_VERSION=0.40.3
ARG GO_VERSION=1.25.0
# mermaid-cli 10.x is broadly compatible and avoids breaking changes in 11
ARG MERMAID_CLI_VERSION=10.9.1
ARG ERD_GO_VERSION=1.4.6

ENV DEBIAN_FRONTEND=noninteractive
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# System dependencies
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      ca-certificates \
      git \
      graphviz \
      wget \
      bzip2 \
      python3 \
      python3-pip \
      python3-dev \
      python3-dbus \
      pkg-config \
      imagemagick \
      curl \
      protobuf-compiler \
      mc \
      libcairo2-dev \
      python3-gi \
      gir1.2-gtk-4.0 \
      dos2unix \
     build-essential \
 && rm -rf /var/lib/apt/lists/*

# -------------------------
# Rust
# -------------------------
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs \
  | sh -s -- -y --default-toolchain="${RUST_TOOLCHAIN}"
ENV PATH="/root/.cargo/bin:${PATH}"

# svgbob_cli pinned (use --locked to respect Cargo.lock of the crate and ensure reproducibility)
RUN cargo install svgbob_cli --version "${SVGBOB_VERSION}" --locked \
 && cp /root/.cargo/bin/svgbob_cli /usr/local/bin/

# -------------------------
# Python
# -------------------------
COPY requirements-legacy.txt /tmp/requirements-legacy.txt
COPY requirements-modern.txt /tmp/requirements-modern.txt

# 1) Ensure old setuptools is present and *kept* for legacy packages
RUN python3 -m pip install --no-cache-dir "pip==24.2" "setuptools==57.5.0" "wheel<0.40"

# 2) Install legacy packages using that setuptools (no isolated build env!)
RUN python3 -m pip install --no-cache-dir --no-build-isolation -r /tmp/requirements-legacy.txt

# 3) Install the rest (these can use modern build behavior)
RUN python3 -m pip install --no-cache-dir -r /tmp/requirements-modern.txt

# -------------------------
# Node
# -------------------------
ENV NVM_DIR=/root/.nvm
RUN curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/v${NVM_VERSION}/install.sh -o /root/install_nvm.sh \
 && bash /root/install_nvm.sh \
 && . "$NVM_DIR/nvm.sh" \
 && nvm install ${NODE_VERSION} \
 && nvm alias default ${NODE_VERSION} \
 && nvm use default
ENV PATH="${NVM_DIR}/versions/node/v${NODE_VERSION}/bin:${PATH}"

# Mermaid CLI pinned
RUN npm install -g @mermaid-js/mermaid-cli@${MERMAID_CLI_VERSION}

# -------------------------
# Go
# -------------------------
RUN arch="$(uname -m)"; \
    case "$arch" in \
      x86_64) go_arch=amd64 ;; \
      aarch64|arm64) go_arch=arm64 ;; \
      *) echo "Unsupported arch: $arch" && exit 1 ;; \
    esac; \
    curl -fsSL "https://go.dev/dl/go${GO_VERSION}.linux-${go_arch}.tar.gz" -o /tmp/go.tgz \
 && tar -C /usr/local -xzf /tmp/go.tgz \
 && rm /tmp/go.tgz
ENV PATH="/usr/local/go/bin:${PATH}"
ENV GOPATH="/root/go"
ENV PATH="${GOPATH}/bin:${PATH}"

# erd-go pinned
RUN go install github.com/kaishuu0123/erd-go@v${ERD_GO_VERSION}

# -------------------------
# GTK Cairo Python bridge (must be after Python deps for syntrax)
# -------------------------
# python3-gi-cairo is separate and sometimes needs to be installed last
RUN apt-get update \
 && apt-get install -y --no-install-recommends python3-gi-cairo \
 && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip freeze > /requirements-frozen.txt

# -------------------------
# Final touches
# -------------------------
WORKDIR /ws
