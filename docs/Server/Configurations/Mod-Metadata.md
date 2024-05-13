# Mod Metadata

!!! info "The format of ([package.toml][package-toml]) used to describe every mod package."

Mod Metadata extends from standard ([package.toml][package-toml]).

| Type                             | Name                               | Description                                                   |
| -------------------------------- | ---------------------------------- | ------------------------------------------------------------- |
| string                           | [Icon-Square](#icon-square)        | Relative path of preview icon.                                |
| GalleryItem[]                    | [Gallery](#gallery)                | Stores preview images for this mod.                           |
| bool                             | [IsLibrary](#is-library)           | If true this mod cannot be explicitly enabled by the user.    |
| Dictionary&lt;string, Target&gt; | [Targets](#targets)                | Specifies the DLLs/binaries used [for each backend.][backend] |
| string[]                         | [SupportedGames](#supported-games) | List of supported titles/games.                               |

## Icons

!!! info "These are paths relative to folder `Package.toml` is stored in."

!!! info "Uses JPEG XL (`.jxl`)."

    Other formats, e.g. `.png`, `.jpg` and `.webp` will be auto converted.

### Icon (Square)

!!! info "Should be a multiple of `256x256`. Recommended `512x512`."

### Icon (Banner)

!!! info "Should be a multiple of `920x430`."

    Same as Steam (Horizontal) banners.

### Icon (Poster)

!!! info "Should be a multiple of `600x900`."

    Same as Steam (Vertical) covers/banners.

## Gallery

!!! info "Gallery images are stored in [images][package-images] folder."

### GalleryItem

| Type    | Name     | Description                                        |
| ------- | -------- | -------------------------------------------------- |
| string  | FileName | Name of file in [images][package-images] folder.   |
| string? | Caption  | [Optional] One line description of the screenshot. |

## Is Library

!!! info "If this is true, the mod cannot be explicitly enabled by the user in the manager."

!!! info "Some libraries may have user [configuration(s)][mod-configurations]. Manager is free to hide other libraries."

## Targets

!!! info "This section specifies info for the individual [backends.][backend]"

Find more info on the pages for the [individual backends][backend], but we'll provide some examples.

[Native Mod][native-backend]:
```json
[Targets."win-x64"]
any = "reloaded3.gamesupport.p5rpc.dll"
x64-v2 = "reloaded3.gamesupport.p5rpc.v2.dll"
x64-v3 = "reloaded3.gamesupport.p5rpc.v3.dll"
```

!!! note "It's not expected for mod authors to ship with multiple [instruction sets][instruction-sets] outside of super high perf scenarios. This is just for example."

[.NET CoreCLR Mod][coreclr-backend]:

```json
[Targets."dotnet-latest"]
any = "Heroes.Graphics.Essentials.dll"
x86 = "x86/Heroes.Graphics.Essentials.dll"
x64 = "x86/Heroes.Graphics.Essentials.dll"
```

[Reloaded-II Mod][reloaded2-backend]:

```json
[Targets."sewer56.reloadedii-custom"]
any = "Heroes.Graphics.Essentials.dll"
x86 = "x86/Heroes.Graphics.Essentials.dll"
x64 = "x86/Heroes.Graphics.Essentials.dll"
CanUnload = true
HasExports = true
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
[instruction-sets]: ../../Loader/Backends/Native.md#instruction-sets
[mod-configurations]: ./Mod-Configurations.md
[native-backend]: ../../Loader/Backends/Native.md
[package-toml]: ../Packaging/Package-Metadata.md
[package-images]: ../Packaging/About.md#images
[ready-to-run]: ../../Loader/Backends/CoreCLR.md#ready-to-run
[reloaded2-backend]: ../../Loader/Backends/CoreCLR.md#reloaded-ii