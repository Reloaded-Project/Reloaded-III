# Merged File Cache Requirements

!!! info "This page specifies the requirements and goals for the Merged File Cache library."

Standard requirements, e.g. Minimal Code Size apply too.

## Automatic Expiration and Cleanup

!!! info "The cache should automatically handle expiration and cleanup of stale entries."

Entries should be considered if the file has not been accessed within a given period of time.

This should be configurable.

!!! tip "Removal of stale entries should be done after all the mods are loaded"

    Sometimes the user might not boot the game, say, for 30 days when cache is set to 28 days.

    In order to avoid clearing merged files that may be otherwise valid, the cache should
    clear stale entries only after mod loads have been completed to avoid false hits.

## Handle Different Versions of Mods

!!! info "Cache should be resilient to mod updates."

If a mod is updated to a new version, the cache should not use any entries associated with the
previous version of the mod.

!!! note "The invalidation of old entries can simply be done based on expiry date"

    No complex logic is needed to detect upgrades/downgrades.

## Caching Based on Loadout

!!! info "Each Cache directory should be specific to the current loadout used in the mod loader and manager."

!!! tip "This is simply achieved by using the native `_loader.GetCacheFolder()` method."

    TODO: Link Pending

When the user changes the loadout, the loader will provide a different cache directory specific to the
loadout. Nothing special to do here.

!!! note "The loader can provide a cache folder for the `mod+loadout` or `mod+version+loadout` combination."

    In our case, we will use the former and try to handle backwards compatibility ourselves.
    If it happens that we made a breaking change, we will discard the whole cache folder and start fresh.

    TODO: Link Pending

## Caches are Scoped Per Mod

!!! info "Caches must be scoped per mod."

The cache must be scoped per mod. In addition to loadout scoping.

Each mod gets its own cache. This works by having the mods create an instance of the cache with
the ModId and version as the constructor parameters.

The caching library then uses an existing cache associated with that ModId+Version, or creates a new
one.

## Efficient Serialization

!!! info "Serialization scheme should minimize deserialization time and code size."

Using [rkyv][rkyv] for Rust is recommended.

In the event a game with many merged files comes along, adding ZStandard compression will also
be beneficial. For now however, pure serialization should be sufficient.

## Thread Safety

!!! tip "The cache should be thread safe for reading."

Any number of threads should be able to read at the same time, and only one thread should be able to
write. Basically a `RwLock` in Rust.

## Value Storage

!!! info "Stored values must adhere to the following rules:"

    - Values MUST be available on Disk in exact form submitted to cache.
        - Not a byte should be modified.
    - The values (files) must not move for the lifetime of the cache.

Do not make assumptions about the data. The data may be used as e.g. input to file emulators,
or just kept in memory. We don't know.

## FileSystem Optimization

!!! info "Because the files are stored on FileSystem, the files should be laid out in a format that's quick to access."

Avoid putting too many files (> 255) in same folder, as that's slow to access.
Instead, group the cached files into directories.

An acceptable strategy here is simply following the directory structure of the original file
paths/keys, or creating a new folder every 255 files, whatever works.

!!! note "We don't expect a single mod to produce >4000 cached files."

    It's unlikely any mod will even hit 100.

## Error Handling and Logging

!!! warning "The cache must not throw errors under any circumstance."

If the cache metadata/format is invalid or corrupt, simply discard the whole cache and start fresh.
Then log the event. Provide any important information for debugging purposes.

## Versioning

!!! warning "The cache must not fail after an upgrade."

If the cache format changes, the cache should be able to detect that and either migrate the
cache or discard the original cache, starting fresh.

[rkyv]: https://rkyv.org/