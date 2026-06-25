#!/usr/bin/env bash
set -euo pipefail

REPO="LukeGeneva/remind"
INSTALL_DIR="/usr/local/bin"
BINARY="remind"

if [[ "$(uname -s)" != "Darwin" ]]; then
    echo "Error: remind is macOS-only." >&2
    exit 1
fi

ARCH="$(uname -m)"
ASSET="remind-${ARCH}"

echo "Fetching latest release..."
LATEST=$(curl -fsSL "https://api.github.com/repos/${REPO}/releases/latest" \
    | grep '"tag_name"' \
    | sed 's/.*"tag_name": *"\([^"]*\)".*/\1/')

if [[ -z "$LATEST" ]]; then
    echo "Error: could not determine latest release." >&2
    exit 1
fi

echo "Installing ${BINARY} ${LATEST} (${ARCH})..."

URL="https://github.com/${REPO}/releases/download/${LATEST}/${ASSET}"
TMP=$(mktemp)
trap 'rm -f "$TMP"' EXIT

if ! curl -fsSL "$URL" -o "$TMP"; then
    echo "Error: no binary available for ${ARCH}. Check https://github.com/${REPO}/releases" >&2
    exit 1
fi

chmod +x "$TMP"

if [[ -w "$INSTALL_DIR" ]]; then
    mv "$TMP" "${INSTALL_DIR}/${BINARY}"
else
    sudo mv "$TMP" "${INSTALL_DIR}/${BINARY}"
fi

echo "Installed: ${INSTALL_DIR}/${BINARY}"
