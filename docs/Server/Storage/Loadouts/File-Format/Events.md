!!! info "This is a full list of events that can be stored in [events.bin][events-bin]"

!!! note "All bit packed fields are in little endian unless specified otherwise."

    They are shown in lowest to highest bit order.

    So an order like `u8`, and `u24` means 0:8 bits, then 8:32 bits.

Each event is represented by a 1 byte `EventType` (denoted in section title ***in hex***).

This is a power of 2, and can be followed by a 1, 3 or 7 byte payload.<br/>
This makes each event 1, 2, 4 or 8 bytes long.

!!! tip "We take advantage of modern 64-bit processors here."

Events are read using full 8 byte reads. In practice this means processing around 2 events per read
on average (expected). For events smaller than 8 bytes, we shift left to get to next instruction.

In addition we enforce alignment on the written data. So for instance if need to write a 4 byte event
and are at offset 6, we will write a 2 byte NOP event to pad to 8 bytes. And in the next 8 byte chunk
the event will be written.

Any event needing data longer than 7 bytes, the data should be stored in another file and
accessed by index.

## An Example

Let's consider a sequence of events to illustrate how padding and reading work in this system.
We'll use a mix of different event types to show various scenarios.

### Writing Events

Suppose we want to write the following sequence of events:

1. [GameLaunched] (1 byte)
2. [PackageStatusChanged24] (4 bytes)
3. [ConfigUpdated24] (2 bytes)
4. [PackageUpdated16] (4 bytes)

Here's how these events would be written to the file:

| Byte 0-7      | Meaning                        |
| ------------- | ------------------------------ |
| `02`          | [GameLaunched] event           |
| `01 ?? ?? ??` | [PackageStatusChanged24] event |
| `00 00 00`    | NOP padding                    |
| `04 ?? ?? ??` | [ConfigUpdated24] event        |
| `17 ?? ?? ??` | [PackageUpdated24] event       |

Explanation:

- The [GameLaunched] event (`02`) takes 1 byte.
- The [PackageStatusChanged24] event (`01 XX XX XX`) takes 4 bytes.
- After these 5 bytes, we add 3 bytes of [NOP] padding (`00 00 00`) to align to the 8-byte boundary.
- The [ConfigUpdated24] event (`04 XX XX XX`) takes 4 bytes.
- The [PackageUpdated24] event (`17 XX XX XX`) takes 4 bytes.

### Reading Events

When reading these events, the system would perform full 8-byte reads:

1. First read (8 bytes): `02 01 XX XX XX 00 00 00`
    - Processes [GameLaunched] (1 byte)
    - Processes [PackageStatusChanged24] (4 bytes)
    - Skips NOP padding (3 bytes)

2. Second read (8 bytes): `04 XX XX XX 17 XX XX XX`
    - Processes [ConfigUpdated24] (4 bytes)
    - Processes [PackageUpdated24] (4 bytes)

## Optimizing for Compression

!!! tip "The events are heavily optimized to maximize compression ratios."

To achieve this we do the following:

- Padding bytes use same byte as EventType to increase repeated bytes.
    - For >=3 bytes.
    - ZStandard does not compress duplicates shorter than 3 bytes well.
- EventType(s) have forms with multiple lengths.
- The same byte should not be repeated twice.

- Use as many opcodes as possible.
    - Any unused opcodes is wasted space, don't be afraid to add more.
    - The format can always have a breaking change up until final release.

## Opcode Distribution

!!! info "The opcode distribution is arbitrary."

    And may be subject to change between versions up until final release (although unlikely).

    However backwards compatibility in the library will always be maintained.

A non-arbitrary optimization was previously considered in the form:

| Sequence | Size |
| -------- | ---- |
| 00       | 0    |
| 01       | 1    |
| 10       | 3    |
| 11       | 7    |

This would reduce (x86) code size and improve decode speed by a small amount, but is not in use here
to favour instead reducing loadout size.

!!! tip "We can instantly load last state from [Snapshots], therefore first load is not as huge a priority."

    Instead, we mainly replay the events to revert a loadout, to an earlier state, a rare event.
    It is therefore acceptable if this takes up a tiny bit longer (up to 300ms on a 100,000 event loadout).

## Event Representation

Each event is represented with something like this:

| EventType (0-7) | Field X (8-11) | Field Y (12-15) |
| --------------- | -------------- | --------------- |
| `01`            | `{XXX}`        | `{YYYY}`        |

Ranges are inclusive.

Elements in curly brackets `{}` indicate binary packing. So the payload `{XXX}` means '`X` is stored
in 3 bits'. These provide a visual representation of the ranges to prevent ambiguity.

In the EventType, the number is provided in hex. Sometimes it can be provided as a range, for example
`03` - `13`; when it is provided as a range, each entry slightly alters the behaviour of the event.

For more details, see the event specific documentation.

## [00] NOP

!!! info "Dummy no-op event for restoring alignment."

    This event is used to pad the next event to the next 8 byte boundary*

| EventType (0-7) |
| --------------- |
| `00`            |

This is used as padding if there is an event that needs to be written, but it will span over the
8 byte boundary. For example, if we've written 7 bytes and are about to write a 2 byte event.

This way we can ensure alignment is maintained.

!!! note "This is not treated as a event, it is padding."

    There are no timestamps or other data associated with this event.

## PackageStatusChanged

!!! info "A new package has been added to `Package References` and can be seen from loadout."

!!! tip "When adding a new package for the first time, i.e. `NewStatus == Added` consider using [PackageAdded](#packageadded) instead."

    This also allows you to set the initial version of the package in a single operation.

### Messages

`PackageType` is the type of package referred to by package at [PackageIdIdx].

- [PACKAGE_ADDED_V0][package-added-v0] when `NewStatus == Added` when `PackageType` is not known.
- [PACKAGE_REMOVED_V0][package-removed-v0] when `NewStatus == Removed` when `PackageType` is not known.
- [PACKAGE_HIDDEN_V0][package-hidden-v0] when `NewStatus == Hidden` when `PackageType` is not known.
- [PACKAGE_DISABLED_V0][package-disabled-v0] when `NewStatus == Disabled` when `PackageType` is not known.
- [PACKAGE_ENABLED_V0][package-enabled-v0] when `NewStatus == Enabled` when `PackageType` is not known.
- [MOD_ADDED_V0][mod-added-v0] when `NewStatus == Added` and `PackageType == Mod`.
- [MOD_REMOVED_V0][mod-removed-v0] when `NewStatus == Removed` and `PackageType == Mod`.
- [MOD_HIDDEN_V0][mod-hidden-v0] when `NewStatus == Hidden` and `PackageType == Mod`.
- [MOD_DISABLED_V0][mod-disabled-v0] when `NewStatus == Disabled` and `PackageType == Mod`.
- [MOD_ENABLED_V0][mod-enabled-v0] when `NewStatus == Enabled` and `PackageType == Mod`.
- [TRANSLATION_ADDED_V0][translation-added-v0] when `NewStatus == Added` and `PackageType == Translation`.
- [TRANSLATION_REMOVED_V0][translation-removed-v0] when `NewStatus == Removed` and `PackageType == Translation`.
- [TRANSLATION_HIDDEN_V0][translation-hidden-v0] when `NewStatus == Hidden` and `PackageType == Translation`.
- [TRANSLATION_DISABLED_V0][translation-disabled-v0] when `NewStatus == Disabled` and `PackageType == Translation`.
- [TRANSLATION_ENABLED_V0][translation-enabled-v0] when `NewStatus == Enabled` and `PackageType == Translation`.
- [TOOL_ADDED_V0][tool-added-v0] when `NewStatus == Added` and `PackageType == Tool`.
- [TOOL_REMOVED_V0][tool-removed-v0] when `NewStatus == Removed` and `PackageType == Tool`.
- [TOOL_HIDDEN_V0][tool-hidden-v0] when `NewStatus == Hidden` and `PackageType == Tool`.
- [TOOL_DISABLED_V0][tool-disabled-v0] when `NewStatus == Disabled` and `PackageType == Tool`.
- [TOOL_ENABLED_V0][tool-enabled-v0] when `NewStatus == Enabled` and `PackageType == Tool`.
- [PACKAGE_INSTALLED_AS_DEPENDENCY_V0][package-installed-as-dependency-v0] when `NewStatus == InstalledAsDependency` when `PackageType` is not known.
- [MOD_INSTALLED_AS_DEPENDENCY_V0][mod-installed-as-dependency-v0] when `NewStatus == InstalledAsDependency` and `PackageType == Mod`.
- [TRANSLATION_INSTALLED_AS_DEPENDENCY_V0][translation-installed-as-dependency-v0] when `NewStatus == InstalledAsDependency` and `PackageType == Translation`.
- [TOOL_INSTALLED_AS_DEPENDENCY_V0][tool-installed-as-dependency-v0] when `NewStatus == InstalledAsDependency` and `PackageType == Tool`.

### [01] PackageStatusChanged24

| EventType (0-7) | NewStatus (8-10) | PackageIdIdx (11-30)            | Reserved (31-31) |
| --------------- | ---------------- | ------------------------------- | ---------------- |
| `02`            | `{XXX}`          | `{YYYYY} {YYYYYYYY} {YYYYYYYY}` | `{Z}`            |

| Data Type              | Name           | Label | Description                                                      |
| ---------------------- | -------------- | ----- | ---------------------------------------------------------------- |
| [PackageStateChange]   | NewStatus      | X     | See [PackageStateChange][pkgstatechange]                         |
| `u20` ([PackageIdIdx]) | [PackageIdIdx] | Y     | [0-1M] Index of package ID in [package-ids.bin][package-ids.bin] |
| `u1`                   | Reserved       | Z     | Currently Unused                                                 |

!!! tip "For adding mods, please use [PackageAddedFull]."

## GameLaunched

!!! info "This event is extremely common. So gets its own opcode."

This event is used to indicate that the game was launched.
This event has no extra data.

!!! note "This event can be added from parsing logs."

    If the launcher detects that Reloaded has been ran through an external logger.

### Messages

- [GAME_LAUNCHED_V0][game-launched-v0] when [GameLaunched]
- [GAME_LAUNCHED_N_V0][game-launched-n-v0] when [GameLaunchedN]

### [02] GameLaunched

| EventType (0-7) |
| --------------- |
| `02`            |

### [03] GameLaunchedN

!!! info "This is equivalent to repeating [GameLaunched] event `N` times."

| EventType (0-7) | Length (8-15) |
| --------------- | ------------- |
| `03`            | `{XXXXXXXX}`  |

| Data Type | Name   | Label | Description                                                 |
| --------- | ------ | ----- | ----------------------------------------------------------- |
| `u8`      | Length | N     | [0-255] Number of times to repeat the [GameLaunched] event. |

!!! danger "This event emits N timestamps in [timestamps.bin]."

    Make sure not to miss this in the decoder!!
    This is a compression opcode over repeating the [GameLaunched] event `N` times.

## ConfigUpdated

!!! info "This event indicates that a package configuration was updated."

### Messages

- [MOD_CONFIG_UPDATED_V0][mod-config-updated-v0] when `PackageType == Mod`.
- [TOOL_CONFIG_UPDATED_V0][tool-config-updated-v0] when `PackageType == Tool`.

When the exact changes are not known, the event is [written as V1][commit-message-versioning]:

- [MOD_CONFIG_UPDATED_V1][mod-config-updated-v1] when `PackageType == Mod` and exact changes are not known.
- [TOOL_CONFIG_UPDATED_V1][tool-config-updated-v1] when `PackageType == Tool` and exact changes are not known.

### [04] - [13] ConfigUpdated24

| EventType (0-7) | [ConfigIdx] (8-21)             | [PackageIdIdx] (22-31) |
| --------------- | ------------------------------ | ---------------------- |
| `04` - `13`     | `{XXXXXXXX} {XXXXXXXX} {XXXX}` | `{YYYY} {YYYYYYYY}`    |

| Data Type              | Name           | Label | Description                                                            |
| ---------------------- | -------------- | ----- | ---------------------------------------------------------------------- |
| `u14` ([ConfigIdx])    | [ConfigIdx]    | X     | [0-16383] Index of associated configuration in [config.bin][configbin] |
| `u10` ([PackageIdIdx]) | [PackageIdIdx] | Y     | [0-1023] Index of package ID in [package-ids.bin][package-ids.bin]     |

The `EventType` has 16 reserved values, each for a different range of [PackageIdIdx].

They function as follows:

- `04` [PackageIdIdx] has range [0-1023].
- `05` [PackageIdIdx] has range [1024-2047].
- ...
- `13` [PackageIdIdx] has range [15360-16383].

i.e. Each `EventType` has a range of 256 package IDs.

### [14] ConfigUpdated32

| EventType (0-7) | Padding (8-31) | [ConfigIdx] (32-47)     | PackageIdIdx (48-63)    |
| --------------- | -------------- | ----------------------- | ----------------------- |
| `14` - `17`     | CNST           | `{XXXXXXXX} {XXXXXXXX}` | `{YYYYYYYY} {YYYYYYYY}` |

| Data Type              | Name           | Label | Description                                                              |
| ---------------------- | -------------- | ----- | ------------------------------------------------------------------------ |
| `u24`                  | Padding        | CNST  | Constant that repeats `EventType` field. Ignored. Maximizes compression. |
| `u16` ([ConfigIdx])    | [ConfigIdx]    | X     | [0-65535] Index of associated configuration in [config.bin][configbin]   |
| `u16` ([PackageIdIdx]) | [PackageIdIdx] | Y     | [0-65535] Index of package ID in [package-ids.bin][package-ids.bin]      |

### [15] ConfigUpdatedFull

| EventType (0-7) | Padding (8-23) | ConfigIdx (24-43)             | PackageIdIdx (44-63)           |
| --------------- | -------------- | ----------------------------- | ------------------------------ |
| `15`            | `15` `15`      | `{XXXXXXX} {XXXXXXXX} {XXXX}` | `{YYYY} {YYYYYYYY} {YYYYYYYY}` |

| Data Type              | Name           | Label | Description                                                         |
| ---------------------- | -------------- | ----- | ------------------------------------------------------------------- |
| `u16`                  | Padding        | `15`  | Repeats `EventType` field. Ignored. Maximizes compression.          |
| `u20` ([ConfigIdx])    | [ConfigIdx]    | X     | [0-1M] Index of associated configuration in [config.bin][configbin] |
| `u20` ([PackageIdIdx]) | [PackageIdIdx] | Y     | [0-1M] Index of package ID in [package-ids.bin][package-ids.bin]    |

## LoadoutDisplaySettingChanged

!!! info "A setting related to how mods are displayed in the UI has changed."

This is rarely changed so has a large 4-byte payload and can change multiple events at once.

### Messages

- [LOADOUT_DISPLAY_SETTINGS_CHANGED_V0][loadout-display-settings-changed-v0] when multiple settings have changed.
- [LOADOUT_GRID_ENABLED_SORT_MODE_CHANGED_V0][loadout-grid-enabled-sort-mode-changed-v0] when only `LoadoutGridEnabledSortMode` has changed.
- [LOADOUT_GRID_DISABLED_SORT_MODE_CHANGED_V0][loadout-grid-disabled-sort-mode-changed-v0] when only `LoadoutGridDisabledSortMode` has changed.
- [MOD_LOAD_ORDER_SORT_CHANGED_V0][mod-load-order-sort-changed-v0] when only `ModLoadOrderSort` has changed.
- [LOADOUT_GRID_STYLE_CHANGED_V0][loadout-grid-style-changed-v0] when only `LoadoutGridStyle` has changed.

### [16] LoadoutDisplaySettingChanged

| EventType (0-7) | Unused (8-11) | LoadoutGridEnabledSortMode (12-18) | LoadoutGridDisabledSortMode (19-25) | ModLoadOrderSort (26-27) | LoadoutGridStyle (28-31) |
| --------------- | ------------- | ---------------------------------- | ----------------------------------- | ------------------------ | ------------------------ |
| `16`            |               | `{WWWWWWW}`                        | `{XXXXXXX}`                         | `{YY}`                   | `{ZZZZ}`                 |

| Data Type                                 | Name                        | Label | Description                                     |
| ----------------------------------------- | --------------------------- | ----- | ----------------------------------------------- |
| `u7` [(SortingMode)][sortingmode]         | LoadoutGridEnabledSortMode  | W     | Sorting mode for enabled items in LoadoutGrid.  |
| `u7` [(SortingMode)][sortingmode]         | LoadoutGridDisabledSortMode | X     | Sorting mode for disabled items in LoadoutGrid. |
| `u2` [(SortOrder)][sortorder]             | ModLoadOrderSort            | Y     | Sorting mode for load order reorderer.          |
| `u4` [(GridDisplayMode)][griddisplaymode] | LoadoutGridStyle            | Z     | Display mode for LoadoutGrid.                   |

## PackageVersionChanged

!!! info "This event indicates that a package has been updated to a new version."

This upgrades a package at [PackageIdIdx] from the old (previous) version to the new version at `NewPackageVerIdx`.

!!! note "`NewPackageVerIdx` can point to either a newly written manifest or a previous one"

    It's a previous one in case of a rollback/undo, otherwise it's a new one.

### Messages

- [PACKAGE_UPDATED_V0][package-updated-v0] when `PackageType` is not known.
- [MOD_UPDATED_V0][mod-updated-v0] when `PackageType == Mod`.
- [TRANSLATION_UPDATED_V0][translation-updated-v0] when `PackageType == Translation`.
- [TOOL_UPDATED_V0][tool-updated-v0] when `PackageType == Tool`.

### [17] PackageUpdated24

| EventType (0-7) | OldPackageVerIdx (8-19) | NewPackageVerIdx (20-31) |
| --------------- | ----------------------- | ------------------------ |
| `17`            | `{XXXXXXXX} {XXXX}`     | `{YYYY} {YYYYYYYY}`      |

| Data Type              | Name             | Label | Description                                                               |
| ---------------------- | ---------------- | ----- | ------------------------------------------------------------------------- |
| `u12` ([PackageIdIdx]) | OldPackageVerIdx | X     | [0-4095] Index of old version in [Package References][packagemetadatabin] |
| `u12` ([PackageIdIdx]) | NewPackageVerIdx | Y     | [0-4095] Index of new version in [Package References][packagemetadatabin] |

The `EventType` has 16 reserved values, each for a different range of [PackageIdIdx].

### [18] PackageUpdatedFull

| EventType (0-7) | Padding (8-23) | OldPackageVerIdx (24-43)      | NewPackageVerIdx (44-63)       |
| --------------- | -------------- | ----------------------------- | ------------------------------ |
| `18`            | `18 18`        | `{XXXXXXX} {XXXXXXXX} {XXXX}` | `{YYYY} {YYYYYYYY} {YYYYYYYY}` |

| Data Type              | Name             | Label | Description                                                             |
| ---------------------- | ---------------- | ----- | ----------------------------------------------------------------------- |
| `u16`                  | Padding          | `18`  | Repeats `EventType` field. Ignored. Maximizes compression.              |
| `u20` ([PackageIdIdx]) | OldPackageVerIdx | X     | [0-1M] Index of old version in [Package References][packagemetadatabin] |
| `u20` ([PackageIdIdx]) | NewPackageVerIdx | Y     | [0-1M] Index of new version in [Package References][packagemetadatabin] |

## PackageLoadOrderChanged

!!! info "This event indicates that the load order of packages has changed."

| Name        | Description                                |
| ----------- | ------------------------------------------ |
| OldPosition | Old position of the mod in the load order. |
| NewPosition | New position of the mod in the load order. |

!!! note "By default, we logically put every added mod to the end of the load order."

    So if you add `A` then `B`, `A` will be at 0 (loads first) and `B` will be at 1.
    If we want to move `B` above `A`, we set an event with `OldPosition = 1` and `NewPosition = 0`.

!!! warning "Efficient reordering is nontrivial"

Based on end-user usage patterns however, I've come up with a fairly efficient way to handle this.
Suppose you have a list of mods and a list of indices pointing to the `mods` array.

```rust
let mods = vec![Mod; 10];
let mod_indices: Vec<u16> = vec![0, 1, 2, 3, 4, 5, 6, 7, 8, 9];
```

When we decide to move item #9 to #4 spot the indices would become:

```
0, 1, 2, 8, 3, 4, 5, 6, 7, 9
```

This can be visualized with two pointers:

```
         L              R
         ↓              ↓
0, 1, 2, 3, 4, 5, 6, 7, 8, 9
```

In this case we have to shift all of the elements at `L` up till `R-1` by one spot.

```
         L              R
         ↓              ↓
0, 1, 2, 3, 3, 4, 5, 6, 7, 9
```

And then write the value of `R` into `L`.

```
0, 1, 2, 8, 3, 4, 5, 6, 7, 9
```

In the opposite case, where the new index is higher than the previous,
we simply switch the roles of `L` and `R`.

First we shift all of the elements from `R` to `L+1` down by one spot.
And then write the previous value of `L` into `R`.

The other neat part is we can add mods while preserving the sort, since
every mod goes to end of the list with last index by default.

!!! question "But what are the performance characteristics of this?"

Moving an item `N` spaces, means doing a memory copy of `N*2` bytes.
This is because this is essentially an overlapping memory copy. i.e. `memmove`.
And we represent each index using 2 bytes.

!!! note "We can dynamically switch to 4 bytes on over 65536 mods."

Speed of memory move here is roughly 20GB/s on a DDR4-3200 system.

In a slightly unrealistic scenario of a 10000 mod loadout. Assuming mods were moved 10000 times, at an average of
(10000/2) spaces each time, this would mean a copy of `10000 * 5000 * 2 = 100MB` of data.

Or roughly `5ms` seconds of time, before factoring additional inefficiencies of small copies.
On something like a GameCube, `50ms`.

### Messages

- [MOD_LOAD_ORDER_CHANGED_V0][mod-load-order-changed-v0] when `PackageType == Mod`.
- [TRANSLATION_LOAD_ORDER_CHANGED_V0][translation-load-order-changed-v0] when `PackageType == Translation`.

### [19] PackageLoadOrderChanged16

| EventType (0-7) | OldPosition (8-15) | NewPosition (16-23) |
| --------------- | ------------------ | ------------------- |
| `19`            | `{XXXXXXXX}`       | `{YYYYYYYY}`        |

| Data Type | Name        | Label | Description                                        |
| --------- | ----------- | ----- | -------------------------------------------------- |
| `u8`      | OldPosition | X     | [0-255] Old position of the mod in the load order. |
| `u8`      | NewPosition | Y     | [0-255] New position of the mod in the load order. |

### [1A] PackageLoadOrderChanged24

| EventType (0-7) | OldPosition (8-19)  | NewPosition (20-31) |
| --------------- | ------------------- | ------------------- |
| `1A`            | `{XXXXXXXX} {XXXX}` | `{YYYY} {YYYYYYYY}` |

| Data Type | Name        | Label | Description                                         |
| --------- | ----------- | ----- | --------------------------------------------------- |
| `u12`     | OldPosition | X     | [0-4095] Old position of the mod in the load order. |
| `u12`     | NewPosition | Y     | [0-4095] New position of the mod in the load order. |

### [1B] PackageLoadOrderMovedToBottom24

Optimized form for common action of moving a mod to the bottom of the load order.

| EventType (0-7) | OldPosition (8-27)             | OffsetFromBottom (28-31) |
| --------------- | ------------------------------ | ------------------------ |
| `1B`            | `{XXXX} {XXXXXXXX} {XXXXXXXX}` | `{YYY}`                  |

| Data Type | Name             | Label | Description                                       |
| --------- | ---------------- | ----- | ------------------------------------------------- |
| `u20`     | OldPosition      | X     | [0-1M] Old position of the mod in the load order. |
| `u4`      | OffsetFromBottom | Y     | [0-15] Offset from bottom.                        |

### [1C] PackageLoadOrderMovedToTop24

Optimized form for common action of moving a mod to the top of the load order.

| EventType (0-7) | OldPosition (8-27)             | OffsetFromTop (28-31) |
| --------------- | ------------------------------ | --------------------- |
| `1C`            | `{XXXX} {XXXXXXXX} {XXXXXXXX}` | `{YYY}`               |

| Data Type | Name          | Label | Description                                       |
| --------- | ------------- | ----- | ------------------------------------------------- |
| `u20`     | OldPosition   | X     | [0-1M] Old position of the mod in the load order. |
| `u4`      | OffsetFromTop | Y     | [0-15] Offset from top.                           |

### [1D] PackageLoadOrderChanged32

| EventType (0-7) | Padding (8-23) | OldPosition (24-43)           | NewPosition (44-63)            |
| --------------- | -------------- | ----------------------------- | ------------------------------ |
| `1D`            | `1D` `1D`      | `{XXXXXXX} {XXXXXXXX} {XXXX}` | `{YYYY} {YYYYYYYY} {YYYYYYYY}` |

| Data Type              | Name           | Label | Description                                                |
| ---------------------- | -------------- | ----- | ---------------------------------------------------------- |
| `u16`                  | Padding        | `1D`  | Repeats `EventType` field. Ignored. Maximizes compression. |
| `u20` ([ConfigIdx])    | [ConfigIdx]    | X     | [0-1M] Old position of the mod in the load order.          |
| `u20` ([PackageIdIdx]) | [PackageIdIdx] | Y     | [0-1M] New position of the mod in the load order.          |

## UpdateGameStoreManifest

!!! info "This is used for upgrading/downgrading a game on supported stores."

And also just seeing when the game got updated.

This sets an index of the new game version in the `NewRevision` field.

This revision corresponds to an entry in the [stores.bin][stores-bin] file.

This event is emitted the files of the game match a known new store manifest/revision.

### Messages

- [UPDATE_GAME_STORE_MANIFEST_V0][update-game-store-manifest-v0]
- [UPDATE_GAME_STORE_MANIFEST_STEAM_V0][update-game-store-manifest-steam-v0] when the store is Steam.
- [UPDATE_GAME_STORE_MANIFEST_GOG_V0][update-game-store-manifest-gog-v0] when the store is GOG.
- [UPDATE_GAME_STORE_MANIFEST_XBOX_V0][update-game-store-manifest-xbox-v0] when the store is Microsoft (Xbox) Store.
- [UPDATE_GAME_STORE_MANIFEST_EGS_V0][update-game-store-manifest-egs-v0] when the store is Epic Games Store.

### [1E] UpdateGameStoreManifest8

| EventType (0-7) | NewRevision (8-15) |
| --------------- | ------------------ |
| `1E`            | `{XXXXXXXX}`       |

| Data Type         | Name        | Label | Description                        |
| ----------------- | ----------- | ----- | ---------------------------------- |
| `u8` (GameVerIdx) | NewRevision | X     | [0-255] New game version revision. |

### [1F] UpdateGameStoreManifest24

!!! note "Unlikely this will ever be used, but just in case."

| EventType (0-7) | NewRevision (8-31)                 |
| --------------- | ---------------------------------- |
| `1F`            | `{XXXXXXXX} {XXXXXXXX} {XXXXXXXX}` |

| Data Type         | Name        | Label | Description                          |
| ----------------- | ----------- | ----- | ------------------------------------ |
| `u8` (GameVerIdx) | NewRevision | X     | [0-16.8M] New game version revision. |

## UpdateCommandline

!!! info "This event updates the commandline parameters passed to the game."

!!! note "Restricted to 255 characters arbitrarily."

    If someone needs a longer commandline, just make an issue please.
    We could encode that as null terminated, probably, while keeping the space savings intact.

### Messages

- [UPDATE_COMMANDLINE_V0][update-commandline]

### [20] UpdateCommandline8

| EventType (0-7) | Length (8-15) |
| --------------- | ------------- |
| `20`            | `{XXXXXXXX}`  |

| Data Type | Name   | Label | Description                                                                                                      |
| --------- | ------ | ----- | ---------------------------------------------------------------------------------------------------------------- |
| `u8`      | Length | X     | [0-255] Length of new commandline parameters in [commandline-parameter-data.bin][commandline-parameter-data.bin] |

## ExternalConfigUpdated

!!! info "This event indicates that an external config file belonging to a package has been updated."

### Messages

- [EXTERNAL_CONFIG_UPDATED_V0][external-config-updated-v0]

### [21] ExternalConfigUpdated24

| EventType (0-7) | PathIndex (8-14) | FileIndex (15-21) | PackageIdIdx (22-31) |
| --------------- | ---------------- | ----------------- | -------------------- |
| `21`            | `{XXX} {XXXX}`   | `{YYY} {YYYY}`    | `{ZZZZ} {ZZZZZZZZ}`  |

| Data Type              | Name           | Label | Description                                                                          |
| ---------------------- | -------------- | ----- | ------------------------------------------------------------------------------------ |
| `u7`                   | PathIndex      | X     | [0-127] Index of file in [external-config.bin][external-config-bin]                  |
| `u7`                   | FileIndex      | Y     | [0-127] Index of file path in [external-config-paths.bin][external-config-paths-bin] |
| `u10` ([PackageIdIdx]) | [PackageIdIdx] | Z     | [0-1024] Index of package ID in [package-ids.bin][package-ids.bin]                   |

### [22] ExternalConfigUpdated56

| EventType (0-7) | PathIndex (8-25)             | FileIndex (26-43)            | [PackageIdIdx] (44-63)         |
| --------------- | ---------------------------- | ---------------------------- | ------------------------------ |
| `22`            | `{XXXXXXXX} {XXXXXXXX} {XX}` | `{YYYYYY} {YYYYYYYY} {YYYY}` | `{ZZZZ} {ZZZZZZZZ} {ZZZZZZZZ}` |

| Data Type            | Name         | Label | Description                                                                           |
| -------------------- | ------------ | ----- | ------------------------------------------------------------------------------------- |
| `u18`                | PathIndex    | X     | [0-256K] Index of file in [external-config.bin][external-config-bin]                  |
| `u18`                | FileIndex    | Y     | [0-256K] Index of file path in [external-config-paths.bin][external-config-paths-bin] |
| `u20` (PackageIdIdx) | PackageIdIdx | Z     | [0-1M] Index of package ID in [package-ids.bin][package-ids.bin]                      |

## PackageEnabled

!!! info "A package has been enabled."

    This is analogous to enabling a mod in the loadout.

    This is an optimization over the full length ([PackageStatusChanged](#packagestatuschanged)) event;

Usually a user would just enable a mod and leave it at that. So [PackageEnabled](#packageenabled) (this)
is expected to be a bit more common than [PackageDisabled](#packagedisabled).

For this reason, the two events have been separated, in case we want to have different event type
opcode ranges for them.

### Messages

`PackageType` is the type of package referred to by package at [PackageIdIdx].

- [PACKAGE_ENABLED_V0][package-enabled-v0] `PackageType` is not known.
- [MOD_ENABLED_V0][mod-enabled-v0] `PackageType == Mod`.
- [TRANSLATION_ENABLED_V0][translation-enabled-v0] `PackageType == Translation`.
- [TOOL_ENABLED_V0][tool-enabled-v0] when `PackageType == Tool`.

### [23] - [52] PackageEnabled8

| EventType (0-7) | [PackageIdIdx] (8-15) |
| --------------- | --------------------- |
| `23` - `52`     | `{XXXXXXXX}`          |

| Data Type             | Name           | Label | Description                                                       |
| --------------------- | -------------- | ----- | ----------------------------------------------------------------- |
| `u8` ([PackageIdIdx]) | [PackageIdIdx] | X     | [0-255] Index of package ID in [package-ids.bin][package-ids.bin] |

The `EventType` has 48 reserved values, each for a different range of [PackageIdIdx].

They function as follows:

- `23` [PackageIdIdx] has range [0-255].
- `24` [PackageIdIdx] has range [256-511].
- ...
- `52` [PackageIdIdx] has range [12032-12287].

!!! info "There is no `PackageEnabled24` variant, instead use [PackageStatusChanged24][PackageStatusChanged24]."

## PackageDisabled

!!! info "A package has been disabled."

    This is analogous to disabling a mod in the loadout.

    This is an optimization over the full length ([PackageStatusChanged](#packagestatuschanged)) event;

Please also see optimization note at start of [PackageEnabled](#packageenabled).

### Messages

`PackageType` is the type of package referred to by package at [PackageIdIdx].

- [PACKAGE_DISABLED_V0][package-disabled-v0] when `PackageType` is not known.
- [MOD_DISABLED_V0][mod-disabled-v0] when `PackageType == Mod`.
- [TRANSLATION_DISABLED_V0][translation-disabled-v0] when `PackageType == Translation`.
- [TOOL_DISABLED_V0][tool-disabled-v0] when `PackageType == Tool`.

### [53] - [82] PackageDisabled8

| EventType (0-7) | [PackageIdIdx] (8-15) |
| --------------- | --------------------- |
| `53` - `82`     | `{XXXXXXXX}`          |

The `EventType` has 48 reserved values, each for a different range of [PackageIdIdx].

They function as follows:

- `53` [PackageIdIdx] has range [0-255].
- `54` [PackageIdIdx] has range [256-511].
- ...
- `82` [PackageIdIdx] has range [12032-12287].

!!! info "There is no `PackageDisabled24` variant, instead use [PackageStatusChanged24]."

## PackageAdded

!!! info "This is a specialized case for adding a new package."

    This is equivalent to adding a new package ([PackageStatusChanged](#packagestatuschanged)) and
    setting its initial version ([PackageVersionChanged](#packageversionchanged)) in a single operation.

### Messages

- [PACKAGE_ADDED_V0][package-added-v0] when `PackageType` is not known.
- [MOD_ADDED_V0][mod-added-v0] when `PackageType == Mod`.
- [TRANSLATION_ADDED_V0][translation-added-v0] when `PackageType == Translation`.
- [TOOL_ADDED_V0][tool-added-v0] when `PackageType == Tool`.

### [83] - [85] PackageAdded24

| EventType (0-7) | [PackageVerIdx]  (8-17) | [PackageIdIdx] (18-31) |
| --------------- | ----------------------- | ---------------------- |
| `83` - `85`     | `{XXXXXXXX} {XX}`       | `{YYYYYY} {YYYYYYYY}`  |

The `EventType` has 3 reserved values to act as an offset to the [PackageVerIdx] field.

Reference:

- `83` [PackageVerIdx] has range [0-1023].
- `84` [PackageVerIdx] has range [1024-2047].
- `85` [PackageVerIdx] has range [2048-3071].

### [86] PackageAddedFull

| EventType (0-7) | Reserved (8-23) | NewStatus (24-43)                   | PackageIdIdx (44-63)             |
| --------------- | --------------- | ----------------------------------- | -------------------------------- |
| `86`            | `86 86`         | `{XX} {XXXXXXXX} {XXXXXXXX}` `{XX}` | `{YYYYYY} {YYYYYYYY} {YYYYYYYY}` |

| Data Type               | Name            | Label | Description                                                                 |
| ----------------------- | --------------- | ----- | --------------------------------------------------------------------------- |
| `u16`                   | Reserved        | 86    | Reserved. Constant `CE` to improve compression.                             |
| `u20` ([PackageVerIdx]) | [PackageVerIdx] | X     | [0-1M] Index of the version in [package-versions.bin][package-versions.bin] |
| `u20` ([PackageIdIdx])  | [PackageIdIdx]  | Y     | [0-1M] Index of package ID in [package-ids.bin][package-ids.bin]            |

The `EventType` has 8 reserved values to act as an offset to the [PackageVerIdx] field.

## PackageAddedWithConfig

!!! info "This is a specialized case that also updates config directly after [adding a versioned package](#packageadded)."

### Messages

First message is one of the following:

- [PACKAGE_ADDED_WITH_CONFIG_V0][package-added-with-config-v0] when `PackageType` is not known.
- [MOD_ADDED_WITH_CONFIG_V0][mod-added-with-config-v0] when `PackageType == Mod`.
- [TRANSLATION_ADDED_WITH_CONFIG_V0][translation-added-with-config-v0] when `PackageType == Translation`.
- [TOOL_ADDED_WITH_CONFIG_V0][tool-added-with-config-v0] when `PackageType == Tool`.

When the exact changes are not known, the event is [written as V1][commit-message-versioning]:

- [PACKAGE_ADDED_WITH_CONFIG_V1][package-added-with-config-v1] when `PackageType` is not known.
- [MOD_ADDED_WITH_CONFIG_V1][mod-added-with-config-v1] when `PackageType == Mod`.
- [TRANSLATION_ADDED_WITH_CONFIG_V1][translation-added-with-config-v1] when `PackageType == Translation`.
- [TOOL_ADDED_WITH_CONFIG_V1][tool-added-with-config-v1] when `PackageType == Tool`.

### [87] PackageAddedWithConfig

!!! info "This also sets the initial config file (i.e. [ConfigUpdated](#configupdated)) when the package is added."

    In the case the user downloads a package and configures it directly after.

| EventType (0-7) | [ConfigIdx] (8-23)    | NewStatus (24-43)                   | PackageIdIdx (44-63)             |
| --------------- | --------------------- | ----------------------------------- | -------------------------------- |
| `87`            | `{XXXXXXXX XXXXXXXX}` | `{YY} {YYYYYYYY} {YYYYYYYY}` `{YY}` | `{ZZZZZZ} {ZZZZZZZZ} {ZZZZZZZZ}` |

| Data Type               | Name            | Label | Description                                                                 |
| ----------------------- | --------------- | ----- | --------------------------------------------------------------------------- |
| `u16` ([ConfigIdx])     | [ConfigIdx]     | X     | [0-65535] Index of associated configuration in [config.bin][configbin]      |
| `u20` ([PackageVerIdx]) | [PackageVerIdx] | Y     | [0-1M] Index of the version in [package-versions.bin][package-versions.bin] |
| `u20` ([PackageIdIdx])  | [PackageIdIdx]  | Z     | [0-1M] Index of package ID in [package-ids.bin][package-ids.bin]            |

## PackageVersion100Added

!!! info "`1.0.0` is by far the most common version for a new package."

    Because many mods don't get updated. So we can exploit this for some additional compression wins.

This is an optimized form of [PackageAdded](#packageadded) for the common case of adding a new
package with version `1.0.0`.

### Messages

- [PACKAGE_ADDED_V0][package-added-v0] when `PackageType` is not known.
- [MOD_ADDED_V0][mod-added-v0] when `PackageType == Mod`.
- [TRANSLATION_ADDED_V0][translation-added-v0] when `PackageType == Translation`.
- [TOOL_ADDED_V0][tool-added-v0] when `PackageType == Tool`.

### [88] - [B7] PackageAddedVersion100_8

| EventType (0-7) | [PackageIdIdx] (8-15) |
| --------------- | --------------------- |
| `88` - `B7`     | `{XXXXXXXX}`          |

| Data Type             | Name           | Label | Description                                                       |
| --------------------- | -------------- | ----- | ----------------------------------------------------------------- |
| `u8` ([PackageIdIdx]) | [PackageIdIdx] | X     | [0-255] Index of package ID in [package-ids.bin][package-ids.bin] |

The `EventType` has 48 reserved values to act as an offset to the [PackageIdIdx] field.

Reference:

- `88` [PackageIdIdx] has range [0-255].
- ...
- `B7` [PackageIdIdx] has range [12032-12287].

[configbin]: Unpacked.md#configbin
[events-bin]: Unpacked.md#eventsbin
[packagemetadatabin]: Unpacked.md#packages
[package-ids.bin]: Unpacked.md#package-idsbin
[package-versions.bin]: ./Unpacked.md#package-versionsbin
[package-added-v0]: ./Commit-Messages.md#package_added_v0
[package-removed-v0]: ./Commit-Messages.md#package_removed_v0
[package-hidden-v0]: ./Commit-Messages.md#package_hidden_v0
[package-disabled-v0]: ./Commit-Messages.md#package_disabled_v0
[package-enabled-v0]: ./Commit-Messages.md#package_enabled_v0
[mod-added-v0]: ./Commit-Messages.md#mod_added_v0
[mod-removed-v0]: ./Commit-Messages.md#mod_removed_v0
[mod-hidden-v0]: ./Commit-Messages.md#mod_hidden_v0
[mod-disabled-v0]: ./Commit-Messages.md#mod_disabled_v0
[mod-enabled-v0]: ./Commit-Messages.md#mod_enabled_v0
[translation-added-v0]: ./Commit-Messages.md#translation_added_v0
[translation-removed-v0]: ./Commit-Messages.md#translation_removed_v0
[translation-hidden-v0]: ./Commit-Messages.md#translation_hidden_v0
[translation-disabled-v0]: ./Commit-Messages.md#translation_disabled_v0
[translation-enabled-v0]: ./Commit-Messages.md#translation_enabled_v0
[tool-added-v0]: ./Commit-Messages.md#tool_added_v0
[tool-removed-v0]: ./Commit-Messages.md#tool_removed_v0
[tool-hidden-v0]: ./Commit-Messages.md#tool_hidden_v0
[tool-disabled-v0]: ./Commit-Messages.md#tool_disabled_v0
[tool-enabled-v0]: ./Commit-Messages.md#tool_enabled_v0
[package-updated-v0]: ./Commit-Messages.md#package_updated_v0
[mod-updated-v0]: ./Commit-Messages.md#mod_updated_v0
[translation-updated-v0]: ./Commit-Messages.md#translation_updated_v0
[tool-updated-v0]: ./Commit-Messages.md#tool_updated_v0
[event-packageloadorderchanged]: ./Events.md#packageloadorderchanged
[mod-load-order-changed-v0]: ./Commit-Messages.md#mod_load_order_changed_v0
[translation-load-order-changed-v0]: ./Commit-Messages.md#translation_load_order_changed_v0
[mod-config-updated-v0]: ./Commit-Messages.md#mod_config_updated_v0
[tool-config-updated-v0]: ./Commit-Messages.md#tool_config_updated_v0
[loadout-display-settings-changed-v0]: ./Commit-Messages.md#loadout_display_settings_changed_v0
[loadout-grid-enabled-sort-mode-changed-v0]: ./Commit-Messages.md#loadout_grid_enabled_sort_mode_changed_v0
[loadout-grid-disabled-sort-mode-changed-v0]: ./Commit-Messages.md#loadout_grid_disabled_sort_mode_changed_v0
[mod-load-order-sort-changed-v0]: ./Commit-Messages.md#mod_load_order_sort_changed_v0
[loadout-grid-style-changed-v0]: ./Commit-Messages.md#loadout_grid_style_changed_v0
[game-launched-v0]: ./Commit-Messages.md#game_launched_v0
[stores-bin]: ./Unpacked.md#storesbin
[commandline-parameter-data.bin]: ./Unpacked.md#commandline-parameter-databin
[update-game-store-manifest-v0]: ./Commit-Messages.md#update_game_store_manifest_v0
[update-game-store-manifest-steam-v0]: ./Commit-Messages.md#update_game_store_manifest_steam_v0
[update-game-store-manifest-gog-v0]: ./Commit-Messages.md#update_game_store_manifest_gog_v0
[update-game-store-manifest-egs-v0]: ./Commit-Messages.md#update_game_store_manifest_egs_v0
[update-game-store-manifest-xbox-v0]: ./Commit-Messages.md#update_game_store_manifest_xbox_v0
[update-commandline]: ./Commit-Messages.md#update_commandline_v0
[featuresbin]: ./About.md#featuresbin
[pkgstatechange]: ./DataTypes.md#packagestatechange
[PackageStateChange]: ./DataTypes.md#packagestatechange
[sortingmode]: ./DataTypes.md#sortingmode
[sortorder]: ./DataTypes.md#sortorder
[griddisplaymode]: ./DataTypes.md#griddisplaymode
[mod-config-updated-v1]: ./Commit-Messages.md#mod_config_updated_v1
[tool-config-updated-v1]: ./Commit-Messages.md#tool_config_updated_v1
[commit-message-versioning]: ./Unpacked.md#commit-parameters-versionsbin
[package-installed-as-dependency-v0]: ./Commit-Messages.md#package_installed_as_dependency_v0
[mod-installed-as-dependency-v0]: ./Commit-Messages.md#mod_installed_as_dependency_v0
[translation-installed-as-dependency-v0]: ./Commit-Messages.md#translation_installed_as_dependency_v0
[tool-installed-as-dependency-v0]: ./Commit-Messages.md#tool_installed_as_dependency_v0
[external-config-bin]: ./Unpacked.md#external-configbin
[external-config-paths-bin]: ./Unpacked.md#external-config-pathsbin
[external-config-refs]: ./Unpacked.md#external-config-refsbin
[external-config-updated-v0]: ./Commit-Messages.md#external_config_updated_v0
[PackageIdIdx]: ./DataTypes.md
[PackageVerIdx]: ./DataTypes.md
[PackageEnabledStateChange]: ./DataTypes.md#packageenabledstatechange
[PackageInstallStateChange]: ./DataTypes.md#packageinstallstatechange
[Snapshots]: ./Snapshot.md
[ConfigIdx]: ./DataTypes.md
[ExternalConfigIdx]: ./DataTypes.md
[package-added-with-config-v0]: ./Commit-Messages.md#package-added-with-config-v0
[mod-added-with-config-v0]: ./Commit-Messages.md#mod_added_with_config_v0
[translation-added-with-config-v0]: ./Commit-Messages.md#translation_added_with_config_v0
[tool-added-with-config-v0]: ./Commit-Messages.md#tool_added_with_config_v0
[package-added-with-config-v1]: ./Commit-Messages.md#package_added_with_config_v1
[mod-added-with-config-v1]: ./Commit-Messages.md#mod_added_with_config_v1
[translation-added-with-config-v1]: ./Commit-Messages.md#translation_added_with_config_v1
[tool-added-with-config-v1]: ./Commit-Messages.md#tool_added_with_config_v1
[PackageAddedFull]: #ce-packageaddedfull
[GameLaunched]: #gamelaunched
[timestamps.bin]: ./Unpacked.md#timestampsbin
[GameLaunchedN]: ./Commit-Messages.md#game_launched_n_v0
[ConfigUpdated24]: #21-externalconfigupdated24
[PackageStatusChanged24]: #packagestatuschanged
[PackageUpdated16]: #1005-packageupdated16
[NOP]: #00-nop