# Package Metadata

!!! info "Describes items common in all Reloaded3 packages"

Inside each package folder is a file named `package.toml`; which stores the metadata of each package.

| Type              | Name                                     | Description                                                               |
| ----------------- | ---------------------------------------- | ------------------------------------------------------------------------- |
| string            | [Id](#id)                                | A name that uniquely identifies the package.                              |
| string            | Name                                     | Human friendly name of the package.                                       |
| string            | Author                                   | Main author of the package. (Individual or Team Name)                     |
| string            | Summary                                  | Short summary of the package. Max 2 sentences.                            |
| PackageType       | [PackageType](#packagetype)              | Type of the package. See [PackageType](#packagetype) for possible values. |
| string            | [DocsFile](#docsfile)                    | [Optional] Entry point for this package documentation.                    |
| SemVer            | [Version](#version)                      | Semantic versioning version of the package.                               |
| bool              | [IsDependency](#is-dependency)           | This package is a dependency (e.g. library) and not directly consumable.  |
| string            | LicenseId                                | [SPDX License Identifier][spdx-license]                                   |
| string[]          | [Tags](#tags)                            | Used to make searching easier within mod managers.                        |
| Credit[]          | [Credits](#credits)                      | [Optional] Stores information about who contributed what to the project.  |
| string?           | SourceUrl                                | [Optional] Link to source code (if applicable).                           |
| string?           | ProjectUrl                               | [Optional] Link to website to learn more about the project.               |
| UpdateData        | [UpdateData](#update-data)               | Stores package specific update information.                               |
| DependencyInfo[]  | [Dependencies](#dependency-info)         | Stores information about this package's dependencies.                     |
| DateTime          | [Published](#published)                  | The time when this package was packed.                                    |
| StoragePreference | [StoragePreference](#storage-preference) | Specifies the preferred storage tier for the package.                     |

These fields are usually only found when [PackageType](#packagetype) == `Mod`:

| Type                                                      | Name                                          | Description                                                                                     |
| --------------------------------------------------------- | --------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| GalleryItem[]                                             | [Gallery](#gallery)                           | Stores preview images for this package.                                                         |
| Dictionary&lt;string, Dictionary&lt;string,string&gt;&gt; | [Targets](#targets)                           | Specifies the settings [for each backend.][backend]                                             |
| string[]                                                  | [SupportedGames](#supported-games)            | List of supported titles/games.                                                                 |
| bool                                                      | [ClientSide](#client-side)                    | [Optional] True if the mod is purely cosmetic and does not have non-visual effects on gameplay. |
| bool                                                      | [AllowRuntimeLoading](#allow-runtime-loading) | [Optional] Allows the mod to be loaded in real-time at runtime, instead of only on startup.     |

These fields are usually only found when [PackageType](#packagetype) == `Tool`:

| Type         | Name                         | Description                                          |
| ------------ | ---------------------------- | ---------------------------------------------------- |
| Task[]       | [Tasks][tasks]               | List of binaries that the `tool` package ships with. |
| ConfigFile[] | [ConfigFiles](#config-files) | List of configuration files synced with Reloaded-II. |

## Implicit Fields

Some items are stored as separate files:

- [license][license]: License file, located in `package/license.md`.
    - This is used if `LicenseId` is not specified.
- [changelog][changelog]: Changelog file(s), located in `package/changelog/*.md`.
- [description][description]: Description file, located in `package/description.md`.
- [config][config]: Configuration schema for the package, located in `config.toml`.

## Example Config

!!! note "Any links, IDs here are sample data and not real."

Example [game support mod][game-support].

```toml
Id = "reloaded3.gamesupport.persona5royal.s56"
Name = "Persona 5 Royal Support"
Summary = "Provides Essential Functionality for Persona 5 Royal."
Author = "Sewer56"
PackageType = "Mod"
DocsFile = "index.html"
Version = "1.0.1"
Tags = ["Utility", "Library"]
SourceUrl = "https://github.com/Sewer56/persona5royal.modloader"
ProjectUrl = "https://sewer56.dev/persona5royal.modloader/"
Published = 2023-06-08T12:34:56Z
ClientSide = false

# Mod Fields
Icon = "icon.jxl"
IsLibrary = false
SupportedGames = ["game1", "game2"]

[[Credits]]
Name = "Sewer56"
Role = "Main Developer"
Url = "https://github.com/Sewer56"

[[Credits]]
Name = "AnimatedSwine37"
Role = "BF Emulator & Maintenance"
Url = "https://github.com/AnimatedSwine37"

[[Credits]]
Name = "LTSophia"
Role = "PAK Merging"
Url = "https://github.com/LTSophia"

[[Credits]]
Name = "SecreC"
Role = "SPD Merging Support"
Url = "https://github.com/Secre-C"

[[Credits]]
Name = "berkayfeci"
Role = "GamePass EXE Detection"
Url = "https://github.com/berkayfeci"

[[Credits]]
Name = "SirGamers"
Role = "Adding Missing Features to Documentation"
Url = "https://github.com/SirGamers"

[[Credits]]
Name = "Atlus"
Role = "Original Game Developer"

[UpdateData]
[UpdateData.GameBanana]
ItemType = "Mod"
ItemId = 408376

[UpdateData.GitHub]
UserName = "Sewer56"
RepositoryName = "reloaded3.gamesupport.persona5royal"

[UpdateData.Nexus]
GameDomain = "persona5"
Id = 789012

[UpdateData.NuGet]
DefaultRepositoryUrls = [
   "http://packages.sewer56.moe:5000/v3/index.json"
]
AllowUpdateFromAnyRepository = false

[[Dependencies]]
Id = "reloaded3.utility.reloadedhooks.s56"
Name = "Reloaded3 Hooking Library"
Author = "Sewer56"
[Dependencies.UpdateData]
[Dependencies.UpdateData.GitHub]
UserName = "Reloaded-Project"
RepositoryName = "reloaded3.utility.reloadedhooks"

[[Dependencies]]
Id = "reloaded3.utility.sigscan.s56"
Name = "Reloaded3 Signature Scanning Library"
Author = "Sewer56"
[Dependencies.UpdateData]
[Dependencies.UpdateData.GitHub]
UserName = "Reloaded-Project"
RepositoryName = "reloaded3.utility.sigscanrs"

[[Dependencies]]
Id = "reloaded3.api.crimiddleware.filesystemv2.modloader.s56"
Name = "CRI File System V2 Mod Loader"
Author = "Sewer56"
[Dependencies.UpdateData]
[Dependencies.UpdateData.GitHub]
UserName = "Sewer56"
RepositoryName = "reloaded3.api.crimiddleware.filesystemv2.modloader"

# Mod Structs
[[Gallery]]
FileName = "screenshot1.jxl"
Caption = "Gameplay screenshot 1"

[[Gallery]]
FileName = "screenshot2.jxl"
Caption = "Gameplay screenshot 2"

[Targets]
[Targets."win"]
any = "reloaded3.gamesupport.persona5royal.dll"
# x86, x64, x64-v2 and x64-v3 etc. will automatically be generated during packaging of relevant package.
# x64-v2 = "reloaded3.gamesupport.persona5royal.dll"
# x64-v3 = "reloaded3.gamesupport.persona5royal.dll"
```

## Id

!!! info "A name that uniquely identifies the package."

!!! warning "Must be a valid Windows & Unix file name."

This format is designed to minimize collisions while providing a human-readable name.

The suggested format to use for names is `game.type.subtype.name.author.target`.

- `game` see [Game 'Id'][game-metadata-id] for more info.
- `type` name should ideally match category of the package on a site like [GameBanana][gamebanana] or [NexusMods][nexus-mods].
- `subtype` [Optional] provides additional information about the item.
- `name` unique name for the package. Can use another `.` dot if additional info is needed.
- `author` primary package author (prefer abbreviated).
- `target` [Optional] target platform and instruction set, can come in one of the following forms
    - [Platform][platforms] only: `win`, `linux`. When package has all architecture binaries.
    - [Platform][platforms]+[Arch][architecture]: `win+x64-v3`, `linux+x64-v3`. When package has only one specific architecture.

Example(s):

- No Subtype: `sonicheroes.skins.seasidehillmidnight.s56`
- With Subtype: `sonicheroes.skins.seasidehill.midnighthill.s56`

Use lowercase, no spaces, no special characters.

!!! tip "The author field may be omitted, if e.g. creating GitHub repositories."

    It's only there to avoid conflicts.

### Architecture Specific Packages

!!! note "The `architecture` field is not usually set by humans."

This field is primarily intended to be used by automated build scripts.

`Build scripts` should amend the original `package.toml` (this file) for each
automatically generated package. Specifically by:

- Setting the [Is Dependency](#is-dependency) field to true.
- Prepending `[Platform]` or `[Platform+Arch]` to the `Name` field.
- Appending the `architecture` part to the [Id](#id) field.
- Updating the [Targets](#targets) field to include the correct architecture (if needed).

!!! warning "***DO NOT*** use architectures be used in [dependency references](#dependency-info)."

  - ✅ `reloaded3.api.windows.vfs.s56`
  - ❌ `reloaded3.api.windows.vfs.s56.win+x64-v3`

!!! note "The `architecture` field is set only by automated build scripts."

    During dependency resolution, the system will try to append the correct architecture.
    If your PC is `win+x64-v3`, it will try searching the package name with `win+x64-v3` appended
    at the end, then it will try searching with `win` appended at the end, until it will search
    with no architecture appended.

### Universal Mods

!!! note

    For mods that are non-game specific such as backends; set the `game` identifier as `reloaded3` and use one of the following.

| Type         | Description                                       | Example                                   |
| ------------ | ------------------------------------------------- | ----------------------------------------- |
| backend      | For [backends][backend].                          | `reloaded3.backend.coreclr.s56`           |
| api          | For [middleware/API hooks][middleware-api-hooks]. | `reloaded3.api.windows.vfs.s56`           |
| game support | For [game support mods][game-support].            | `reloaded3.gamesupport.persona5royal.s56` |
| utility      | For utility mods with reusable code.              | `reloaded3.utility.hooks.s56`             |
| tool         | For non-game specific modding tools.              | `reloaded3.tool.steamlaunchupdater.s56`   |

Server can choose whether to show non game-specific mods (`reloaded3` id) on a specific game's page or not.

### Diagnostics

!!! info "For diagnostics, use the format: `reloaded3server.diagnostic.game.name.author`"

| Type       | Description                     | Example                                                   |
| ---------- | ------------------------------- | --------------------------------------------------------- |
| diagnostic | For [diagnostics][diagnostics]. | `reloaded3server.diagnostic.general.textureoptimizer.s56` |

### Translations

!!! info "For [translations][overriding-translations], append the [language code][language-code] to the package name."

In the form `tl-{code}`.

For example, for the package name `reloaded3server.diagnostic.general`, use the name
`reloaded3server.diagnostic.general.tl-de`.

### Workflows

!!! info "For workflows, use the format: `reloaded3.workflow.game.name.author`"

| Type       | Description                 | Example                                            |
| ---------- | --------------------------- | -------------------------------------------------- |
| diagnostic | For [workflows][workflows]. | `reloaded3.workflow.sonicheroes.addacharacter.s56` |

## PackageType

!!! info "Represents the type of the package."

`PackageType` is an enumerable with the following possible values:

- `Mod` (Default): Stores a game modification.
- `Profile`: Stores user profile.
- `Translation`: Stores a [translation for another package][overriding-translations].
- `Tool`: Represents a modding tool or binary.

This field helps identify the purpose and nature of the package.

!!! warning "TODO: Link the other package type pages when complete."

## DocsFile

!!! info "Stores the documentation entry point in `package/docs` folder."

See [Docs][docs] for more details.

## Version

!!! info "Reloaded Packages use [Semantic Versioning][semantic-versioning]."

    This is required for update support, and consistency.

!!! warning

    For legacy/foreign packages with non-semver versions, we will use `0.0.0.{originalVersion}`.
    Stripping all spaces and/or invalid characters.

## Is Dependency

!!! info "Specifies that this is a package that is not directly consumable by the user."

`Dependency` packages are not directly consumable by the user, and are instead used as dependencies
for other packages. That is to say, you can't enable a 'dependency mod'.

Examples of dependencies include:

- Libraries used by mods at runtime.
- Runtimes, e.g. `.NET Runtime`.

When `mod` packages are distributed as dependencies, they may be hidden from the loadout (profile) view
inside a mod manager; provided it does not have a [configuration][package-configuration].

!!! tip "When a dependency is present that no mod depends on, it can be removed from the system."

    This allows the user to save space on their system.

## Tags

!!! info "Used to make searching within mod managers easier; i.e. `filter by tag`."

These are completely arbitrary, up to end users.

### Mod Tags

The default set of suggested tags include:

| Tag Name     | Description                   |
| ------------ | ----------------------------- |
| GUI/HUD      | Any 2D element on the screen. |
| Stage/Level  | Self explanatory.             |
| Character    | Playable characters.          |
| 3D Model     | Any non-Player 3D model.      |
| Pack         | Compilation of several mods.  |
| Sound Effect | Sound effects.                |
| Music        | Music to enjoy.               |
| Texture      | Texture overhauls.            |
| NSFW         | Not safe for work.            |

## Credits

!!! info "Stores information about who contributed what to the project."

    This field may also include credits to the original devs for ported content,
    and/or any other relevant information.

Each credit uses a `Credit` structure with following fields:

| Type   | Field | Name Description                                    |
| ------ | ----- | --------------------------------------------------- |
| string | Name  | Name of the person or group.                        |
| string | Role  | What the person or group did.                       |
| string | Url   | [Optional] Link to the person's website or profile. |

## Update Data

!!! info

    Information tied to Reloaded3's update library.

    This info is stored in a way that avoids direct dependency on Update library by using an `Abstractions` package.

!!! note

    This section might be moved to dedicated Update library section.

| Type                 | Name                                  | Description                            |
| -------------------- | ------------------------------------- | -------------------------------------- |
| GameBananaUpdateInfo | [GameBanana](#gamebanana-update-info) | Info on how to update from GitHub.     |
| GitHubUpdateInfo     | [GitHub](#github-update-info)         | Info on how to update from GameBanana. |
| NexusUpdateInfo      | [Nexus](#nexus-update-info)           | Info on how to update from Nexus.      |
| NuGetUpdateInfo      | [NuGet](#nuget-update-info)           | Info on how to update from NuGet.      |

### GameBanana Update Info

| Type   | Name     | Description                                                                                                                                           |
| ------ | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| string | ItemType | Type of item on GameBanana API, e.g. 'Mod', 'Sound', 'Wip'                                                                                            |
| int    | ItemId   | Id of the item on GameBanana, this is the last number in the URL to your mod page; e.g. 150115 if your mod URL is https://gamebanana.com/mods/150115. |

### GitHub Update Info

| Type   | Name           | Description                                                                           |
| ------ | -------------- | ------------------------------------------------------------------------------------- |
| string | UserName       | The user/organization name associated with the repository to fetch files from.        |
| string | RepositoryName | The name of the repository to fetch files from.                                       |
| bool   | AssetFileName  | [Optional] Pattern for the file name to download if no metadata file is found.        |
| bool   | UseReleaseTag  | [Optional] If true, uses the release tag to denote version of the package as speedup. |

The field `AssetFileName` is provided for backwards compatibility only. e.g. `*update.zip` will look for any file ending with `update.zip`

### Nexus Update Info

!!! warning "Implementation delayed until API allows non-premium members to generate download links."

| Type   | Name       | Description                               |
| ------ | ---------- | ----------------------------------------- |
| string | GameDomain | The ID/Domain for the game. e.g. 'skyrim' |
| int    | Id         | Unique id for the mod.                    |

### NuGet Update Info

| Type     | Name                  | Description                                        |
| -------- | --------------------- | -------------------------------------------------- |
| string[] | DefaultRepositoryUrls | List of NuGet URLs/repos this mod can update from. |

## Dependency Info

!!! info "The dependency resolution strategy is to simply copy update info of all dependencies into this structure."

    Justification:

    - Helps resolve mods if missing.
    - Ensures user downloads same as mod author used.
        - This improves consistency.
        - And improves overall security.

    We cannot unfortunately guarantee there's only ever 1 mod with a given ID uploaded to a website.
    A malicious attacker could try to upload a mod with an existing ID to 'take over' an existing
    package. We avoid this by ensuring the user downloads the same version as the mod author used.

`DependencyInfo` is defined as:

| Type       | Name                       | Description                             |
| ---------- | -------------------------- | --------------------------------------- |
| string     | Id                         | Unique ID of the dependency.            |
| string     | Name                       | Human friendly name of dependency.      |
| string     | Author                     | Name of the dependency author.          |
| UpdateData | [UpdateData](#update-data) | Stores mod update specific information. |

All of these fields are copied from the dependency packages.

This struct contains only the info needed to locate the dependency, and troubleshoot if a dependency is missing.

## Published

!!! info "This is the time in which the package containing this mod was compressed."

!!! warning "This value is autogenerated when packing file."

This is used to show when the package was last updated in mod managers and other visual applications.

## Storage Preference

!!! info "Specifies the preferred storage tier for the package."

The `StoragePreference` field is an enum that indicates where the package should be stored, based
on the storage speed. It can have the following values:

- `FASTEST`: The package should be stored on the fastest available storage (e.g. SSD).
- `SLOWEST`: The package can be stored on slowest storage (e.g. HDD) without significant performance impact.

The values are represented as integers ranging from 0 to 255, with 0 being the fastest and 255 being
the slowest. We currently use only two values: `FASTEST` (0) and `SLOWEST` (255).

## Ignored Diagnostics

!!! info "Specifies a list of diagnostics to ignore as false positives."

The `IgnoredDiagnostics` field is an array of `IgnoredDiagnostic` structures that contain information
about diagnostics that should be ignored for the package.

This is useful when a diagnostic is incorrectly triggered for a specific package, and you want to
suppress it.

The `IgnoredDiagnostic` structure has the following fields:

| Type   | Name | Description                                                                                                            |
| ------ | ---- | ---------------------------------------------------------------------------------------------------------------------- |
| string | Id   | The ID of the diagnostic to ignore. Should match the format specified in the [Diagnostics documentation][diagnostics]. |

Example:
```toml
[[IgnoredDiagnostics]]
Id = "R3.S56.PKGTIER-01"

[[IgnoredDiagnostics]]
Id = "R3.S56.TEXTUREOPT-02"
```

In this example, the package will ignore the `R3.S56.PKGTIER-01` and `R3.S56.TEXTUREOPT-02` diagnostics,
treating them as false positives.

If the `IgnoredDiagnostics` field is not specified or is an empty array, no diagnostics will be ignored.

## Implicit Fields

Some items are stored as separate files:

- [IconSearch](#icon-search): Search icon file, located at `package/images/icon-search.jxl`.
- [IconListCompact](#icon-list-compact-view): List compact view icon file, located at `package/images/icon-list-compact.jxl`.
- [IconList](#icon-list-view): List view icon file, located at `package/images/icon-list.jxl`.

## Icons

!!! info "Gallery images are stored in [images][package-images] folder."

!!! info "Each entry is a name of file in [images][package-images] folder."

!!! info "Images use [JPEG XL (`.jxl`)][images]"

### Icon (List Compact View)

!!! info "This is the preview icon used when displaying mods as a list (compact)."

    It corresponds to [GridDisplayMode 1][grid-display-mode].

The size of this image should be `84x48`.

This image is expected to be around 2KiB.

!!! note "The `84x48` is the target resolution for 4K displays."

!!! note "This view is meanf for showing only 1 line of text, alongside the image."

### Icon (List View)

!!! info "This is the preview icon used when displaying mods as a list."

    It corresponds to [GridDisplayMode 2][grid-display-mode].

The size of this image should be `168x96`.

This image is expected to be around 5KiB.

!!! note "The `168x96` is the target resolution for 4K displays."

!!! note "This view enables a second line of text for additional mod info in the list."

    As opposed to the [compact view](#icon-list-compact-view) which is meant for only showing 1 line.

### Icon (Search)

!!! info "This is the preview icon used for mod search results."

    It corresponds to [GridDisplayMode 3][grid-display-mode].

The size of this image should be `880x440` (2:1) with a `content` area of `600x440`.

Depending on the user's window size, the will be cropped to some size
between `880x440` and `600x440`. Thus you should aim to put all the important
detail within the `600x440` area.

This image is expected to be around 50KiB.

!!! note "The `880x440` is the target resolution for 4K displays."

!!! note "This image size is directly lifted from Reloaded-II's mod search results scale."

## Gallery

!!! info "Gallery images are stored in [images][package-images] folder."

### GalleryItem

| Type    | Name     | Description                                        |
| ------- | -------- | -------------------------------------------------- |
| string  | FileName | Name of file in [images][package-images] folder.   |
| string? | Caption  | [Optional] One line description of the screenshot. |

## Targets

!!! info "This section specifies info for the individual [backends.][backend]"

!!! info "These specify file paths relative to [`modfiles`][package-structure] folder."

[Native Mod][native-backend]:
```json
[Targets."win"]
x64-v1 = "reloaded3.gamesupport.persona5royal.dll"
```

!!! note "It's not expected for mod authors to ship with multiple [instruction sets][instruction-sets] outside of super high perf scenarios. This is just for example."

[.NET CoreCLR Mod (Any OS)][coreclr-backend]:

```json
[Targets."dotnet"]
any = "Heroes.Graphics.Essentials.dll"
```

[.NET CoreCLR Mod (With `ReadyToRun`)][coreclr-backend]:

```json
[Targets."dotnet"]
any = "Heroes.Graphics.Essentials.dll"
x86 = "x86/Heroes.Graphics.Essentials.dll"
x64 = "x64/Heroes.Graphics.Essentials.dll"
```

[Reloaded-II Mod (Example)][reloaded2-backend]:

```json
[Targets."sewer56.reloadedii-custom"]
default = "Heroes.Graphics.Essentials.dll"
x86 = "x86/Heroes.Graphics.Essentials.dll"
x64 = "x64/Heroes.Graphics.Essentials.dll"
CanUnload = true
HasExports = true
```

## Supported Games

!!! info "Stores a list of supported games; by using their known [Game ID][game-metadata-id]."

Alternatively, when experimenting with new games which do not have a specified Game ID, you can also specify `.exe` name, e.g. `tsonic_win.exe`.

Mod managers will automatically update this to appropriate ID during process of querying [Community Repository][community-repository].

## Client Side

!!! info "If true, this mod won't be disabled when joining an online multiplayer lobby."

This allows for mods such as UI mods to be used in mods that add online play without forcibly being disabled.

By default this value is false. So mod would get disabled.

## Allow Runtime Loading

!!! info "If true, then this mod can be loaded after the game has been started."

This can be used for mods which don't require hooking critical game code that is only ran
at startup. This can be useful for rapid testing of mods and speeding up debugging.

By default this value is `false` for code mods and `true` for asset mods. However
the mods which read the contents of asset mods may choose to ignore the unload request
if they themselves don't support it. (These mods should log a warning to console if they do so.)

## Config Files

!!! info "For `Tools`, this allows the [ingesting of configuration files][ingest-config] from an external location."

Example section:

```toml
# A file inside the package directory
# If the tool writes config files to its own folders
[[ConfigFiles]]
Type = "File"
Description = "Main configuration file"
[[ConfigFiles.Paths]]
OS = "any"
Path = "{PackageDir}/bin/config/config.json"

# Example of using globs with a base directory
[[ConfigFiles]]
Type = "Glob"
Description = "All XML files in the config directory"
[[ConfigFiles.Paths]]
OS = "any"
Path = "{PackageDir}/bin/config"
Extension = "json"
IncludeSubfolders = false

# Example of using AppData across different OS
[[ConfigFiles]]
Type = "File"
Description = "User settings in AppData folder matching across OSes"
[[ConfigFiles.Paths]]
OS = "any"
Path = "{AppData}/ToolName/settings.json"
# Windows: C:\Users\{Username}\AppData\Roaming\ToolName\settings.json
# Linux: /home/{Username}/.config/ToolName/settings.json
# macOS: /Users/{Username}/Library/Application Support/ToolName/settings.json

# Example of a folder with OS-specific locations
[[ConfigFiles]]
Type = "Folder"
Description = "OS-specific data folder"
[[ConfigFiles.Paths]]
OS = "win"
Path = "{LocalAppData}/ToolName/Data"
[[ConfigFiles.Paths]]
OS = "linux"
Path = "{XDG_DATA_HOME}/ToolName"
[[ConfigFiles.Paths]]
OS = "macos"
Path = "{Library}/Application Support/ToolName"
```

When a loadout is loaded or the relevant `Tool` started by Reloaded3 stops running, updated
configs are `ingested` (integrated) into the loadout.

For more details, see [Tools as Packages][tools-as-packages].

### ConfigFile

| Type            | Name        | Description                                                     |
| --------------- | ----------- | --------------------------------------------------------------- |
| string          | Type        | Type of the config entry: `File`, `Folder`, or `Glob`           |
| [Path](#path)[] | Paths       | Array of OS-specific paths for the config file or folder        |
| string          | Description | A brief description of the configuration file or group of files |

#### Path

| Type   | Name              | Description                                              |
| ------ | ----------------- | -------------------------------------------------------- |
| string | OS                | Target OS: `any`, `win`, `linux` or `macos`.             |
| string | Path              | The path or to the file/folder, can include placeholders |
| string | Extension         | Name of extension when `Glob` is used.                   |
| bool   | IncludeSubfolders | Whether to recurse folders when `Glob` is used.          |

The OS field names are based on the [Backend Names][native-backend].

## Path Placeholders

!!! info "The `Path` field allows for some placeholders."

These are based on the `Windows` folder names, with equivalent `Linux` and `macOS` folders.

| Placeholder      | Windows                   | Linux                                     | macOS                               |
| ---------------- | ------------------------- | ----------------------------------------- | ----------------------------------- |
| `{PackageDir}`   | Package directory         | Package directory                         | Package directory                   |
| `{AppData}`      | `%APPDATA%`               | `$XDG_CONFIG_HOME` or `$HOME/.config`     | `$HOME/Library/Application Support` |
| `{LocalAppData}` | `%LOCALAPPDATA%`          | `$XDG_DATA_HOME` or `$HOME/.local/share`  | `$HOME/Library/Application Support` |
| `{ProgramData}`  | `%PROGRAMDATA%`           | `/usr/local/share`                        | `/Library/Application Support`      |
| `{Temp}`         | `%TEMP%`                  | `$XDG_RUNTIME_DIR` or `/tmp`              | `$TMPDIR`                           |
| `{Documents}`    | `%USERPROFILE%\Documents` | `$XDG_DOCUMENTS_DIR` or `$HOME/Documents` | `$HOME/Documents`                   |
| `{Home}`         | `%USERPROFILE%`           | `$HOME`                                   | `$HOME`                             |

These are typically used for the following:

- `{PackageDir}`: The directory containing the current package.
- `{AppData}`: User-specific (roaming) application data folder
- `{LocalAppData}`: User-specific local application data folder
- `{ProgramData}`: Application data for all users
- `{Temp}`: Temporary folder
- `{Documents}`: User's Documents folder

### Linux Specific Placeholders

On `Linux`, the [XDG Path Spec][xdg-path-spec] is also supported:

| Placeholder           | Linux Location                            |
| --------------------- | ----------------------------------------- |
| `{XDG_DATA_HOME}`     | `$XDG_DATA_HOME` or `$HOME/.local/share`  |
| `{XDG_CONFIG_HOME}`   | `$XDG_CONFIG_HOME` or `$HOME/.config`     |
| `{XDG_CACHE_HOME}`    | `$XDG_CACHE_HOME` or `$HOME/.cache`       |
| `{XDG_DOCUMENTS_DIR}` | `$XDG_DOCUMENTS_DIR` or `$HOME/Documents` |

Explanation of Linux Folders:

- `{XDG_DATA_HOME}`: Directory for user-specific data files, typically used for non-configuration files like runtime data. Defaults to $HOME/.local/share.
- `{XDG_CONFIG_HOME}`: Directory for user-specific configuration files. Defaults to $HOME/.config.
- `{XDG_CACHE_HOME}`: Directory for user-specific non-essential data files, such as cache. Defaults to $HOME/.cache.
- `{XDG_DOCUMENTS_DIR}`: Directory for user-specific documents, usually mapped to $HOME/Documents.

### macOS Specific Placeholders

On `macOS`, the following placeholders map to directories commonly used by macOS-specific applications and are not part of the common cross-platform placeholders:

| Placeholder            | macOS Location              |
| ---------------------- | --------------------------- |
| `{Library}`            | `$HOME/Library`             |
| `{LibraryCaches}`      | `$HOME/Library/Caches`      |
| `{LibraryPreferences}` | `$HOME/Library/Preferences` |
| `{LibraryLogs}`        | `$HOME/Library/Logs`        |
| `{LibraryContainers}`  | `$HOME/Library/Containers`  |
| `{SystemLibrary}`      | `/Library`                  |

Explanation of macOS Folders:

- **`{Library}`**: The root directory for user-specific application support files, caches, preferences, etc. Located at `$HOME/Library`.
- **`{LibraryCaches}`**: Directory for user-specific cache files. Located at `$HOME/Library/Caches`.
- **`{LibraryPreferences}`**: Directory for user-specific application preference files. Located at `$HOME/Library/Preferences`.
- **`{LibraryLogs}`**: Directory for user-specific application log files. Located at `$HOME/Library/Logs`.
- **`{LibraryContainers}`**: Directory for containerized app data, used primarily for sandboxed apps. Located at `$HOME/Library/Containers`.
- **`{SystemLibrary}`**: The system-wide equivalent of the user’s Library folder, containing system-level application support files. Located at `/Library`.

<!-- Links -->
[game-metadata-id]: ../Storage/Games/About.md#id
[backend]: ../../Loader/Backends/About.md
[changelog]: ./About.md#changelog
[config]: ./About.md#config
[community-repository]: ../../Services/Community-Repository.md
[coreclr-backend]: ../../Loader/Backends/CoreCLR.md
[description]: ./About.md#description
[docs]: ./About.md#docs
[diagnostics]: ../Diagnostics.md
[workflows]: ../Workflows/About.md
[gamebanana]: https://gamebanana.com
[game-support]: ../../Loader/Core-Architecture.md#game-support-layer-2
[language-code]: ../../Common/Localisation/Adding-Localisations.md#language-naming-convention
[license]: ./About.md#license
[middleware-api-hooks]: ../../Loader/Core-Architecture.md#middlewareos-handling-mods-layer-1
[package-configuration]: ../../Common/Configuration/About.md
[mod-metadata]: ./Configurations/Mod-Metadata.md
[nexus-mods]: https://www.nexusmods.com
[native-backend]: ../../Loader/Backends/About.md#platforms
[overriding-translations]: ../../Common/Localisation/Adding-Localisations.md#sideloading-translations
[ready-to-run]: ../../Loader/Backends/CoreCLR.md#ready-to-run
[reloaded2-backend]: ../../Loader/Backends/CoreCLR.md#reloaded-ii
[semantic-versioning]: https://semver.org
[spdx-license]: https://spdx.org/licenses/
[platforms]: ../../Loader/Backends/About.md#platforms
[architecture]: ../../Loader/Backends/About.md#architectures
[tasks]: ./Tasks.md
[package-structure]: ./About.md#package-structure
[ingest-config]: ../Storage/Locations.md#package-config-handling
[tools-as-packages]: ./Tools-As-Packages.md#chosen-approach
[xdg-path-spec]: https://specifications.freedesktop.org/basedir-spec/latest/index.html