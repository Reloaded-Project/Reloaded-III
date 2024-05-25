!!! info "Game config stores all of the user's preferences for launcher/loader behaviour related to a game."

## Background Knowledge

Before reading this, read the basics over at the [Loadouts page][event-sourcing].

The approach and requirements here are generally the same.

Likewise, storing Game configurations also makes use of *Event Sourcing* for backups.

## What's inside an Game Configuration?

| Type    | Name           | Description                                                        |
| ------- | -------------- | ------------------------------------------------------------------ |
| string? | [Id](#id)      | A name that uniquely identifies the game. Should be user friendly. |
| string  | [Name](#name)  | User friendly name for the game, e.g. 'Sonic Heroes'.              |
| Task[]  | [Tasks][tasks] | List of executables that can be launched for this game.            |

### Id

!!! info "A known, standardized name that uniquely identifies this application."

!!! warning "For games without established communities or people experimenting with new titles, this may be left blank."

For games which a user added before it had an entry in the [Community Repository][community-repository].

This value will be autopopulated based on configurations within a future version of [Reloaded.Community][reloaded-community].

### Name

!!! info "A user friendly name for the game."

This can be populated from the following sources (in order of preference):

- Game Store Name
- Friendly Name embedded in executable.
- The game's executable name.

The user can overwrite the name if they wish.



## Game Versioning Strategy

!!! warning

    In some rare cases games can be updated to completely different ports; e.g. an older game can get a '64-bit' upgrade
    that totally would break all code mods and even change some file formats.

To mitigate this; we will use binary hashes.
This value will be autopopulated based on configurations within a future version of [Reloaded.Community][reloaded-community].

```json
{
  "Id": "tsonic_win.exe",
  "AppName": "Sonic Heroes",
  "AppLocation": "C:\\Users\\sewer\\Desktop\\Sonic Heroes\\Tsonic_win.EXE",
  "AppArguments": "",
  "AppIcon": "Icon.png",
  "RelativeWorkingDirectory": null,
  "PluginData": {
    "GBPackageProvider": {
      "GameId": 6061
    }
  }
}
```

<!-- Links -->
## File Format

!!! info "A config for an application has the following file format."

| Data Type | Name   | Label | Description                                                                                                      |
| --------- | ------ | ----- | ---------------------------------------------------------------------------------------------------------------- |
| `u8`      | Length | X     | [0-255] Length of new commandline parameters in [commandline-parameter-data.bin][commandline-parameter-data.bin] |

!!! tip "Games in Reloaded3 use the concept of 'events' to track and manage changes over time."

Consider reading more about this in the

- ❌ [Create Shortcut]
- ❌ [Show Console]
- ❌ [Deployment Type (e.g. ASI Loader)]
- ❌ [Extra Commandline Arguments]

[event-sourcing]: ../Loadouts/About.md#event-sourcing
[community-repository]: ../../../Services/Community-Repository.md
[reloaded-community]: https://github.com/Reloaded-Project/Reloaded.Community
[tasks]: ./Tasks.md
