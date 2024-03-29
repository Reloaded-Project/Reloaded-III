# App Metadata

!!! warning "Work in Progress"

!!! info

    Describes the syntax of the minimal config file used to store application data.

| Type   | Name           | Description                              |
|--------|----------------|------------------------------------------|
| string | [Id](#id)      | A name that uniquely identifies the app. |

## Id

!!! info "A known, standardized name that uniquely identifies this application."

!!! warning "For games without established communities or people experimenting with new titles, this may be left blank."

For games which a user added before it had an entry in the [Community Repository](../../Services/Community-Repository.md).

This value will be autopopulated based on configurations within a future version of [Reloaded.Community](https://github.com/Reloaded-Project/Reloaded.Community).

## Game Versioning Strategy

!!! warning

    In some rare cases games can be updated to completely different ports; e.g. an older game can get a '64-bit' upgrade
    that totally would break all code mods and even change some file formats.

To mitigate this; we will use binary hashes.
This value will be autopopulated based on configurations within a future version of [Reloaded.Community](https://github.com/Reloaded-Project/Reloaded.Community).

```json
{
  "AppId": "tsonic_win.exe",
  "AppName": "Sonic Heroes",
  "AppLocation": "C:\\Users\\sewer\\Desktop\\Sonic Heroes\\Tsonic_win.EXE",
  "AppArguments": "",
  "AppIcon": "Icon.png",
  "AutoInject": false,
  "EnabledMods": [
    "sonicheroes.controller.hook.custom",
    "criware.filesystem.hook",
    "sonicheroes.utils.discordrpc",
    "sonicheroes.controller.hook.postprocess",
    "sonicheroes.skins.hdtextures",
    "sonicheroes.essentials.graphics",
    "sonicheroes.stages.radicalhighway",
    "sonicheroes.gamefiles.characteroverhaul",
    "sonicheroes.utils.toner",
    "Reloaded.Universal.DInputPleaseCooperate"
  ],
  "WorkingDirectory": null,
  "PluginData": {
    "GBPackageProvider": {
      "GameId": 6061
    }
  }
}
```