# Snapshots

!!! info "Reloaded3 loadouts use a single snapshot for quick loading and fault tolerance."

A snapshot contains the current state of the parser containing the [Unpacked Loadout Data][unpacked],
allowing for fast loading and efficient updates.

## Snapshot Contents (Schema)

```rust
struct Snapshot {
    // Metadata
    num_events: u32,

    // Loadout ID (This is the same as the loadout {UID}.)
    loadout_id: String,

    // Packages
    packages: Vec<PackageInfo>,

    // Configurations
    configurations: Vec<Vec<u8>>,
    config_hashes: HashMap<XXH3, u32>, // Hash to index in 'configurations'

    // External Configurations
    external_configs: Vec<ExternalConfigInfo>,
    external_config_hashes: HashMap<XXH3, u32>, // Hash to index in 'external_configs'

    // Mod Load Order
    mod_load_order: Vec<u32>, // Vec of indices into packages

    // Loadout Display Settings
    display_settings: LoadoutDisplaySettings,

    // Game Store Manifest
    game_store_manifest: GameStoreManifest,

    // Commandline Parameters
    commandline_parameters: String,
}

struct PackageInfo {
    package_id: XXH3, // XXH3(PackageID)
    version: String, // Semantic version
    state: PackageState,
    configuration_index: Option<u32>, // Index into configurations Vec
}

struct ExternalConfigInfo {
    package_id: XXH3, // XXH3(PackageID)
    path: String, // Relative path to the external config file
    data: Vec<u8>, // Raw content of the external config file
}

struct LoadoutDisplaySettings {
    loadout_grid_enabled_sort_mode: SortingMode,
    loadout_grid_disabled_sort_mode: SortingMode,
    mod_load_order_sort: SortOrder,
    loadout_grid_style: GridDisplayMode,
}

struct GameStoreManifest {
    store_type: StoreType,
    store_data: StoreData,
}

struct StoreData {
    // Common fields
    exe_hash: u64,
    exe_path: String,
    app_id: String,

    // Store-specific data
    gog: Option<GOGStoreData>,
    steam: Option<SteamStoreData>,
    epic: Option<EpicStoreData>,
    microsoft: Option<MicrosoftStoreData>,
}

struct GOGStoreData {
    game_id: u64,
    build_id: u64,
    version_name: String,
}

struct SteamStoreData {
    app_id: u64,
    depot_id: u64,
    manifest_id: u64,
    branch: String,
    branch_password: String,
}

struct EpicStoreData {
    catalog_item_id: String, // 128-bit identifier stored as a string
    app_version_string: String,
}

struct MicrosoftStoreData {
    package_family_name: String,
    package_version: String,
}
```

### Human-Friendly Explanation

1. **Metadata**
    - Event Counter: A number tracking how many events have occurred (u32).
        - This matches [header.bin][headerbin]'s number of events in the unpacked loadout.

2. **Packages**
    - A list of all packages in the loadout, each containing:
        - Package ID: A unique identifier for the package ([XXH3 hash][hashing] of the package ID).
        - Version: The semantic version of the package as a string (e.g., `1.2.3`).
        - State: The current state of the package using the [`PackageState`][packagestate] enum.
        - Configuration Index: An optional index into the configurations Vec.
    - Corresponds to [Package References][packagereferenceidsbin].
    - Only one version of a package can be installed at a time.

3. **Configurations**
    - A list of raw configuration data for packages.
    - Indexed by the `configuration_index` in `PackageInfo`.
    - Corresponds to [config.bin & config-data.bin][configbin].
    - Configurations are not version specific. They persist across package versions.

4. **External Configurations**
    - A list of external configuration information for packages, each containing:
        - Package ID: The [XXH3 hash][hashing] of the package ID this config belongs to.
        - Path: The relative path to the external config file.
        - Data: The raw content of the external config file.
    - Corresponds to [external-config.bin, external-config-data.bin, & external-config-paths.bin][externalconfigbin].
    - External configurations are tracked separately from internal configurations.

5. **Mod Load Order**
    - An ordered list of indices representing the current load order of mods.
    - These indices correspond to the positions in the `packages` list.

6. **Loadout Display Settings**
    - Enabled Grid Sort Mode: How enabled mods are sorted in the mod view ([`SortingMode`][sortingmode]).
    - Disabled Grid Sort Mode: How disabled mods are sorted in the mod view ([`SortingMode`][sortingmode]).
    - Mod Load Order Sort: Whether mods are shown `top to bottom` or `bottom to top` for load ordering ([`SortOrder`][sortorder]).
    - Grid Display Style: The visual style of the grid that displays enabled mods ([`GridDisplayMode`][griddisplaymode]).

7. **Game Store Manifest**
    - Store Type: Which store the game is from ([`StoreType`][storetype]).
    - Store Data: A structure containing common fields and store-specific data:
        - Common fields for all store types:
            - `exe_hash`: Hash of the game executable ([XXH3 hash][hashing]).
            - `exe_path`: Path to the game executable.
            - `app_id`: Application ID of the game (string format for flexibility).
        - Store-specific data is included in separate sub-structs:
            - [GOG][gog-store-data]: `game_id`, `build_id`, `version_name`.
            - [Steam][steam-store-data]: `app_id` (as u64), `depot_id`, `manifest_id`, `branch`, `branch_password`.
            - [Epic][epic-store-data]: `catalog_item_id`, `app_version_string`.
            - [Microsoft][microsoft-store-data]: `package_family_name`, `package_version`.

        The `store_type` field determines which store-specific struct is populated and should be used.

8. **Commandline Parameters**
    - A string containing the current commandline parameters for the game.

## How Snapshots are Used

!!! info "Snapshots are the ***current*** in-memory representation of the current state of the [unpacked loadout][unpacked]."

Snapshots are used to restore the [unpacked loadout][unpacked] without replaying all events.

## How Snapshots are Stored

!!! info "Snapshots are stored as a [single `.snapshot.bin` file][loadout-location]."

- Serialized with [bitcode][bitcode].
    - This data will be mutated after loading, so `zero-copy` serialization is not desireable.
- Compressed with Zstandard.
- Updated periodically, or when a loadout is flushed back to disk.

Snapshots will be prefixed with a version declared as `u32` integer.

Any incompatible changes to the snapshot schema; for example:

- Changing the order of a field.
- Adding a new field.
- Removing a field.
- Changing the type of a field.

Will increment the version number. Migration is a possibility, but changes in schema are not
expected to be frequent, and replaying events is expected to be very fast; therefore initially
there will be no migration code; as to avoid bloating the binary.

## Extra Benefits

- Used in [fault handling][fault-handling] to recover from crashes.
    - Can partially reconstruct event history if needed.

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
[gog-store-data]: ./Unpacked.md#gog
[steam-store-data]: ./Unpacked.md#steam
[epic-store-data]: ./Unpacked.md#epic
[microsoft-store-data]: ./Unpacked.md#microsoft
[unpacked]: ./Unpacked.md
[loadout-location]: ../About.md#location
[bitcode]: ../../../../Research/Library-Sizes/Serializers.md#bitcode
[configbin]: ./Unpacked.md#configbin
[externalconfigbin]: ./Unpacked.md#external-configbin
[packagereferenceidsbin]: ./Unpacked.md#package-idsbin