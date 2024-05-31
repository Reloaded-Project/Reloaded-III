# Package Metadata

!!! info "Describes items common in all Reloaded3 packages"

Inside each package folder is a file named `package.toml`; which stores the metadata of each package.

| Type                | Name                                       | Description                                                               |
| ------------------- | ------------------------------------------ | ------------------------------------------------------------------------- |
| string              | [Id](#id)                                  | A name that uniquely identifies the package.                              |
| string              | Name                                       | Human friendly name of the package.                                       |
| string              | Author                                     | Main author of the package. (Individual or Team Name)                     |
| string              | Summary                                    | Short summary of the package. Max 2 sentences.                            |
| PackageType         | [PackageType](#packagetype)                | Type of the package. See [PackageType](#packagetype) for possible values. |
| string              | [DocsFile](#docsfile)                      | [Optional] Entry point for this package documentation.                    |
| SemVer              | [Version](#version)                        | Semantic versioning version of the package.                               |
| string              | LicenseId                                  | [SPDX License Identifier][spdx-license]                                   |
| string[]            | [Tags](#tags)                              | Used to make searching easier within mod managers.                        |
| Credit[]            | [Credits](#credits)                        | [Optional] Stores information about who contributed what to the project.  |
| string?             | SourceUrl                                  | [Optional] Link to source code (if applicable).                           |
| string?             | ProjectUrl                                 | [Optional] Link to website to learn more about the project.               |
| UpdateData          | [UpdateData](#update-data)                 | Stores package specific update information.                               |
| DependencyInfo[]    | [Dependencies](#dependency-info)           | Stores information about this package's dependencies.                     |
| DateTime            | [Published](#published)                    | The time when this package was packed.                                    |
| StoragePreference   | [StoragePreference](#storage-preference)   | Specifies the preferred storage tier for the package.                     |
| IgnoredDiagnostic[] | [IgnoredDiagnostics](#ignored-diagnostics) | List of diagnostics to ignore as false positives.                         |

## Implicit Fields

Some items are stored as separate files:

- [license][license]: License file, located in `package/license.md`.
    - This is used if `LicenseId` is not specified.
- [changelog][changelog]: Changelog file(s), located in `package/changelog/*.md`.
- [description][description]: Description file, located in `package/description.md`.
- [config][config]: Configuration schema for the package, located in `package/config.toml`.

## Example Config

!!! note "Any links, IDs here are sample data and not real."

Example [game support mod][game-support].

```toml
Id = "reloaded3.gamesupport.p5rpc.s56"
Name = "Persona 5 Royal Support"
Summary = "Provides Essential Functionality for Persona 5 Royal."
Author = "Sewer56"
PackageType = "Mod"
DocsFile = "index.html"
Version = "1.0.1"
Tags = ["Utility", "Library"]
SourceUrl = "https://github.com/Sewer56/p5rpc.modloader"
ProjectUrl = "https://sewer56.dev/p5rpc.modloader/"
Published = 2023-06-08T12:34:56Z

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
RepositoryName = "reloaded3.gamesupport.p5rpc"

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
[Targets."win-x64"]
any = "reloaded3.gamesupport.p5rpc.dll"
x64-v2 = "reloaded3.gamesupport.p5rpc.v2.dll"
x64-v3 = "reloaded3.gamesupport.p5rpc.v3.dll"
```

## Id

!!! info "A name that uniquely identifies the package."

!!! warning "Must be a valid Windows & Unix file name."

This format is designed to minimize collisions while providing a human-readable name.

The suggested format to use for names is `game.type.subtype.name.author`.

- `game` should ideally match [Game 'Id'][game-metadata-id] for the given application.
- `type` name should ideally match category of the package on a site like [GameBanana][gamebanana] or [NexusMods][nexus-mods].
- `subtype` [Optional] provides additional information about the item.
- `name` unique name for the package. Can use another `.` dot if additional info is needed.
- `author` primary package author (prefer abbreviated).

Example(s):

- No Subtype: `sonicheroes.skins.seasidehillmidnight.s56`
- With Subtype: `sonicheroes.skins.seasidehill.midnighthill.s56`

Use lowercase, no spaces, no special characters.

!!! tip "The author field may be omitted, if e.g. creating GitHub repositories."

    It's only there to avoid conflicts.

### Universal Mods

!!! note

    For mods that are non-game specific such as backends; set the `game` identifier as `reloaded3` and use one of the following.

| Type         | Description                                       | Example                           |
| ------------ | ------------------------------------------------- | --------------------------------- |
| backend      | For [backends][backend].                          | `reloaded3.backend.coreclr.s56`   |
| api          | For [middleware/API hooks][middleware-api-hooks]. | `reloaded3.api.windows.vfs.s56`   |
| game support | For [game support mods][game-support].            | `reloaded3.gamesupport.p5rpc.s56` |
| utility      | For utility mods with reusable code.              | `reloaded3.utility.hooks.s56`     |

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

## PackageType

!!! info "Represents the type of the package."

`PackageType` is an enumerable with the following possible values:

- [Mod][mod-metadata] (Default): Stores a game modification.
- `Profile`: Stores user profile.
- `Translation`: Stores a [translation for another package][overriding-translations].
- `Tool`: Represents a modding tool.

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
[gamebanana]: https://gamebanana.com
[game-support]: ../../Loader/Core-Architecture.md#game-support-layer-2
[language-code]: ../../Common/Localisation/Adding-Localisations.md#language-naming-convention
[license]: ./About.md#license
[middleware-api-hooks]: ../../Loader/Core-Architecture.md#middlewareos-handling-mods-layer-1
[mod-configurations]: ./Mod-Configurations.md
[mod-metadata]: ./Configurations/Mod-Metadata.md
[nexus-mods]: https://www.nexusmods.com
[native-backend]: ../../Loader/Backends/Native.md
[overriding-translations]: ../../Common/Localisation/Adding-Localisations.md#sideloading-translations
[ready-to-run]: ../../Loader/Backends/CoreCLR.md#ready-to-run
[reloaded2-backend]: ../../Loader/Backends/CoreCLR.md#reloaded-ii
[semantic-versioning]: https://semver.org
[spdx-license]: https://spdx.org/licenses/