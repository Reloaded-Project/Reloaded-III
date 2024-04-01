# Native Support

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
| string | x86-v2 | Path to DLL targeting x86-64-v2 |
| string | x86-v3 | Path to DLL targeting x86-64-v3 |
| string | x86-v4 | Path to DLL targeting x86-64-v4 |

Compilers based on LLVM (Clang, Rust etc.) can directly target these.

!!! tip "This functionality is provided for high performance dependencies, where every fraction of a nanosecond counts."

It is not expected that mod authors will manually leverage this functionality; that said; it is 
hoped we can make it easy to use during the [publish process][mod-publishing] if possible.

## Information for Project Template Authors

!!! info "For project templates it is recommended to target LLVM-based toolchains (Clang, Rust, etc.)"

For the following reasons:

- They can directly target the microarchitecture levels mentioned above.
- More portable, for example, you can `cross compile` (e.g. build for Windows from Linux).
- They can generate better code.

<!-- Links -->
[microarchitecture-levels]: https://en.wikipedia.org/wiki/X86-64#Microarchitecture_levels
[mod-metadata-targets]: ../../Server/Configurations/Mod-Metadata.md#targets
[mod-publishing]: ../Mod-Publishing.md