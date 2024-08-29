!!! note "This is documentation to use for the actual packaging library, once it's available as a separate component."

    This is a Rust successor to [Sewer56/Update].

## About `reloaded3packaging`

!!! info "`reloaded3packaging` is [Reloaded3][Reloaded3]'s package management library."

    It follows the general package specification outlined in [Reloaded3: About Packages][Package-Metadata]

`reloaded3packaging` is a library that provides a set of tools to manage and update packages
conforming to the [Reloaded3 Package Specification][Package-Metadata].

It is designed to be used for the purpose of updating arbitrary 'packages', including but not limited to:

- Current Application
- Plugins
- Modules

The goal of this library is to be extensible; allowing users to easily add support for their own
components such as download sources and compression formats without requiring changes to the library code.

`reloaded3packaging` is based on [Sewer56/Update] which was inspired by [Onova] by Alexey Golub.
The Rust library in particular adds additional features such as more advanced delta compression and
[.nx][nx] integration at the expense of sacrificing support for some common file formats
(such as `.rar`, `.7z` etc.)

## When to use `reloaded3packaging`

- You ship very big updates and require delta compression support between versions.
- You want to update things other than just the application you are running.
- You need to support Semantic Versioning (and thus Prereleases).

## When to not use `reloaded3packaging`

!!! info "`reloaded3packaging` may not be suitable for your use under the following conditions"

- You need a simpler CI/CD deployment & integration experience.
- You can only upload 1 file to a given website.

## How the Library Works (Overview)

### Creating a Release

1. Create the [.nx][nx] archives for your release.
    - Either using pre-included tool (`reloaded3packagingtool`).
    - Or by using the library API.

2. Generated [.nx][nx] archives contain [special metadata][header-metadata] in the package.
    - Package metadata is embedded [in the `.nx` header][nx-header] for efficient access.

3. Upload the [.nx][nx] archives to a supported file host.

### Download Routine (via Package Index)

!!! info "Discovering downloadable `.nx` archives is *usually* done via a ***package index*** like the [Reloaded3 Central Server]"

In the case of the [Reloaded3 Central Server] you's use the [Get Package Metadata] API to discover
info about a given package and the [Download Information] API to get the download links.

The [Delta Verification API] may also be used to determine if you can apply a `Delta Update` to
your package without starting a download from the remote host.

This is all abstracted away in the `reloaded3packageindexclient` library.
<!-- TODO: Add Link -->

### Download Routine (Manually)

!!! warning "It is not recommended to do this if you are managing more than 1 package."

    The library does not provide caching functionality around limitations such as GitHub's
    60/hour API rate limit. So there is an implicit risk that managing more than 60 packages
    will lead to some packages never being updated.

If you're just self-updating your own program or a very small number of packages,
it is possible to use the `reloaded3packaging` library directly to query for updates.

This is rather efficient, since we're embedding metadata in the [.nx header itself][header-metadata].

### Delta Patching Logic

!!! info "This is documented in a separate document."

See [Delta Patching Logic] for more information.

### Self Updating

If the data to be updated is ***something other than the current application***,
everything is done inside the current process.

If the data to be updated is ***the current application itself*** AND ***you are on Windows***,
then files may be in use. In this case, the library extracts the files to a temporary directory
and launches itself inside that target directory. Afterwards, the files are copied back to
the original directory.

## Cross Platform Support

!!! info "`reloaded3packaging` follows the [Code Guidelines] of the `reloaded3` project."

Expect the tech to `just work` on most OSes where low level libraries like [mio] work.

!!! warnings "If used for self-updating, it is assumed the folder itself is writable."

    The library does not check for write permissions on the folder where the application is located.
    If the folder is read-only, the update will fail.

[Reloaded3]: ../../../index.md
[Package-Metadata]: ../About.md
[Sewer56/Update]: https://sewer56.dev/Update/
[Onova]: https://github.com/Tyrrrz/Onova
[nx]: https://nexus-mods.github.io/NexusMods.Archives.Nx/
[header-metadata]: ../File-Format/Archive-User-Data-Format.md
[nx-header]: https://nexus-mods.github.io/NexusMods.Archives.Nx/Specification/File-Header/#how-the-header-is-used
[Delta Patching Logic]: ../File-Format/Delta-Patching-Logic.md
[Reloaded3 Central Server]: ../../../Services/Central-Server.md
[Get Package Metadata]: ../../../Services/Central-Server.md#get-package-metadata
[Download Information]: ../../../Services/Central-Server.md#download-information
[Delta Verification API]: ../../../Services/Central-Server.md#delta-verification-api
[Code Guidelines]: ../../../Code-Guidelines/Code-Guidelines.md
[mio]: https://github.com/tokio-rs/mio