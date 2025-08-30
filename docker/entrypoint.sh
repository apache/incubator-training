#!/usr/bin/env bash
set -euo pipefail

WS_DIR=${WS_DIR:-/ws}

# Detect host uid/gid of the bind mount; default to 1000 if unknown
HOST_UID=$(stat -c '%u' "$WS_DIR" 2>/dev/null || echo 1000)
HOST_GID=$(stat -c '%g' "$WS_DIR" 2>/dev/null || echo 1000)

# If the bind mount is owned by root (0), allow env overrides; else use stat values
if [ "$HOST_UID" = "0" ] && [ "${UID:-}" != "" ]; then HOST_UID="$UID"; fi
if [ "$HOST_GID" = "0" ] && [ "${GID:-}" != "" ]; then HOST_GID="$GID"; fi
if [ "$HOST_UID" = "0" ]; then HOST_UID=1000; fi
if [ "$HOST_GID" = "0" ]; then HOST_GID=1000; fi

# Create group/user if missing (ids-only; no home needed)
if ! getent group "$HOST_GID" >/dev/null; then groupadd -g "$HOST_GID" hostgrp; fi
if ! id -u "$HOST_UID" >/dev/null 2>&1; then useradd -u "$HOST_UID" -g "$HOST_GID" -M -s /bin/bash hostusr; fi

# Ensure a writable HOME inside the bind mount for tools writing dotfiles
export HOME="$WS_DIR/.home"
mkdir -p "$HOME"

# Prefer Maven repo inside the workspace unless caller overrides
export MAVEN_CONFIG="${MAVEN_CONFIG:-$HOME/.m2}"

# Exec final command as host uid:gid
exec gosu "$HOST_UID:$HOST_GID" "$@"
