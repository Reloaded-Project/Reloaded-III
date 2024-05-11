!!! info "Loadouts encapsulate a group of mods and their configurations."

A Loadout is a way to organize and manage a specific set of mods and their associated configurations.

!!! tip "Think of it like your `Create a Class` loadout in `Call of Booty`"

Loadouts allow you to experiment with different mod setups and configurations, with the ability
to switch between them on the fly.

## What a Loadout Contains

!!! tip "A Loadout consists of the following components"

- **Mod List**: Historical metadata of mods (NOT FILES) used in the Loadout.
- **Mod Configurations**: History of configuration settings for each mod in the Loadout.

## Event Sourcing

!!! tip "Loadouts in Reloaded-III use the concept of 'events' to track and manage changes over time."

Event sourcing is a design pattern that represents the state of a system as a sequence of events.

Examples of events include:

- ***Adding a mod***: This stores the mod's metadata in the Loadout.
- ***Editing a mod's configuration***: This stores the new configuration settings for the mod.

These events are stored in a sequential manner. This means that the Loadout can be reverted to any
previous state by "replaying" the events in order.

Additional benefits include:

- **History**: The event log is a complete history, enabling users to review past states and changes.
- **Efficiency**: Incremental changes use very little disk space.
- **Reproducibility**: You can reproduce the ***exact 1:1 state*** of the Loadout at any point in time.

## Sharing and Syncing Loadouts

!!! info "Loadouts in Reloaded-III are designed to be easily shared & synced across different devices or with other users."

Since Loadouts are represented as a sequence of events, they can be efficiently serialized and
stored in a compact format.

Loadouts just like pretty much everything else in Reloaded-III are packages. This means they can be
packed and downloaded by another user as a single file. The only caveat is they are stored outside
of the main `Packages` directory.

Loadouts can be shared with other users with or without historical data. If shared without historical data,
a 'snapshot' of the current state is created, and event history is trimmed to reduce the package size.

### Sync Methods

!!! info "Reloaded-III loadouts are intended to be share-able through the following methods"

- **Cloud Sync**: GDrive, MEGA, Dropbox, etc.
- **Game Store SaveData Sync**: e.g. Steam Cloud, GOG Galaxy SDK
- **Sharing as a Package**: Can be uploaded to a modding site, like any regular mod.
    - Other users can then import it by downloading it like a normal mod.

## Loadout Locations (Files)

Items at [root level][root-level]:

| Item                     | Path                             | Description |
| ------------------------ | -------------------------------- | ----------- |
| [HashCache](#hash-cache) | `hashes.bin` & `strings.bin.zst` |             |

### Hash Cache

!!! info "Contains a cache of every file's hash in the Loadout"

!!! note "This item is not packed when a loadout is exported."

!!! tip "If missing this file is regenerated."

This file (`hashes.bin`) has the following format:

- `u8`: Version
- `u24`: Reserved
- `u32`: EntryCount
- `Entry [EntryCount]`: Entries

The struct `Entry` (32 bytes) is defined as:

| Data Type | Name         | Description                                |
| --------- | ------------ | ------------------------------------------ |
| `u48`     | PathOffset   | Offset into the start of the UTF-8 string. |
| `u16`     | PathLength   | Length of the string at offset.            |
| `u64`     | FileHash     | Hash of the file (`XXH3`)                  |
| `u64`     | FileSize     | Size of the file.                          |
| `u64`     | LastModified | Converted from `chrono::DateTime<Utc>`     |

We store the hash of the file to avoid recomputing it, as the I/O reads involved
would otherwise be too expensive. Hash of the file path (if needed) can be computed
dynamically on the other hand.

Unlike general [hashing guidelines][hashing], we use XXH3 so the struct can be kept at 32-bytes,
this makes our structure more cache friendly as it aligns nicer with 64-byte cache lines.

#### Strings.bin.zst

!!! info "This is a raw buffer of strings encoded using UTF-8"

The start and length of each string can be found in the above `Entry` struct(s).

It is compressed with `ZStandard -16` when being written to disk.

## Loadout Locations (Folders)

| Item                                      | Subfolder | Description                           |
| ----------------------------------------- | --------- | ------------------------------------- |
| [Configurations](#package-configurations) | `Configs` | Mod and other package configurations. |

## Packing Strategy

!!! info "To minimize loadout size when packed, the following strategy is used"


[root-level]: ../Locations.md#items-to-store
[hashing]: ../../../Common/Hashing.md