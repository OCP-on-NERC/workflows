import os
import subprocess
import pytest
import yaml

manifests_should_succeed = {
    "files": {
        "overlays/test/kustomization.yaml": {
            "resources": [
                "service.yaml",
            ]
        },
        "overlays/test/service.yaml": {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": {
                "name": "test-service",
            },
            "spec": {
                "ports": [
                    {
                        "port": 80,
                        "protocol": "TCP",
                        "name": "http",
                        "targetPort": "http",
                    }
                ],
            },
        },
    },
}

manifests_should_fail = {
    "expect_in_output": [
        "expected array or null, but got object",
    ],
    "files": {
        "overlays/test/kustomization.yaml": {
            "resources": [
                "service.yaml",
            ]
        },
        "overlays/test/service.yaml": {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": {
                "name": "test-service",
            },
            "spec": {
                "ports": {
                    "port": "80",
                    "protocol": "TCP",
                    "name": "http",
                    "targetPort": "http",
                },
            },
        },
    },
}


def write_test_manifests(prefix, manifests):
    for path, data in manifests["files"].items():
        fullpath = os.path.join(prefix, path)
        os.makedirs(os.path.dirname(fullpath), exist_ok=True)
        with open(fullpath, "w") as fd:
            yaml.safe_dump(data, fd)


@pytest.fixture(autouse=True)
def setup_environment(tmp_path):
    topdir = os.getcwd()

    subprocess.check_call(
        [f"{topdir}/scripts/install-kustomize.sh"],
        cwd=tmp_path,
    )
    subprocess.check_call(
        [f"{topdir}/scripts/install-kubeconform.sh"],
        cwd=tmp_path,
    )


def test_validate_manifests_no_manifests(tmp_path):
    topdir = os.getcwd()
    subprocess.check_call(
        [f"{topdir}/scripts/validate-manifests.sh"],
        cwd=tmp_path,
    )


def test_validate_manifests_okay(tmp_path):
    topdir = os.getcwd()
    write_test_manifests(tmp_path, manifests_should_succeed)
    subprocess.run(
        [f"{topdir}/scripts/validate-manifests.sh"],
        cwd=tmp_path,
        check=True,
    )


def test_validate_manifests_fail(tmp_path):
    topdir = os.getcwd()
    write_test_manifests(tmp_path, manifests_should_fail)
    with pytest.raises(subprocess.CalledProcessError) as excinfo:
        subprocess.run(
            [f"{topdir}/scripts/validate-manifests.sh"],
            cwd=tmp_path,
            check=True,
            capture_output=True,
        )

        for expected in manifests_should_fail["expected_in_output"]:
            assert expected in excinfo.value.output
