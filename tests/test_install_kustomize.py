import os
import subprocess


def test_install_kustomize(tmp_path, kustomize_version):
    topdir = os.getcwd()
    subprocess.run(
        [f"{topdir}/scripts/install-kustomize.sh"],
        cwd=tmp_path,
        env=os.environ | {"KUSTOMIZE_VERSION": kustomize_version},
        check=True,
    )
    out = subprocess.run(
        [f"{os.environ['BINDIR']}/kustomize", "version"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    )
    assert kustomize_version in out.stdout
