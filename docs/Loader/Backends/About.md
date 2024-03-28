# Backends

!!! info

    'Backend' in the context of this spec refers to language/runtime support; for some programming languages,
    it might be necessary to manually bootstrap a runtime.

!!! note

    For simplicity; assume Windows builds are dynamically linked to MSVC.
    i.e. `win-x86` really means `win-x86-msvc`.

!!! tip

    It is preferred to use universally recognisable names over internal ones i.e. prefer `switch` over `horizon`.

Example backends include:

| Backend          | Description                              |
|------------------|------------------------------------------|
| `win-x86`        | Native x86 Support on Windows            |
| `win-x64`        | Native x64 Support on Windows            |
| `coreclr-latest` | Latest .NET Runtime                      |

The following backends are backlogged; will be implemented when/if there is demand:

| Backend        | Description                              |
|----------------|------------------------------------------|
| `switch-arm64` | Native ARM64 Support on Switch (Horizon) |
| `linux-x64`    | Native x64 Support on Switch (Horizon)   |

These backends are directly specified inside the [mod configurations](../Configurations/Mod-Metadata.md#targets). When the loader is about to load a
mod, it looks up a dictionary specified in the mod config, and starts the mod using the appropriate backend.

It's possible to ship a mod for multiple platforms by including multiple backends in a mod config
and shipping separate binaries for multiple platforms.

## Custom Backends

In some cases, some custom bootstrapping might be required.

For example:

- For a .NET game, it might be desirable to execute mods inside the game's own runtime.
- For supporting mods for older mod loaders, a backend can act as a wrapper translating exports and implementing old loader APIs.

| Example Backend                | Description                                                                |
|--------------------------------|----------------------------------------------------------------------------|
| `unity.unity-custom`           | Runs mods in `coreclr-latest` for Il2Cpp; `mono` otherwise.                |
| `sewer56.reloadedii-custom`    | Runs in `coreclr-latest`, provides backwards compatibility for R2 mods.    |
| `taleworlds.bannerlord-custom` | Loads using .NET Framework (older versions) or .NET Core (newer versions). |

To allow for maximum modularity; custom backends are implemented via regular mods [TODO: link pending]; allowing them to be updated
independently from the loader.