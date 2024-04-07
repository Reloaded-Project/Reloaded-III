# Mod Metadata

!!! warning "Work in Progress"

!!! info "Describes the format of `Package.toml` for mods."

Mod Metadata extends from standard package metadata ([Package.toml][package-toml]).

| Type                             | Name                               | Description                                                       |
| -------------------------------- | ---------------------------------- | ----------------------------------------------------------------- |
| string                           | Description                        | Short description of the mod. (<= 200 chars)                      |
| string                           | [Icon](#icon)                      | Relative path of preview icon.                                    |
| bool                             | [IsLibrary](#is-library)           | If true this mod cannot be explicitly enabled by the user.        |
| Dictionary&lt;string, Target&gt; | [Targets](#targets)                | Specifies the DLLs/binaries used [for each backend.][backend]     |
| string[]                         | [SupportedGames](#supported-games) | List of supported titles/games.                                   |

## Icon

!!! info "Stores path relative to folder `ModConfig.json` is stored in."

!!! info "Supported formats include `.png`, `.jpg` and `.webp`."

!!! info "Should be a multiple of `256x256`. Recommended `512x512`."

## Is Library

!!! info "If this is true, the mod cannot be explicitly enabled by the user in the manager."

!!! info "Some libraries may have user [configuration(s)][mod-configurations]. Manager is free to hide other libraries."

## Targets

!!! info "This section specifies info for the individual [backends.][backend]"

Find more info on the pages for the [individual backends][backend], but we'll provide some examples.

[Native Mod][native-backend]:
```json
{
  "win-x64" : {
    "any": "Mod.dll",
    "x86-sse41": "Mod-SSE41.dll",
    "x86-avx": "Mod-AVX.dll",
    "x86-avx2": "Mod-AVX2.dll"
  }
}
```

!!! note "It's not expected for mod authors to ship with multiple [instruction sets](#instruction-sets) outside of super high perf scenarios. This is just for example."

[.NET CoreCLR Mod][coreclr-backend]:

```json
{
  "dotnet-latest" : {
    "any": "Heroes.Graphics.Essentials.dll",
    "x86": "x86/Heroes.Graphics.Essentials.dll",
    "x64": "x86/Heroes.Graphics.Essentials.dll"
  }
}
```

[Reloaded-II Mod][reloaded2-backend]:

```json
{
  "sewer56.reloadedii-custom": {
    "any": "Heroes.Graphics.Essentials.dll",
    "x86": "x86/Heroes.Graphics.Essentials.dll",
    "x64": "x86/Heroes.Graphics.Essentials.dll",
    "CanUnload": true,
    "HasExports": true,
    "OptionalDependencies": []
  }
}
```

!!! info "For .NET, the `x86` and `x64` fields indicate binaries using [ReadyToRun][ready-to-run] technology. Usually a mod will only specify `any` or a `x86`+`x64` pair."

## Supported Games

!!! info "Stores a list of supported games; by using their known [Application ID][app-metadata-id]."

Alternatively, when experimenting with new games which do not have a specified Application ID, you can also specify `.exe` name, e.g. `tsonic_win.exe`.

Mod managers will automatically update this to appropriate ID during process of querying [Community Repository][community-repository].

<!-- Links -->
[app-metadata-id]: ../../Server/Configurations/App-Metadata.md#id
[backend]: ../../Loader/Backends/About.md
[community-repository]: ../../Services/Community-Repository.md
[coreclr-backend]: ../../Loader/Backends/CoreCLR.md
[mod-configurations]: ./Mod-Configurations.md
[native-backend]: ../../Loader/Backends/Native.md
[package-toml]: ../Packaging/Package-Metadata.md
[ready-to-run]: ../../Loader/Backends/CoreCLR.md#ready-to-run
[reloaded2-backend]: ../../Loader/Backends/CoreCLR.md#reloaded-ii