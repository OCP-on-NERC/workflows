import os
import subprocess


def test_install_kubeconform(tmp_path, kubeconform_version):
    topdir = os.getcwd()
    subprocess.run(
        [f"{topdir}/scripts/install-kubeconform.sh"],
        cwd=tmp_path,
        env=os.environ | {"KUBECONFORM_VERSION": kubeconform_version},
        check=True,
    )
    out = subprocess.run(
        [f"{os.environ['BINDIR']}/kubeconform", "-v"], cwd=tmp_path, check=True, capture_output=True
    )
    assert kubeconform_version in out.stdout
