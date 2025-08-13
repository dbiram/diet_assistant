#!/usr/bin/env bash
set -euo pipefail

AGENT_VERSION=v0.38.2
AGENT_DIR=/var/tmp/agent
CONFIG_PATH=/opt/render/project/src/observability/agent/agent.yaml

echo "[INFO] Starting Grafana Agent..."
mkdir -p "$AGENT_DIR"

if [ ! -f "$AGENT_DIR/agent" ]; then
  echo "[INFO] Downloading Grafana Agent $AGENT_VERSION..."
  curl -fsSL -o "$AGENT_DIR/agent.tar.gz" \
    "https://github.com/grafana/agent/releases/download/${AGENT_VERSION}/grafana-agent-${AGENT_VERSION}-linux-amd64.tar.gz"
  tar -xzf "$AGENT_DIR/agent.tar.gz" -C "$AGENT_DIR" --strip-components=1
fi

exec "$AGENT_DIR/agent" --config.file="$CONFIG_PATH"
