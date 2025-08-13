#!/usr/bin/env bash
set -euo pipefail

# Download a recent linux AMD64 agent binary (adjust version if needed)
AGENT_VERSION="v0.38.2"
curl -L -o /tmp/agent.tar.gz https://github.com/grafana/agent/releases/download/${AGENT_VERSION}/grafana-agent-${AGENT_VERSION}-linux-amd64.tar.gz
mkdir -p /opt/agent
tar -xzf /tmp/agent.tar.gz -C /opt/agent --strip-components=1

# Run the agent with our config
exec /opt/agent/agent --config.file=/opt/config/agent.yaml
