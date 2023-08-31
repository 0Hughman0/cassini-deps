import shutil
from pathlib import Path

import pytest
from semantic_version import Version

from cassini import Project, DEFAULT_TIERS

from cassini_deps import extend_project
from cassini_deps.import_tools import PatchImporter


@pytest.fixture
def create_project(tmp_path):
    Project._instance = None
    project = Project(DEFAULT_TIERS, tmp_path)

    return project

@pytest.fixture
def setup_project(create_project):
    project = create_project
    project = extend_project(project)

    project.setup_files()

    shutil.copytree('tests/mock_libraries', project.project_folder / 'cas_deps', dirs_exist_ok=True)

    return project


def test_extend(create_project):
    project = create_project
    project = extend_project(project)

    for tier in project.hierarchy:
        assert hasattr(tier, 'cas_deps')


def test_import_init(setup_project):
    project = setup_project
    wp = project['WP1']
    wp.setup_files()
    
    importer = wp.cas_deps()
    
    assert wp.cas_deps_version == Version('0.2.0')
    assert isinstance(importer, PatchImporter)
    
    with pytest.raises(ImportError):
        import module

    with importer:
        import module

        assert module.__version__ == "0.2.0"

        import my_package

        assert my_package.__version__ == "0.2.0"

    

def test_import_force_version(setup_project):
    project = setup_project

    wp = project['WP1']

    importer = wp.cas_deps('0.1.0')

    assert Path(importer.path).name == '0.1.1'

    with importer:
        import module

        assert module.__version__ == "0.1.1"
    
        import my_package

        assert my_package.__version__ == "0.1.1"
