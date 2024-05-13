!!! info "This is a full list of events in [events.bin][events-bin]"

All bit packed fields are in little endian unless specified otherwise.
They are shown in lowest to highest bit order.

So an order like `u8`, and `u24` means 0:8 bits, then 8:32 bits.

## Shared Structures

### Max Numbers

- Max number of Package Manifests (MetadataIdx): `268,435,456` (28 bits)
- Max number of Configs (ConfigIdx): `134,217,727` (27 bits)
- Max number of Events: `4,294,967,295` (32 bits)
- Max timestamp. R3TimeStamp: `2,199,023,255,551` (40 bits).
    - This is `2^40 - 1` * 10 milliseconds from `1st January 2024`.
    - Max year 2111.

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
- `2`: Grid (Squares)
- `3`: Grid (Horizontal Rectangles, Steam Size)
- `4`: Grid (Vertical Rectangles, Steam Size)

## Events

!!! info "Lists each event type that can be stored in [events.bin][events-bin]."

Each event should strive to be inlineable, i.e. be under 56 bits.

### 00: PackageStatusChanged

!!! info "A new package has been added to `package-metadata.bin` and can be seen from loadout."

| Data Type    | Name        | Description                                                     |
| ------------ | ----------- | --------------------------------------------------------------- |
| `u28`        | MetadataIdx | Index of metadata in [package-metadata.bin][packagemetadatabin] |
| PackageState | NewStatus   | See [PackageState](#packagestate)                               |
| `u25`        | Reserved    |                                                                 |

### 01: GameLaunched

This event is used to indicate that the game was launched.
This event has no extra data. Timestamp for commit message is in from [commit-msg.bin][commitmsgbin].

### 02: ConfigUpdated

!!! info "This event indicates that a package configuration was updated."

| Data Type           | Name        | Description                                                     |
| ------------------- | ----------- | --------------------------------------------------------------- |
| `u28` (MetadataIdx) | MetadataIdx | Index of metadata in [package-metadata.bin][packagemetadatabin] |
| `u27` (ConfigIdx)   | ConfigIdx   | Index of associated configuration in [config.bin][configbin]    |
| `u1`                | Reserved    |                                                                 |

### 03: PackageStateSet

!!! info "This event indicates that a package has been enabled, disabled etc."

| Data Type           | Name        | Description                                                     |
| ------------------- | ----------- | --------------------------------------------------------------- |
| `u28`               | MetadataIdx | Index of metadata in [package-metadata.bin][packagemetadatabin] |
| `u3` (PackageState) | State       | See [PackageState](#packagestate)                               |
| `u25`               | Reserved    |                                                                 |

### 04: LoadoutDisplaySettingChanged

!!! info "A setting related to mod has been changed."

| Data Type              | Name                        | Description                                     |
| ---------------------- | --------------------------- | ----------------------------------------------- |
| `u7` (SortingMode)     | LoadoutGridEnabledSortMode  | Sorting mode for enabled items in LoadoutGrid.  |
| `u7` (SortingMode)     | LoadoutGridDisabledSortMode | Sorting mode for disabled items in LoadoutGrid. |
| `u2` (SortOrder)       | ModLoadOrderSort            | Sorting mode for load order reorderer.          |
| `u4` (GridDisplayMode) | LoadoutGridStyle            | Display mode for LoadoutGrid.                   |
| `u36`                  | Reserved                    |                                                 |

Sure, I can suggest some additional events that may exist in the Reloaded3 loadout system, based on my knowledge of Reloaded-II and common mod loader functionality. Here are a few ideas:

### 05: PackageUpdated

!!! info "This event indicates that a package has been updated to a new version."

| Data Type           | Name           | Description                                                        |
| ------------------- | -------------- | ------------------------------------------------------------------ |
| `u28` (MetadataIdx) | OldMetadataIdx | Index of old version in [package-metadata.bin][packagemetadatabin] |
| `u28` (MetadataIdx) | NewMetadataIdx | Index of new version in [package-metadata.bin][packagemetadatabin] |

This discards the previous manifest at `OldMetadataIdx` and replaces it with the new manifest at `NewMetadataIdx`.

!!! note "`NewMetadataIdx` can point to either a newly written manifest or a previous one"

    It's a previous one in case of a rollback/undo, otherwise it's a new one.

### 06: PackageLoadOrderChanged

!!! info "This event indicates that the load order of packages has changed."

| Data Type | Name        | Description                                |
| --------- | ----------- | ------------------------------------------ |
| `u28`     | OldPosition | Old position of the mod in the load order. |
| `u28`     | NewPosition | New position of the mod in the load order. |

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

[commit-messages]: About.md#commit-msgbin
[commitmsgbin]: About.md#commit-msgbin
[configbin]: About.md#configbin
[events-bin]: About.md#eventsbin
[packagemetadatabin]: About.md#package-metadatabin