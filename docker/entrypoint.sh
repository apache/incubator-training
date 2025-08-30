#!/usr/bin/env bash
set -euo pipefail

WS_DIR=${WS_DIR:-/ws}

# Detect host uid/gid of the bind mount; default to 1000 if unknown
HOST_UID=$(stat -c '%u' "$WS_DIR" 2>/dev/null || echo 1000)
HOST_GID=$(stat -c '%g' "$WS_DIR" 2>/dev/null || echo 1000)

# Create group if needed (skip if GID already exists)
if ! getent group "$HOST_GID" >/dev/null; then
  groupadd -g "$HOST_GID" hostgrp
fi

# Ensure a writable HOME inside the workspace
HOST_HOME="$WS_DIR/.home"
mkdir -p "$HOST_HOME"
# Make sure it's owned by the target uid:gid; this only changes the small .home dir
chown "$HOST_UID:$HOST_GID" "$HOST_HOME"

# Create user if needed, with home set to $WS_DIR/.home but do NOT auto-create /home/*
if ! id -u "$HOST_UID" >/dev/null 2>&1; then
  useradd -u "$HOST_UID" -g "$HOST_GID" -M -d "$HOST_HOME" -s /bin/bash hostusr
fi

# Export HOME so tools that honor env use it; matches passwd home to avoid surprises
export HOME="$HOST_HOME"

# Optional: Maven config inside HOME (prevents writing to /root/.m2)
export MAVEN_CONFIG="${MAVEN_CONFIG:-$HOME/.m2}"

# Drop privileges and run the requested command
exec gosu "$HOST_UID:$HOST_GID" "$@"
