import os
import pytest

@pytest.fixture
def kubeconform_version():
    return b"0.6.1"

@pytest.fixture
def kustomize_version():
    return b"4.5.7"

@pytest.fixture(autouse=True)
def set_bindir(tmp_path):
    if 'BINDIR' not in os.environ:
        os.environ['BINDIR'] = os.path.join(tmp_path, 'bin')
