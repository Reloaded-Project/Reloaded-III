!!! info "This is a full list of events in [events.bin][events-bin]"

All bit packed fields are in little endian unless specified otherwise.
They are shown in lowest to highest bit order.

So an order like `u8`, and `u24` means 0:8 bits, then 8:32 bits.

## Shared Structures

### Max Numbers

- Max number of Package Download Data/Metadata (MetadataIdx): `268,435,456` (28 bits)
- Max number of Configs (ConfigIdx): `134,217,727` (27 bits)
- Max number of Events: `4,294,967,295` (32 bits)
- Max number of Game Versions/Revisions (GameVerIdx): `65,536` (16 bits)
- Max timestamp. R3TimeStamp: `4,294,967,295` (32 bits).
    - This is the number of seconds since `1st January 2024`.
    - Max year 2160.

### PackageState

!!! info "Represents the state of a package in the loadout."

    - Size: 3 bits
    - Possible values: 0-7

`PackageState` is defined as:

- `0`: `Removed`. The package was removed from the loadout.
- `1`: `Hidden`. The package was hidden from the loadout.
- `2`: `Disabled` (Default State). The package was disabled in the loadout.
- `3`: `Added`. The package was added to the loadout.
- `4`: `Enabled`. The package was enabled in the loadout.

### SortingMode

!!! info "Represents the sorting mode for packages in the LoadoutGrid."

    - Size: 7 bits
    - Possible values: 0-127

`SortingMode` is defined as:

- `0`: Unchanged
- `1`: `Static`. The order of mods is fixed and does not change between reboots.
- `2`: `Release Date Ascending`. Show from oldest to newest.
- `3`: `Release Date Descending`. Show from newest to oldest.
- `4`: `Install Date Ascending`. Show from oldest to newest.
- `5`: `Install Date Descending`. Show from newest to oldest.

### SortOrder

!!! info "Represents the sort order for the load order reorderer."

    - Size: 2 bits
    - Possible values: 0-3

`SortOrder` is defined as:

- `0`: Unchanged
- `1`: `BottomToTop` (Default). Mods at bottom load first, mods at top load last and 'win'.
- `2`: `TopToBottom`. Sort in ascending order.

### GridDisplayMode

!!! info "Represents the display mode for the LoadoutGrid."

    - Size: 4 bits
    - Possible values: 0-15

`GridDisplayMode` is defined as:

- `0`: Unchanged
- `1`: List (Compact)
- `2`: List (Thick)
- `3`: Grid (Search)

### StoreType

!!! info "Represents the store or location from which a game has shipped from."

    - Size: 8 bits
    - Possible values: 0-15

- 0: `Unknown` (Disk)
- 1: `GOG`
- 2: `Steam`
- 3: `Epic`
- 4: `Microsoft`

This can also include game launchers.

## Events

!!! info "Lists each event type that can be stored in [events.bin][events-bin]."

Each event is represented by a 1 byte `EventType` (denoted in section title).
This is a power of 2, and can be followed by a 1, 3 or 7 byte payload. This makes each event 1, 2,
4 or 8 bytes long.

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

### Optimizing for Compression

!!! tip "The events are heavily optimized to maximize compression ratios."

To achieve this we do the following:

- Padding bytes use same byte as EventType to increase repeated bytes.
- EventType(s) have forms with multiple lengths (to minimize unused bytes).

### Event Ranges

The payload size is determined by the 2 high bits of the event type.

| Sequence | Size |
| -------- | ---- |
| 00       | 0    |
| 01       | 1    |
| 10       | 3    |
| 11       | 7    |

This leaves the remaining next 6 bits (0-63) for the event type.

i.e. `{YY}{XXXXXX}`.

### Event Representation

Each event is represented with something like this:

| EventType (0-7)  | Field X (8-11) | Field Y (12-15) |
| ---------------- | -------------- | --------------- |
| 01 (`{00} + 01`) | `{XXX}`        | `{YYYY}`        |

Ranges are inclusive.

Elements in curly brackets `{}` indicate binary packing. So the payload `{XXX}` means '`X` is stored
in 3 bits'. These provide a visual representation of the ranges to prevent ambiguity.

In the EventType, the `{00}` denotes the size prefix, and the `+` shows the offset into
the given prefix (0-63, in hex).

### {00}+00: NOP

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

### PackageStatusChanged

!!! info "A new package has been added to `Package References` and can be seen from loadout."

#### Messages

`PackageType` is the type of package referred to `MetadataIdx`.

- [package-added][package-added] when `NewStatus == Added` when `PackageType` is not known.
- [package-removed][package-removed] when `NewStatus == Removed` when `PackageType` is not known.
- [package-hidden][package-hidden] when `NewStatus == Hidden` when `PackageType` is not known.
- [package-disabled][package-disabled] when `NewStatus == Disabled` when `PackageType` is not known.
- [package-enabled][package-enabled] when `NewStatus == Enabled` when `PackageType` is not known.
- [mod-added][mod-added] when `NewStatus == Added` and `PackageType == Mod`.
- [mod-removed][mod-removed] when `NewStatus == Removed` and `PackageType == Mod`.
- [mod-hidden][mod-hidden] when `NewStatus == Hidden` and `PackageType == Mod`.
- [mod-disabled][mod-disabled] when `NewStatus == Disabled` and `PackageType == Mod`.
- [mod-enabled][mod-enabled] when `NewStatus == Enabled` and `PackageType == Mod`.
- [translation-added][translation-added] when `NewStatus == Added` and `PackageType == Translation`.
- [translation-removed][translation-removed] when `NewStatus == Removed` and `PackageType == Translation`.
- [translation-hidden][translation-hidden] when `NewStatus == Hidden` and `PackageType == Translation`.
- [translation-disabled][translation-disabled] when `NewStatus == Disabled` and `PackageType == Translation`.
- [translation-enabled][translation-enabled] when `NewStatus == Enabled` and `PackageType == Translation`.
- [tool-added][tool-added] when `NewStatus == Added` and `PackageType == Tool`.
- [tool-removed][tool-removed] when `NewStatus == Removed` and `PackageType == Tool`.
- [tool-hidden][tool-hidden] when `NewStatus == Hidden` and `PackageType == Tool`.
- [tool-disabled][tool-disabled] when `NewStatus == Disabled` and `PackageType == Tool`.
- [tool-enabled][tool-enabled] when `NewStatus == Enabled` and `PackageType == Tool`.

#### {01}+00: PackageStatusChanged8

| EventType (0-7)  | NewStatus (8-10) | MetadataIdx (11-15) |
| ---------------- | ---------------- | ------------------- |
| 40 (`{01} + 00`) | `{XXX}`          | `{YYYYY}`           |

| Data Type    | Name        | Label | Description                                                          |
| ------------ | ----------- | ----- | -------------------------------------------------------------------- |
| PackageState | NewStatus   | X     | See [PackageState](#packagestate)                                    |
| `u5`         | MetadataIdx | Y     | [0-31] Index of metadata in [Package References][packagemetadatabin] |

#### {10}+00: PackageStatusChanged16

| EventType (0-7)  | Padding (8-15) | NewStatus (16-18) | MetadataIdx (19-31)  |
| ---------------- | -------------- | ----------------- | -------------------- |
| 80 (`{10} + 00`) | 80             | `{XXX}`           | `{YYYYY} {YYYYYYYY}` |

| Data Type    | Name        | Label | Description                                                            |
| ------------ | ----------- | ----- | ---------------------------------------------------------------------- |
| `u8`         | Padding     | 80    | Constant `80`. Repeats previous byte.                                  |
| PackageState | NewStatus   | X     | See [PackageState](#packagestate)                                      |
| `u13`        | MetadataIdx | Y     | [0-8192] Index of metadata in [Package References][packagemetadatabin] |

#### {10}+01: PackageStatusChanged24

| EventType (0-7)  | NewStatus (8-10) | MetadataIdx (11-31)             |
| ---------------- | ---------------- | ------------------------------- |
| 81 (`{10} + 01`) | `{XXX}`          | `{YYYYY} {YYYYYYYY} {YYYYYYYY}` |

| Data Type    | Name        | Label | Description                                                          |
| ------------ | ----------- | ----- | -------------------------------------------------------------------- |
| PackageState | NewStatus   | X     | See [PackageState](#packagestate)                                    |
| `u21`        | MetadataIdx | Y     | [0-2M] Index of metadata in [Package References][packagemetadatabin] |

#### {11}+00: PackageStatusChanged32

| EventType (0-7)  | Padding (8-31) | Unused (32-32) | NewStatus (33-35) | MetadataIdx (36-63)                       |
| ---------------- | -------------- | -------------- | ----------------- | ----------------------------------------- |
| C0 (`{11} + 00`) | C0 C0 C0       | 0              | `{XXX}`           | `{YYYY} {YYYYYYYY} {YYYYYYYY} {YYYYYYYY}` |

| Data Type    | Name        | Label | Description                                                            |
| ------------ | ----------- | ----- | ---------------------------------------------------------------------- |
| `u24`        | Padding     | C0    | Constant `C0`. Repeats previous byte.                                  |
| `u1`         | Unused      | 0     |                                                                        |
| PackageState | NewStatus   | X     | See [PackageState](#packagestate)                                      |
| `u28`        | MetadataIdx | Y     | [0-268M] Index of metadata in [Package References][packagemetadatabin] |

### GameLaunched

!!! info "This event is extremely common. So gets its own opcode."

This event is used to indicate that the game was launched.
This event has no extra data.

!!! note "This event can be added from parsing logs."

    If the launcher detects that Reloaded has been ran through an external logger.

#### Messages

- [game-launched][game-launched]

#### {00}+01: GameLaunched

| EventType (0-7)  |
| ---------------- |
| 01 (`{00} + 01`) |

### ConfigUpdated

!!! info "This event indicates that a package configuration was updated."

#### Messages

- [mod-config-updated][mod-config-updated] when `PackageType == Mod`.
- [tool-config-updated][tool-config-updated] when `PackageType == Tool`.

#### {01}+01: ConfigUpdated8

| EventType (0-7)  | NewStatus (8-11) | MetadataIdx (12-15) |
| ---------------- | ---------------- | ------------------- |
| 41 (`{01} + 01`) | `{XXXX}`         | `{YYYY}`            |

| Data Type          | Name        | Label | Description                                                          |
| ------------------ | ----------- | ----- | -------------------------------------------------------------------- |
| `u4` (ConfigIdx)   | ConfigIdx   | X     | [0-15] Index of associated configuration in [config.bin][configbin]  |
| `u4` (MetadataIdx) | MetadataIdx | Y     | [0-15] Index of metadata in [Package References][packagemetadatabin] |

#### {10}+02: ConfigUpdated16

| EventType (0-7)  | Padding (8-15) | ConfigIdx (16-22) | MetadataIdx (23-31) |
| ---------------- | -------------- | ----------------- | ------------------- |
| 82 (`{10} + 02`) | 82             | `{XXXXXXX}`       | `{Y} {YYYYYYYY}`    |

| Data Type          | Name        | Label | Description                                                           |
| ------------------ | ----------- | ----- | --------------------------------------------------------------------- |
| `u8`               | Padding     | 82    | Constant `82`. Repeats previous byte.                                 |
| `u7` (ConfigIdx)   | ConfigIdx   | X     | [0-127] Index of associated configuration in [config.bin][configbin]  |
| `u9` (MetadataIdx) | MetadataIdx | Y     | [0-511] Index of metadata in [Package References][packagemetadatabin] |

#### {10}+03: ConfigUpdated24

| EventType (0-7)  | ConfigIdx (8-18)              | MetadataIdx (19-31)             |
| ---------------- | ----------------------------- | ------------------------------- |
| 83 (`{10} + 01`) | `{XXXXXXXX} {XXXXXXXX} {XXX}` | `{YYYYY} {YYYYYYYY} {YYYYYYYY}` |

| Data Type           | Name        | Label | Description                                                            |
| ------------------- | ----------- | ----- | ---------------------------------------------------------------------- |
| `u11` (ConfigIdx)   | ConfigIdx   | X     | [0-2047] Index of associated configuration in [config.bin][configbin]  |
| `u13` (MetadataIdx) | MetadataIdx | Y     | [0-8191] Index of metadata in [Package References][packagemetadatabin] |

#### {11}+01 ConfigUpdated32

| EventType (0-7)  | Padding (8-31) | ConfigIdx (32-46)      | MetadataIdx (47-63)         |
| ---------------- | -------------- | ---------------------- | --------------------------- |
| C1 (`{11} + 01`) | C1 C1 C1       | `{XXXXXXX} {XXXXXXXX}` | `{Y} {YYYYYYYY} {YYYYYYYY}` |

| Data Type           | Name        | Label | Description                                                              |
| ------------------- | ----------- | ----- | ------------------------------------------------------------------------ |
| `u24`               | Padding     | C1    | Constant `C1`. Maximize compression.                                     |
| `u15` (ConfigIdx)   | ConfigIdx   | X     | [0-32767] Index of associated configuration in [config.bin][configbin]   |
| `u17` (MetadataIdx) | MetadataIdx | Y     | [0-131071] Index of metadata in [Package References][packagemetadatabin] |

#### {11}+02 ConfigUpdatedFull

| EventType (0-7)  | ConfigIdx (8-35)       | MetadataIdx (36-63)         |
| ---------------- | ---------------------- | --------------------------- |
| C2 (`{11} + 02`) | `{XXXXXXX} {XXXXXXXX}` | `{Y} {YYYYYYYY} {YYYYYYYY}` |

| Data Type           | Name        | Label | Description                                                            |
| ------------------- | ----------- | ----- | ---------------------------------------------------------------------- |
| `u27` (ConfigIdx)   | ConfigIdx   | X     | [0-134M] Index of associated configuration in [config.bin][configbin]  |
| `u28` (MetadataIdx) | MetadataIdx | Y     | [0-268M] Index of metadata in [Package References][packagemetadatabin] |

### LoadoutDisplaySettingChanged

!!! info "A setting related to how mods are displayed in the UI has changed."

This is rarely changed so has a large 4-byte payload and can change multiple events at once.

#### Messages

- [loadout-display-setting-changed][loadout-display-setting-changed]
- [loadout-grid-enabled-sort-mode-changed][loadout-grid-enabled-sort-mode-changed] when only `LoadoutGridEnabledSortMode` has changed.
- [loadout-grid-disabled-sort-mode-changed][loadout-grid-disabled-sort-mode-changed] when only `LoadoutGridDisabledSortMode` has changed.
- [mod-load-order-sort-changed][mod-load-order-sort-changed] when only `ModLoadOrderSort` has changed.
- [loadout-grid-style-changed][loadout-grid-style-changed] when only `LoadoutGridStyle` has changed.

#### {10}+04 LoadoutDisplaySettingChanged

| EventType (0-7)  | Unused (8-11) | LoadoutGridEnabledSortMode (12-18) | LoadoutGridDisabledSortMode (19-25) | ModLoadOrderSort (26-27) | LoadoutGridStyle (28-31) |
| ---------------- | ------------- | ---------------------------------- | ----------------------------------- | ------------------------ | ------------------------ |
| 84 (`{10} + 04`) |               | `{WWWWWWW}`                        | `{XXXXXXX}`                         | `{YY}`                   | `{ZZZZ}`                 |

| Data Type                                  | Name                        | Label | Description                                     |
| ------------------------------------------ | --------------------------- | ----- | ----------------------------------------------- |
| `u7` [(SortingMode)](#sortingmode)         | LoadoutGridEnabledSortMode  | W     | Sorting mode for enabled items in LoadoutGrid.  |
| `u7` [(SortingMode)](#sortingmode)         | LoadoutGridDisabledSortMode | X     | Sorting mode for disabled items in LoadoutGrid. |
| `u2` [(SortOrder)](#sortorder)             | ModLoadOrderSort            | Y     | Sorting mode for load order reorderer.          |
| `u4` [(GridDisplayMode)](#griddisplaymode) | LoadoutGridStyle            | Z     | Display mode for LoadoutGrid.                   |

### PackageUpdated

!!! info "This event indicates that a package has been updated to a new version."

This discards the previous manifest at `OldMetadataIdx` and replaces it with the new manifest at `NewMetadataIdx`.

!!! note "`NewMetadataIdx` can point to either a newly written manifest or a previous one"

    It's a previous one in case of a rollback/undo, otherwise it's a new one.

!!! note "Some mods can receive updates quite often"

    That's why `OldMetadatIdx` and `NewMetadataIdx` are evenly distributed in bits.

#### Messages

- [package-updated][package-updated] when `PackageType` is not known.
- [mod-updated][mod-updated] when `PackageType == Mod`.
- [translation-updated][translation-updated] when `PackageType == Translation`.
- [tool-updated][tool-updated] when `PackageType == Tool`.

#### {10}+05: PackageUpdated16

| EventType (0-7)  | Padding (8-15) | OldMetadataIdx (16-23) | NewMetadataIdx (24-31) |
| ---------------- | -------------- | ---------------------- | ---------------------- |
| 85 (`{10} + 05`) | 85             | `{XXXXXXXX}`           | `{YYYYYYYY}`           |

| Data Type          | Name           | Label | Description                                                              |
| ------------------ | -------------- | ----- | ------------------------------------------------------------------------ |
| `u8`               | Padding        | 85    | Constant `85`. Repeats previous byte.                                    |
| `u8` (MetadataIdx) | OldMetadataIdx | X     | [0-255] Index of old version in [Package References][packagemetadatabin] |
| `u8` (MetadataIdx) | NewMetadataIdx | Y     | [0-255] Index of new version in [Package References][packagemetadatabin] |

#### {10}+06: PackageUpdated24

| EventType (0-7)  | OldMetadataIdx (8-19)          | NewMetadataIdx (20-31)         |
| ---------------- | ------------------------------ | ------------------------------ |
| 86 (`{10} + 06`) | `{XXXXXXXX} {XXXXXXXX} {XXXX}` | `{YYYY} {YYYYYYYY} {YYYYYYYY}` |

| Data Type           | Name           | Label | Description                                                               |
| ------------------- | -------------- | ----- | ------------------------------------------------------------------------- |
| `u12` (MetadataIdx) | OldMetadataIdx | X     | [0-4095] Index of old version in [Package References][packagemetadatabin] |
| `u12` (MetadataIdx) | NewMetadataIdx | Y     | [0-4095] Index of new version in [Package References][packagemetadatabin] |

#### {11}+03 PackageUpdated32

| EventType (0-7)  | Padding (8-31) | OldMetadataIdx (8-35)                     | NewMetadataIdx (36-63)                    |
| ---------------- | -------------- | ----------------------------------------- | ----------------------------------------- |
| C3 (`{11} + 03`) | C3 C3 C3       | `{XXXXXXXX} {XXXXXXXX} {XXXXXXXX} {XXXX}` | `{YYYY} {YYYYYYYY} {YYYYYYYY} {YYYYYYYY}` |

| Data Type           | Name           | Label | Description                                                                |
| ------------------- | -------------- | ----- | -------------------------------------------------------------------------- |
| `u24`               | Padding        | C3    | Constant `C3`. Repeats previous byte.                                      |
| `u16` (MetadataIdx) | OldMetadataIdx | X     | [0-65535] Index of old version in [Package References][packagemetadatabin] |
| `u16` (MetadataIdx) | NewMetadataIdx | Y     | [0-65535] Index of new version in [Package References][packagemetadatabin] |

#### {11}+04 PackageUpdated56

| EventType (0-7)  | OldMetadataIdx (8-35)                     | NewMetadataIdx (36-63)                    |
| ---------------- | ----------------------------------------- | ----------------------------------------- |
| C4 (`{11} + 04`) | `{XXXXXXXX} {XXXXXXXX} {XXXXXXXX} {XXXX}` | `{YYYY} {YYYYYYYY} {YYYYYYYY} {YYYYYYYY}` |

| Data Type           | Name           | Label | Description                                                               |
| ------------------- | -------------- | ----- | ------------------------------------------------------------------------- |
| `u28` (MetadataIdx) | OldMetadataIdx | X     | [0-268M] Index of old version in [Package References][packagemetadatabin] |
| `u28` (MetadataIdx) | NewMetadataIdx | Y     | [0-268M] Index of new version in [Package References][packagemetadatabin] |

### PackageLoadOrderChanged

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

#### Messages

- [mod-load-order-changed][mod-load-order-changed] when `PackageType == Mod`.
- [translation-load-order-changed][translation-load-order-changed] when `PackageType == Translation`.

#### {10}+07: PackageLoadOrderChanged16

| EventType (0-7)  | OldPosition (8-15) | NewPosition (16-23) |
| ---------------- | ------------------ | ------------------- |
| 87 (`{10} + 07`) | `{XXXXXXXX}`       | `{YYYYYYYY}`        |

| Data Type | Name        | Label | Description                                        |
| --------- | ----------- | ----- | -------------------------------------------------- |
| `u8`      | OldPosition | X     | [0-255] Old position of the mod in the load order. |
| `u8`      | NewPosition | Y     | [0-255] New position of the mod in the load order. |

#### {10}+08: PackageLoadOrderChanged24

| EventType (0-7)  | OldPosition (8-19)  | NewPosition (20-31) |
| ---------------- | ------------------- | ------------------- |
| 88 (`{10} + 08`) | `{XXXXXXXX} {XXXX}` | `{YYYY} {YYYYYYYY}` |

| Data Type | Name        | Label | Description                                         |
| --------- | ----------- | ----- | --------------------------------------------------- |
| `u12`     | OldPosition | X     | [0-4095] Old position of the mod in the load order. |
| `u12`     | NewPosition | Y     | [0-4095] New position of the mod in the load order. |

#### {10}+09: PackageLoadOrderMovedToBottom24

Optimized form for common action of moving a mod to the bottom of the load order.

| EventType (0-7)  | OldPosition (8-27)             | OffsetFromBottom (28-31) |
| ---------------- | ------------------------------ | ------------------------ |
| 89 (`{10} + 09`) | `{XXXX} {XXXXXXXX} {XXXXXXXX}` | `{YYY}`                  |

| Data Type | Name             | Label | Description                                       |
| --------- | ---------------- | ----- | ------------------------------------------------- |
| `u20`     | OldPosition      | X     | [0-1M] Old position of the mod in the load order. |
| `u4`      | OffsetFromBottom | Y     | [0-15] Offset from bottom.                        |

#### {10}+0A: PackageLoadOrderMovedToTop24

Optimized form for common action of moving a mod to the top of the load order.

| EventType (0-7)  | OldPosition (8-27)             | OffsetFromTop (28-31) |
| ---------------- | ------------------------------ | --------------------- |
| 8A (`{10} + 0A`) | `{XXXX} {XXXXXXXX} {XXXXXXXX}` | `{YYY}`               |

| Data Type | Name          | Label | Description                                       |
| --------- | ------------- | ----- | ------------------------------------------------- |
| `u20`     | OldPosition   | X     | [0-1M] Old position of the mod in the load order. |
| `u4`      | OffsetFromTop | Y     | [0-15] Offset from top.                           |

#### {11}+05: PackageLoadOrderChanged32

| EventType (0-7)  | Padding (8-31) | OldPosition (32-47)     | NewPosition (48-63)     |
| ---------------- | -------------- | ----------------------- | ----------------------- |
| C5 (`{11} + 05`) | C5 C5 C5       | `{XXXXXXXX} {XXXXXXXX}` | `{YYYYYYYY} {YYYYYYYY}` |

| Data Type | Name        | Label | Description                                          |
| --------- | ----------- | ----- | ---------------------------------------------------- |
| `u24`     | Padding     | C5    | Constant `C5`. Repeats previous byte.                |
| `u16`     | OldPosition | X     | [0-65535] Old position of the mod in the load order. |
| `u16`     | NewPosition | Y     | [0-65535] New position of the mod in the load order. |

#### {11}+06: PackageLoadOrderChanged56

| EventType (0-7)  | OldPosition (8-35)                        | NewPosition (36-63)                       |
| ---------------- | ----------------------------------------- | ----------------------------------------- |
| C6 (`{11} + 06`) | `{XXXXXXXX} {XXXXXXXX} {XXXXXXXX} {XXXX}` | `{YYYY} {YYYYYYYY} {YYYYYYYY} {YYYYYYYY}` |

| Data Type | Name        | Label | Description                                         |
| --------- | ----------- | ----- | --------------------------------------------------- |
| `u28`     | OldPosition | X     | [0-268M] Old position of the mod in the load order. |
| `u28`     | NewPosition | Y     | [0-268M] New position of the mod in the load order. |

### UpdateGameStoreManifest

!!! info "This is used for upgrading/downgrading a game on supported stores."

And also just seeing when the game got updated.

This sets an index of the new game version in the `NewRevision` field.

This revision corresponds to an entry in the [stores.bin][stores-bin] file.

This event is emitted the files of the game match a known new store manifest/revision.

#### Messages

- [update-game-store-manifest][update-game-store-manifest]
- [update-game-store-manifest-steam][update-game-store-manifest-steam] when the store is Steam.
- [update-game-store-manifest-gog][update-game-store-manifest-gog] when the store is GOG.
- [update-game-store-manifest-microsoft][update-game-store-manifest-microsoft] when the store is Microsoft Store.
- [update-game-store-manifest-epic][update-game-store-manifest-epic] when the store is Epic Games Store.

#### {01}+02: UpdateGameStoreManifest

| EventType (0-7)  | NewRevision (8-15) |
| ---------------- | ------------------ |
| 42 (`{01} + 02`) | `{XXXXXXXX}`       |

| Data Type         | Name        | Label | Description                        |
| ----------------- | ----------- | ----- | ---------------------------------- |
| `u8` (GameVerIdx) | NewRevision | X     | [0-255] New game version revision. |

#### {10}+0B: UpdateGameStoreManifest

!!! note "Unlikely this will ever be used, but just in case."

| EventType (0-7)  | NewRevision (8-31)                 |
| ---------------- | ---------------------------------- |
| 8B (`{10} + 0B`) | `{XXXXXXXX} {XXXXXXXX} {XXXXXXXX}` |

| Data Type         | Name        | Label | Description                          |
| ----------------- | ----------- | ----- | ------------------------------------ |
| `u8` (GameVerIdx) | NewRevision | X     | [0-16.8M] New game version revision. |

### UpdateCommandline

!!! info "This event updates the commandline parameters passed to the game."

!!! note "Restricted to 255 characters arbitrarily."

    If someone needs a longer commandline, just make an issue please.
    We could encode that as null terminated, probably, while keeping the space savings intact.

#### Messages

- [update-commandline][update-commandline]

#### {01}+03: UpdateCommandline8

| EventType (0-7)  | Length (8-15) |
| ---------------- | ------------- |
| 43 (`{01} + 03`) | `{XXXXXXXX}`  |

| Data Type | Name   | Label | Description                                                                                                      |
| --------- | ------ | ----- | ---------------------------------------------------------------------------------------------------------------- |
| `u8`      | Length | X     | [0-255] Length of new commandline parameters in [commandline-parameter-data.bin][commandline-parameter-data.bin] |

[configbin]: About.md#configbin
[events-bin]: About.md#eventsbin
[packagemetadatabin]: About.md#package-references
[package-added]: ./Commit-Messages.md#packageadded
[package-removed]: ./Commit-Messages.md#packageremoved
[package-hidden]: ./Commit-Messages.md#packagehidden
[package-disabled]: ./Commit-Messages.md#packagedisabled
[package-enabled]: ./Commit-Messages.md#packageenabled
[package-added]: ./Commit-Messages.md#packageadded
[package-removed]: ./Commit-Messages.md#packageremoved
[package-hidden]: ./Commit-Messages.md#packagehidden
[package-disabled]: ./Commit-Messages.md#packagedisabled
[package-enabled]: ./Commit-Messages.md#packageenabled
[mod-added]: ./Commit-Messages.md#modadded
[mod-removed]: ./Commit-Messages.md#modremoved
[mod-hidden]: ./Commit-Messages.md#modhidden
[mod-disabled]: ./Commit-Messages.md#moddisabled
[mod-enabled]: ./Commit-Messages.md#modenabled
[translation-added]: ./Commit-Messages.md#translationadded
[translation-removed]: ./Commit-Messages.md#translationremoved
[translation-hidden]: ./Commit-Messages.md#translationhidden
[translation-disabled]: ./Commit-Messages.md#translationdisabled
[translation-enabled]: ./Commit-Messages.md#translationenabled
[tool-added]: ./Commit-Messages.md#tooladded
[tool-removed]: ./Commit-Messages.md#toolremoved
[tool-hidden]: ./Commit-Messages.md#toolhidden
[tool-disabled]: ./Commit-Messages.md#tooldisabled
[tool-enabled]: ./Commit-Messages.md#toolenabled
[package-updated]: ./Commit-Messages.md#packageupdated
[mod-updated]: ./Commit-Messages.md#modupdated
[translation-updated]: ./Commit-Messages.md#translationupdated
[tool-updated]: ./Commit-Messages.md#toolupdated
[event-packageloadorderchanged]: ./Events.md#packageloadorderchanged
[mod-load-order-changed]: ./Commit-Messages.md#modloadorderchanged
[translation-load-order-changed]: ./Commit-Messages.md#translationloadorderchanged
[mod-config-updated]: ./Commit-Messages.md#modconfigupdated
[tool-config-updated]: ./Commit-Messages.md#toolconfigupdated
[loadout-display-setting-changed]: ./Commit-Messages.md#display-setting-changed
[loadout-grid-enabled-sort-mode-changed]: ./Commit-Messages.md#loadoutgridenabledsortmodechanged
[loadout-grid-disabled-sort-mode-changed]: ./Commit-Messages.md#loadoutgriddisabledsortmodechanged
[mod-load-order-sort-changed]: ./Commit-Messages.md#modloadordersortchanged
[loadout-grid-style-changed]: ./Commit-Messages.md#loadoutgridstylechanged
[game-launched]: ./Commit-Messages.md#game-launched
[stores-bin]: ./About.md#storesbin
[commandline-parameter-data.bin]: ./About.md#commandline-parameter-databin
[update-game-store-manifest]: ./Commit-Messages.md#updategamestoremanifest
[update-game-store-manifest-steam]: ./Commit-Messages.md#steam
[update-game-store-manifest-gog]: ./Commit-Messages.md#gog
[update-game-store-manifest-epic]: ./Commit-Messages.md#epic-games-store
[update-game-store-manifest-microsoft]: ./Commit-Messages.md#microsoft-store
[update-commandline]: ./Commit-Messages.md#updatecommandline
[featuresbin]: ./About.md#featuresbin