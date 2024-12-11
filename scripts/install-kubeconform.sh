#!/bin/bash

set -eu

: "${KUBECONFORM_VERSION:=0.6.7}"

echo "Installing kubeconform to ${BINDIR}/kubeconform..."
mkdir -p "$BINDIR"
curl -Lsf "https://github.com/yannh/kubeconform/releases/download/v${KUBECONFORM_VERSION}/kubeconform-linux-amd64.tar.gz" |
        tar -C "$BINDIR" -xzf- kubeconform
