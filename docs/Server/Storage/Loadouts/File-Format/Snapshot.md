## Snapshots

!!! info "Reloaded3 loadouts use a single snapshot for quick loading and fault tolerance."

A snapshot contains the current state of all loadout data, allowing for fast loading and efficient updates.

#### Snapshot Contents (Schema)

1. **Metadata**
    - EventCounter: `u32` (for diffing in fault handling)
    - TimestampLastUpdate: `u32` ([R3TimeStamp][max-numbers])

2. **Package References**
    - Array of PackageReference:
        - PackageId: `u64` ([XXH3(PackageID)][hashing])
        - Version: `String`

3. **Package States**
    - Dictionary<PackageId, PackageState>
        - PackageState: `u3` enum (Removed, Hidden, Disabled, Added, Enabled)

4. **Mod Load Order**
    - Array of PackageId (in load order)

5. **Package Configurations**
    - Dictionary<PackageId, byte[]> (raw configuration data)

6. **Loadout Display Settings**
    - LoadoutGridEnabledSortMode: `u7` enum (SortingMode)
    - LoadoutGridDisabledSortMode: `u7` enum (SortingMode)
    - ModLoadOrderSort: `u2` enum (SortOrder)
    - LoadoutGridStyle: `u4` enum (GridDisplayMode)

7. **Game Store Manifest**
    - StoreType: `u8` enum
    - NewRevision: `u16` (GameVerIdx)

8. **Commandline Parameters**
    - String (current commandline parameters)

#### Technical Details

- Serialized with MessagePack
    - Allows easy access by external software
- Compressed with Zstandard
- Updated incrementally as new events occur

#### Snapshot Usage

- Loaded first when opening a loadout
- Provides fast access to current state
- Used as a base for applying recent events

#### Benefits

- Faster loadout loading times
- Quick access to current state
- Maintains full event history
- Efficient updates (apply only changes since last snapshot)

#### Fault Tolerance

- Can reconstruct event history if needed
- Used in [fault handling][fault-handling] to recover from crashes

!!! tip "Snapshots balance performance with the flexibility of event sourcing."

[fault-handling]: ../About.md#fault-handling