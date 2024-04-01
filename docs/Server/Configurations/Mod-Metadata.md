# Mod Metadata

!!! warning "Work in Progress"

!!! info

    Describes the syntax of the minimal config file used to store mod metadata.

Inside each mod folder is a file named `R3ModConfig.json`; which stores the metadata of each mod.

| Type                             | Name                               | Description                                                       |
| -------------------------------- | ---------------------------------- | ----------------------------------------------------------------- |
| string                           | [Id](#id)                          | A name that uniquely identifies the mod.                          |
| string                           | Name                               | Name of the mod.                                                  |
| string                           | Author                             | Main author(s) of the mod. Separate multiple authors with commas. |
| SemVer                           | [Version](#version)                | Semantic versioning version of the mod.                           |
| string                           | Description                        | Short description of the mod. (<= 200 chars)                      |
| string[]                         | [Tags](#tags)                      | Used to make searching easier within mod managers.                |
| string                           | [Icon](#icon)                      | Relative path of preview icon.                                    |
| bool                             | [IsLibrary](#is-library)           | If true this mod cannot be explicitly enabled by the user.        |
| UpdateData                       | [UpdateData](#update-data)         | Stores mod update specific information.                           |
| DependencyInfo                   | [Dependencies](#dependency-info)   | Stores information about this mod's dependencies.                 |
| string                           | SourceUrl                          | Link to source code (if applicable).                              |
| string                           | ProjectUrl                         | Link to website to learn more about the project.                  |
| Dictionary&lt;string, Target&gt; | [Targets](#targets)                | Specifies the DLLs/binaries used [for each backend.][backend]     |
| string[]                         | [SupportedGames](#supported-games) | List of supported titles/games.                                   |

## Id

A name that uniquely identifies the mod.

The suggested format to use for names is `game.type.subtype.name`.

- `game` should ideally match [App 'Id'][app-metadata-id] for the given application.
- `type` name should ideally match category of the mod on a site like [GameBanana](https://gamebanana.com) or [NexusMods](https://www.nexusmods.com).
- `subtype` [Optional] provides additional information about the item.
- `name` unique identifier for the mod. Can use another `.` dot if additional info is needed.

Example(s):

- `sonicheroes.skins.seasidehillmidnight`
- `sonicheroes.skins.seasidehill.midnighthill`

Use lowercase, no spaces, no special characters.

### Non-Game Specific Components

!!! note

    For mods that are non-game specific such as backends; set the `game` identifier as `reloaded3` and use one of the following.

| Type    | Description                                       | Example                     |
| ------- | ------------------------------------------------- | --------------------------- |
| backend | For [backends][backend].                          | `reloaded3.backend.coreclr` |
| api     | For [middleware/API hooks][middleware-api-hooks]. | `reloaded3.api.windows.vfs` |
| utility | For utility mods with reusable code.              | `reloaded3.utility.hooks`   |

Mod manager can choose whether to show non game-specific mods (`reloaded3` id) on a specific game's page or not.

## Version

!!! info

    This stores a mod version specified using a [Semantic Versioning][semantic-versioning] compatible standard.
    This is required for update support.

!!! warning

    For legacy mods converted from other loaders. If a non-semver version is used, we strip all spaces and write it as `0.0.0.{originalVersion}`.

## Tags

!!! info "Used to make searching within mod managers easier; i.e. `filter by tag`."

These are completely arbitrary, up to end users.
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

## Icon

!!! info "Stores path relative to folder `ModConfig.json` is stored in."

!!! info "Supported formats include `.png`, `.jpg` and `.webp`."

!!! info "Should be a multiple of `256x256`. Recommended `512x512`."

## Is Library

!!! info "If this is true, the mod cannot be explicitly enabled by the user in the manager."

!!! info "Some libraries may have user [configuration(s)][mod-configurations]. Manager is free to hide other libraries."

## Update Data

!!! info

    Information tied to Reloaded3's update library. This info is stored in a way that avoids direct dependency
    on Update library by using an `Abstractions` package.

!!! note

    This section might be moved to dedicated Update library section.

| Type                 | Name                                                   | Description                              |
| -------------------- | ------------------------------------------------------ | ---------------------------------------- |
| string               | [ReleaseMetadataFileName](#release-metadata-file-name) | A name that uniquely identifies the mod. |
| GameBananaUpdateInfo | [GameBananaUpdateInfo](#gamebanana-update-info)        | Info on how to update from GitHub.       |
| GitHubUpdateInfo     | [GitHubUpdateInfo](#github-update-info)                | Info on how to update from GameBanana.   |
| NexusUpdateInfo      | [ReleaseMetadataFileName](#nexus-update-info)          | Info on how to update from Nexus.        |
| NuGetUpdateInfo      | [NuGetUpdateInfo](#nuget-update-info)                  | Info on how to update from NuGet.        |
| DependencyInfo       | [DependencyInfo](#dependency-info)                     | A name that uniquely identifies the mod. |

### Release Metadata File Name

!!! info "This filename is used by Update Library to fetch information about current version on GitHub/Nexus/GameBanana/etc."

This name defaults to `{Id}.ReleaseMetadata.json` upon the creation of a mod and should never be modified by the end user
unless they know what they're doing.

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
| int    | ModId      | Unique index for the mod.                 |

### NuGet Update Info

| Type     | Name                  | Description                                        |
| -------- | --------------------- | -------------------------------------------------- |
| string[] | DefaultRepositoryUrls | List of NuGet URLs/repos this mod can update from. |

## Dependency Info

!!! info "The dependency resolution strategy is to simply copy update info of all dependencies into this structure. We can use that info to resolve mods if they are missing."

| Type           | Name           | Description                                                     |
| -------------- | -------------- | --------------------------------------------------------------- |
| DependencyItem | DependencyItem | A tuple of mod ID and copy of mod's [UpdateData](#update-data). |

`DependencyItem` is defined as:

| Type       | Name                       | Description                             |
| ---------- | -------------------------- | --------------------------------------- |
| string     | ModId                      | Unique ID of the dependency.            |
| UpdateData | [UpdateData](#update-data) | Stores mod update specific information. |

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
  "coreclr-latest" : {
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
[middleware-api-hooks]: ../../Loader/Core-Architecture.md#middlewareos-handling-mods-layer-1
[mod-configurations]: ./Mod-Configurations.md
[native-backend]: ../../Loader/Backends/Native.md
[ready-to-run]: ../../Loader/Backends/CoreCLR.md#ready-to-run
[reloaded2-backend]: ../../Loader/Backends/CoreCLR.md#reloaded-ii
[semantic-versioning]: https://semver.org