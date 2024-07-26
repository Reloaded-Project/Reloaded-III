# Community Repository

!!! info "About the Community Repository"

    This allows us to provide real-time updates for per-game specific information without explicitly having to recompile the mod loader/server/manager.

!!! note "This documents a future iteration of [Reloaded.Community][reloaded-community] repository."

## About

The `Community Repository` contains game-specific information for the Reloaded3 backend server.

The idea is we can update the information we know about various games without ever having to update the actual server itself. This is sometimes called 'out of band' information.

Some use cases include:

- Automatically registering GameBanana/Nexus/GitHub download sources.
- Helping automatic detection of games installed via Steam/Epic/Origin etc.
- Providing compatibility warnings for pre-patched/pre-modded legacy games.
- Informing user of wrong game binary. (e.g. User has EU EXE but mods target US)
- Auto assign Game IDs in [Application Configurations][game-metadata].
- Updating [Mod Configurations][mod-metadata] with correct [Game ID][game-metadata-id]s marking which games a mod supports.
- Providing SteamGridDB IDs for game icons and banners.

## Schema

!!! note "This represents the schema of games the individual users add to the repo manually."

All configurations are written as TOML (for editing convenience).

They can have any name (as long as they use their own unique folder), in this spec we will refer to them as `App.toml`.

| Type                      | Item                                                          | Description                                                                                      |
| ------------------------- | ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| string                    | [Id][game-metadata]                                           | Unique identifier for this game. Copied to [Game Id][game-metadata].                             |
| string                    | Name                                                          | User-friendly name for the game, e.g. 'Sonic Heroes'. Copied to [Game Name][game-metadata-name]. |
| Version[]                 | [Versions](#version)                                          | Versions of the executable.                                                                      |
| OtherBinary[]             | [OtherBinaries](#other-binaries)                              | Stores information about other executables in game folder you probably don't wanna mod.          |
| StoreInfo                 | [StoreInformation](#store-information)                        | Game store specific information.                                                                 |
| ModSourceInfo             | [ModSourceInformation](#mod-source-information)               | Mod source (Nexus/GameBanana/OtherModSite) specific information.                                 |
| Diagnostic[]              | [Diagnostics](#diagnostics)                                   | Diagnostics to display based on game's current folder state.                                     |
| string                    | [BadHashMessage](#bad-hash-message)                           | Message to display if the user has a bad EXE hash.                                               |
| u32                       | [SteamGridDBGameId](#obtain-a-steamgriddb-id)                 | Unique Game ID from SteamGridDB API. Optional.                                                   |
| SteamGridDBCategoryAndId? | [SteamGridDBIcon](#icons-and-banners-steamgriddb)             | SteamGridDB category and ID for the game's icon. Optional.                                       |
| SteamGridDBCategoryAndId? | [SteamGridDBBannerSquare](#icons-and-banners-steamgriddb)     | SteamGridDB category and ID for the game's app grid square. Optional.                            |
| SteamGridDBCategoryAndId? | [SteamGridDBBannerHorizontal](#icons-and-banners-steamgriddb) | SteamGridDB category and ID for the game's horizontal banner. Optional.                          |
| SteamGridDBCategoryAndId? | [SteamGridDBBannerVertical](#icons-and-banners-steamgriddb)   | SteamGridDB category and ID for the game's vertical banner. Optional.                            |
| Task[]                    | [Tasks](#tasks)                                               | Various maintenance tasks and executables to run for the game.                                   |

!!! note "All hashes listed in this page are `XXH3_128bits` (XXH128) unless specified otherwise."

    For more details, see the page on [Hashing Page][hashing].

!!! note "Not all of this information has to be hand typed, some information such as version numbers, hashes, dates can be automatically extracted."

### Minimal Example

!!! note "Some Fields are Made Up, for Completeness"

```toml
Id = "SonicHeroes"
Name = "Sonic Heroes"
BadHashDescription = "Mods target the NoCD version of Sonic Heroes; specifically the Reloaded release. That said, any NoCD version with removed SafeDisc DRM should work, including Sega's own Sonic PC Collection."

[[Versions]]
ID = 0
Hash = "8ac32285128d165e011860da2234f9d1"
ExeName = "tsonic_win.exe"
Version = "1.0.0.1"
Date = 2004-10-18T08:15:02Z

[[OtherBinaries]]
ID = 1
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

# Icons to Use
[SteamGridDBIcon]
Category = "Icon"
Id = 1393

[SteamGridDBBannerSquare]
Category = "Grid"
Id = 162786

[SteamGridDBBannerHorizontal]
Category = "Grid"
Id = 78140

[SteamGridDBBannerVertical]
Category = "Grid"
Id = 78138

# Pretend the title was on some stores.
[StoreInformation.Steam]
SteamAppId = 71340

[StoreInformation.Gog]
Id = 1705545557
```

!!! note "Note: Better examples are welcome!"

### Version

!!! info "Stores individual version information for a binary with a given hash."

| Type          | Item                            | Description                                                                      |
| ------------- | ------------------------------- | -------------------------------------------------------------------------------- |
| u32           | ID                              | Unique number for this version entry within a `Game`.                            |
| string        | Hash                            | Hash of executable. (XXH128)                                                     |
| string        | ExeName                         | Name of executable.                                                              |
| string        | FriendlyName                    | Friendly name for this game version. e.g. `1.0.1 (GOG)`.                         |
| DateTime      | Date                            | Date of this version, as ISO 8601.                                               |
| ReferenceFile | [ReferenceFile](#referencefile) | [Optional] Unique reference file and hash for this specific version of the game. |
| StoreVersion  | [StoreInfo](#storeinfo)         | Store-specific information for this game version.                                |

The `ID` is a unique integer for each entry, ideally incrementing from 0.
It should never be changed. This allows for changing other information on
the struct without breaking existing references to it

This `FriendlyName` and `Date` are purely informative. (For Launcher UIs etc.)

Ideally the `FriendlyName` field should stick to official version names (if available).
Include the store name in the brackets e.g. `(GOG)` if the code differs between stores.

#### StoreInfo

!!! note "Ignore this for legacy games from before the era of digital distribution."

The `StoreInfo` field is an optional field that contains store-specific information
for each game version.

It is defined as follows:

| Type                      | Item      | Description                              |
| ------------------------- | --------- | ---------------------------------------- |
| [(StoreType)][store-type] | StoreType | The store from which the game came from. |

**GOG Specific Fields**:

| Type | Item       | Description                                                                                           |
| ---- | ---------- | ----------------------------------------------------------------------------------------------------- |
| u64  | GogBuildId | [GOG Only] The [unique identifier for the build][gog-buildid]. Only applicable when `Store` is `GOG`. |

**Steam Specific Fields**:

| Type   | Item                | Description                                                                                                      |
| ------ | ------------------- | ---------------------------------------------------------------------------------------------------------------- |
| u64    | SteamDepotId        | [Steam Only] The Steam depot ID. Only applicable when `Store` is `Steam`.                                        |
| u64    | SteamManifestId     | [Steam Only] The Steam manifest ID. Only applicable when `Store` is `Steam`.                                     |
| string | SteamBranch         | [Steam Only] The Steam branch name. Only applicable when `Store` is `Steam`.                                     |
| string | SteamBranchPassword | [Steam Only] The password for the Steam branch (if password-protected). Only applicable when `Store` is `Steam`. |

**Epic Specific Fields**:

| Type   | Item                 | Description                                                                                 |
| ------ | -------------------- | ------------------------------------------------------------------------------------------- |
| string | EpicAppVersionString | [Epic Only] The version string of the game on Epic. Only applicable when `Store` is `Epic`. |

**Microsoft Specific Fields**:

| Type   | Item                    | Description                                                                                                                                      |
| ------ | ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| string | MicrosoftPackageVersion | [Microsoft Only] The version of the game package on the Microsoft Store, from the `Identity` field. Only applicable when `Store` is `Microsoft`. |

Example:

```toml
[Versions.StoreVersion]
Store = "Steam"
SteamDepotId = 1234567890
SteamManifestId = 9876543210
SteamBranch = "beta"
SteamBranchPassword = "secretpassword"
```

#### ReferenceFile

Specifies a unique reference file and hash.

| Type    | Item         | Description                                             |
| ------- | ------------ | ------------------------------------------------------- |
| string  | RelativePath | Path to the reference file relative to the game folder. |
| string? | Hash1M       | Hash of the first 1MB bytes of file. (XXH128)           |
| string  | Hash         | Hash of the reference file. (XXH128)                    |

This allows disambiguating between different versions of a game that may share the same executable.
For example, when the executable is a stub that loads main game code from a DLL.

```toml
ReferenceFile = { RelativePath = "dvdroot/advertise/E/adv_title.one", Hash = "986cc4f000fb530245f44c7b49206628" }
```

!!! tip "Choose a file that is short, exists in all game versions, and is unique to this version."

!!! tip "Prefer using same file across all version entries if possible."

!!! tip "Hash1M can be used as a speedup if game only has big files."

    For example 2GB archives.<br/>
    Consider files over 10MB to be a decent threshold for using this, as we also have to account
    for the likes of hard drives.

### Other Binaries

!!! info "Structure type is `OtherBinary` and it extends from [Version](#version)"

| Type   | Item                | Description                                |
| ------ | ------------------- | ------------------------------------------ |
| string | Message             | Message to display for this executable.    |
| string | SuggestedExecutable | Relative path of the suggested executable. |

Example:

```toml
[[OtherBinaries]]
ID = 1
Hash = "9ef04af103c974659a01310c7c7013eb"
ExeName = "launcher.exe"
Version = "1.0.0.1"
Date = 2004-10-18T06:51:29Z
SuggestedExecutable = "tsonic_win.exe"
Message = "This executable is the launcher for this game. Would you like to select {SuggestedExecutable} instead?"
```

This gives the user a yes/no prompt. If they select 'yes', the `SuggestedExecutable` is used instead.

### Icons and Banners (SteamGridDB)

!!! info "Technical Note (Icon)"

    **Aspect ratio**: 1:1. <br/>
    **Expected Resolution**: `256x256`. (4K Display ✅) <br/>
    **Preferred Resolution**: `512x512`. (8K Display ✅) <br/>
    **Expected Size @ `256x256`**: ~60KiB. <br/>
    **Format**: [JPEG XL][images]. <br/>

!!! info "Technical Note (Banner Square)"

    **Aspect ratio**: 1:1. <br/>
    **Expected Resolution**: `512x512`. (4K Display ✅) <br/>
    **Preferred Resolution**: `1024x1024`. (8K Display ✅) <br/>
    **Expected Size @ `512x512`**: ~120KiB. <br/>
    **Format**: [JPEG XL][images]. <br/>

!!! info "Technical Note (BannerV)"

    **Aspect ratio**: 2:3. <br/>
    **Expected Resolution (BannerV)**: `600x900`. (4K Display ✅) <br/>
    **Expected Size @ `600x900`**: ~210KiB.<br/>
    **Format**: [JPEG XL][images].<br/>

!!! info "Technical Note (BannerH)"

    **Aspect ratio**: 92:43. <br/>
    **Expected Resolution (BannerV)**: `920x430`. (4K Display ✅) <br/>
    **Expected Size @ `920x430`**: ~180KiB. <br/>
    **Format**: [JPEG XL][images]. <br/>

!!! question "Where is are these images used?"

    All resolutions listed target 96 DPI and reference 1st party launcher.
    So for 4K, double the resolution.

    **Icons (1:1)**:

      - 48x48 in Windows Desktop Shortcut
      - 96x96 in Spine
      - 100x100 in Gnome 3 Shortcut (All Apps View)

    **BannerSquare (1:1)**:

      - 192x192 in Game Grid (Default)
      - 256x256 in Game Grid (Larger)

    **BannerH (92:43)**:

      - 460x215 App View (Grid Horizontal)

    **BannerV (2:3)**:

      - 300x450 App View (Grid Vertical)

The `SteamGridDbCategoryAndId` struct is defined as follows:

| Type                | Item     | Description                            |
| ------------------- | -------- | -------------------------------------- |
| SteamGridDbCategory | Category | 0 = Grid, 1 = Hero, 2 = Logo, 3 = Icon |
| u32                 | Id       | ID of this specific entry.             |

If an icon is specified, the launcher will contact the [Reloaded Central Server][reloaded-central-server]
to fetch the image from SteamGridDB using the provided category and ID.

If not specified (null), the launcher will attempt to fetch the first image tagged as `official`
in style from SteamGridDB.

If there is no internet connection, the launcher will default to extracting the app icon from the
game's executable for the icon, reuse that for `Square Banner` and use a placeholder for
the `Horizontal` and `Vertical` banners.

!!! note "Relevant Game & Loadout Setting [GridDisplayMode][grid-display-mode]"

!!! tip "[Fetching assets from SteamGridDB][steam-grid-db-docs]"

#### Obtain a SteamGridDB ID

Look at the URL, for example:

- **Game**: `https://www.steamgriddb.com/game/38740`
- **Grid**: `https://www.steamgriddb.com/grid/196080`

It's the number at the end.

### Store Information

| Type          | Item                      | Description                                   |
| ------------- | ------------------------- | --------------------------------------------- |
| EAGameInfo    | [EADesktop](#ea-desktop)  | Contains EA Desktop related information.      |
| EpicGameInfo  | [Epic](#epic-games-store) | Contains Epic Game Store related information. |
| GogGameInfo   | [Gog](#gog)               | Contains EA Desktop related information.      |
| SteamGameInfo | [Steam](#steam)           | Contains Steam related information.           |
| XboxGameInfo  | [Xbox](#xbox)             | Xbox Game Pass information.                   |

Supported stores are based on [GameFinder][gamefinder] library.

This information is used to link up locally installed games with the community repository.

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
| u64  | ID   | Unique ID for this game used in 'GOG'. |

#### Steam

!!! tip "You can use the [SteamDB][steamdb] to look up these IDs."

| Type | Item       | Description                  |
| ---- | ---------- | ---------------------------- |
| u64  | SteamAppId | Unique ID for game in Steam. |

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
| u32  | Id   | Unique identifier for game, e.g. 6061 for https://gamebanana.com/games/6061 |

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

### Tasks

!!! info "Games can define additional tasks in the Community Repository."

The `Tasks` field is an optional array of `Task` objects that represent additional tasks or
actions that can be performed for the game.

For detailed information about the structure and fields of a `Task` object, please refer to
the [Tasks][tasks] page.

**Example:**

```toml
[[Tasks]]
Type = "File"
VisualHint = "Settings"
Name = "Configuration Tool"
GroupNames = ["Community"]
Description = "Launches the configuration program."
Path = "Config2_DX9.exe"
IsPrimary = false
InjectLoader = false
IsHidden = false
Platform = 0
```

The tasks defined in the Community Repository will be merged with the tasks defined for the game
locally, with the local tasks taking precedence in case of conflicts.

## File Layout

!!! note "The folder names under the `Apps` folder are named after the IDs."

```
.
└── Apps
    ├── SonicHeroes
    │   └── App.toml
    └── SonicRiders
        └── App.toml
```

## Building The Repository

!!! info "The raw files specified in [schema](#schema) go through a 'build' process."

The result of the 'build' is the following:

```
.
├── Apps
│   ├── SonicHeroes
│   │   └── App.msgpack
│   └── SonicRiders
│       └── App.msgpack
└── Index.msgpack
```

The files are converted to `MessagePack` format and a new file is produced:

- [Index](#index) for searching games & metadata.

### Index

!!! info "The Index contains serialized dictionaries responsible for quick lookup of individual games."

| Type                                  | Item       | Description                                      |
| ------------------------------------- | ---------- | ------------------------------------------------ |
| Dictionary&lt;string, IndexItem[]&gt; | ExeToApps  | Maps game `.exe` file to App.                    |
| Dictionary&lt;XXH128, IndexItem[]&gt; | HashToApps | Maps game `.exe` hash to App.                    |
| HashEntry[]                           | Hashes     | A listing of all files and corresponding hashes. |

#### HashEntry

`HashEntry` is defined as:

| Type   | Item     | Description                                              |
| ------ | -------- | -------------------------------------------------------- |
| XXH128 | Hash     | Hash of the file (XXH128)                                |
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

In case of duplicates, they will be auto resolved using the [ReferenceFile](#referencefile).

!!! note "In super rare case of unresolvable duplicates, the user will be prompted to select the correct game."

## Hosting

!!! info "The Community Repository will be hosted on [GitHub Pages][github-pages]."

    Because this makes life easier, we will build the Repo with GitHub Actions.

The [built repository](#building-the-repository) will be compressed into an `.nx` archive and
uploaded as a sole file to pages. Named `CommunityRepository.nx`.

Because this data is very small and stale, it's expected that most of the time a user will already
have the latest version.

### Caching

!!! info "See [Locations/Server Cache Files][server-cache-files-communityrepo] for details"

### Bandwidth Numbers

!!! info "GitHub pages sites are soft limited to [100GB of bandwidth per month][pages-limits]."

Expected sizes:

- `30KB`: Index.msgpack.zst (~100 games)
- `1KB`: App.msgpack.zst (per game)

For 100 games, therefore expect `130KB`.
This makes for around 770,000 queries per month.

If we ever get notified from GitHub about bandwidth usage, we will migrate this to
[Central Server][reloaded-central-server].

<!-- Links -->
[game-metadata]: ../Server/Storage/Games/About.md#whats-inside-an-game-configuration
[game-metadata-name]: ../Server/Storage/Games/About.md#whats-inside-an-game-configuration
[game-metadata-id]: ../Server/Storage/Games/About.md#whats-inside-an-game-configuration
[appx-manifest-identity]: https://learn.microsoft.com/en-us/uwp/schemas/appxpackage/uapmanifestschema/element-identity
[diagnostics]: ../Server/Diagnostics.md#file-based-diagnostics
[ea-desktop]: https://www.ea.com/en-gb/news/ea-app
[ea-desktop-docs]: https://github.com/erri120/GameFinder/wiki/EA-Desktop
[gamefinder]: https://github.com/erri120/GameFinder
[github-pages]: https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages
[gog-db]: https://www.gogdb.org/
[hashing]: ../Common/Hashing.md
[mod-metadata]: ../Server/Packaging/Configurations/Mod-Metadata.md
[pages-limits]: https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages#usage-limits
[reloaded-community]: https://github.com/Reloaded-Project/Reloaded.Community
[steamdb]: https://steamdb.info/
[images]: ../Common/Images.md
[grid-display-mode]: ../Server/Storage/Loadouts/File-Format/DataTypes.md#griddisplaymode
[steam-grid-db-docs]: ../Research/External-Services/SteamGridDB.md
[reloaded-central-server]: ./Central-Server.md
[stores-bin]: ../Server/Storage/Loadouts/About.md#storesbin
[gog-buildid]: ../Server/Storage/Loadouts/Stores/GOG.md#retrieving-available-game-versions
[store-type]: ../Server/Storage/Loadouts/File-Format/DataTypes.md#storetype
[server-cache-files-communityrepo]: ../Server/Storage/Locations.md#community-repository
[tasks]: ../Server/Storage/Games/Tasks.md