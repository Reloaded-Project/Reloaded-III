# Community Repository

!!! info

    The community repository. This allows us to apply per-game specific support/rules without having to recompile mod managers.

!!! note "This documents a future iteration of [Reloaded.Community](https://github.com/Reloaded-Project/Reloaded.Community) repository."

## About

The `Community Repository` contains game-specific information for launchers implementing the Reloaded3 spec.

The idea is we can update the information we know about various games without ever having to recompile individual launchers,
instead, dynamically downloading them from the web.

Some use cases include:

- Automatically registering GameBanana/Nexus/GitHub download sources.
- Helping automatic detection of games installed via Steam/Epic/Origin etc.
- Providing compatibility warnings for pre-patched/pre-modded legacy games.
- Informing user of wrong game binary. (e.g. User has EU EXE but mods target US)
- Auto assign Game IDs in [Application Configurations](../Server/Configurations/App-Metadata.md).
- Updating [Mod Configurations](../Loader/Configurations/Mod-Metadata.md) with correct [App ID](../Server/Configurations/App-Metadata.md#id)s marking which games an app supports.

## Schema

!!! note

    This represents the schema of items the individual users add to the repo manually.
    This schema can produce 1 or more files in the [API](#api) (depending on number of game versions, etc.)

All configurations are written as YAML (for editing convenience), but are converted to JSON for applications to consume.

They can have any name (as long as they use their own unique folder), in this spec we will refer to them as `App.yml`.

| Type          | Item                                            | Description                                                                                    |
| ------------- | ----------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| string        | [Id](../Server/Configurations/App-Metadata.md)  | Unique identifier for this game. Copied to [App Id](../Server/Configurations/App-Metadata.md). |
| string        | Name                                            | User friendly name for the game, e.g. 'Sonic Heroes'.                                          |
| Version[]     | [Versions](#version)                            | Versions of the executable.                                                                    |
| Version[]     | [Launchers](#other-binaries)                    | Stores information about other executables in game folder you probably don't wanna mod.        |
| string        | [Icon](#icon)                                   | Icon for the game in 1:1 aspect ratio.                                                         |
| string        | [BannerH](#banner)                              | Horizontal banner for the game.                                                                |
| string        | [BannerV](#banner)                              | Vertical banner for the game.                                                                  |
| StoreInfo     | [StoreInformation](#store-information)          | Game store specific information.                                                               |
| ModSourceInfo | [ModSourceInformation](#mod-source-information) | Mod source (Nexus/GameBanana/GitHub) specific information.                                     |
| Warning[]     | [Warnings](#warnings)                           | Warnings to display if specific files are found in game folder.                                |
| string        | [BadHashMessage](#bad-hash-message)             | Message to display if the user has a bad EXE hash.                                             |
| string[]      | [DllEntryPoints](#dll-entry-points)             | Names of DLLs we can use with [DLL Hijacking](../Loader/Bootloaders/Windows-DllHijack.md).     |

!!! note "Note: All hashes listed in this specification are `xxHash64`."

!!! note "Not all of this information has to be hand typed, some information such as version numbers, hashes, dates can be automatically extracted."

### Example

```yaml
Id: "SonicHeroes"
Versions:
  - Hash: "33A911467398D820"
    ExeName: "tsonic_win.exe"
    Version: "1.0.0.1"
    Date: "2004-10-18T08:15:02"

OtherBinaries:
  - Hash: "8CF7D3CD8CDBBFE"
    ExeName: "launcher.exe"
    Version: "1.0.0.1"
    Date: "2004-10-18T06:51:29"

Icon: "TSonic.png"
BannerH: "BannerH.png"
BannerV: "BannerV.png"
# This game was never digitally released :(
ModSourceInformation:
  - GameBanana:
      Id: 6061

Warnings:
  - Message: "Your game folder contains ThirteenAG's WidescreenFix. You might experience a crash in Special Stage 4 and some other mods.\n\nWorkaround:\n- Delete `scripts/SonicHeroes.WidescreenFix.asi`\n- Download Heroes Graphics Essentials."
    Items:
      - Hash: "7180B796B297ED77"
        FilePath: "scripts/SonicHeroes.WidescreenFix.asi"

BadHashDescription: "Mods target the NoCD version of Sonic Heroes; specifically the Reloaded release. That said, any NoCD version with removed SafeDisc DRM should work, including Sega's own Sonic PC Collection."
```

!!! note "Note: Better examples are welcome!"

### Version

!!! info "Stores individual version information for a binary with a given hash."

| Type     | Item        | Description                                                                                       |
| -------- | ----------- | ------------------------------------------------------------------------------------------------- |
| string   | Hash        | Hash of executable.                                                                               |
| string   | ExeName     | Name of executable.                                                                               |
| string[] | EntryPoints | [Optional*] Name of [entry point DLLs for hijacking.](../Loader/Bootloaders/Windows-DllHijack.md) |
| string   | Version     | [Optional] Version of game bound to this executable.                                              |
| DateTime | Date        | [Optional] Date of this version, as ISO 8601.                                                     |

This version and their time are supposed to be purely informative.

!!! note "`EntryPoints` is required for EXEs but optional for any other type that inherits `Version`"

!!! warning

    In cases where a game significantly differs after a update to the point where handling it using existing mods
    is not possible (e.g. 32bit -> 64bit + changed file formats); you should make a new entry for the game in the repository,
    e.g. `Persona 4 Golden 64-bit`, rather than adding a new version.

### Other Binaries

!!! info "Extends from [Version](#version)"

| Type   | Item    | Description                             |
| ------ | ------- | --------------------------------------- |
| string | Message | Message to display for this executable. |

And all existing fields in [Version](#version)...

Example Message:

- `This executable is the launcher for this game. Are you sure you didn't want to select <X>?`.

### Icon

!!! info "Stores path relative to folder `App.yml` is stored in."

!!! info "Supported formats include `.png`, `.jpg` and `.webp`."

!!! info "Should be a multiple of `128x128`. Recommended `512x512`."

### Banner

!!! info "Stores path relative to folder `App.yml` is stored in."

!!! info "Supported formats include `.png`, `.jpg` and `.webp`."

!!! info "BannerV: Use `600x900` or a multiple of this resolution."

!!! info "BannerH: Use `920x430` or a multiple of this resolution."

We use the Steam resolutions for `BannerV` and `BannerH`, and official Steam assets when possible.

Mod manager can choose to display either, or not use any at all.

### Store Information

| Type           | Item                      | Description                                   |
| -------------- | ------------------------- | --------------------------------------------- |
| EAGameInfo     | [EADesktop](#ea-desktop)  | Contains EA Desktop related information.      |
| EpicGameInfo   | [Epic](#epic-games-store) | Contains Epic Game Store related information. |
| GogGameInfo    | [Gog](#gog)               | Contains EA Desktop related information.      |
| OriginGameInfo | [Origin](#origin)         | Contains Origin related information.          |
| SteamGameInfo  | [Steam](#steam)           | Contains Steam related information.           |
| XboxGameInfo   | [Xbox](#xbox)             | Xbox Game Pass information.                   |

Supported stores are based on [GameFinder](https://github.com/erri120/GameFinder) library.

#### EA Desktop

!!! failure "[Given how hard they are trying to stop you from finding out where your games are installed by using military grade SHA3-256 encryption](https://github.com/erri120/GameFinder/wiki/EA-Desktop); changes here might be needed someday."

| Type   | Item       | Description                                               |
| ------ | ---------- | --------------------------------------------------------- |
| string | SoftwareID | Unique ID for this game used in 'EA Desktop' application. |

#### Epic Games Store

!!! warning "It is unconfirmed whether this is the best item to use, this may still be changed."

| Type   | Item          | Description                     |
| ------ | ------------- | ------------------------------- |
| string | CatalogItemId | Unique ID in catalog for 'EGS'. |

#### GOG

!!! tip "You can use the [GOG Database](https://www.gogdb.org/) to look up these IDs."

| Type | Item | Description                            |
| ---- | ---- | -------------------------------------- |
| long | ID   | Unique ID for this game used in 'GOG'. |

#### Origin

!!! warning "EA is [deprecating Origin in favour of EA Desktop](https://www.ea.com/en-gb/news/ea-app)"

| Type   | Item | Description                               |
| ------ | ---- | ----------------------------------------- |
| string | ID   | Unique ID for this game used in 'Origin'. |

#### Steam

!!! tip "You can use the [SteamDB](https://steamdb.info/) to look up these IDs."

| Type   | Item          | Description                     |
| ------ | ------------- | ------------------------------- |
| string | CatalogItemId | Unique ID in catalog for 'EGS'. |

#### Xbox

| Type   | Item | Description                                                                                                                                                         |
| ------ | ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| string | ID   | Unique ID. Corresponds to [Package.Identity.Name in AppxManifest.xml](https://learn.microsoft.com/en-us/uwp/schemas/appxpackage/uapmanifestschema/element-identity) |

### Mod Source Information

| Type           | Item                      | Description                     |
| -------------- | ------------------------- | ------------------------------- |
| GameBananaInfo | [GameBanana](#gamebanana) | Info for GameBanana Mod Search. |
| NexusInfo      | [NexusMods](#nexus-mods)  | Info for NexusMods Mod Search.  |

#### GameBanana

!!! info "Derived from URL to game page."

| Type | Item | Description                                                                 |
| ---- | ---- | --------------------------------------------------------------------------- |
| int  | Id   | Unique identifier for game, e.g. 6061 for https://gamebanana.com/games/6061 |

#### Nexus Mods

!!! info "Derived from URL to game page."

| Type   | Item | Description                                                             |
| ------ | ---- | ----------------------------------------------------------------------- |
| string | Id   | Domain for the game, e.g. `skyrim` for https://www.nexusmods.com/skyrim |

In the Nexus API this ID is usually referred to as `Domain`.

### Warnings

Can be used to provide warnings for 3rd party components. e.g. Old DLL mods incompatible with Reloaded, Steam API Emulator DLLs, etc.

| Type        | Item                   | Description                                            |
| ----------- | ---------------------- | ------------------------------------------------------ |
| string      | Message                | The error message to display if any files are matched. |
| WarningItem | [Items](#warning-item) | Warning Item(s) List of files to match against.        |

#### Warning Item

| Type   | Item     | Description                                                            |
| ------ | -------- | ---------------------------------------------------------------------- |
| string | Hash     | [Optional] Hash of the item.                                           |
| string | FilePath | Path of the file relative to the folder in which the EXE is contained. |

### Bad Hash Message

!!! info "This message is displayed if user specifies 'I 100% want this game', but no EXE hash is matched."

## File Layout

```
Repository Root
└── Apps
    ├── Game 1
    │   └── App.yml
    └── Game 2
        └── App.yml
```

## Building The Repository

!!! info

    The raw files specified in [schema](#schema) go through a 'build' process.
    This build process converts the files to `.json` and spit it out in a format suitable for hosting on [GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages).

Output format:

```
Repository Root
├── Index.json.br
├── Apps
    ├── Game 1
    │   └── App.json.br
    └── Game 2
        └── App.json.br
```

The build process performs 2 steps:

- Converts the `.yml` files to `.json` for easier consumption from managers.
- Produces an [Index](#index) for searching for a given game.

### Index

!!! info

    The Index contains serialized dictionaries responsible for quick lookup of individual games.

| Type                            | Item       | Description                   |
| ------------------------------- | ---------- | ----------------------------- |
| Dictionary<string, IndexItem[]> | ExeToApps  | Maps game `.exe` file to App. |
| Dictionary<string, IndexItem>   | HashToApps | Maps game `.exe` hash to App. |

`IndexItem` is defined as:

| Type   | Item     | Description                                                       |
| ------ | -------- | ----------------------------------------------------------------- |
| string | AppName  | User friendly name for the game.                                  |
| string | FilePath | Relative path to this `.json` file to the game [Schema](#schema). |

In the case of `ExeToApps`; if there are multiple entries, the user must select the appropriate choice from their UI.