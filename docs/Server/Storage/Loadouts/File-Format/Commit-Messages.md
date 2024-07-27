!!! info "This is a full list of Commit Messages for each event in [events.bin][events-bin]"

Note that these use markdown formatting, so double stars `**` mean **bold**.

Most parameters are auto inferred from [(events.bin)][events-bin], any parameters not inferred are listed
in the respective section.

## Formatting

!!! tip "Commit Messages use Markdown, with placeholders for parameters."

## Built In Parameters

!!! info "Some parameters can be derived from the context of the event, these are listed below."

For example, for the [Package Status Changed](#package-status-changed) event, the following
parameters can be inferred:

- `Version`: The name of the package, mod, translation or tool.

## Package Status Changed

!!! info "Source: Event [PackageStatusChanged][event-packagestatuschanged]"

### Parameters

- `Name`: The name of the package, mod, translation or tool.

### PackageAdded

```
Added '**{Name}**' with ID '**{ID}**' and version '**{Version}**'.
```

### PackageRemoved

```
Removed '**{Name}**' with ID '**{ID}**' and version '**{Version}**'.
```

### PackageHidden

```
Hidden '**{Name}**' with ID '**{ID}**' and version '**{Version}**' from view.
```

### PackageDisabled

```
Disabled '**{Name}**' with ID '**{ID}**' and version '**{Version}**'.
```

### PackageEnabled

```
Enabled '**{Name}**' with ID '**{ID}**' and version '**{Version}**'.
```

### ModAdded

```
Added mod '**{Name}**' with ID '**{ID}**' and version '**{Version}**'.
```

### ModRemoved

```
Removed mod '**{Name}**' with ID '**{ID}**' and version '**{Version}**'.
```

### ModHidden

```
Hidden mod '**{Name}**' with ID '**{ID}**' and version '**{Version}**' from view.
```

### ModDisabled

```
Disabled mod '**{Name}**' with ID '**{ID}**' and version '**{Version}**'.
```

### ModEnabled

```
Enabled mod '**{Name}**' with ID '**{ID}**' and version '**{Version}**'.
```

### TranslationAdded

```
Added translation '**{Name}**' with ID '**{ID}**' and version '**{Version}**'.
```

### TranslationRemoved

```
Removed translation '**{Name}**' with ID '**{ID}**' and version '**{Version}**'.
```

### TranslationHidden

```
Hidden translation '**{Name}**' with ID '**{ID}**' and version '**{Version}**' from view.
```

### TranslationDisabled

```
Disabled translation '**{Name}**' with ID '**{ID}**' and version '**{Version}**'.
```

### TranslationEnabled

```
Enabled translation '**{Name}**' with ID '**{ID}**' and version '**{Version}**'.
```

### ToolAdded

```
Added tool '**{Name}**' with ID '**{ID}**' and version '**{Version}**'.
```

### ToolRemoved

```
Removed tool '**{Name}**' with ID '**{ID}**' and version '**{Version}**'.
```

### ToolHidden

```
Hidden tool '**{Name}**' with ID '**{ID}**' and version '**{Version}**' from view.
```

### ToolDisabled

```
Disabled tool '**{Name}**' with ID '**{ID}**' and version '**{Version}**'.
```

### ToolEnabled

```
Enabled tool '**{Name}**' with ID '**{ID}**' and version '**{Version}**'.
```
## Package Updated

!!! info "Source: Event [PackageUpdated][event-packageupdated]"

### PackageUpdated

```
Updated '**{Name}**' from version '**{OldVersion}**' to '**{NewVersion}**'.
(ID: '{ID}').
```

### ModUpdated

```
Updated mod '**{Name}**' from version '**{OldVersion}**' to '**{NewVersion}**'.
(ID: '{ID}').
```

### TranslationUpdated

```
Updated translation '**{Name}**' from version '**{OldVersion}**' to '**{NewVersion}**'.
(ID: '{ID}').
```

### ToolUpdated

```
Updated tool '**{Name}**' from version '**{OldVersion}**' to '**{NewVersion}**'.
(ID: '{ID}').
```

## Game Launched

!!! info "Invoked by [GameLaunched][event-game-launched]"

```
Launched game at {EventTimestamp}.
```

`EventTimestamp` is human readable absolute date.
e.g. `11th of May 2020`.

## Config Updated

- `{ChangeList}` is sourced from [commit-parameters.bin][commit-parametersbin].

### Change

!!! note "This is an individual item in the `ChangeList` items below"

```
- **{Key}**: **{OldValue}** -> **{NewValue}**
```

It is sourced from [commit-parameters.bin][commit-parametersbin].

### ModConfigUpdated

!!! info "Source: Event [ConfigUpdated][event-configupdated]"

```
Updated settings for mod '**{ModName}**'.

Changes:
{ChangeList}

(ID: '{ModID}')
```

#### Generic Message

When the exact changes cannot be determined.

```
Updated settings for mod '**{ModName}**' (ID: '{ID}').
```

### ToolConfigUpdated

!!! info "Source: Event [ConfigUpdated][event-configupdated]"

```
Updated settings for tool '**{ToolName}**'.

Changes:
{ChangeList}

(ID: '{ID}')
```

#### Generic Message

When the exact changes cannot be determined.

```
Updated settings for tool '**{ToolName}**' (ID: '{ID}').
```

## Load Order Changed

!!! info "Source: Event [PackageLoadOrderChanged][event-packageloadorderchanged]"

### ModLoadOrderChanged

```
Changed load order for mod '**{Name}**' from **{OldPosition}** to **{NewPosition}**.
(ID: '{ID}')
```

### TranslationLoadOrderChanged

```
Changed load order for translation '**{Name}**' from **{OldPosition}** to **{NewPosition}**.
(ID: '{ID}')
```

## Display Setting Changed

!!! info "Source: Event [LoadoutDisplaySettingChanged][event-loadout-display-setting-changed]"

### Multiple Settings Changed

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

### LoadoutGridEnabledSortModeChanged

```
Enabled item sorting changed: '**{OldEnabledSortMode}**' to '**{NewEnabledSortMode}**'.
```

### LoadoutGridDisabledSortModeChanged

```
Changed sorting mode for disabled items from '{OldDisabledSortMode}' to '{NewDisabledSortMode}'.
```

### ModLoadOrderSortChanged
```
Load reorderer sort mode changed: '**{OldLoadOrderSort}**' to '**{NewLoadOrderSort}**'.
```

### LoadoutGridStyleChanged

```
Mod display mode changed from '{OldLoadoutGridStyle}' to '{NewLoadoutGridStyle}'.
```

## UpdateGameStoreManifest

!!! info "Source: Event [UpdateGameStoreManifest][event-updategamestoremanifest]"

!!! tip "See: [Store Data][store-data] for more info."

### Steam

```
Updated game to manifest `{ManifestId}` (from `{OldManifestId}`) on Steam.
```

### GOG

```
Updated game to version '{VersionName}' (from version `{OldVersionName}`) on GOG.
```

### Microsoft Store

```
Updated game to version '{VersionName}' (from version `{OldVersionName}`) on Xbox.
```

### Epic Games Store

```
Updated game to version '{VersionName}' (from version `{OldVersionName}`) on Epic Store.
```

### Generic Message

```
Game was updated to a new version or EXE was modified.
```

## UpdateCommandline

!!! info "Source: Event [UpdateCommandline][event-updatecommandline]"

```
Updated command line parameters from:
- `{OldCommandLine}`
to
- `{NewCommandLine}`
```

## Enumerables

The individual enum values are translated to the following.

### SortingMode

- `0`: "Unchanged"
- `1`: "Static"
- `2`: "Release Date (Ascending)"
- `3`: "Release Date (Descending)"
- `4`: "Install Date (Ascending)"
- `5`: "Install Date (Descending)"

### SortOrder

- `0`: "Unchanged"
- `1`: "Bottom to Top (First Mod Wins)"
- `2`: "Top to Bottom (Last Mod Wins)"

### GridDisplayMode

- `0`: "Unchanged"
- `1`: "List (Compact)"
- `2`: "Grid (Squares)"
- `3`: "Grid (Horizontal Rectangles, Steam Size)"
- `4`: "Grid (Vertical Rectangles, Steam Size)"

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