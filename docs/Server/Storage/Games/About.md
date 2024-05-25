!!! info "Game config stores all of the user's preferences for launcher/loader behaviour related to a game."

This is a singleton stored in [`Added Games (User)` (`Games/{gameId}`) folder.][added-games-location]

All data here is user specific, for cloud syncing but not sharing.

## Background Knowledge

Before reading this, read the basics over at the [Loadouts page][event-sourcing].

The approach and requirements here are generally the same.

Likewise, storing Game configurations also makes use of *Event Sourcing* for backups.

## What's inside an Game Configuration?

| Type                   | Name                                                 | Description                                           |
| ---------------------- | ---------------------------------------------------- | ----------------------------------------------------- |
| string?                | [Id](#id)                                            | A name that uniquely identifies the game.             |
| string                 | [Name](#name)                                        | User friendly name for the game, e.g. 'Sonic Heroes'. |
| Task[]                 | [ExtraTasks][tasks]                                  | List of extra ways to launche the game.               |
| AutoCreateShortcutKind | [AutoCreateShortcuts](#autocreateshortcuts)          | If true, auto creates shortcuts on the desktop.       |
| StoreInfo              | [UserStoreInformation](#user-store-information)      | Store specific information for current user.          |
| MachineSpecificInfo    | [MachineSpecificInformation](#machine-specific-info) | Machine specific information tied to this user.       |

### Id

!!! info "A known, standardized name that uniquely identifies this application."

!!! warning "For games without established communities or people experimenting with new titles, this may be left blank."

This ID links the item with the [Community Repository][community-repository].
If the community repository has no data for this game, the field will be left blank.

### Name

!!! info "A user friendly name for the game."

This can be populated from the following sources (in order of preference):

- Game Store Name
- Friendly Name embedded in executable.
- The game's executable name.

The user can overwrite the name if they wish.

### AutoCreateShortcuts

!!! info "If true, shortcuts are automatically created on desktop."

| Value | Description                                                         |
| ----- | ------------------------------------------------------------------- |
| 0     | **Dont**: Never make any shortcuts.                                 |
| 1     | **PromptOnNewMachine**: Prompt when on a new PC for the first time. |
| 2     | **Sync**: Create a shortcut for each [loadout][loadout].            |

These shortcuts auto launch the game with a specific configuration.

### User Store Information

!!! tip "The information tied to the specific store that the user installed the game from."

!!! note "The `StoreInformation` here is NOT copied from the [Community Repository][community-repository]."

This is a local copy of the *user's* store information for the game.

This distinction is important. If we use the `Community` store information, we will not know
which store the user bought the game from. This may cause confusion if the user has the game
installed in more than one store.

### Machine Specific Info

!!! tip "This contains machine specific information tied to this user."

This structure is defined as: `HashMap<MachineName, MachineInfo>`.

MachineName is a unique name tied to this machine; and is usually the machine's hostname.

- Linux & macOS: `hostname`
- Windows: `ComputerName`

`MachineInfo` is defined as:

| Type           | Name                              | Description                                                   |
| -------------- | --------------------------------- | ------------------------------------------------------------- |
| bool           | DisplayedCreateShortcutPrompt     | Displayed the [Create Shortcut](#autocreateshortcuts) prompt. |
| string         | MainExePath                       | Last path to the main executable.                             |
| string         | MainExeHash                       | Original hash of the main executable. [XXH128][hashing]       |
| DeploymentType | [DeploymentType](#deploymenttype) | Dictates how the loader is injected into the game.            |

#### DeploymentType

!!! info "This defines user's preference for how the loader is injected into the game."

| Value | Description                                                            |
| ----- | ---------------------------------------------------------------------- |
| 0     | **Undecided**: Default value.                                          |
| 1     | **CodeInjection**: Inject code, i.e. Shared Library (DLL) Injection.   |
| 2     | **DllHijacking**: Place a 'shim' executable to the user's game folder. |

## Icons and Banners

!!! warning "TODO: Override for specifying icon from an external source."

!!! info "If present, the following will be used."

| Value         | Item                                   | Description                            |
| ------------- | -------------------------------------- | -------------------------------------- |
| `Icon.jxl`    | [Icon][community-repository-icon]      | Icon for the game in 1:1 aspect ratio. |
| `BannerH.jxl` | [BannerH][community-repository-banner] | Horizontal banner for the game.        |
| `BannerV.jxl` | [BannerV][community-repository-banner] | Vertical banner for the game.          |

### Icon from SteamGridDB

!!! note "To avoid having end users register on SteamGridDB, we will expose a 1st party server that wraps the API"

    TODO: Talk to the SteamGridDB guys to find if they're ok with this.
    As it'll end up being a lot of requests against my single API key.

API Docs:
- `https://www.steamgriddb.com/api/v2`

If you run a query like:
- `https://www.steamgriddb.com/api/v2/icons/game/5247913`

You'll get multiple results in the form:

```json
"success": true,
    "data": [
        {
            "id": 21699,
            "score": 0,
            "style": "official",
            "width": 0,
            "height": 0,
            "nsfw": false,
            "humor": false,
            "notes": "Pulled from the game executable.",
            "mime": "image/vnd.microsoft.icon",
            "language": "en",
            "url": "https://cdn2.steamgriddb.com/icon/61d647c1a3d7b66b408e4a21c3167fe2.ico",
            "thumb": "https://cdn2.steamgriddb.com/icon/61d647c1a3d7b66b408e4a21c3167fe2/32/256x256.png",
            "lock": false,
            "epilepsy": false,
            "upvotes": 0,
            "downvotes": 0,
            "author": {
                "name": "cynojien",
                "steam64": "76561197971169044",
                "avatar": "https://avatars.steamstatic.com/a5dda94a5752ec305ff430dda89b034b41f42cff_medium.jpg"
            }
        },
```

We can convert the `thumb` URL to a `jxl` image and store it in the game configuration.

## Information Sourced Externally

!!! info "Some data is dynamically pulled from the [Community Repository][community-repository]."

| Type          | Item                                           | Description                                                                             |
| ------------- | ---------------------------------------------- | --------------------------------------------------------------------------------------- |
| Version[]     | [Versions][community-repo-versions]            | Versions of the executable.                                                             |
| OtherBinary[] | [OtherBinaries][community-repo-other-binaries] | Stores information about other executables in game folder you probably don't wanna mod. |
| StoreInfo     | [StoreInformation][store-information]          | Game store specific information.                                                        |
| ModSourceInfo | [ModSourceInformation][mod-source-information] | Mod source (Nexus/GameBanana/OtherModSite) specific information.                        |
| Diagnostic[]  | [Diagnostics][diagnostics]                     | Diagnostics to display based on game's current folder state.                            |

## Game Versioning Strategy

!!! warning

    In some rare cases games can be updated to completely different ports; e.g. an older game can get a '64-bit' upgrade
    that totally would break all code mods and even change some file formats.

To mitigate this; we will use binary hashes.
This value will be autopopulated based on configurations within a future version of [Reloaded.Community][reloaded-community].

```json
{
  "PluginData": {
    "GBPackageProvider": {
      "GameId": 6061
    }
  }
}
```

Consider reading more about this in the

[added-games-location]: ../Locations.md#items-to-store
[community-repository]: ../../../Services/Community-Repository.md
[event-sourcing]: ../Loadouts/About.md#event-sourcing
[images]: ../../../Common/Images.md
[reloaded-community]: https://github.com/Reloaded-Project/Reloaded.Community
[task-placeholders]: Tasks.md#commandline-placeholders
[tasks]: ./Tasks.md
[tasks-arguments]: Tasks.md#arguments
[community-repository-icon]: ../../../Services/Community-Repository.md#icon
[community-repository-banner]: ../../../Services/Community-Repository.md#banner
[store-info]: ../../../Services/Community-Repository.md#store-information
[mod-source-info]: ../../../Services/Community-Repository.md#mod-source-information
[community-repo-versions]: ../../../Services/Community-Repository.md#version
[community-repo-other-binaries]: ../../../Services/Community-Repository.md#other-binaries
[store-information]: ../../../Services/Community-Repository.md#store-information
[mod-source-information]: ../../../Services/Community-Repository.md#mod-source-information
[diagnostics]: ../../../Services/Community-Repository.md#diagnostics
[store-information]: ../../../Services/Community-Repository.md#store-information
[loadout]: ../Loadouts/About.md
[hashing]: ../../../Common/Hashing.md