# Merged File Cache

!!! info "The Merged File Cache is a key-value file store for storing merged files from multiple sources."

    The values in this case, are locations of the merged files on disk inside the cache.

It is designed to be used in scenarios where files need to be merged from multiple mods, and the
merged result needs to be cached for faster subsequent access.

## Why a Merged File Cache?

!!! question "Why do we need a Merged File Cache?"

When working with mods that modify game files, it's common to have multiple mods that affect the
same file. In such cases, the files need to be merged to produce the final result.

Merging should be done using one of the following methods:

- [File Emulation][file-emulation], a method which does not use any extra disk space.
    - At the overhead of around `15ns` per file read operation.
- Merged File Cache, merging in memory and saving to disk, in all other cases

Merging can sometimes be a time consuming process if there are many input files being used.

Very often, merging the files between different runs of the modded game will also
result in the same output; wasting time.

The `Merged File Cache` provides a standardized approach to cache merged files, while also
automatically handling cache invalidation based on changes to the source files.

!!! tip "We opt to provide a standardized approach for efficiency reasons"

## When to Prefer Merged File Cache

!!! tip "Use Merged File Cache rather than [File Emulation][file-emulation] if all/most following criteria hold true"

- User has a Hard Drive (HDD)
- Merged file is small (<32MB)
- There are many small files (<1MB) from many sources.

For more info, see [Read Performance of SOLID Files][read-perf-solid-files].

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

[file-emulation]: ../../Essentials/File-Emulation-Framework/About.md
[read-perf-solid-files]: ../../Essentials/File-Emulation-Framework/Read-Performance.md