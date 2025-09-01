#!/usr/bin/env bash

# Ensure running in Bash
if [ -z "${BASH_VERSION:-}" ]; then
    echo "❌ ERROR: This script must be run with Bash."
    echo "Use: bash $0"
    exit 1
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
    # shellcheck disable=SC1091
    . /etc/os-release
    DISTRO="${ID:-unknown}"
    DISTRO_LIKE="${ID_LIKE:-}"
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

# Prompt user for --break-system-packages
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
