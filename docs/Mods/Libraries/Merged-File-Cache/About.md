# Merged File Cache

!!! info "The Merged File Cache is a key-value file store for storing merged files from multiple sources."

    The values in this case, are locations of the merged files on disk inside the cache.

It is designed to be used in scenarios where files need to be merged from multiple mods, and the
merged result needs to be cached for faster subsequent access.

!!! tip "Merged files are preferred over File Emulation [TODO: Link Pending] when the size of the file is small (i.e. smaller than 50MB)."

## Why a Merged File Cache?

!!! question "Why do we need a Merged File Cache?"

When working with mods that modify game files, it's common to have multiple mods that affect the
same file. In such cases, the files need to be merged to produce the final result.

Merging should be done using one of the following methods:

- File Emulation [TODO: Link Pending], for archives and large files greater than 50MB
- Merging in memory and saving to disk, in all other cases

For the latter of the two, merging can sometimes be a time consuming process if there are many input
files being used. Very often, merging the files between different runs of the modded game will also
result in the same output; wasting time.

The `Merged File Cache` provides a standardized approach to cache merged files, while also
automatically handling cache invalidation based on changes to the source files.

!!! tip "We opt to provide a standardized approach for efficiency reasons"

## How It Works

!!! info "Each mod gets its own scoped cache instance, created using the mod's ID and version."

The cache is ***scoped per mod AND loadout***. When a mod requests a cache instance, it provides its
mod ID and version to the constructor. The caching system internally maintains a global registry of
all known mod caches.

If a cache instance for the given mod ID and version already exists, it is returned. Otherwise, a
new cache instance is created and added to the registry.

### How the Values are Stored

Each item in the cache has a unique key composed of the following:

- **File Path**: The relative path to the file being cached.
- **Mod IDs**: An array of mod IDs, one for each source mod, representing the unique identifier of each mod.
- **Timestamps**: An array of timestamps, one for each source mod, representing the last modification time of the file in each mod.
- **Mod Versions**: An array of mod versions, one for each source mod, representing the version of each mod.

The timestamps and mod version arrays are specified in the mod load order. If there is only
one source mod, they will contain only one item.

### How the Cache is Used

When you are merging a file, first create the key and check the cache if it exists.
If the file does not exist in the cache, create the file and add it to the cache.

## Overview

- [Requirements](Requirements.md): Specifies the requirements and goals for the Merged File Cache library.
- [Implementation Details](Implementation-Details.md): Provides details on the implementation of the Merged File Cache, including API reference and expiration details.