# Mod Metadata

!!! info "The format of ([package.toml][package-toml]) used to describe every mod package."

Mod Metadata extends from standard ([package.toml][package-toml]).

| Type                             | Name                               | Description                                                   |
| -------------------------------- | ---------------------------------- | ------------------------------------------------------------- |
| string                           | [IconSquare](#icon-square)         | Relative path of preview icon (square format).                |
| string                           | [IconSearch](#icon-search)         | Relative path of preview icon (search format).                |
| GalleryItem[]                    | [Gallery](#gallery)                | Stores preview images for this mod.                           |
| bool                             | [IsLibrary](#is-library)           | If true this mod cannot be explicitly enabled by the user.    |
| Dictionary&lt;string, Target&gt; | [Targets](#targets)                | Specifies the DLLs/binaries used [for each backend.][backend] |
| string[]                         | [SupportedGames](#supported-games) | List of supported titles/games.                               |

## Icons

!!! info "Gallery images are stored in [images][package-images] folder."

!!! info "Each entry is a name of file in [images][package-images] folder."

!!! info "Images use [JPEG XL (`.jxl`)][images]"

### Icon (Square)

!!! info "Should be a multiple of `256x256`. Recommended `512x512`."

### Icon (Search)

!!! info "This is the preview icon used for mod search results."

    It corresponds to [GridDisplayMode 3][grid-display-mode].

The size of this image should be `880x440` (2:1) with a `content` area of `600x440`.

Depending on the user's window size, the will be cropped to some size
between `880x440` and `600x440`. Thus you should aim to put all the important
detail within the `600x440` area.

This image is expected to be around 50KiB.

!!! note "The `880x440` is the target resolution for 4K displays."

### Icon (List Compact View)

!!! info "This is the preview icon used when displaying mods as a list (compact)."

    It corresponds to [GridDisplayMode 1][grid-display-mode].

The size of this image should be `84x48`.

This image is expected to be around 2KiB.

!!! note "The `84x48` is the target resolution for 4K displays."

### Icon (List View)

!!! info "This is the preview icon used when displaying mods as a list."

    It corresponds to [GridDisplayMode 2][grid-display-mode].

The size of this image should be `168x96`.

This image is expected to be around 5KiB.

!!! note "The `84x48` is the target resolution for 4K displays."

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

!!! info "These specify file paths relative to `modfiles` folder."

Find more info on the pages for the [individual backends][backend], but we'll provide some examples.

[Native Mod][native-backend]:
```json
[Targets."win-x64"]
any = "reloaded3.gamesupport.persona5royal.dll"
x64-v2 = "reloaded3.gamesupport.persona5royal.v2.dll"
x64-v3 = "reloaded3.gamesupport.persona5royal.v3.dll"
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

!!! info "Stores a list of supported games; by using their known [Game ID][game-id]."

Alternatively, when experimenting with new games which do not have a specified Game ID, you can also specify `.exe` name, e.g. `tsonic_win.exe`.

Mod managers will automatically update this to appropriate ID during process of querying [Community Repository][community-repository].

<!-- Links -->
[backend]: ../../../Loader/Backends/About.md
[community-repository]: ../../../Services/Community-Repository.md
[coreclr-backend]: ../../../Loader/Backends/CoreCLR.md
[game-id]: ../../Storage/Games/About.md#id
[instruction-sets]: ../../../Loader/Backends/Native.md#instruction-sets
[mod-configurations]: ./Mod-Configurations.md
[native-backend]: ../../../Loader/Backends/Native.md
[package-toml]: ../Package-Metadata.md
[package-images]: ../About.md#images
[ready-to-run]: ../../../Loader/Backends/CoreCLR.md#ready-to-run
[reloaded2-backend]: ../../../Loader/Backends/CoreCLR.md#reloaded-ii
[images]: ../../../Common/Images.md
[grid-display-mode]: ../../../Server/Storage/Loadouts/Events.md#griddisplaymode