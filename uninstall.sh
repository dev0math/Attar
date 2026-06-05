#!/usr/bin/env bash

ATTAR_DIR="${HOME}/.attar"
BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
AUTOSTART_DIR="${HOME}/.config/autostart"

echo "=== Uninstalling Attar ==="

PID_FILE="${ATTAR_DIR}/daemon.pid"
if [[ -f "${PID_FILE}" ]]; then
    PID=$(cat "${PID_FILE}")
    if kill -0 "${PID}" 2>/dev/null; then
        kill "${PID}" 2>/dev/null || true
        echo "Stopped daemon (PID: ${PID})"
    fi
    rm -f "${PID_FILE}"
fi

if [[ -e "${BIN_DIR}/attar" ]]; then
    rm -rf "${BIN_DIR}/attar"
    echo "Removed command from ${BIN_DIR}"
fi

if [[ -f "${DESKTOP_DIR}/attar.desktop" ]]; then
    rm "${DESKTOP_DIR}/attar.desktop"
fi
if [[ -f "${AUTOSTART_DIR}/attar.desktop" ]]; then
    rm "${AUTOSTART_DIR}/attar.desktop"
fi

if grep -q "# ATTAR PATH" "${HOME}/.bashrc" 2>/dev/null; then
    sed -i '/# ATTAR PATH/d' "${HOME}/.bashrc"
    sed -i "/export PATH=\".*\.local\/bin:\\\${PATH}\"/d" "${HOME}/.bashrc"
    echo "Cleaned PATH from .bashrc"
fi

if [[ -d "${ATTAR_DIR}" ]]; then
    rm -rf "${ATTAR_DIR}"
    echo "Removed ${ATTAR_DIR}"
fi

echo ""
echo "=== Attar uninstalled successfully ==="
