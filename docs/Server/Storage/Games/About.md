!!! info "Game config stores all of the user's preferences for launcher/loader behaviour related to a game."

This is a singleton stored in [`Added Games (User)` (`Games/{gameId}`) folder.][added-games-location]

All data here is user specific, for cloud syncing but not sharing.

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

    Use lowercase, don't abbreviate.
    For example use `persona5royal`, not `p5r`. Use `sonicheroes`, not `sh`. etc.

!!! warning "For games without established communities or people experimenting with new titles, this may be left blank."

This ID links the item with the [Community Repository][community-repository].
If the community repository has no data for this game, the field will be left blank.

!!! question "What do I do if the game has no known ID?"

    The launcher should block publish until a valid ID is set.

    On publish the launcher should take the user to a readme page that tells you how to add game to
    [Community Repository][community-repository]. This should be a largely automated step.

    New submissions can be made via GitHub PRs to Community repo, or by Discord request.
    This ensures all shared mods have the same game ID.

    !!! warning "There will be a need to introduce a 'rename package ID in loadout' operation"

        As a new game ID will need injecting into package name.

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

This structure is defined as: `HashMap<EntryID, MachineInfo>`.

#### Deriving the EntryID

!!! info "`EntryID` is derived as `{MachineID}+{UserName}`"

`MachineID` is derived as:

- Linux: `/etc/machine-id`
- Windows: `MachineGuid`
    - This is `HKEY_LOCAL_MACHINE/SOFTWARE/Microsoft/Cryptography` -> `MachineGuid`
- macOS: TODO

`UserName` is well, as the name describes.

#### MachineInfo

`MachineInfo` is defined as:

| Type           | Name                              | Description                                                   |
| -------------- | --------------------------------- | ------------------------------------------------------------- |
| bool           | DisplayedCreateShortcutPrompt     | Displayed the [Create Shortcut](#autocreateshortcuts) prompt. |
| string         | FriendlyName                      | Friendly Name for the Machine.                                |
| string         | MainExePath                       | Last path to the main executable.                             |
| string         | MainExeHash                       | Original hash of the main executable. [XXH128][hashing]       |
| DeploymentType | [DeploymentType](#deploymenttype) | Dictates how the loader is injected into the game.            |

The `FriendlyName` is derived from `UserName` and `MachineName`.
`MachineName` is derived as `hostname` on Linux/macOS and `ComputerName` on Windows.

Usually it's formatted as `{UserName}'s {MachineName}`.

##### DeploymentType

!!! info "This defines user's preference for how the loader is injected into the game."

| Value | Description                                                            |
| ----- | ---------------------------------------------------------------------- |
| 0     | **Undecided**: Default value.                                          |
| 1     | **CodeInjection**: Inject code, i.e. Shared Library (DLL) Injection.   |
| 2     | **DllHijacking**: Place a 'shim' executable to the user's game folder. |

## Icons and Banners

!!! info "If present, the following will be used."

| Value              | Item                                      | Description                                   |
| ------------------ | ----------------------------------------- | --------------------------------------------- |
| `Icon.jxl`         | [Icon][community-repository-icon]         | Icon for the game in 1:1 aspect ratio.        |
| `BannerSquare.jxl` | [BannerSquare][community-repository-icon] | Grid Square for the game in 1:1 aspect ratio. |
| `BannerHorz.jxl`   | [BannerHorz][community-repository-banner] | Horizontal banner for the game.               |
| `BannerVert.jxl`   | [BannerVert][community-repository-banner] | Vertical banner for the game.                 |

## Information Sourced Externally

!!! info "Some data is dynamically pulled from the [Community Repository][community-repository]."

| Type          | Item                                           | Description                                                                             |
| ------------- | ---------------------------------------------- | --------------------------------------------------------------------------------------- |
| Version[]     | [Versions][community-repo-versions]            | Versions of the executable.                                                             |
| OtherBinary[] | [OtherBinaries][community-repo-other-binaries] | Stores information about other executables in game folder you probably don't wanna mod. |
| StoreInfo     | [StoreInformation][store-information]          | Game store specific information.                                                        |
| ModSourceInfo | [ModSourceInformation][mod-source-information] | Mod source (Nexus/GameBanana/OtherModSite) specific information.                        |
| Diagnostic[]  | [Diagnostics][diagnostics]                     | Diagnostics to display based on game's current folder state.                            |

[added-games-location]: ../Locations.md#items-to-store
[community-repository]: ../../../Services/Community-Repository.md
[event-sourcing]: ../Loadouts/About.md#event-sourcing
[images]: ../../../Common/Images.md
[reloaded-community]: https://github.com/Reloaded-Project/Reloaded.Community
[task-placeholders]: Tasks.md#commandline-placeholders
[tasks]: ./Tasks.md
[tasks-arguments]: Tasks.md#arguments
[community-repository-icon]: ../../../Services/Community-Repository.md#icons-and-banners-steamgriddb
[community-repository-banner]: ../../../Services/Community-Repository.md#icons-and-banners-steamgriddb
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