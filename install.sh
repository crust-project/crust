#!/usr/bin/env bash

set -euo pipefail

# Ensure script is running in Bash
if [ -z "${BASH_VERSION:-}" ]; then
    echo "❌ ERROR: This script must be run with Bash, not sh or zsh."
    echo "Use: bash $0"
    exit 1
fi

# Normalize line endings in case of CRLF
if file "$0" | grep -q CRLF; then
    echo "⚠️ Converting CRLF line endings to LF"
    sed -i 's/\r$//' "$0"
fi

echo "⚠️ Dependencies required: git and pip"
echo "Cloning and installing Crust..."

git clone https://github.com/mostypc123/crust
cd crust || { echo "❌ Failed to enter crust directory"; exit 1; }

# Detect platform
OS="$(uname -s)"
DISTRO="unknown"
DISTRO_LIKE=""
if [ -f /etc/os-release ]; then
    . /etc/os-release
    DISTRO="$ID"
    DISTRO_LIKE="$ID_LIKE"
fi

# Platform messages
case "$OS" in
    Darwin)
        echo "⚠️ Crust is untested on macOS. Please help test it!"
        echo "👉 GitHub: https://github.com/mostypc123/crust"
        ;;
    MINGW*|MSYS*|CYGWIN*|Windows_NT)
        echo "⚠️ Crust is untested on Windows. Please help test it!"
        echo "👉 GitHub: https://github.com/mostypc123/crust"
        ;;
    Linux)
        if [ "$DISTRO" != "arch" ] && [[ "$DISTRO_LIKE" != *"arch"* ]]; then
            echo "📦 Please help package Crust for $DISTRO!"
            echo "👉 GitHub: https://github.com/mostypc123/crust"
        fi
        ;;
esac

# Prompt for --break-system-packages
read -p "Use --break-system-packages? [Y/n] " choice
case "$choice" in
    [nN]*)
        pip install .
        ;;
    *)
        pip install . --break-system-packages
        ;;
esac

# Cleanup
cd ..
rm -rf crust

echo "✅ Installation complete!"
