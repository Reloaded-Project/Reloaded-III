# Snapshots

!!! info "Reloaded3 loadouts use a single snapshot for quick loading and fault tolerance."

A snapshot contains the current state of all loadout data, allowing for fast loading and efficient updates.

## Snapshot Contents (Schema)

```rust
struct Snapshot {
    // Metadata
    num_events: u32,

    // Packages
    packages: Vec<PackageInfo>,

    // Mod Load Order
    mod_load_order: Vec<u64>, // Vec of PackageIds

    // Loadout Display Settings
    display_settings: LoadoutDisplaySettings,

    // Game Store Manifest
    game_store_manifest: GameStoreManifest,

    // Commandline Parameters
    commandline_parameters: String,
}

struct PackageInfo {
    package_id: u64, // XXH3(PackageID)
    version: String,
    state: PackageState,
    configuration: Option<Vec<u8>>, // Raw configuration data
}

struct LoadoutDisplaySettings {
    loadout_grid_enabled_sort_mode: SortingMode,
    loadout_grid_disabled_sort_mode: SortingMode,
    mod_load_order_sort: SortOrder,
    loadout_grid_style: GridDisplayMode,
}

struct GameStoreManifest {
    store_type: StoreType,
    new_revision: u16, // GameVerIdx
}
```

### Human-Friendly Explanation

1. **Metadata**
    - Event Counter: A number tracking how many events have occurred (u32).
        - This matches [header.bin][headerbin]'s number of events in the unpacked loadout.

2. **Packages**
    - A list of all packages in the loadout, each containing:
        - Package ID: A unique identifier for the package ([XXH3 hash][hashing] of the package ID).
        - Version: The version of the package as a string.
        - State: The current state of the package using the [`PackageState`][packagestate] enum.
        - Configuration: Optional raw configuration data for the package.

3. **Mod Load Order**
    - An ordered list of Package IDs representing the current load order of mods.

4. **Loadout Display Settings**
    - Enabled Grid Sort Mode: How enabled mods are sorted in the grid view ([`SortingMode`][sortingmode]).
    - Disabled Grid Sort Mode: How disabled mods are sorted in the grid view ([`SortingMode`][sortingmode]).
    - Mod Load Order Sort: How mods are sorted in the load order view ([`SortOrder`][sortorder]).
    - Grid Display Style: The visual style of the grid ([`GridDisplayMode`][griddisplaymode]).

5. **Game Store Manifest**
    - Store Type: Which store the game is from ([`StoreType`][storetype]).
    - New Revision: A version number for the game (u16).

6. **Commandline Parameters**
    - A string containing the current commandline parameters for the game.

## Technical Details

- Serialized with MessagePack
    - Allows easy access by external software
- Compressed with Zstandard
- Updated incrementally as new events occur

## Snapshot Usage

- Loaded first when opening a loadout
- Provides fast access to current state
- Used as a base for applying recent events

## Benefits

- Faster loadout loading times
- Quick access to current state
- Maintains full event history
- Efficient updates (apply only changes since last snapshot)

## Fault Tolerance

- Can reconstruct event history if needed
- Used in [fault handling][fault-handling] to recover from crashes

!!! tip "Snapshots balance performance with the flexibility of event sourcing."

[max-numbers]: ./DataTypes.md#max-numbers
[hashing]: ../../../../Common/Hashing.md
[packagestate]: ./DataTypes.md#packagestate
[sortingmode]: ./DataTypes.md#sortingmode
[sortorder]: ./DataTypes.md#sortorder
[griddisplaymode]: ./DataTypes.md#griddisplaymode
[storetype]: ./DataTypes.md#storetype
[fault-handling]: ../About.md#fault-handling
[headerbin]: ./Unpacked.md#headerbin