# Performance Characteristics

!!! note "The numbers here are expected worst-case numbers."

    These were gathered from the original heavily optimized C# implementation of the VFS.

    Some of these may improve a bit, others, not so much.

All numbers were obtained on a stock clock AMD Ryzen 5900X and 3000MHz CL16 RAM.

## File Mapping Performance & Memory Usage

!!! note "These are numbers from the original C# version."

    We can save some additional memory in Rust with clever use of [custom string pooling][string-pooling].<br/>
    AHash is also a better hash algorithm. Expect both memory and speed numbers to improve a tiny bit.

!!! info "This section describes how long it takes to create a file map."

    A file map is used to redirect original files to their new versions found in mod folders.<br/>
    Whenever changes are made to mod folders, a 'rebuild' of the map is done.

Two types of maps exist, [RedirectionTree][redirection-tree] and [LookupTree][lookup-tree].
The latter, `LookupTree` is optimized for performance, but takes roughly twice as long to build as
it is built from the former `RedirectionTree`.

| Folder Type                  | Directories | Total Items | RedirectionTree (Time) | RedirectionTree (Memory) | LookupTree (Time) | LookupTree (Memory) |
| ---------------------------- | ----------- | ----------- | ---------------------- | ------------------------ | ----------------- | ------------------- |
| Windows Folder               | 40,796      | 170,438     | 43ms                   | 27MB                     | 32ms              | 25MB                |
| Steam Folder <br/>(65 games) | 9,318       | 172,896     | 18ms                   | 12MB                     | 20ms              | 11MB                |

The performance of mapping operations mainly depends on the directory count. The table above shows
the time and memory usage for building the `RedirectionTree` and `LookupTree` for both Windows and
Steam folders. The `LookupTree` memory usage should be approximately equal to the total runtime
memory usage.

For a typical game (based on the median of a Steam library), building the `RedirectionTree` should
take around `0.017ms` and allocate `48KB`. Creating the optimized `LookupTree` takes about `0.012ms`
(+ time taken for `RedirectionTree`) and allocates `47KB`.

In other words, you can assume remapping files is basically real-time.

### Fast Append

!!! tip "It's possible to skip a 'rebuild' in some situations."

Both `LookupTree` and `RedirectionTree` can have `'fast append'` operations.
(Just like in the original C# implementation)

If a file is added to the mod folder while the game is running and isn't previously mapped,
it can be added to the tree directly without a full rebuild.

However, if the currently mapped file's source mod cannot be determined, the entire tree must be rebuilt.

This process doesn't require scanning mod folders again for files when not necessary.
Each folder mapping can have a cache of subdirectories and files, and the same string instances can be
reused between the trees and cache to save memory.

## File Open Overhead

!!! info "These are numbers for original C# implementation"

File open has negligible performance difference compared to not using VFS.
In a test with opening+closing 21,000 files (+70,000 virtualized), the difference was
only ~41ms (~3%) or less than 2 microseconds per file.

```
// All tests done in separate processes for accuracy.
| Method                           |    Mean |    Error |   StdDev | Ratio |
| -------------------------------- | ------: | -------: | -------: | ----: |
| OpenAllHandles_WithVfs           | 1.650 s | 0.0102 s | 0.0095 s |  1.03 |
| OpenAllHandles_WithVfs_Optimized | 1.643 s | 0.0145 s | 0.0135 s |  1.03 |
| OpenAllHandles_WithoutVfs        | 1.602 s | 0.0128 s | 0.0120 s |  1.00 |
```

In real-world `"cold-start"` scenarios (e.g. after a machine reboot), opening these many files
would take around 80 seconds, making this difference effectively margin of error (~0%).

## Existing Benchmarks

A lot of microbenchmarks are available in the original C# project under the
[Reloaded.Universal.Redirector.Benchmarks][microbenchmarks] project; have a look!

[ahash]: https://github.com/tkaitchuck/aHash
[equivalent]: https://docs.rs/hashbrown/latest/hashbrown/trait.Equivalent.html
[lookup-tree]: ./Implementation-Details/Trees.md#lookup-tree
[make-ascii-uppercase]: https://github.com/rust-lang/rust/blob/80d1c8349ab7f1281b9e2f559067380549e2a4e6/library/core/src/num/mod.rs#L627
[microbenchmarks]: https://github.com/Reloaded-Project/reloaded.universal.redirector/tree/rewrite-usvfs-read-features/Reloaded.Universal.Redirector.Benchmarks
[redirection-tree]: ./Implementation-Details/Trees.md#redirection-tree
[reloaded-memory-hash]: https://github.com/Reloaded-Project/Reloaded.Memory/blob/5d13b256c89ffa2b18bf430b6ef39925e4324412/src/Reloaded.Memory/Internals/Algorithms/UnstableStringHash.cs#L16
[reloaded-memory-toupper]: https://github.com/Reloaded-Project/Reloaded.Memory/blob/5d13b256c89ffa2b18bf430b6ef39925e4324412/src/Reloaded.Memory/Internals/Backports/System/Globalization/TextInfo.cs#L79
[string-pooling]: ./Implementation-Details/Optimizations.md#memory-storage
[smhasher]: https://github.com/rurban/smhasher
