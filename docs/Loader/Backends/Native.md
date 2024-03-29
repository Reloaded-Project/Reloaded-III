# Native Support

This backend provides support for native mods on all platforms, for example:

| Backend        | Description                     |
|----------------|---------------------------------|
| `win-x86`      | Native x86 Support on Windows   |
| `win-x64`      | Native x64 Support on Windows   |
| `win-arm64`    | Native ARM64 Support on Windows |
| `linux-x86`    | Native x86 Support on Linux     |
| `linux-x64`    | Native x64 Support on Linux     |
| `switch-arm64` | Native ARM64 Support on Switch  |

This is the only backend that is directly implemented in the mod loader itself (as we are already in a native environment);
all other backends are implemented as external mods.

## Configuration

!!! info "These are the configuration properties that apply to [Mod Metadata Targets](../Configurations/Mod-Metadata.md#targets)"

| Type   | Name | Description  |
|--------|------|--------------|
| string | any  | Path to DLL. |

For `any`, platform default extensions are assumed.
For example, if the backend specified is `win-x64`, it is assumed the CPU supports SSE2; which is required by `x64` spec.

### Instruction Sets

!!! info "Configurations can define DLLs built for processor-specific feature sets."

The following are currently recognized by the spec:

| Type   | Name      | Description               |
|--------|-----------|---------------------------|
| string | x86-sse3  | Path to DLL using SSE3.   |
| string | x86-sse41 | Path to DLL using SSE4.1. |
| string | x86-sse42 | Path to DLL using SSE4.2. |
| string | x86-avx   | Path to DLL using AVX.    |
| string | x86-avx2  | Path to DLL using AVX2.   |

This functionality is provided for high performance dependencies, where every fraction of a nanosecond counts.

It is not expected that mod authors will manually leverage this functionality; that said; it is hoped we could inject it
during the [publish process](../Mod-Publishing.md) if possible for the given platform.