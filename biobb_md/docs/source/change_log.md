# Biobb MD changelog

## What's new in version [3.7.2](https://github.com/bioexcel/biobb_md/releases/tag/v3.7.2)?

* Deprecated Package: biobb_md is no longer maintained and has been superseded by the biobb_gromacs package.

## What's new in version [3.7.1](https://github.com/bioexcel/biobb_md/releases/tag/v3.7.1)?

### Bug fixes

* Problem with Gmx version check (mdrun) [#48](https://github.com/bioexcel/biobb_md/issues/48)

## What's new in version [3.7.0](https://github.com/bioexcel/biobb_md/releases/tag/v3.7.0)?
In version 3.7.0 the dependency biobb_common has been updated to 3.7.0 version.

### New features

* Update to biobb_common 3.7.0 (general)

## What's new in version [3.6.0](https://github.com/bioexcel/biobb_md/releases/tag/v3.6.0)?
In version 3.6.0 Python has been updated to version 3.7 and Biopython to version 1.79.
Big changes in the documentation style and content. Finally a new conda installation recipe has been introduced.

### New features

* Update to Python 3.7 (general)
* Update to Biopython 1.79 (general)
* New conda installer (installation)
* Adding type hinting for easier usage (API)
* Deprecating os.path in favour of pathlib.path (modules)
* New command line documentation (documentation)

### Bug fixes

* Replace container Quay.io badge (documentation)
* Remove unused system and step arguments from command line causing execution errors (cli) [#9](https://github.com/bioexcel/biobb_model/issues/9)

### Other changes

* New documentation styles (documentation) [#8](https://github.com/bioexcel/biobb_model/issues/8)
