# Package Metadata

!!! info "Describes items common in all Reloaded3 packages"

Inside each package folder is a file named `Package.toml`; which stores the metadata of each package.

| Type             | Name                             | Description                                                           |
| ---------------- | -------------------------------- | --------------------------------------------------------------------- |
| string           | [Id](#id)                        | A name that uniquely identifies the package.                          |
| string           | Name                             | Human friendly name of the package.                                   |
| string           | Author                           | Main author(s) of the package. Separate multiple authors with commas. |
| string           | Summary                          | Short summary of the package. Max 2 sentences.                        |
| SemVer           | [Version](#version)              | Semantic versioning version of the package.                           |
| string[]         | [Tags](#tags)                    | Used to make searching easier within mod managers.                    |
| UpdateData       | [UpdateData](#update-data)       | Stores package specific update information.                           |
| DependencyInfo[] | [Dependencies](#dependency-info) | Stores information about this package's dependencies.                 |
| string           | SourceUrl                        | Link to source code (if applicable).                                  |
| string           | ProjectUrl                       | Link to website to learn more about the project.                      |

## Package Types

!!! info "These are the types whose configurations extend from the base package configuration."

- [Mod Metadata][mod-metadata]

## Example Config

!!! note "Any links, IDs here are sample data and not real."

Example [game support mod][game-support].

```toml
Id = "reloaded3.gamesupport.p5rpc.s56"
Name = "Persona 5 Royal Support"
Summary = "Provides Essential Functionality for Persona 5 Royal."
Author = "Sewer56"
Version = "1.0.1"
Tags = ["Utility", "Library"]
SourceUrl = "https://github.com/Sewer56/p5rpc.modloader"
ProjectUrl = "https://sewer56.dev/p5rpc.modloader/"

[UpdateData]
[UpdateData.GameBanana]
ItemType = "Mod"
ItemId = 123456

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
Id = "reloaded3.utility.reloadedhooksrs.s56"
Name = "Reloaded3 Hooking Library"
Author = "Sewer56"
[Dependencies.UpdateData]
[Dependencies.UpdateData.GitHub]
UserName = "Reloaded-Project"
RepositoryName = "reloaded3.utility.reloadedhooksrs"

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
```

## Id

!!! info "A name that uniquely identifies the package."

This format is designed to minimize collisions while providing a human-readable name.

The suggested format to use for names is `game.type.subtype.name.author`.

- `game` should ideally match [App 'Id'][app-metadata-id] for the given application.
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

!!! info "For diagnostics, use the format: `reloaded3server.diagnostic.game.name`"

| Type       | Description                     | Example                                               |
| ---------- | ------------------------------- | ----------------------------------------------------- |
| diagnostic | For [diagnostics][diagnostics]. | `reloaded3server.diagnostic.general.textureoptimizer` |

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

<!-- Links -->
[app-metadata-id]: ../../Server/Configurations/App-Metadata.md#id
[backend]: ../../Loader/Backends/About.md
[community-repository]: ../../Services/Community-Repository.md
[coreclr-backend]: ../../Loader/Backends/CoreCLR.md
[diagnostics]: ../Diagnostics.md
[gamebanana]: https://gamebanana.com
[game-support]: ../../Loader/Core-Architecture.md#game-support-layer-2
[middleware-api-hooks]: ../../Loader/Core-Architecture.md#middlewareos-handling-mods-layer-1
[mod-configurations]: ./Mod-Configurations.md
[mod-metadata]: ../Configurations/Mod-Metadata.md
[nexus-mods]: https://www.nexusmods.com
[native-backend]: ../../Loader/Backends/Native.md
[ready-to-run]: ../../Loader/Backends/CoreCLR.md#ready-to-run
[reloaded2-backend]: ../../Loader/Backends/CoreCLR.md#reloaded-ii
[semantic-versioning]: https://semver.org