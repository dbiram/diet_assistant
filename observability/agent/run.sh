#!/usr/bin/env bash
set -euo pipefail

# Download a recent linux AMD64 agent binary (adjust version if needed)
AGENT_VERSION="v0.38.2"
curl -L -o /var/tmp/agent.tar.gz https://github.com/grafana/agent/releases/download/${AGENT_VERSION}/grafana-agent-${AGENT_VERSION}-linux-amd64.tar.gz
mkdir -p /var/opt/agent
tar -xzf /var/tmp/agent.tar.gz -C /var/opt/agent --strip-components=1

# Run the agent with our config
exec /var/opt/agent/agent --config.file=/var/opt/config/agent.yaml
