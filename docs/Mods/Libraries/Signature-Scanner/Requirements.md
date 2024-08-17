# Signature Scanner Requirements

!!! info "The Signature Scanner mod in Reloaded3 should meet the following criteria."

| Feature                                       | Supported by Existing C# Library or Mod |
| --------------------------------------------- | --------------------------------------- |
| [Caching Scan Results](#caching-scan-results) | ❌                                       |
| [Parallel Scanning](#parallel-scanning)       | ✅ (⚠️ has 1 known bug)                   |
| [Hardware Intrinsics](#parallel-scanning)     | ✅ X86, ❌ ARM64                          |
| [Bit Level Scanning](#bit-level-scanning)     | ❌                                       |

Files marked with a cross will need to be implemented in the Rust version of the library after porting
the C# logic.

## Caching Scan Results

!!! success "The Signature Scanner mod should cache scan results between runs to improve performance and reduce redundant scans."

- Compare module (EXE/ELF) size.
- Hash (EXE/ELF) to ensure it hasn't changed since last run.
- If the hash matches, load the cached scan results instead of performing a new scan.
- If the hash does not match, perform a new scan and update the cache.

Caching scan results can significantly improve the startup time of mods that rely on signature
scanning, especially for large games or mods with many signatures.

!!! tip "This is expected to bring ~400ms startup time gain on a typical mid-range 2023 PC."

    In Denuvo titles where ~95% of the EXE is just the Copy Protection (DRM) as opposed to real
    game code. For games not defective by design with this kind of Copy Protection (DRM),
    the gain is expected to be negligible.

!!! warning "TODO: Link documentation on Standard Directories for Caching in Loader Mods"

!!! note "Don't implement a custom cache."

    Use the `cache provider` mod instead. [TODO: Link Pending]

## Parallel Scanning

!!! success "The Signature Scanner library should utilize multiple threads to perform parallel scanning."

Namely, we gather up signatures to scan from each individual mod, and once all mods have finished loading,
we will scan all of the signatures in parallel.

The results of the scan must be returned in the same order as the scan requests were made. Because
the library consumers are likely to hook the returned addresses, it is important to maintain the load
order of the mods.

!!! note "It's possible the same address may be requested by multiple scans."

    It's recommended to cache the results in a dictionary and look up the address in the dictionary
    before doing each full scan.

!!! warning "All parallel scans MUST return in the EXACT order they were submitted."

    In the [Reloaded-II mod][r2-sigscan-mod] there is a slight bug in that `RunMainModuleScans`
    results are all returned before `RunArbitraryScans` results. This is incorrect behaviour.

## Hardware Intrinsics

!!! success "Leverage hardware intrinsics (e.g., AVX, SSE) to accelerate pattern matching where possible."

- Implement optimized pattern matching routines using intrinsics for supported instruction sets.
- Fall back to a generic, non-intrinsic implementation for platforms or CPUs that do not support the required instruction sets.

!!! info "In the mod, use [Microarchitecture Levels][microarch-levels] to determine which code paths to take."

    Don't ship dead code for intrinsics that will not be used.

## Bit-Level Scanning

!!! success "The Signature Scanner library should support scanning at the bit level to handle bit-packed instructions."

    Instruction sets like AArch64 may have cases where you may want to scan for instructions at the bit
    level as the instructions are bit-packed.

Existing C# library does pattern scanning like this:

```csharp
scanner.FindPattern("89 15 ??");
```

Essentially we're saying to allow an alternative format where patterns can be defined at the bit
level.

For example, if we wanted to scan for `"89 ?5 ??"`, we could also define that as:

```csharp
scanner.FindBitPattern("10001001 ????0101 ????????");
```

## Native Implementation

!!! success "The Signature Scanner library should be implemented in a native language."

    This is to make it portable to platforms .NET is not supported.

Basically, ideally with Rust or C.
I (Sewer) would prefer Rust.

## Reference Code

!!! tip "The following existing implementations can be used as a reference for the Reloaded3 Signature Scanner library:"

- **[Reloaded.Memory.Sigscan (C#)][reloaded-memory-sigscan]**: The C# Implementation to port.
    - [Reloaded-II mod][r2-sigscan-mod] which aggregates and parallelises scans from multiple mods.
- **[lazysimd (Rust)][lazysimd]**: A minimal Rust port of `Reloaded.Memory.Sigscan` by RayTwo.

<!-- Links -->
[lazysimd]: https://github.com/Raytwo/lazysimd
[reloaded-memory-sigscan]: https://github.com/Reloaded-Project/Reloaded.Memory.SigScan
[r2-sigscan-mod]: https://github.com/Reloaded-Project/Reloaded.Memory.SigScan/blob/master/External/Reloaded.Memory.SigScan.ReloadedII/StartupScanner.cs
[microarch-levels]: ../../../Loader/Backends/About.md#microarchitecture-levels