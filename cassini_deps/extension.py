from typing import TYPE_CHECKING
from semantic_version import Version

from .import_tools import PatchImporter, latest_version

if TYPE_CHECKING:
    from cassini import Project
    from pathlib import Path


def extend_project(project: Project, cas_deps_dir: str | Path = 'cas_deps'):
    cas_deps_dir = project.project_folder / cas_deps_dir
    
    for Tier in project.hierarchy:
        if Tier.meta_file:
            Tier.cas_deps = create_cas_deps(cas_deps_dir)

    return project


def create_cas_deps(cas_deps_dir: Path):

    def _tools(self, version=None):
        if version is None:
            if self.tools_version:
                version = self.tools_version
            else:
                version = self.tools_version = latest_version(cas_deps_dir)
                print(f"Set {self}.tools_version = {version}")

        if version == 'lastest':
            version = latest_version(cas_deps_dir)
        
        if isinstance(version, str):
            version = Version(version)
    
        return PatchImporter(version, cas_deps_dir)
    
    return _tools
