#!/usr/bin/env bash

set -e  # Exit immediately if a command fails
set -u  # Treat unset variables as errors

echo "⚠️ Dependencies required: git and pip"
echo "Cloning and installing Crust..."

# Clone repo
git clone https://github.com/mostypc123/crust
cd crust || { echo "Failed to enter crust directory"; exit 1; }

# Detect platform
OS="$(uname -s)"
DISTRO="unknown"
DISTRO_LIKE=""
if [ -f /etc/os-release ]; then
    . /etc/os-release
    DISTRO="$ID"
    DISTRO_LIKE="$ID_LIKE"
fi

# Platform-specific messages
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

# Ask about --break-system-packages
read -p "Use --break-system-packages? [Y/n] " choice

case "$choice" in
    [nN]*)
        pip install .
        ;;
    *)
        pip install . --break-system-packages
        ;;
esac

# Clean up
cd ..
rm -rf crust

echo "✅ Installation complete!"
