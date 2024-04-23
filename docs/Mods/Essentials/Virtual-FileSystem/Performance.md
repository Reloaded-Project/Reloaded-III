# Performance Characteristics

All numbers were obtained on a stock clock AMD Ryzen 5900X and 3000MHz CL16 RAM.

The Reloaded VFS is heavily optimized for performance. A lot of micro-optimizations were done to squeeze every bit out of making opening files faster...

- All strings stored as Wide Strings.
    - Windows APIs use Wide Strings under the hood, even for ANSI APIs.
    - Therefore we save time by not having to widen them again.

- Custom string Hash Function for file paths.
    - With AVX and SSE implementations; as well as unrolled `nint` as backup.

- Custom Vectorized `ToUpper` for Strings.
    - Modified backport from .NET 8.
    - Super fast for 99% of the paths that are pure ASCII.
    - Non-ASCII paths use slower fallback since they can't be vectorized.
    - Partial ASCII paths have the first ASCII part vectorized and rest handled in fallback.

- Custom Dictionary (HashMap) that can query string slices (to avoid copying/realloc).

- Uses a custom ['LookupTree'](./implementationdetails/lookup-tree.md).
    - Provides lookup for resolving file paths in O(3) time.

## File Mapping Performance & Memory Usage

This section describes how long it takes to create a file map. A file map is a structure that helps redirect original files to their new versions found in mod folders.

Whenever changes are made to mod folders, the file map needs to be rebuilt.

Two types of maps exist, [RedirectionTree](./implementationdetails/redirection-tree.md) and [LookupTree](./implementationdetails/lookup-tree.md). The latter, `LookupTree` is optimized for performance, but takes roughly twice as long to build as it is built from the former `RedirectionTree`.

| Folder Type                  | Directories | Total Items | RedirectionTree (Time) | RedirectionTree (Memory) | LookupTree (Time) | LookupTree (Memory) |
|------------------------------|-------------|-------------|------------------------|-------------------------|-------------------|---------------------|
| Windows Folder               | 40,796      | 170,438     | 43ms                   | 27MB                    | 32ms              | 25MB                |
| Steam Folder <br/>(65 games) | 9,318       | 172,896     | 18ms                   | 12MB                    | 20ms              | 11MB                |

The performance of mapping operations mainly depends on the directory count. The table above shows the time and memory usage for building the `RedirectionTree` and `LookupTree` for both Windows and Steam folders. The `LookupTree` memory usage should be approximately equal to the total runtime memory usage.

For a typical game (based on the median of a Steam library), building the `RedirectionTree` should take around `0.017ms` and allocate `48KB`.
Creating the optimized `LookupTree` takes about `0.012ms` and allocates `47KB`.

In other words, you can assume remapping files is basically real-time.

### Fast Append

Both `LookupTree` and `RedirectionTree` support `'fast append'` operations.

If a file is added to the mod folder while the game is running and isn't previously mapped, it can be added to the tree directly without a full rebuild.

However, if the currently mapped file's source mod cannot be determined, the entire tree must be rebuilt.

This process doesn't require scanning mod folders again for files when not necessary. Each folder mapping has a cache of subdirectories and files, and the same string instances are reused between the trees and cache to save memory.

## File Open Overhead

File open has negligible performance difference compared to not using VFS.
In a test with opening+closing 21,000 files (+70,000 virtualized), the difference was only ~41ms (~3%) or less than 2 microseconds per file.

```
// All tests done in separate processes for accuracy.
|                           Method |    Mean |    Error |   StdDev | Ratio |
|--------------------------------- |--------:|---------:|---------:|------:|
|           OpenAllHandles_WithVfs | 1.650 s | 0.0102 s | 0.0095 s |  1.03 |
| OpenAllHandles_WithVfs_Optimized | 1.643 s | 0.0145 s | 0.0135 s |  1.03 |
|        OpenAllHandles_WithoutVfs | 1.602 s | 0.0128 s | 0.0120 s |  1.00 |
```

In real-world `"cold-start"` scenarios (e.g. after a machine reboot), opening these many files would take around 80 seconds, making this difference effectively margin of error (~0%).

## Built-in Benchmarks

If you're a programmer, a lot of microbenchmarks are available in the `Reloaded.Universal.Redirector.Benchmarks` project; have a look!