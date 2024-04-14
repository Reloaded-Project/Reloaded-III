# Community Repository

!!! info "About the Community Repository"

    This allows us to provide real time updates for per-game specific information without
    explicitly having having to recompile mod loader/server/manager.

!!! note "This documents a future iteration of [Reloaded.Community][reloaded-community] repository."

## About

The `Community Repository` contains game-specific information for the Reloaded3 backend server.

The idea is we can update the information we know about various games without ever having to 
update the actual server itself. This is sometimes called 'out of band' information.

Some use cases include:

- Automatically registering GameBanana/Nexus/GitHub download sources.
- Helping automatic detection of games installed via Steam/Epic/Origin etc.
- Providing compatibility warnings for pre-patched/pre-modded legacy games.
- Informing user of wrong game binary. (e.g. User has EU EXE but mods target US)
- Auto assign Game IDs in [Application Configurations][app-metadata].
- Updating [Mod Configurations][mod-metadata] with correct [App ID][app-metadata-id]s marking which games an app supports.

## Schema

!!! note

    This represents the schema of games the individual users add to the repo manually.

All configurations are written as TOML (for editing convenience).

They can have any name (as long as they use their own unique folder), in this spec we will refer to them as `App.toml`.

| Type          | Item                                            | Description                                                                             |
| ------------- | ----------------------------------------------- | --------------------------------------------------------------------------------------- |
| string        | [Id][app-metadata]                              | Unique identifier for this game. Copied to [App Id][app-metadata].                      |
| string        | Name                                            | User friendly name for the game, e.g. 'Sonic Heroes'.                                   |
| Version[]     | [Versions](#version)                            | Versions of the executable.                                                             |
| OtherBinary[] | [OtherBinaries](#other-binaries)                | Stores information about other executables in game folder you probably don't wanna mod. |
| string[]      | [ReferenceFiles](#referencefiles)               | Stores relative file paths of arbitrary files to disambiguate shared EXE names.         |
| StoreInfo     | [StoreInformation](#store-information)          | Game store specific information.                                                        |
| ModSourceInfo | [ModSourceInformation](#mod-source-information) | Mod source (Nexus/GameBanana/GitHub) specific information.                              |
| Diagnostic[]  | [Diagnostics](#diagnostics)                     | Diagnostics to display based on game's current folder state.                            |
| string        | [BadHashMessage](#bad-hash-message)             | Message to display if the user has a bad EXE hash.                                      |

!!! note "Note: All hashes listed in this specification are `XXH3_128bits` (XXH128) unless specified otherwise."

!!! note "Not all of this information has to be hand typed, some information such as version numbers, hashes, dates can be automatically extracted."

### Implicit Files

!!! info "If present, the following will be used."

| Value         | Item               | Description                            |
| ------------- | ------------------ | -------------------------------------- |
| `Icon.jxl`    | [Icon](#icon)      | Icon for the game in 1:1 aspect ratio. |
| `BannerH.jxl` | [BannerH](#banner) | Horizontal banner for the game.        |
| `BannerV.jxl` | [BannerV](#banner) | Vertical banner for the game.          |

### Minimal Example

!!! note "Some Fields are Made Up, for Completeness"

```toml
Id = "SonicHeroes"
Name = "Sonic Heroes"
BadHashDescription = "Mods target the NoCD version of Sonic Heroes; specifically the Reloaded release. That said, any NoCD version with removed SafeDisc DRM should work, including Sega's own Sonic PC Collection."
ReferenceFiles = [
    "dvdroot/advertise/E/adv_title.one"
]

[[Versions]]
Hash = "8ac32285128d165e011860da2234f9d1"
ExeName = "tsonic_win.exe"
Version = "1.0.0.1"
Date = 2004-10-18T08:15:02Z

[[OtherBinaries]]
Hash = "9ef04af103c974659a01310c7c7013eb"
ExeName = "launcher.exe"
Version = "1.0.0.1"
Date = 2004-10-18T06:51:29Z
SuggestedExecutable = "tsonic_win.exe"
Message = "This executable is the launcher for this game. Would you like to select {SuggestedExecutable} instead?"

[[ModSourceInformation]]
GameBanana = { Id = 6061 }

[[Diagnostics]]
Message = "Your game folder contains ThirteenAG's old Legacy WidescreenFix. You might experience a crash in Special Stage 4 and some other mods.\n\nWorkaround:\n- Delete `scripts/SonicHeroes.WidescreenFix.asi`\n- Download Heroes Graphics Essentials."

[[Diagnostics.Items]]
Hash = "abcdefabcdefabcdefabcdefabcdefab"
FilePath = "scripts/SonicHeroes.WidescreenFix.asi"
```

!!! note "Note: Better examples are welcome!"

### Version

!!! info "Stores individual version information for a binary with a given hash."

| Type     | Item    | Description                                          |
| -------- | ------- | ---------------------------------------------------- |
| string   | Hash    | Hash of executable. (XXH128)                         |
| string   | ExeName | Name of executable.                                  |
| string   | Version | [Optional] Version of game bound to this executable. |
| DateTime | Date    | [Optional] Date of this version, as ISO 8601.        |

This version and their time are supposed to be purely informative.

Ideally the `Version` field should stick to official version names (if available). Otherwise use the
date of the release as the version.

!!! warning

    In cases where a game significantly differs after a update to the point where handling it using existing mods
    is not possible (e.g. 32bit -> 64bit + changed file formats); you should make a new entry for the game in the repository,
    e.g. `Persona 4 Golden 64-bit`, rather than adding a new version.

### Other Binaries

!!! info "Structure type is `OtherBinary` and it extends from [Version](#version)"

| Type   | Item                | Description                                |
| ------ | ------------------- | ------------------------------------------ |
| string | Message             | Message to display for this executable.    |
| string | SuggestedExecutable | Relative path of the suggested executable. |

Example:

```toml
[[OtherBinaries]]
Hash = "9ef04af103c974659a01310c7c7013eb"
ExeName = "launcher.exe"
Version = "1.0.0.1"
Date = 2004-10-18T06:51:29Z
SuggestedExecutable = "tsonic_win.exe"
Message = "This executable is the launcher for this game. Would you like to select {SuggestedExecutable} instead?"
```

### ReferenceFiles

!!! info "Here we can add 1 or more files that are unique to this game."

The intent of this field is to disambiguate games that share the same executable name.

For example if two games have `Engine.exe`, AND `Engine.exe` does not have a known hash, we can use 
this field to disambiguate the two games.

!!! tip "Prefer longer file paths, to game files unlikely to change between updates."

```toml
# Sonic Heroes' Title Screen File
ReferenceFiles = [
    "dvdroot/advertise/E/adv_title.one"
]
```

### Icon

!!! info "Stores path relative to folder `App.toml` is stored in."

!!! info "Images use JPEG XL (`.jxl`)."

    Images in other supported formats will be auto converted.

!!! info "Should be a multiple of `128x128`. Recommended `512x512`."

### Banner

!!! info "Stores path relative to folder `App.toml` is stored in."

!!! info "Images use JPEG XL (`.jxl`)."

    Images in other supported formats will be auto converted.

!!! info "BannerV: Use `600x900` or a multiple of this resolution."

!!! info "BannerH: Use `920x430` or a multiple of this resolution."

We use the Steam resolutions for `BannerV` and `BannerH`, and official Steam assets when possible.

Mod manager can choose to display either, or not use any at all.

### Store Information

| Type          | Item                      | Description                                   |
| ------------- | ------------------------- | --------------------------------------------- |
| EAGameInfo    | [EADesktop](#ea-desktop)  | Contains EA Desktop related information.      |
| EpicGameInfo  | [Epic](#epic-games-store) | Contains Epic Game Store related information. |
| GogGameInfo   | [Gog](#gog)               | Contains EA Desktop related information.      |
| SteamGameInfo | [Steam](#steam)           | Contains Steam related information.           |
| XboxGameInfo  | [Xbox](#xbox)             | Xbox Game Pass information.                   |

Supported stores are based on [GameFinder][gamefinder] library.

#### EA Desktop

!!! failure "[Given how hard they are trying to stop you from finding out where your games are installed by using military grade SHA3-256 encryption][ea-desktop-docs]; changes here might be needed someday."

| Type   | Item       | Description                                               |
| ------ | ---------- | --------------------------------------------------------- |
| string | SoftwareID | Unique ID for this game used in 'EA Desktop' application. |

#### Epic Games Store

!!! warning "It is unconfirmed whether this is the best item to use, this may still be changed."

| Type   | Item          | Description                     |
| ------ | ------------- | ------------------------------- |
| string | CatalogItemId | Unique ID in catalog for 'EGS'. |

#### GOG

!!! tip "You can use the [GOG Database][gog-db] to look up these IDs."

| Type | Item | Description                            |
| ---- | ---- | -------------------------------------- |
| long | ID   | Unique ID for this game used in 'GOG'. |

#### Steam

!!! tip "You can use the [SteamDB][steamdb] to look up these IDs."

| Type   | Item          | Description                     |
| ------ | ------------- | ------------------------------- |
| string | CatalogItemId | Unique ID in catalog for 'EGS'. |

#### Xbox

| Type   | Item | Description                                                                                   |
| ------ | ---- | --------------------------------------------------------------------------------------------- |
| string | ID   | Unique ID. Corresponds to [Package.Identity.Name in AppxManifest.xml][appx-manifest-identity] |

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

!!! tip "In the Nexus API this ID is usually referred to as the `Domain`."

### Diagnostics

!!! info "Games can use the [File Based Diagnostics System][diagnostics] to perform general purpose diagnostics."

### Bad Hash Message

!!! info "This message is displayed if user specifies 'I 100% want this game', but no EXE hash is matched."

In some rare cases, the user may be using a modified EXE, or an unknown version of the game.

If this is the case, we simply provide a message to the user via the `BadHashMessage` field.

## File Layout

!!! note "The folder names under the `Apps` folder are named after the IDs."

```
.
└── Apps
    ├── SonicHeroes
    │   ├── App.toml
    │   ├── BannerH.jxl
    │   ├── BannerV.jxl
    │   └── Icon.jxl
    └── SonicRiders
        ├── App.toml
        ├── BannerH.jxl
        ├── BannerV.jxl
        └── Icon.jxl
```

## Building The Repository

!!! info "The raw files specified in [schema](#schema) go through a 'build' process."

The result of the 'build' is the following:

```
.
├── Apps
│   ├── SonicHeroes
│   │   ├── App.msgpack.zst
│   │   ├── BannerH.jxl
│   │   ├── BannerV.jxl
│   │   └── Icon.jxl
│   └── SonicRiders
│       ├── App.msgpack.zst
│       ├── BannerH.jxl
│       ├── BannerV.jxl
│       └── Icon.jxl
└── Index.msgpack.zst
```

A new file is produced:

- [Index](#index) for searching games & metadata.

### Compression

!!! info "Files on the Index are packed with MessagePack and compressed using ZStandard."

It's expected most games will fit under 1 disk block, so 4096 bytes.

And ideally, under 1 packet, so under 1280 bytes.

### Caching

!!! info "Received data should be cached by the client."

To minimize bandwidth usage, any file from the community repository should be cached by the client.

The data is generally expected to be stale, however in the event of game updates, it's expected that
the user receives any updates immediately.

Therefore, we will use `ETag`(s) to cache the index if possible.

### Index

!!! info "The Index contains serialized dictionaries responsible for quick lookup of individual games."

| Type                                   | Item       | Description                                      |
| -------------------------------------- | ---------- | ------------------------------------------------ |
| Dictionary&lt;string, IndexItem[]&gt;  | ExeToApps  | Maps game `.exe` file to App.                    |
| Dictionary&lt;string, IndexItemp[]&gt; | HashToApps | Maps game `.exe` hash to App.                    |
| HashEntry[]                            | Hashes     | A listing of all files and corresponding hashes. |

#### HashEntry

`HashEntry` is defined as:

| Type   | Item     | Description                                              |
| ------ | -------- | -------------------------------------------------------- |
| string | Hash     | Hash of the file (XXH128)                                |
| string | FilePath | Relative path to the root folder containing Hashes file. |

#### IndexItem

`IndexItem` is defined as:

| Type   | Item     | Description                                                       |
| ------ | -------- | ----------------------------------------------------------------- |
| string | AppName  | User friendly name for the game.                                  |
| string | FilePath | Relative path to this `.toml` file to the game [Schema](#schema). |

Note that there can be cases where there may be duplicates. In terms of `ExeToApps` it's quite
obvious, but in terms of `HashToApps` it's less so. In some rare cases of game engines, it's 
technically possible to reuse the EXE, if it's just some bootstrapper to the proper DLL etc. 
containing the code.

On the other hand, the `ExeToApps` field is for handling unknown game versions. In those cases,
a user will manually select their intended game.

In case of duplicates, they will be auto resolved using the [ReferenceFiles](#referencefiles).

!!! note "In super rare case of unresolvable duplicates, the user will be prompted to select the correct game."

## Hosting

!!! info "Initially the Community Repository will be hosted on [GitHub Pages][github-pages]."

With caching of assets on the end user's side.

Then, if we ever find we're serving too much traffic, we will self
host the repository.

The repository is set up in such a way that any HTTP server with downloads can host it.

<!-- Links -->
[app-metadata]: ../Server/Configurations/App-Metadata.md
[app-metadata-id]: ../Server/Configurations/App-Metadata.md#id
[appx-manifest-identity]: https://learn.microsoft.com/en-us/uwp/schemas/appxpackage/uapmanifestschema/element-identity
[ea-desktop]: https://www.ea.com/en-gb/news/ea-app
[ea-desktop-docs]: https://github.com/erri120/GameFinder/wiki/EA-Desktop
[gamefinder]: https://github.com/erri120/GameFinder
[github-pages]: https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages
[gog-db]: https://www.gogdb.org/
[mod-metadata]: ../Server/Configurations/Mod-Metadata.md
[reloaded-community]: https://github.com/Reloaded-Project/Reloaded.Community
[steamdb]: https://steamdb.info/
[diagnostics]: ../Server/Diagnostics.md#file-based-diagnostics