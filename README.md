# Cassini-deps

A Cassini extension providing per-notebook dependencies.

```
# project.py

from cassini import DEFAULT_TIERS, Project
from cassini import jlgui
import cassini_deps

project = Project(DEFAULT_TIERS, __file__)
jlgui.extend_project(project)
cassini_deps.extend_project(project)

if __name__ == '__main__':
    project.launch()
```

Will create a folder in `project.project_folder` called `cas_deps/0.1.0`.

Place any useful modules or packages into that folder.

```
# cas_deps/0.1.0/my_module.py
me = 'my_module 0.1.0'

```

Tier objects extended to allow:

```
>>> wp = project['WP1']
>>> 
>>> with wp.cas_deps():
>>>     from my_module import me
>>> me
"my module 0.1.0"
```

On first call of `tier.cas_deps()`, dependency version is locked:

```
>>> wp.cas_dep_version
Version('0.1.0')
```

`cassini_deps` understands semver, so if a bug is fixed and e.g. `0.1.1` is released:

```
# cas_deps/0.1.1/my_module.py
me = 'my_module 0.1.1'
```

Re-running the `cassini_deps` import:

```
>>> wp = project['WP1']
>>> 
>>> with wp.cas_deps():  # understands semver so will fetch the patch.
>>>     from my_module import me
>>> me
"my module 0.1.1"
```

`MAJOR.MINOR.x` versions can be enforced (bypassing `tier.cas_dep_version`) using:

```
>>> with wp.cas_deps('0.2.0'):  # ignores tier.cas_dep_version
>>>     from my_module import me  # assuming 0.2.1 exists!
>>> me
'my module 0.2.1'
```

Or you can just overwrite the `tier.cas_dep_version` attribute:

```
>>> wp.cas_dep_version = '0.5.1'
>>> with wp.cas_deps():
>>>     from my_module import me  # assuming 0.5.4 exists!
>>> me
'my module 0.5.4'  # patch versions are always imported 
```