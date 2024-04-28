# Merged File Cache Implementation Details

!!! info "This page provides details on the implementation of the Merged File Cache, including API reference and expiration details."

!!! warning "Provided API is not 'final', it's just a plan/rough draft."

    The APIs use C# types for simplicity, but should be translateable to other languages.

The Merged File Cache is composed of a two level system.

At the first level is a binary file with a listing of all known caches.
Each mod + mod version having their own cache folder.

## Top Level View

!!! info "The entry folder of the cache mod looks like this"

```
.
├── reloaded3.utility.examplemod.s56+1.0.0
│   └── cache.bin
├── reloaded3.utility.examplemod.s56+2.0.0
│   └── cache.bin
└── caches.bin
```

We read `caches.bin` in order to discover all cache folders.

Then read from the cache folders to get the actual per mod cache.

!!! tip "Each folder is composed of [Mod Id][mod-id] and the [Mod Version][mod-version] concatenated with a `+`."

    It is technically possible that this produces a filename which cannot be created on some filesystems.

    This should not happen on Linux or Windows, but it may be possible in more niche systems.
    For this reason, we store the `FolderName` in the `Cache` struct.

    If a folder with a given name can't be created, we create a folder with a random ASCII name
    and store that name in the `FolderName` field.


### Caches.bin

!!! info "The caches.bin file is composed of `Cache` entries and some metadata."

#### `CachesHeader`

| Property  | Type                          | Description                                         |
| --------- | ----------------------------- | --------------------------------------------------- |
| `Version` | int                           | Version of the cache. Increment on breaking change. |
| `Caches`  | `Dictionary<CacheKey, Cache>` | Mapping of `CacheKey` to `Cache`. (HashMap)         |

If the version field does not match or the file fails to parse, the cache is considered invalid
and the entire folder should be wiped.

#### `CacheKey` Struct

| Property  | Type     | Description                   |
| --------- | -------- | ----------------------------- |
| `ModId`   | `string` | Unique identifier of the mod. |
| `Version` | `SemVer` | Semantic version of the mod.  |

#### `Cache` Struct

| Property     | Type       | Description                                      |
| ------------ | ---------- | ------------------------------------------------ |
| `FolderName` | `string`   | The directory where the cache folder are stored. |
| `Expiration` | `DateTime` | The last access date + predefined amount.        |

The `Expiration` field is updated every time the cache is accessed. To it, we add the user's chosen
expiration duration, which we default to 14 days.

## Deeper Level View

If we further expand the view, we may get something like this:

```
.
├── reloaded3.utility.examplemod.s56+1.0.0
│   ├── somefolder
│   │   └── cachedfile.bin
│   ├── someotherfolder
│   │   └── anothercachedfile.bin
│   └── cache.bin
├── reloaded3.utility.examplemod.s56+2.0.0
│   ├── somefolder
│   │   └── cachedfile.bin
│   ├── someotherfolder
│   │   └── anothercachedfile.bin
│   └── cache.bin
└── caches.bin
```

And if we scope it to a given mod+version's cache folder, we get:

```
.
├── somefolder
│   └── cachedfile.bin
├── someotherfolder
│   └── anothercachedfile.bin
└── cache.bin
```

The `cache.bin` file contains info of the contents of the cache.

### Cache.bin

The `cache.bin` file is composed of a dictionary (hashset) of `CacheFileKey` to `CacheFileEntry` entries.

#### `CacheFileKey` Struct

| Property      | Type         | Description                                                                          |
| ------------- | ------------ | ------------------------------------------------------------------------------------ |
| `FilePath`    | `string`     | The path to the file relative to folder of `cache.bin`.                              |
| `ModIds`      | `string[]`   | An array of unique mod IDs from which the mods are sourced.                          |
| `Timestamps`  | `DateTime[]` | An array of timestamps representing the last modification times of the source files. |
| `ModVersions` | `string[]`   | An array of mod versions representing the versions of the source mods.               |

#### `CacheFileEntry` Struct

!!! info "Represents an individual cached file entry."

| Property     | Type       | Description                                             |
| ------------ | ---------- | ------------------------------------------------------- |
| `FilePath`   | `string`   | The path to the file relative to folder of `cache.bin`. |
| `Expiration` | `DateTime` | The date after which the item should be removed.        |

## API Reference

### `ICacheFactory` Interface

!!! info "This is an abstraction over [Caches.bin](#cachesbin)"

| Method             | Description                                                                                                | Parameters                          |
| ------------------ | ---------------------------------------------------------------------------------------------------------- | ----------------------------------- |
| `GetOrCreateCache` | Retrieves the cache instance for the specified mod ID and version. If it doesn't exist, creates a new one. | `string modId`, `string modVersion` |

This creates an [IMergedFileCache](#imergedfilecache-interface).

### `IMergedFileCache` Interface

!!! info "This is an abstraction over [Cache.bin](#cachebin)"

!!! info "Returned from [ICacheFactory](#icachefactory-interface)"

| Method               | Description                                                                | Parameters                           |
| -------------------- | -------------------------------------------------------------------------- | ------------------------------------ |
| `TryGet`             | Attempts to retrieve a cached file based on the specified cache key.       | `CacheFileKey key`                   |
| `Add`                | Adds a merged file to the cache using the specified cache key and content. | `CacheFileKey key`, `byte[] content` |
| `Remove`             | Removes a cache entry with the specified cache key.                        | `CacheFileKey key`                   |
| `Clear`              | Removes all cache entries.                                                 | -                                    |
| `RemoveExpiredItems` | Removes all stale cache entries based on the expiration duration.          | -                                    |

## Usage Example

!!! info "How using the cache should look in different languages."

=== "C#"

    ```csharp

    // Get the cache factory instance
    var cacheFactory = _modLoader.GetService<ICacheFactory>();

    // Get the cache instance for the current mod
    var cache = cacheFactory.GetOrCreateCache(GetModId(), GetModVersion());

    // Define the cache key
    var cacheKey = new CacheFileKey
    {
        FilePath = "path/to/file.txt",
        ModIds = new string[] { "mod1", "mod2" },
        Timestamps = new DateTime[] { File.GetLastWriteTime("path/to/mod1/file.txt"), File.GetLastWriteTime("path/to/mod2/file.txt") },
        ModVersions = new string[] { "1.0.0", "2.1.3" }
    };

    // Try to get the cached file
    if (cache.TryGet(cacheKey, out string cachedFilePath))
    {
        // Cache hit, use the cached file
        string mergedFileContent = File.ReadAllText(cachedFilePath);
    }
    else
    {
        // Cache miss, merge the files and cache the result
        string mergedFileContent = MergeFiles("path/to/mod1/file.txt", "path/to/mod2/file.txt");
        cache.Add(cacheKey, Encoding.UTF8.GetBytes(mergedFileContent));
    }
    ```

=== "Rust"

    ```rust

    // Get the cache factory instance
    let cache_factory = mod_loader.get_service::<ICacheFactory>();

    // Get the cache instance for the current mod
    let cache = cache_factory.get_or_crate_cache(get_mod_id(), get_mod_version());

    // Define the cache key
    let cache_key = CacheFileKey {
        file_path: "path/to/file.txt".to_string(),
        mod_ids: vec!["mod1".to_string(), "mod2".to_string()],
        timestamps: vec![
            std::fs::metadata("path/to/mod1/file.txt").unwrap().modified().unwrap(),
            std::fs::metadata("path/to/mod2/file.txt").unwrap().modified().unwrap(),
        ],
        mod_versions: vec!["1.0.0".to_string(), "2.1.3".to_string()],
    };

    // Try to get the cached file
    if let Some(cached_file_path) = cache.try_get(&cache_key) {
        // Cache hit, use the cached file
        let merged_file_content = std::fs::read_to_string(cached_file_path).unwrap();
    } else {
        // Cache miss, merge the files and cache the result
        let merged_file_content = merge_files("path/to/mod1/file.txt", "path/to/mod2/file.txt");
        cache.add(&cache_key, merged_file_content.as_bytes());
    }
    ```

=== "C++"

    ```cpp

    // Get the cache factory instance
    auto cacheFactory = modLoader->GetService<ICacheFactory>();

    // Get the cache instance for the current mod
    auto cache = cacheFactory->GetOrCreateCache(GetModId(), GetModVersion());

    // Define the cache key
    CacheFileKey cacheKey;
    cacheKey.FilePath = "path/to/file.txt";
    cacheKey.ModIds = { "mod1", "mod2" };
    cacheKey.Timestamps = {
        std::filesystem::last_write_time("path/to/mod1/file.txt"),
        std::filesystem::last_write_time("path/to/mod2/file.txt")
    };
    cacheKey.ModVersions = { "1.0.0", "2.1.3" };

    // Try to get the cached file
    std::optional<std::string> cachedFilePath = cache->TryGet(cacheKey);
    if (cachedFilePath.has_value()) {
        // Cache hit, use the cached file
        std::string mergedFileContent = ReadFile(cachedFilePath.value());
    } else {
        // Cache miss, merge the files and cache the result
        std::string mergedFileContent = MergeFiles("path/to/mod1/file.txt", "path/to/mod2/file.txt");
        cache->Add(cacheKey, mergedFileContent.data(), mergedFileContent.size());
    }
    ```

The `ICacheFactory` instance is obtained from the mod loader using the `GetService` method.

The cache instance for the current mod is then retrieved using the `GetOrCreateCache` method of the factory,
passing the current mod's ID and version.

The `CacheFileKey` struct is then defined using the file path, mod IDs, timestamps, and mod versions.

The `TryGet` method is used to attempt to retrieve the cached file using the `CacheFileKey`, and if a
cache miss occurs, the files are merged and added to the cache using the `Add` method with the
`CacheFileKey` and merged content.

## Expiration and Cleanup

!!! info "The Merged File Cache automatically handles expiration and cleanup of stale cache entries."

When all mods are done loading, the cache will crawl through all the cache entries and remove
stale entries.

This can also be force triggered when the `RemoveExpiredItems` method is called explicitly.

The directory structure of the cached files mimics the actual file paths used in the cache, in order
to minimize the amount of files per directory.

## Thread Safety

!!! tip "The merged file cache can have multiple readers or 1 writer at once."

Since the cache is scoped per mod, that effectively means that there will only ever be concurrent
access if said mod uses multiple threads for merging at startup.

In other words, `TryGet`, can be performed simultaneously by multiple threads without any
synchronization overhead.

But if someone calls `Add`, other read/write threads will have to wait until the write
operation is completed.

!!! note "Regarding Write Lock Duration"

    Writing the actual file does not lock. Only updating the internal cache state locks,
    so in practice the cache is pretty much always unlocked.

[mod-id]: ../../../Server/Packaging/Package-Metadata.md#id
[mod-version]: ../../../Server/Packaging/Package-Metadata.md#version