#!/bin/bash

set -eu

: "${KUSTOMIZE_VERSION:=4.5.7}"

echo "Installing kustomize to ${BINDIR}/kustomize..."
mkdir -p "$BINDIR"
curl -Lsf "https://github.com/kubernetes-sigs/kustomize/releases/download/kustomize%2Fv${KUSTOMIZE_VERSION}/kustomize_v${KUSTOMIZE_VERSION}_linux_amd64.tar.gz" |
    tar -C "$BINDIR" -xzf- kustomize
