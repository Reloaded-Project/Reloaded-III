!!! info "Reloaded3's hash cache provides efficient integrity verification."

The Hash Cache is a crucial component of Reloaded3's package management system, allowing us
to quickly detect that packages, and other similar folders are not unexpectedly modified.

## Why We Need a Hash Cache

1. **Delta Updates**: We can quickly detect which files have changed and only update those.
2. **Integrity Verification**: Detect if packages have been tampered with post install.
    - Example: A modder was working on a mod, and accidentally left a non-clean version on their disk.
    - Example: Detect if game files were externally modified since last launch.

The needs of Reloaded3 are that we scan a folder on disk, and compare against an older, serialized
cache state. Therefore, the cache should allow for quick lookups of files without the need of
constructing entire hash tables.

This format should be useful in accomodating both the needs of the package manager (updating),
and the integrity verification (quick lookups).

## Requirements

The Hash Cache system must meet the following requirements:

1. **Embeddable**: The cache should be easy to embed in external file formats and larger systems.
2. **Compressible**: The cache should be friendly towards compression algorithms.
3. **Quick Lookup**: The cache should allow for quick lookups of individual file information.
4. **Scalable**: Should be fast regardless of number of files.

## Sections

| Section                                          | Description                                                           |
| ------------------------------------------------ | --------------------------------------------------------------------- |
| [File Format][file-format]                       | Describes specification of how hash cache data is serialized to disk. |
| [Implementation Details][implementation-details] | Extra info on how to implement the hash cache.                        |
| [API][file-format]                               | Describes how to work with the hash cache implementation.             |

[file-format]: ./File-Format.md
[implementation-details]: ./Implementation-Details.md
[api]: ./API.md