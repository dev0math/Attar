#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
ATTAR_DIR="${HOME}/.attar"
BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
AUTOSTART_DIR="${HOME}/.config/autostart"

echo "=== Installing Attar v3.0.0 ==="

if ! command -v python3 >/dev/null 2>&1; then
    echo "ERROR: python3 is required but not installed."
    exit 1
fi

if ! python3 -c "import PyQt6" 2>/dev/null; then
    echo "WARNING: PyQt6 is not installed."
    echo "Install it with: sudo apt install python3-pyqt6"
    echo "Or: pip3 install PyQt6"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

mkdir -p "${ATTAR_DIR}"
mkdir -p "${BIN_DIR}"
mkdir -p "${DESKTOP_DIR}"
mkdir -p "${AUTOSTART_DIR}"

if [[ -e "${BIN_DIR}/attar" ]]; then
    echo "Cleaning old attar from ${BIN_DIR}..."
    rm -rf "${BIN_DIR}/attar"
fi

rm -rf "${ATTAR_DIR}/attar"
cp -r "${REPO_DIR}/attar" "${ATTAR_DIR}/attar"
cp "${REPO_DIR}/install.sh" "${ATTAR_DIR}/install.sh"
cp "${REPO_DIR}/uninstall.sh" "${ATTAR_DIR}/uninstall.sh"
cp "${REPO_DIR}/README.md" "${ATTAR_DIR}/README.md" 2>/dev/null || true

WRAPPER="${BIN_DIR}/attar"
printf '%s\n' '#!/usr/bin/env python3' 'import sys, os' 'sys.path.insert(0, os.path.expanduser("~/.attar"))' 'from attar.main import main' 'main()' > "${WRAPPER}"
chmod +x "${WRAPPER}"

if [[ ":${PATH}:" != *":${BIN_DIR}:"* ]]; then
    if ! grep -q "# ATTAR PATH" "${HOME}/.bashrc" 2>/dev/null; then
        echo "" >> "${HOME}/.bashrc"
        echo "# ATTAR PATH" >> "${HOME}/.bashrc"
        echo "export PATH=\"${BIN_DIR}:\${PATH}\"" >> "${HOME}/.bashrc"
        echo "" >> "${HOME}/.bashrc"
        echo "Added ${BIN_DIR} to PATH. Run: source ~/.bashrc"
    fi
fi

ICON="${ATTAR_DIR}/attar/assets/icon.svg"
{
    echo "[Desktop Entry]"
    echo "Name=Attar"
    echo "Name[ar]=عطار"
    echo "Comment=Islamic Remembrance Daemon"
    echo "Comment[ar]=تذكير إسلامي"
    echo "Exec=${WRAPPER} --gui"
    echo "Icon=${ICON}"
    echo "Type=Application"
    echo "Terminal=false"
    echo "Categories=Utility;"
} > "${DESKTOP_DIR}/attar.desktop"
chmod +x "${DESKTOP_DIR}/attar.desktop"

echo ""
echo "=== Attar installed successfully ==="
echo "Run: attar --gui    (Open control panel)"
echo "Run: attar --start   (Start daemon)"
echo "Run: attar --version (Verify)"
echo ""
