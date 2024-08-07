# Hash Cache Usage in Server

!!! info "This describes how the Reloaded3 server uses the hash cache for packages and game folders."

The Reloaded3 server utilizes a hash cache system to efficiently store and retrieve hash information
for both packages and games.

<!-- TODO: Move this to separate section when the File Hash Cache is implemented as separate library -->

## Package Hash Cache

For packages, the hash cache items are stored using a combination of the package name and version:

```
{PackageID}+{PackageVersion}.hashcache
```

Where:

- [{PackageID}][package-id] is the unique identifier of the package.
- [{PackageVersion}][package-version] is the semantic version of the package.

!!! example

    For a package with ID `reloaded3.utility.examplemod.s56` with version `1.2.3`,
    the hash cache file would be:

    ```
    reloaded3.utility.examplemod.s56+1.2.3.hashcache
    ```

### Usage

When the server needs to access or update the hash cache for a specific package:

1. Construct the file name using the package name and version.
2. Try to open the file in the designated [hash cache database][location-hashcache-package].
3. If the open operation succeeds, read the [hash cache file][hash-cache-file].
4. If the file doesn't exist, create a new hash cache file for the package.

## Game Hash Cache

!!! info "Hash cache for games is tricky, because a user can have multiple versions of the same game installed."

    For example, a `Steam` release of a game, and a `GOG` release of a game.

In addition, a user may have multiple computers, where the local files for a game may differ.

Therefore, the file name for the hash cache for games is stored within the [Machine Specific Info][machine-specific-info]
structure of each installed game entry.

### Usage

1. Check the [hash cache database][location-hashcache-package] for the game as it's loaded.
2. Compare timestamps and short hashes of files.
3. If any file is different, suggest to the user that the game folder has been modified.
4. This can be done via a [Diagnostic][diagnostic].

For game files, only the short hash and timestamp parts of the hash cache are used. Full hashes
would take too long to verify; so we simply omit them and write them as `0`.

[package-id]: ../../Server/Packaging/Package-Metadata.md#id
[package-version]: ../../Server/Packaging/Package-Metadata.md#version
[hash-cache-file]: ./File-Format.md
[location-hashcache-package]: ../../Server/Storage/Locations.md#hash-cache-files
[game-id]: ../../Server/Storage/Games/About.md
[machine-specific-info]: ../../Server/Storage/Games/About.md#machine-specific-info
[diagnostic]: ../../Server/Diagnostics.md