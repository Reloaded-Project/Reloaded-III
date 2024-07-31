!!! info "This is a full list of Commit Messages for each event in [events.bin][events-bin]"

Note that these use markdown formatting, so double stars `**` mean **bold**.

Most parameters are auto inferred from [(events.bin)][events-bin], any parameters not inferred are listed
in the respective section.

## Formatting

!!! tip "Commit Messages use Markdown, with placeholders for parameters."

## How the Localisation is Loaded

!!! tip "The localisations use the [Reloaded3 Localisation System][r3-locale-format]."

The section names denote the keys used here, for example:

```toml
## Update 1.1.0 | 2024 May 2nd
[[PACKAGE_ADDED_V0]]
Added '**{Name}**' with ID '**{ID}**' and version '**{Version}**'.

[[PACKAGE_REMOVED_V0]]
Removed '**{Name}**' with ID '**{ID}**' and version '**{Version}**'.
```

## Contextual Parameters

!!! info "Some parameters can be derived from the context of the event, these are listed below."

For example, for the [Package Status Changed](#package-status-changed-v0) event, the following
parameters can be inferred:

- `Version`: The name of the package, mod, translation or tool.
- `EventTime`: The timestamp of the event.

Parameters marked `[Contextual]` are inferred from the event context.

## Parameter Ordering

!!! info "Parameters are written to the message in the order they are listed."

The `[0]` in `Name [0]` means that it is written to the file as the first parameter.
The `[1]` in `ID [1]` means that it is the second parameter.

etc.

When the parameter is [contextual](#contextual-parameters), the value is read from
the context and the order is set to `[-1]`.

## Package Status Changed (V0)

!!! info "Source: Event [PackageStatusChanged][event-packagestatuschanged]"

### Parameters

- `Name` [0]: The name of the package, mod, translation or tool. [String][commit-param-type]
- `ID` [1]: The package ID. [String][commit-param-type]
- `Version` [-1]: The package version. [String [Contextual]](#contextual-parameters)

### PACKAGE_ADDED_V0

```
Added '**{Name}**' with ID '**{ID}**' and version '**{Version}**'.
```

### PACKAGE_REMOVED_V0

```
Removed '**{Name}**' with ID '**{ID}**' and version '**{Version}**'.
```

### PACKAGE_HIDDEN_V0

```
Hidden '**{Name}**' with ID '**{ID}**' and version '**{Version}**' from view.
```

### PACKAGE_DISABLED_V0

```
Disabled '**{Name}**' with ID '**{ID}**' and version '**{Version}**'.
```

### PACKAGE_ENABLED_V0

```
Enabled '**{Name}**' with ID '**{ID}**' and version '**{Version}**'.
```

### MOD_ADDED_V0

```
Added mod '**{Name}**' with ID '**{ID}**' and version '**{Version}**'.
```

### MOD_REMOVED_V0

```
Removed mod '**{Name}**' with ID '**{ID}**' and version '**{Version}**'.
```

### MOD_HIDDEN_V0

```
Hidden mod '**{Name}**' with ID '**{ID}**' and version '**{Version}**' from view.
```

### MOD_DISABLED_V0

```
Disabled mod '**{Name}**' with ID '**{ID}**' and version '**{Version}**'.
```

### MOD_ENABLED_V0

```
Enabled mod '**{Name}**' with ID '**{ID}**' and version '**{Version}**'.
```

### TRANSLATION_ADDED_V0

```
Added translation '**{Name}**' with ID '**{ID}**' and version '**{Version}**'.
```

### TRANSLATION_REMOVED_V0

```
Removed translation '**{Name}**' with ID '**{ID}**' and version '**{Version}**'.
```

### TRANSLATION_HIDDEN_V0

```
Hidden translation '**{Name}**' with ID '**{ID}**' and version '**{Version}**' from view.
```

### TRANSLATION_DISABLED_V0

```
Disabled translation '**{Name}**' with ID '**{ID}**' and version '**{Version}**'.
```

### TRANSLATION_ENABLED_V0

```
Enabled translation '**{Name}**' with ID '**{ID}**' and version '**{Version}**'.
```

### TOOL_ADDED_V0

```
Added tool '**{Name}**' with ID '**{ID}**' and version '**{Version}**'.
```

### TOOL_REMOVED_V0

```
Removed tool '**{Name}**' with ID '**{ID}**' and version '**{Version}**'.
```

### TOOL_HIDDEN_V0

```
Hidden tool '**{Name}**' with ID '**{ID}**' and version '**{Version}**' from view.
```

### TOOL_DISABLED_V0

```
Disabled tool '**{Name}**' with ID '**{ID}**' and version '**{Version}**'.
```

### TOOL_ENABLED_V0

```
Enabled tool '**{Name}**' with ID '**{ID}**' and version '**{Version}**'.
```

## Package Updated (V0)

!!! info "Source: Event [PackageUpdated][event-packageupdated]"

### Parameters

- `Name` [0]: The name of the package, mod, translation or tool. [String][commit-param-type]
- `ID` [1]: The package ID. [String][commit-param-type]
- `OldVersion` [-1]: The previous package version. [String [Contextual]](#contextual-parameters)
- `NewVersion` [-1]: The new package version. [String [Contextual]](#contextual-parameters)

### PACKAGE_UPDATED_V0

```
Updated '**{Name}**' from version '**{OldVersion}**' to '**{NewVersion}**'.
(ID: '{ID}').
```

### MOD_UPDATED_V0

```
Updated mod '**{Name}**' from version '**{OldVersion}**' to '**{NewVersion}**'.
(ID: '{ID}').
```

### TRANSLATION_UPDATED_V0

```
Updated translation '**{Name}**' from version '**{OldVersion}**' to '**{NewVersion}**'.
(ID: '{ID}').
```

### TOOL_UPDATED_V0

```
Updated tool '**{Name}**' from version '**{OldVersion}**' to '**{NewVersion}**'.
(ID: '{ID}').
```

## GAME_LAUNCHED_V0

!!! info "Invoked by [GameLaunched][event-game-launched]"

```
Launched game at {EventTimestamp}.
```

`EventTimestamp` is human readable absolute date.
e.g. `11th of May 2020`.

- `EventTimestamp` [-1]: [TimeStamp [Contextual]](#contextual-parameters)

## Config Updated (V0)

### Parameters


- `Name` [0]: The name of the package, mod, translation or tool. [String][commit-param-type]
- `ModID` [1]: The package ID for mod/tool. [String][commit-param-type]
- `Key` [2]: The name of the setting field as a string. [String][commit-param-type]
- `OldValue` [3]: The previous value for the item. [Type Depends on Value][commit-param-type]
- `NewValue` [4]: The new value for the item. [Type Depends on Value][commit-param-type]

- `{ChangeList}` [5] is a [Parameter List][commit-param-list].

### CHANGE_V0

!!! note "This is an individual item in the `ChangeList` items below"

```
- **{Key}**: **{OldValue}** -> **{NewValue}**
```

### MOD_CONFIG_UPDATED_V0

!!! info "Source: Event [ConfigUpdated][event-configupdated]"

```
Updated settings for mod '**{ModName}**'.

Changes:
{ChangeList}

(ID: '{ID}')
```

#### MOD_CONFIG_UPDATED_V1

When the exact changes cannot be determined.

```
Updated settings for mod '**{ModName}**' (ID: '{ID}').
```

### TOOL_CONFIG_UPDATED_V0

!!! info "Source: Event [ConfigUpdated][event-configupdated]"

```
Updated settings for tool '**{ToolName}**'.

Changes:
{ChangeList}

(ID: '{ID}')
```

#### TOOL_CONFIG_UPDATED_V1

When the exact changes cannot be determined.

```
Updated settings for tool '**{ToolName}**' (ID: '{ID}').
```

## Load Order Changed

!!! info "Source: Event [PackageLoadOrderChanged][event-packageloadorderchanged]"

### Parameters

- `Name` [0]: The name of the package, mod, translation or tool. [String][commit-param-type]
- `ID` [1]: The package ID. [String][commit-param-type]
- `Version` [-1]: The package version. [String [Contextual]](#contextual-parameters)

### MOD_LOAD_ORDER_CHANGED_V0

```
Changed load order for mod '**{Name}**' from **{OldPosition}** to **{NewPosition}**.
(ID: '{ID}')
```

### TRANSLATION_LOAD_ORDER_CHANGED_V0

```
Changed load order for translation '**{Name}**' from **{OldPosition}** to **{NewPosition}**.
(ID: '{ID}')
```

## Display Setting Changed

!!! info "Source: Event [LoadoutDisplaySettingChanged][event-loadout-display-setting-changed]"

### LOADOUT_GRID_ENABLED_SORT_MODE_CHANGED_V0

```
Enabled item sorting changed: '**{OldEnabledSortMode}**' to '**{NewEnabledSortMode}**'.
```

### LOADOUT_GRID_DISABLED_SORT_MODE_CHANGED_V0

```
Changed sorting mode for disabled items from '{OldDisabledSortMode}' to '{NewDisabledSortMode}'.
```

### MOD_LOAD_ORDER_SORT_CHANGED_V0
```
Load reorderer sort mode changed: '**{OldLoadOrderSort}**' to '**{NewLoadOrderSort}**'.
```

### LOADOUT_GRID_STYLE_CHANGED_V0

```
Mod display mode changed from '{OldLoadoutGridStyle}' to '{NewLoadoutGridStyle}'.
```

### LOADOUT_DISPLAY_SETTINGS_CHANGED_V0

!!! info "This is used when multiple settings are being"

```
Changed loadout display settings.

{ChangeList}
```

!!! note "ChangeList is constructed in code since we know all possibilities ahead of time"

    Below shows the messages added when the `ChangeList` is constructed.

When `LoadoutGridEnabledSortMode` has changed:

```
- Enabled item sorting changed: '**{OldEnabledSortMode}**' to '**{NewEnabledSortMode}**'.
```

When `LoadoutGridDisabledSortMode` has changed:
```
- Disabled item sorting changed: '**{OldDisabledSortMode}**' to '**{NewDisabledSortMode}**'.
```

When `ModLoadOrderSort` has changed:
```
- Load reorderer sort mode changed: '**{OldLoadOrderSort}**' to '**{NewLoadOrderSort}**'.
```

When `LoadoutGridStyle` has changed:

```
- Mod display mode changed from '{OldLoadoutGridStyle}' to '{NewLoadoutGridStyle}'.
```

## UpdateGameStoreManifest

!!! info "Source: Event [UpdateGameStoreManifest][event-updategamestoremanifest]"

!!! tip "See: [Store Data][store-data] for more info."

### UPDATE_GAME_STORE_MANIFEST_STEAM_V0

```
Updated game to manifest `{ManifestId}` (from `{OldManifestId}`) on Steam.
```

### UPDATE_GAME_STORE_MANIFEST_GOG_V0

```
Updated game to version '{VersionName}' (from version `{OldVersionName}`) on GOG.
```

### UPDATE_GAME_STORE_MANIFEST_XBOX_V0

```
Updated game to version '{VersionName}' (from version `{OldVersionName}`) on Xbox.
```

### UPDATE_GAME_STORE_MANIFEST_EGS_V0

```
Updated game to version '{VersionName}' (from version `{OldVersionName}`) on Epic Games Store.
```

### UPDATE_GAME_STORE_MANIFEST_V0

```
Game was updated to a new version or EXE was modified.
```

## UPDATE_COMMANDLINE_V0

!!! info "Source: Event [UpdateCommandline][event-updatecommandline]"

```
Updated command line parameters from:
- `{OldCommandLine}`
to
- `{NewCommandLine}`
```

[events-bin]: ./Unpacked.md#eventsbin
[event-packagestatuschanged]: ./Events.md#packagestatuschanged
[event-config-updated]: ./Events.md#configupdated
[event-loadout-display-setting-changed]: ./Events.md#1004-loadoutdisplaysettingchanged
[event-game-launched]: ./Events.md#gamelaunched
[event-packageupdated]: ./Events.md#packageupdated
[event-configupdated]: ./Events.md#configupdated
[event-packageloadorderchanged]: ./Events.md#packageloadorderchanged
[event-updategamestoremanifest]: ./Events.md#updategamestoremanifest
[store-data]: ./Unpacked.md#store-databin
[event-updatecommandline]: ./Events.md#updatecommandline
[commit-param-type]: ./Unpacked.md#parametertype
[commit-param-list]: ./Unpacked.md#parameter-lists
[commit-param-version]: ./Unpacked.md#commit-parameters-versionsbin
[r3-locale-format]: ../../../../Common/Localisation/File-Format.md