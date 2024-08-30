!!! info "`Package Indexing` is the monitoring of Mod Sites for new Mods and Packages."

This gets us information such as [Package Metadata] needed to resolve missing dependencies in [Loadouts].

## Indexing Rules

### Putting Packages 'on Hold' Until Cross Referenced

!!! warning "This is an important security feature"

    Without this feature, it's possible to construct an attack where you upload a higher version
    of an existing package to an alternate site and users (incorrectly) receive an update.

### External Sites are the Moderators

!!! warning "Third party websites act as moderators for entries"

    They will still be available on [archive.org] of course, and other sites.

### Automatic Backup to [archive.org]

!!! info "Automatically backup all packages to [archive.org]"

    This is to ensure that packages are not lost.

This needs to be done indiscriminately, regardless of whether the package has been removed or not.

<!-- TODO: More Details -->

[Loadouts]: ../../Services/Central-Server/
[Package Metadata]: ./Online-API.md#package-metadata-batch
[archive.org]: https://archive.org