# Backends

!!! info "'Backend' in the context of this spec refers to language/runtime support."

    For some programming languages, it might be necessary to manually bootstrap a runtime.

## Platforms

!!! info "The following platform names are standardised."

| Backend  | Description      | MVP | MVP Note                                                |
| -------- | ---------------- | --- | ------------------------------------------------------- |
| `win`    | Windows (`.dll`) | ✅   | Support MSVC or Static Linked                           |
| `linux`  | Linux (`.so`)    | ✅   | Support glibc or Static Linked                          |
| `macos`  | macOS (`.dylib`) | ❌   | Lacking necessary hardware.                             |
| `switch` | Horizon (`.nro`) | ❌   | Lacking in expertise. But there's interest.             |
| `dotnet` | .NET (`.dll`)    | ✅   | CoreCLR. Including support for platforms targeting R2R. |

!!! tip "It is preferred to use universally recognisable names over internal ones."

    For example, prefer:

    - `switch` over `horizon`
    - `dotnet` over `coreclr`

## Architectures

!!! info "The following architectures are standardised."

| Arch      | Note                             |
| --------- | -------------------------------- |
| `x86-any` | Assuming `i686` as the baseline. |
| `x64-any` | Also known as `x86-64-v1`        |
| `arm64`   |                                  |

### Microarchitecture Levels

!!! tip "[Microarchitecture levels][microarchitecture-levels] for purposes of micro-optimisation are also supported."

    This is present for high performance dependencies, where every nanosecond counts.

    Generally, it is not expected that mod authors will manually leverage this functionality however,
    that said; it is hoped we can make it easy to use during the [publish process][mod-publishing] if possible.

| Type   | Name   | Description                                   |
| ------ | ------ | --------------------------------------------- |
| string | x64-v2 | Path to DLL targeting x86-64-v2               |
| string | x64-v3 | Path to DLL targeting x86-64-v3               |
| string | x64-v4 | Path to DLL targeting x86-64-v4               |
| string | x86-v2 | Path to DLL targeting x86-64-v2 (32-bit mode) |
| string | x86-v3 | Path to DLL targeting x86-64-v3 (32-bit mode) |
| string | x86-v4 | Path to DLL targeting x86-64-v4 (32-bit mode) |

Compilers based on LLVM (Clang, Rust etc.) can directly target these.

For example, if the backend specified is `x64-v3`, it is assumed the CPU supports AVX2.

!!! tip "For more information, including how the `x86` targets are derived, see [Research: Microarchitecture Levels][research-march-levels]."

## TOML Representation

!!! info "Backends have arbitrary information, thus in all serialized data in configs are represented as dictionaries"

Take for example [Package Metadata], where the [`Targets`][mod-configurations-targets] field
is a nested dictionary.

```toml
[Targets.win]
x64-any = "mod.dll"
```

The dictionary name is [`Targets`][mod-configurations-targets], with the first level
[Platform](#platforms) key being `win`, and the second level [Architecture](#architectures) key
being `x64-any`.

## Runtime Library Assumptions

!!! note "Assume each backend links to the common C runtime for the platform."

    In other words:

    - `win` really means `win` + `msvc`.
    - `linux` really means `linux` + `glibc`.
    - `dotnet` really means `dotnet-coreclr`.

## Loader Behaviour

When the loader is about to load a mod, it looks up a dictionary specified in the [Package Metadata],
and starts the mod using the appropriate backend.

If the backend is not one supported by the loader, the loader will try to find an already loaded
mod which may have [registered the backend](#custom-backends).

It's possible to ship a mod for multiple platforms by including multiple backends in a mod config
and shipping separate binaries for multiple platforms.

### Custom Backends

!!! note "In some cases, some custom bootstrapping might be required."

For example:

- For a .NET game, it might be desirable to execute mods inside the game's own runtime.
- For a `Unity` game handler, you may want to swap between `mono` and `dotnet-latest` based on runtime version & `Il2Cpp` status.
- Backwards compatibility for legacy mods written for a previous mod loader.

| Example Backend                | Description                                                                |
| ------------------------------ | -------------------------------------------------------------------------- |
| `unity.unity-custom`           | Runs mods in `dotnet-latest` for Il2Cpp; `mono` otherwise.                 |
| `sewer56.reloadedii-custom`    | Runs in `dotnet-latest`, provides backwards compatibility for R2 mods.     |
| `taleworlds.bannerlord-custom` | Loads using .NET Framework (older versions) or .NET Core (newer versions). |

To allow for maximum modularity; custom backends are implemented via [regular mods][regular-mods];
allowing them to be updated independently from the loader.

## Information for Project Template Authors

!!! info "For project templates it is recommended to target LLVM-based toolchains (Clang, Rust, etc.)"

For the following reasons:

- They can directly target the microarchitecture levels mentioned above.
- More portable, for example, you can `cross compile` (e.g. build for Windows from Linux).
- They can generate better code.

<!-- Links -->
[mod-configurations-targets]: ../../Server/Packaging/Package-Metadata.md#targets
[regular-mods]: ../Core-Architecture.md#regular-mods-layer-3
[Package Metadata]: ../../Server/Packaging/Package-Metadata.md
[microarchitecture-levels]: https://en.wikipedia.org/wiki/X86-64#Microarchitecture_levels
[mod-publishing]: ../../Server/Packaging/Publishing-Packages.md
[research-march-levels]: ../../Research/Microarchitecture-Levels.md