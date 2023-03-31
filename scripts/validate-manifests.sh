#!/bin/bash

set -eu

: "${BINDIR:=""}"
: "${KUSTOMIZE:=${BINDIR:+${BINDIR}/}kustomize}"
: "${KUBECONFORM:=${BINDIR:+${BINDIR}/}kubeconform}"

find_overlays() {
    find . -regex '.*/overlays/[^/]*/kustomization.yaml' -exec dirname {} \;
}

okay() {
    echo -n "$(tput setaf 2)${1}:okay$(tput sgr0) "
}

fail() {
    echo "$(tput setaf 1)${1}:failed$(tput sgr0)"
    if [[ -s "$tmpdir/stdout" ]]; then
        echo
        cat "$tmpdir/stdout"

        # Annotation for GitHub
        echo "::error::$(tr '\n' ' ' < "$tmpdir/stdout")"
    fi

    if [[ -s "$tmpdir/stderr" ]]; then
        echo
        cat "$tmpdir/stderr"

        # Annotation for GitHub
        echo "::error::$(tr '\n' ' ' < "$tmpdir/stderr")"
    fi
    exit 1
}

tmpdir=$(mktemp -d buildXXXXXX)
trap "rm -rf $tmpdir" EXIT

for overlay in $(find_overlays); do
    : > "$tmpdir/stdout"

    echo -n "$overlay "
    if $KUSTOMIZE build "$overlay" > "$tmpdir/manifests.yaml" 2> "$tmpdir/stderr"; then
        okay build
    else
        fail build
    fi

    if $KUBECONFORM \
            -schema-location default \
            ${ADDITIONAL_SCHEMAS:+-schema-location "$ADDITIONAL_SCHEMAS"} \
            -ignore-missing-schemas \
            "$tmpdir/manifests.yaml" > "$tmpdir/stdout" 2> "$tmpdir/stderr"; then
        okay verify
    else
        fail verify
    fi

    echo
done
