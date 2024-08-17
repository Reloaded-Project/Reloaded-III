# Backends

!!! info "'Backend' in the context of this spec refers to language/runtime support."

    For some programming languages, it might be necessary to manually bootstrap a runtime.

!!! note "Assume each backend links to the common C runtime for the platform."

    In other words:

    - `win-x86` really means `win-x86-msvc`.
    - `linux-x86` really means `linux-x86-glibc`.
    - `dotnet-latest` really means `dotnet-latest-coreclr`.

!!! tip "It is preferred to use universally recognisable names over internal ones."

    For example, prefer:

    - `switch` over `horizon`
    - `dotnet` over `coreclr`

Planned backends include:

| Backend         | Description                   |
| --------------- | ----------------------------- |
| `win-x86`       | Native x86 Support on Windows |
| `win-x64`       | Native x64 Support on Windows |
| `linux-x64`     | Native x64 Support on Linux   |
| `linux-x86`     | Native x86 Support on Linux   |
| `dotnet-latest` | Latest .NET Runtime           |

Backends that will be delivered if there's community interest in terms of donations/code contributions:

| Backend       | Description                     |
| ------------- | ------------------------------- |
| `win-arm64`   | Native ARM64 Support on Windows |
| `linux-arm64` | Native ARM64 Support on Linux   |

Some potential backends could only be delivered with community involvement, due to lack of knowledge:

| Backend        | Description                              |
| -------------- | ---------------------------------------- |
| `switch-arm64` | Native ARM64 Support on Switch (Horizon) |

These backends are directly specified inside the [mod configurations][mod-configurations-targets].

When the loader is about to load a mod, it looks up a dictionary specified in the mod config,
and starts the mod using the appropriate backend.

It's possible to ship a mod for multiple platforms by including multiple backends in a mod config
and shipping separate binaries for multiple platforms.

## Custom Backends

!!! note "In some cases, some custom bootstrapping might be required."

For example:

- For a .NET game, it might be desirable to execute mods inside the game's own runtime.
- For supporting mods for older mod loaders, a backend can act as a wrapper translating exports and implementing old loader APIs.

| Example Backend                | Description                                                                |
| ------------------------------ | -------------------------------------------------------------------------- |
| `unity.unity-custom`           | Runs mods in `dotnet-latest` for Il2Cpp; `mono` otherwise.                 |
| `sewer56.reloadedii-custom`    | Runs in `dotnet-latest`, provides backwards compatibility for R2 mods.     |
| `taleworlds.bannerlord-custom` | Loads using .NET Framework (older versions) or .NET Core (newer versions). |

To allow for maximum modularity; custom backends are implemented via [regular mods][regular-mods];
allowing them to be updated independently from the loader.

<!-- Links -->
[mod-configurations-targets]: ../../Server/Packaging/Package-Metadata.md#targets
[regular-mods]: ../Core-Architecture.md#regular-mods-layer-3