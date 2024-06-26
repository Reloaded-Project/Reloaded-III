﻿# Native Support

!!! info "This backend provides support for native mods on all platforms."

For example:

| Backend       | Description                     |
| ------------- | ------------------------------- |
| `win-x86`     | Native x86 Support on Windows   |
| `win-x64`     | Native x64 Support on Windows   |
| `win-arm64`   | Native ARM64 Support on Windows |
| `linux-x86`   | Native x86 Support on Linux     |
| `linux-x64`   | Native x64 Support on Linux     |
| `linux-arm64` | Native ARM64 Support on Linux   |

This is the only backend that is directly implemented in the mod loader itself
(as we are already in a native environment). All other backends are implemented as external mods.

## Configuration Fields

!!! info "These are the configuration properties that apply to [Mod Metadata Targets][mod-metadata-targets]"

| Type   | Name | Description  |
| ------ | ---- | ------------ |
| string | any  | Path to DLL. |

For `any`, platform default extensions are assumed.
For example, if the backend specified is `win-x64`, it is assumed the CPU supports SSE2;
which is required by `x64` spec.

### Instruction Sets

!!! info "Configurations can define DLLs built for processor-specific feature sets."

We use [microarchitecture levels][microarchitecture-levels] to define the supported targets:

| Type   | Name   | Description                     |
| ------ | ------ | ------------------------------- |
| string | x64-v2 | Path to DLL targeting x86-64-v2 |
| string | x64-v3 | Path to DLL targeting x86-64-v3 |
| string | x64-v4 | Path to DLL targeting x86-64-v4 |

Compilers based on LLVM (Clang, Rust etc.) can directly target these.

!!! tip "This functionality is provided for high performance dependencies, where every fraction of a nanosecond counts."

It is not expected that mod authors will manually leverage this functionality; that said; it is
hoped we can make it easy to use during the [publish process][mod-publishing] if possible.

#### Determining Supported Instruction Set on Local Machine

Start with [core-detect][core-detect] crate, and make a separate library with helper methods to
determine which category the current CPU falls under.

You can use `rustc --print=cfg -C target-cpu=x86-64-v3` to print the specific `target_feature`(s)
available to a CPU.

#### Emulating Instruction Sets for 32-bit Targets

!!! warning "x86-64-v* don't have equivalents for 32-bit targets in LLVM."

    But we can derive them!

To derive them, use the Rust compiler like so `rustc --print=cfg -C target-cpu=x86-64-v4`.
This will print a list of details for the target, alongside, most importantly, ***target features***.

!!! example "Example for x86-64-v2"

    ```
    target_feature="avx"
    target_feature="avx2"
    target_feature="avx512bw"
    target_feature="avx512cd"
    target_feature="avx512dq"
    target_feature="avx512f"
    target_feature="avx512vl"
    ```

From there, we have to filter out features which are not available in 32-bit mode.

- `avx512bw`, `avx512cd`, `avx512dq`, `avx512f`, `avx512vl`: These AVX-512 extensions are 64-bit only.
- `cmpxchg16b`: This extension is only available in 64-bit mode. May be possible to use in 32-bit programs but atomic read/write of 128-bit values is not guaranteed in 32-bit mode.

Therefore we can derive the following:

| Type   | Name   | Features                                                                       |
| ------ | ------ | ------------------------------------------------------------------------------ |
| string | x86-v2 | `fxsr` `lahfsahf` `popcnt` `sse` `sse2` `sse3` `sse4.1` `sse4.2` `ssse3`       |
| string | x86-v3 | all previous + `avx` `avx2` `bmi1` `bmi2` `f16c` `fma` `lzcnt` `movbe` `xsave` |

The microarch level `i686-v4` is redundant, because all new features in `x86-64-v4` are not
supported in 32-bit mode.

These features come from LLVM, so can also be used with Clang, etc.

## Information for Project Template Authors

!!! info "For project templates it is recommended to target LLVM-based toolchains (Clang, Rust, etc.)"

For the following reasons:

- They can directly target the microarchitecture levels mentioned above.
- More portable, for example, you can `cross compile` (e.g. build for Windows from Linux).
- They can generate better code.

<!-- Links -->
[core-detect]: https://docs.rs/core_detect/latest/core_detect/
[microarchitecture-levels]: https://en.wikipedia.org/wiki/X86-64#Microarchitecture_levels
[mod-metadata-targets]: ../../Server/Packaging/Configurations/Mod-Metadata.md#targets
[mod-publishing]: ../../Server/Packaging/Publishing-Packages.md