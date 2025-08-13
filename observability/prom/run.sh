#!/usr/bin/env bash
set -euo pipefail

PROM_VERSION="v2.54.1"
PROM_DIR="/var/tmp/prom"
CONFIG_PATH="/opt/render/project/src/observability/prom/prometheus.yml"

echo "[INFO] Starting Prometheus ${PROM_VERSION}..."
mkdir -p "${PROM_DIR}"

if [ ! -f "${PROM_DIR}/prometheus" ]; then
  echo "[INFO] Downloading Prometheus ${PROM_VERSION}..."
  curl -fsSL -o "${PROM_DIR}/prom.tar.gz" \
    "https://github.com/prometheus/prometheus/releases/download/${PROM_VERSION}/prometheus-${PROM_VERSION#v}.linux-amd64.tar.gz"
  tar -xzf "${PROM_DIR}/prom.tar.gz" -C "${PROM_DIR}"
  # Move binaries to predictable paths
  mv "${PROM_DIR}/prometheus-${PROM_VERSION#v}.linux-amd64/prometheus" "${PROM_DIR}/prometheus"
  mv "${PROM_DIR}/prometheus-${PROM_VERSION#v}.linux-amd64/promtool" "${PROM_DIR}/promtool"
fi

exec "${PROM_DIR}/prometheus" \
  --config.file="${CONFIG_PATH}" \
  --storage.tsdb.path="/tmp/prom-data" \
  --web.listen-address="0.0.0.0:9090"
