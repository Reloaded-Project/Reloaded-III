# Storage

!!! info "This section talks about where and how everything is stored on disk."

The server is ultimately responsible for managing all of the files on disk, including assets
which may be requested by the front-end, packaages (mods/tools etc.) and configuration files.

## Requirements

* On uninstall, the application should be able to remove all of its files from the system.
* Package locations should be configurable.
    * As these are 99% of the disk space used.
* The application should have a 'portable' mode.
    * In other words, it should be able to be run from a USB stick, etc.
* Application data should be user accessible.
    * In other words, easy to find/navigate to.
    * Because application data may also contains logs and user accessible files.
    * e.g. If the loader crashes on boot, finding logs should be easy.
* Cross-platform consistency.
    * The paths should be consistent across different operating systems.
    * i.e. Use the most appropriate standardised native directories.
    * And everything under these directories should be consistent.

## Sections

| Section                        | Description                                            |
| ------------------------------ | ------------------------------------------------------ |
| [Locations][locations]         | Describes where all the data is stored.                |
| [Package Tiering][pkg-tiering] | Smart storage location selection for packages.         |
| [Loadouts][loadouts]           | Encapsulates a group of mods and their configurations. |

<!-- Links -->
[locations]: ./Locations.md
[loadouts]: ./Loadouts/About.md
[pkg-tiering]: ./Package-Tiering.md