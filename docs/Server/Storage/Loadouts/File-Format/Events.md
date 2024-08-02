!!! info "This is a full list of events that can be stored in [events.bin][events-bin]"

!!! note "All bit packed fields are in little endian unless specified otherwise."

    They are shown in lowest to highest bit order.

    So an order like `u8`, and `u24` means 0:8 bits, then 8:32 bits.

Each event is represented by a 1 byte `EventType` (denoted in section title).

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

!!! note "`EventType` 0xF0 - 0xFF are 2 byte codes."

    This allows extending the total number of opcodes to 4336.

## An Example

Let's consider a sequence of events to illustrate how padding and reading work in this system.
We'll use a mix of different event types to show various scenarios.

### Writing Events

Suppose we want to write the following sequence of events:

1. [GameLaunched](#gamelaunched) (1 byte)
2. [PackageStatusChanged8](#0100-packagestatuschanged8) (2 bytes)
3. [ConfigUpdated8](#0101-configupdated8) (2 bytes)
4. [PackageUpdated16](#1005-packageupdated16) (4 bytes)

Here's how these events would be written to the file:

```
| Byte 0-7    | Meaning                                                    |
| ----------- | ---------------------------------------------------------- |
| 01          | [GameLaunched](#gamelaunched) event                        |
| 40 ??       | [PackageStatusChanged8](#0100-packagestatuschanged8) event |
| 41 ??       | [ConfigUpdated8](#0101-configupdated8) event               |
| 00 00 00    | NOP padding to align next event to 8-byte boundary         |
| 85 85 ?? ?? | [PackageUpdated16](#1005-packageupdated16) event           |
```

Explanation:

- The [GameLaunched](#gamelaunched) event (`01`) takes 1 byte.
- The [PackageStatusChanged8](#0100-packagestatuschanged8) event (`40 XX`) takes 2 bytes.
- The [ConfigUpdated8](#0101-configupdated8) event (`41 XX`) takes 2 bytes.
- At this point, we've written 5 bytes. To ensure the next 4-byte event ([PackageUpdated16](#1005-packageupdated16)) starts on an 8-byte boundary, we add 3 bytes of [NOP](#0000-nop) padding (`00 00 00`).
- Finally, we write the [PackageUpdated16](#1005-packageupdated16) event (`85 85 XX XX`), which takes 4 bytes.

### Reading Events

When reading these events, the system would perform full 8-byte reads:

1. First read (8 bytes): `01 40 ?? 41 ?? 00 00 00`
    - Processes [GameLaunched](#gamelaunched) (1 byte)
    - Processes [PackageStatusChanged8](#0100-packagestatuschanged8) (2 bytes)
    - Processes [ConfigUpdated8](#0101-configupdated8) (2 bytes)
    - Skips NOP padding (3 bytes)

2. Second read (8 bytes): `85 85 ?? ?? ?? ?? ?? ??`
   - Processes [PackageUpdated16](#1005-packageupdated16) (4 bytes)
   - The last 2 bytes (XX XX) would be the start of the next event or additional padding

## Optimizing for Compression

!!! tip "The events are heavily optimized to maximize compression ratios."

To achieve this we do the following:

- Padding bytes use same byte as EventType to increase repeated bytes.
- EventType(s) have forms with multiple lengths (to minimize unused bytes).

## Event Ranges

The payload size is determined by the 2 high bits of the event type.

| Sequence | Size |
| -------- | ---- |
| 00       | 0    |
| 01       | 1    |
| 10       | 3    |
| 11       | 7    |

This leaves the remaining next 6 bits (0-63) for the event type.

i.e. `{YY}{XXXXXX}`.

## Event Representation

Each event is represented with something like this:

| EventType (0-7)  | Field X (8-11) | Field Y (12-15) |
| ---------------- | -------------- | --------------- |
| 01 (`{00} + 01`) | `{XXX}`        | `{YYYY}`        |

Ranges are inclusive.

Elements in curly brackets `{}` indicate binary packing. So the payload `{XXX}` means '`X` is stored
in 3 bits'. These provide a visual representation of the ranges to prevent ambiguity.

In the EventType, the `{00}` denotes the size prefix, and the `+` shows the offset into
the given prefix (0-63, in hex).

## {00}+00: NOP

!!! info "Dummy no-op event for restoring alignment."

    This event is used to pad the next event to the next 8 byte boundary*

| EventType (0-7)  |
| ---------------- |
| 00 (`{00} + 00`) |

This is used as padding if there is an event that needs to be written, but it will span over the
8 byte boundary. For example, if we've written 7 bytes and are about to write a 2 byte event.

This way we can ensure alignment is maintained.

!!! note "This is not treated as a event, it is padding."

    There are no timestamps or other data associated with this event.

## PackageStatusChanged

!!! info "A new package has been added to `Package References` and can be seen from loadout."

### Messages

`PackageType` is the type of package referred to `MetadataIdx`.

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

### {01}+00: PackageStatusChanged8

| EventType (0-7)  | NewStatus (8-10) | MetadataIdx (11-15) |
| ---------------- | ---------------- | ------------------- |
| 40 (`{01} + 00`) | `{XXX}`          | `{YYYYY}`           |

| Data Type          | Name        | Label | Description                                                          |
| ------------------ | ----------- | ----- | -------------------------------------------------------------------- |
| PackageStateChange | NewStatus   | X     | See [PackageStateChange][pkgstatechange]                             |
| `u5`               | MetadataIdx | Y     | [0-31] Index of metadata in [Package References][packagemetadatabin] |

### {10}+00: PackageStatusChanged16

| EventType (0-7)  | Padding (8-15) | NewStatus (16-18) | MetadataIdx (19-31)  |
| ---------------- | -------------- | ----------------- | -------------------- |
| 80 (`{10} + 00`) | 80             | `{XXX}`           | `{YYYYY} {YYYYYYYY}` |

| Data Type          | Name        | Label | Description                                                            |
| ------------------ | ----------- | ----- | ---------------------------------------------------------------------- |
| `u8`               | Padding     | 80    | Constant `80`. Repeats previous byte.                                  |
| PackageStateChange | NewStatus   | X     | See [PackageStateChange][pkgstatechange]                               |
| `u13`              | MetadataIdx | Y     | [0-8192] Index of metadata in [Package References][packagemetadatabin] |

### {10}+01: PackageStatusChanged24

| EventType (0-7)  | NewStatus (8-10) | MetadataIdx (11-31)             |
| ---------------- | ---------------- | ------------------------------- |
| 81 (`{10} + 01`) | `{XXX}`          | `{YYYYY} {YYYYYYYY} {YYYYYYYY}` |

| Data Type          | Name        | Label | Description                                                          |
| ------------------ | ----------- | ----- | -------------------------------------------------------------------- |
| PackageStateChange | NewStatus   | X     | See [PackageStateChange][pkgstatechange]                             |
| `u21`              | MetadataIdx | Y     | [0-2M] Index of metadata in [Package References][packagemetadatabin] |

### {11}+00: PackageStatusChanged32

| EventType (0-7)  | Padding (8-31) | Unused (32-32) | NewStatus (33-35) | MetadataIdx (36-63)                       |
| ---------------- | -------------- | -------------- | ----------------- | ----------------------------------------- |
| C0 (`{11} + 00`) | C0 C0 C0       | 0              | `{XXX}`           | `{YYYY} {YYYYYYYY} {YYYYYYYY} {YYYYYYYY}` |

| Data Type          | Name        | Label | Description                                                            |
| ------------------ | ----------- | ----- | ---------------------------------------------------------------------- |
| `u24`              | Padding     | C0    | Constant `C0`. Repeats previous byte.                                  |
| `u1`               | Unused      | 0     |                                                                        |
| PackageStateChange | NewStatus   | X     | See [PackageStateChange][pkgstatechange]                               |
| `u28`              | MetadataIdx | Y     | [0-268M] Index of metadata in [Package References][packagemetadatabin] |

## GameLaunched

!!! info "This event is extremely common. So gets its own opcode."

This event is used to indicate that the game was launched.
This event has no extra data.

!!! note "This event can be added from parsing logs."

    If the launcher detects that Reloaded has been ran through an external logger.

### Messages

- [GAME_LAUNCHED_V0][game-launched-v0]

### {00}+01: GameLaunched

| EventType (0-7)  |
| ---------------- |
| 01 (`{00} + 01`) |

## ConfigUpdated

!!! info "This event indicates that a package configuration was updated."

### Messages

- [MOD_CONFIG_UPDATED_V0][mod-config-updated-v0] when `PackageType == Mod`.
- [TOOL_CONFIG_UPDATED_V0][tool-config-updated-v0] when `PackageType == Tool`.

When the exact changes are not known, the event is [written as V1][commit-message-versioning]:

- [MOD_CONFIG_UPDATED_V1][mod-config-updated-v1] when `PackageType == Mod` and exact changes are not known.
- [TOOL_CONFIG_UPDATED_V1][tool-config-updated-v1] when `PackageType == Tool` and exact changes are not known.

### {01}+01: ConfigUpdated8

| EventType (0-7)  | NewStatus (8-11) | MetadataIdx (12-15) |
| ---------------- | ---------------- | ------------------- |
| 41 (`{01} + 01`) | `{XXXX}`         | `{YYYY}`            |

| Data Type          | Name        | Label | Description                                                          |
| ------------------ | ----------- | ----- | -------------------------------------------------------------------- |
| `u4` (ConfigIdx)   | ConfigIdx   | X     | [0-15] Index of associated configuration in [config.bin][configbin]  |
| `u4` (MetadataIdx) | MetadataIdx | Y     | [0-15] Index of metadata in [Package References][packagemetadatabin] |

### {10}+02: ConfigUpdated16

| EventType (0-7)  | Padding (8-15) | ConfigIdx (16-22) | MetadataIdx (23-31) |
| ---------------- | -------------- | ----------------- | ------------------- |
| 82 (`{10} + 02`) | 82             | `{XXXXXXX}`       | `{Y} {YYYYYYYY}`    |

| Data Type          | Name        | Label | Description                                                           |
| ------------------ | ----------- | ----- | --------------------------------------------------------------------- |
| `u8`               | Padding     | 82    | Constant `82`. Repeats previous byte.                                 |
| `u7` (ConfigIdx)   | ConfigIdx   | X     | [0-127] Index of associated configuration in [config.bin][configbin]  |
| `u9` (MetadataIdx) | MetadataIdx | Y     | [0-511] Index of metadata in [Package References][packagemetadatabin] |

### {10}+03: ConfigUpdated24

| EventType (0-7)  | ConfigIdx (8-18)              | MetadataIdx (19-31)             |
| ---------------- | ----------------------------- | ------------------------------- |
| 83 (`{10} + 01`) | `{XXXXXXXX} {XXXXXXXX} {XXX}` | `{YYYYY} {YYYYYYYY} {YYYYYYYY}` |

| Data Type           | Name        | Label | Description                                                            |
| ------------------- | ----------- | ----- | ---------------------------------------------------------------------- |
| `u11` (ConfigIdx)   | ConfigIdx   | X     | [0-2047] Index of associated configuration in [config.bin][configbin]  |
| `u13` (MetadataIdx) | MetadataIdx | Y     | [0-8191] Index of metadata in [Package References][packagemetadatabin] |

### {11}+01 ConfigUpdated32

| EventType (0-7)  | Padding (8-31) | ConfigIdx (32-46)      | MetadataIdx (47-63)         |
| ---------------- | -------------- | ---------------------- | --------------------------- |
| C1 (`{11} + 01`) | C1 C1 C1       | `{XXXXXXX} {XXXXXXXX}` | `{Y} {YYYYYYYY} {YYYYYYYY}` |

| Data Type           | Name        | Label | Description                                                              |
| ------------------- | ----------- | ----- | ------------------------------------------------------------------------ |
| `u24`               | Padding     | C1    | Constant `C1`. Maximize compression.                                     |
| `u15` (ConfigIdx)   | ConfigIdx   | X     | [0-32767] Index of associated configuration in [config.bin][configbin]   |
| `u17` (MetadataIdx) | MetadataIdx | Y     | [0-131071] Index of metadata in [Package References][packagemetadatabin] |

### {11}+02 ConfigUpdatedFull

| EventType (0-7)  | ConfigIdx (8-35)       | MetadataIdx (36-63)         |
| ---------------- | ---------------------- | --------------------------- |
| C2 (`{11} + 02`) | `{XXXXXXX} {XXXXXXXX}` | `{Y} {YYYYYYYY} {YYYYYYYY}` |

| Data Type           | Name        | Label | Description                                                            |
| ------------------- | ----------- | ----- | ---------------------------------------------------------------------- |
| `u27` (ConfigIdx)   | ConfigIdx   | X     | [0-134M] Index of associated configuration in [config.bin][configbin]  |
| `u28` (MetadataIdx) | MetadataIdx | Y     | [0-268M] Index of metadata in [Package References][packagemetadatabin] |

## LoadoutDisplaySettingChanged

!!! info "A setting related to how mods are displayed in the UI has changed."

This is rarely changed so has a large 4-byte payload and can change multiple events at once.

### Messages

- [LOADOUT_DISPLAY_SETTINGS_CHANGED_V0][loadout-display-settings-changed-v0] when multiple settings have changed.

- [LOADOUT_GRID_ENABLED_SORT_MODE_CHANGED_V0][loadout-grid-enabled-sort-mode-changed-v0] when only `LoadoutGridEnabledSortMode` has changed.
- [LOADOUT_GRID_DISABLED_SORT_MODE_CHANGED_V0][loadout-grid-disabled-sort-mode-changed-v0] when only `LoadoutGridDisabledSortMode` has changed.
- [MOD_LOAD_ORDER_SORT_CHANGED_V0][mod-load-order-sort-changed-v0] when only `ModLoadOrderSort` has changed.
- [LOADOUT_GRID_STYLE_CHANGED_V0][loadout-grid-style-changed-v0] when only `LoadoutGridStyle` has changed.

### {10}+04 LoadoutDisplaySettingChanged

| EventType (0-7)  | Unused (8-11) | LoadoutGridEnabledSortMode (12-18) | LoadoutGridDisabledSortMode (19-25) | ModLoadOrderSort (26-27) | LoadoutGridStyle (28-31) |
| ---------------- | ------------- | ---------------------------------- | ----------------------------------- | ------------------------ | ------------------------ |
| 84 (`{10} + 04`) |               | `{WWWWWWW}`                        | `{XXXXXXX}`                         | `{YY}`                   | `{ZZZZ}`                 |

| Data Type                                 | Name                        | Label | Description                                     |
| ----------------------------------------- | --------------------------- | ----- | ----------------------------------------------- |
| `u7` [(SortingMode)][sortingmode]         | LoadoutGridEnabledSortMode  | W     | Sorting mode for enabled items in LoadoutGrid.  |
| `u7` [(SortingMode)][sortingmode]         | LoadoutGridDisabledSortMode | X     | Sorting mode for disabled items in LoadoutGrid. |
| `u2` [(SortOrder)][sortorder]             | ModLoadOrderSort            | Y     | Sorting mode for load order reorderer.          |
| `u4` [(GridDisplayMode)][griddisplaymode] | LoadoutGridStyle            | Z     | Display mode for LoadoutGrid.                   |

## PackageUpdated

!!! info "This event indicates that a package has been updated to a new version."

This discards the previous manifest at `OldMetadataIdx` and replaces it with the new manifest at `NewMetadataIdx`.

!!! note "`NewMetadataIdx` can point to either a newly written manifest or a previous one"

    It's a previous one in case of a rollback/undo, otherwise it's a new one.

!!! note "Some mods can receive updates quite often"

    That's why `OldMetadatIdx` and `NewMetadataIdx` are evenly distributed in bits.

### Messages

- [PACKAGE_UPDATED_V0][package-updated-v0] when `PackageType` is not known.
- [MOD_UPDATED_V0][mod-updated-v0] when `PackageType == Mod`.
- [TRANSLATION_UPDATED_V0][translation-updated-v0] when `PackageType == Translation`.
- [TOOL_UPDATED_V0][tool-updated-v0] when `PackageType == Tool`.

### {10}+05: PackageUpdated16

| EventType (0-7)  | Padding (8-15) | OldMetadataIdx (16-23) | NewMetadataIdx (24-31) |
| ---------------- | -------------- | ---------------------- | ---------------------- |
| 85 (`{10} + 05`) | 85             | `{XXXXXXXX}`           | `{YYYYYYYY}`           |

| Data Type          | Name           | Label | Description                                                              |
| ------------------ | -------------- | ----- | ------------------------------------------------------------------------ |
| `u8`               | Padding        | 85    | Constant `85`. Repeats previous byte.                                    |
| `u8` (MetadataIdx) | OldMetadataIdx | X     | [0-255] Index of old version in [Package References][packagemetadatabin] |
| `u8` (MetadataIdx) | NewMetadataIdx | Y     | [0-255] Index of new version in [Package References][packagemetadatabin] |

### {10}+06: PackageUpdated24

| EventType (0-7)  | OldMetadataIdx (8-19)          | NewMetadataIdx (20-31)         |
| ---------------- | ------------------------------ | ------------------------------ |
| 86 (`{10} + 06`) | `{XXXXXXXX} {XXXXXXXX} {XXXX}` | `{YYYY} {YYYYYYYY} {YYYYYYYY}` |

| Data Type           | Name           | Label | Description                                                               |
| ------------------- | -------------- | ----- | ------------------------------------------------------------------------- |
| `u12` (MetadataIdx) | OldMetadataIdx | X     | [0-4095] Index of old version in [Package References][packagemetadatabin] |
| `u12` (MetadataIdx) | NewMetadataIdx | Y     | [0-4095] Index of new version in [Package References][packagemetadatabin] |

### {11}+03 PackageUpdated32

| EventType (0-7)  | Padding (8-31) | OldMetadataIdx (8-35)                     | NewMetadataIdx (36-63)                    |
| ---------------- | -------------- | ----------------------------------------- | ----------------------------------------- |
| C3 (`{11} + 03`) | C3 C3 C3       | `{XXXXXXXX} {XXXXXXXX} {XXXXXXXX} {XXXX}` | `{YYYY} {YYYYYYYY} {YYYYYYYY} {YYYYYYYY}` |

| Data Type           | Name           | Label | Description                                                                |
| ------------------- | -------------- | ----- | -------------------------------------------------------------------------- |
| `u24`               | Padding        | C3    | Constant `C3`. Repeats previous byte.                                      |
| `u16` (MetadataIdx) | OldMetadataIdx | X     | [0-65535] Index of old version in [Package References][packagemetadatabin] |
| `u16` (MetadataIdx) | NewMetadataIdx | Y     | [0-65535] Index of new version in [Package References][packagemetadatabin] |

### {11}+04 PackageUpdated56

| EventType (0-7)  | OldMetadataIdx (8-35)                     | NewMetadataIdx (36-63)                    |
| ---------------- | ----------------------------------------- | ----------------------------------------- |
| C4 (`{11} + 04`) | `{XXXXXXXX} {XXXXXXXX} {XXXXXXXX} {XXXX}` | `{YYYY} {YYYYYYYY} {YYYYYYYY} {YYYYYYYY}` |

| Data Type           | Name           | Label | Description                                                               |
| ------------------- | -------------- | ----- | ------------------------------------------------------------------------- |
| `u28` (MetadataIdx) | OldMetadataIdx | X     | [0-268M] Index of old version in [Package References][packagemetadatabin] |
| `u28` (MetadataIdx) | NewMetadataIdx | Y     | [0-268M] Index of new version in [Package References][packagemetadatabin] |

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

### {10}+07: PackageLoadOrderChanged16

| EventType (0-7)  | OldPosition (8-15) | NewPosition (16-23) |
| ---------------- | ------------------ | ------------------- |
| 87 (`{10} + 07`) | `{XXXXXXXX}`       | `{YYYYYYYY}`        |

| Data Type | Name        | Label | Description                                        |
| --------- | ----------- | ----- | -------------------------------------------------- |
| `u8`      | OldPosition | X     | [0-255] Old position of the mod in the load order. |
| `u8`      | NewPosition | Y     | [0-255] New position of the mod in the load order. |

### {10}+08: PackageLoadOrderChanged24

| EventType (0-7)  | OldPosition (8-19)  | NewPosition (20-31) |
| ---------------- | ------------------- | ------------------- |
| 88 (`{10} + 08`) | `{XXXXXXXX} {XXXX}` | `{YYYY} {YYYYYYYY}` |

| Data Type | Name        | Label | Description                                         |
| --------- | ----------- | ----- | --------------------------------------------------- |
| `u12`     | OldPosition | X     | [0-4095] Old position of the mod in the load order. |
| `u12`     | NewPosition | Y     | [0-4095] New position of the mod in the load order. |

### {10}+09: PackageLoadOrderMovedToBottom24

Optimized form for common action of moving a mod to the bottom of the load order.

| EventType (0-7)  | OldPosition (8-27)             | OffsetFromBottom (28-31) |
| ---------------- | ------------------------------ | ------------------------ |
| 89 (`{10} + 09`) | `{XXXX} {XXXXXXXX} {XXXXXXXX}` | `{YYY}`                  |

| Data Type | Name             | Label | Description                                       |
| --------- | ---------------- | ----- | ------------------------------------------------- |
| `u20`     | OldPosition      | X     | [0-1M] Old position of the mod in the load order. |
| `u4`      | OffsetFromBottom | Y     | [0-15] Offset from bottom.                        |

### {10}+0A: PackageLoadOrderMovedToTop24

Optimized form for common action of moving a mod to the top of the load order.

| EventType (0-7)  | OldPosition (8-27)             | OffsetFromTop (28-31) |
| ---------------- | ------------------------------ | --------------------- |
| 8A (`{10} + 0A`) | `{XXXX} {XXXXXXXX} {XXXXXXXX}` | `{YYY}`               |

| Data Type | Name          | Label | Description                                       |
| --------- | ------------- | ----- | ------------------------------------------------- |
| `u20`     | OldPosition   | X     | [0-1M] Old position of the mod in the load order. |
| `u4`      | OffsetFromTop | Y     | [0-15] Offset from top.                           |

### {11}+05: PackageLoadOrderChanged32

| EventType (0-7)  | Padding (8-31) | OldPosition (32-47)     | NewPosition (48-63)     |
| ---------------- | -------------- | ----------------------- | ----------------------- |
| C5 (`{11} + 05`) | C5 C5 C5       | `{XXXXXXXX} {XXXXXXXX}` | `{YYYYYYYY} {YYYYYYYY}` |

| Data Type | Name        | Label | Description                                          |
| --------- | ----------- | ----- | ---------------------------------------------------- |
| `u24`     | Padding     | C5    | Constant `C5`. Repeats previous byte.                |
| `u16`     | OldPosition | X     | [0-65535] Old position of the mod in the load order. |
| `u16`     | NewPosition | Y     | [0-65535] New position of the mod in the load order. |

### {11}+06: PackageLoadOrderChanged56

| EventType (0-7)  | OldPosition (8-35)                        | NewPosition (36-63)                       |
| ---------------- | ----------------------------------------- | ----------------------------------------- |
| C6 (`{11} + 06`) | `{XXXXXXXX} {XXXXXXXX} {XXXXXXXX} {XXXX}` | `{YYYY} {YYYYYYYY} {YYYYYYYY} {YYYYYYYY}` |

| Data Type | Name        | Label | Description                                         |
| --------- | ----------- | ----- | --------------------------------------------------- |
| `u28`     | OldPosition | X     | [0-268M] Old position of the mod in the load order. |
| `u28`     | NewPosition | Y     | [0-268M] New position of the mod in the load order. |

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

### {01}+02: UpdateGameStoreManifest

| EventType (0-7)  | NewRevision (8-15) |
| ---------------- | ------------------ |
| 42 (`{01} + 02`) | `{XXXXXXXX}`       |

| Data Type         | Name        | Label | Description                        |
| ----------------- | ----------- | ----- | ---------------------------------- |
| `u8` (GameVerIdx) | NewRevision | X     | [0-255] New game version revision. |

### {10}+0B: UpdateGameStoreManifest

!!! note "Unlikely this will ever be used, but just in case."

| EventType (0-7)  | NewRevision (8-31)                 |
| ---------------- | ---------------------------------- |
| 8B (`{10} + 0B`) | `{XXXXXXXX} {XXXXXXXX} {XXXXXXXX}` |

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

### {01}+03: UpdateCommandline8

| EventType (0-7)  | Length (8-15) |
| ---------------- | ------------- |
| 43 (`{01} + 03`) | `{XXXXXXXX}`  |

| Data Type | Name   | Label | Description                                                                                                      |
| --------- | ------ | ----- | ---------------------------------------------------------------------------------------------------------------- |
| `u8`      | Length | X     | [0-255] Length of new commandline parameters in [commandline-parameter-data.bin][commandline-parameter-data.bin] |

[configbin]: Unpacked.md#configbin
[events-bin]: Unpacked.md#eventsbin
[packagemetadatabin]: Unpacked.md#package-references
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
[sortingmode]: ./DataTypes.md#sortingmode
[sortorder]: ./DataTypes.md#sortorder
[griddisplaymode]: ./DataTypes.md#griddisplaymode
[mod-config-updated-v1]: ./Commit-Messages.md#mod_config_updated_v1
[tool-config-updated-v1]: ./Commit-Messages.md#tool_config_updated_v1
[commit-message-versioning]: ./Unpacked.md#commit-parameters-versionsbin