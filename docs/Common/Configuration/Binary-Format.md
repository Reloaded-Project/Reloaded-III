!!! warning "Work in Progress"

# Config Binary Format

!!! info "This page describes the binary format used for serializing and deserializing the [config.toml][config-schema] file."

The binary format is designed to be compact and efficient for storing and loading configuration settings.

## Format Overview

The binary format consists of a header followed by a series of key-value pairs representing the
configuration settings.

All numbers are stored as little endian.

### Header

The header is a single byte containing version and key size information.

| Bits | Description                                          |
| ---- | ---------------------------------------------------- |
| 0-2  | Version number, 0-7. Currently `0` and `1` are used. |
| 3-5  | Reserved                                             |
| 6-7  | Key size in bytes. 1, 2, 4, or 8                     |

!!! note "The higher bits of the version number may be repurposed some day."

Currently 2 versions exist:

- `Version 0`: (Basic Types only)
- `Version 1`: (Extended Types)

Version 0 allows for twice amount of items if the config only uses basic primitives.
That is the case for most mods at least.

### Key-Value Pairs

Following the header, the file contains a sequence of key-value pairs.

The size of the key depends on the [header](#header), so if the key size is set to 2, the `Index`
will have 12 bits available.

#### Key (Version 0)

| Index (0-3) | ValueType (4-7) |
| ----------- | --------------- |
| `{XXXX}`    | `{YYYY}`        |

| Data Type | Name      | Label | Description                                           |
| --------- | --------- | ----- | ----------------------------------------------------- |
| `u4`      | Index     | X     | (0-15) Corresponds to [Index][config-schema]          |
| `u4`      | ValueType | Y     | (0-15) Type of [Value (V1)](#version-1-table) stored. |

#### Key (Version 1)

| Index (0-4) | ValueType (5-7) |
| ----------- | --------------- |
| `{XXXXX}`   | `{YYY}`         |

| Data Type | Name      | Label | Description                                          |
| --------- | --------- | ----- | ---------------------------------------------------- |
| `u5`      | Index     | X     | (0-31) Corresponds to [Index][config-schema]         |
| `u3`      | ValueType | Y     | (0-7) Type of [Value (V0)](#version-0-table) stored. |

## Value

### Version 0 (Table)

| Type | Name       | Size (bytes) |
| ---- | ---------- | ------------ |
| 00   | Bool (ON)  | 0            |
| 01   | Bool (OFF) | 0            |
| 02   | i8         | 1            |
| 03   | i16        | 2            |
| 04   | i32        | 4            |
| 05   | i64        | 8            |
| 06   | f32        | 4            |
| 07   | String     | Variable     |

### Version 1 (Table)

!!! note "This is an extension of [Version 0](#version-0-table) table"

| Type | Name       | Size (bytes) |
| ---- | ---------- | ------------ |
| 00   | Bool (ON)  | 0            |
| 01   | Bool (OFF) | 0            |
| 02   | i8         | 1            |
| 03   | i16        | 2            |
| 04   | i32        | 4            |
| 05   | i64        | 8            |
| 06   | f32        | 4            |
| 07   | String     | Variable     |
| 08   | u8         | 1            |
| 09   | u16        | 2            |
| 0A   | u32        | 4            |
| 0B   | u64        | 8            |
| 0C   | f64        | 8            |
| 0D   | StringList | Variable     |
| 0E   | i24        | 3            |

### Value Mapping

The schema's settings map in the following way:

| Type                                                               | Value Type         |
| ------------------------------------------------------------------ | ------------------ |
| [Boolean][setting-bool]                                            | Bool ON/OFF        |
| [Enum][setting-enum]                                               | u8/16/32/64        |
| [Integer][setting-int] & [Int Range][setting-int-range]            | (i/u)(8/16/32/64)  |
| [Float][setting-float] & [Float Range][setting-float-range]        | (f32/f64)          |
| [File][setting-file], [Folder][setting-folder], [URL][setting-url] | (string)           |
| [Color][setting-color]                                             | (i24) or (i32/u32) |

### Color Setting

A color setting is serialized as 4 bytes in RGBA order.

| Byte | Channel |
| ---- | ------- |
| 0    | Red     |
| 1    | Green   |
| 2    | Blue    |
| 3    | Alpha   |

If the alpha channel is not present, the value serialized as an `03` (i24), otherwise it's stored
as an `07` i32.

### String List Setting

!!! info "A string list setting is serialized as a series of null-terminated UTF-8 strings."

Followed by an additional null byte to indicate the end of the list. i.e. an `empty string`.

## Parsing the File

!!! tip "Read the key-value pairs until you reach the end of file."

    It's that simple.

## Optimizing Compression Efficiency

!!! tip "To maximize compression efficiency, we use a couple of tricks."

### SOLID Compression

!!! info "To optimize for SOLID compression, we write the values in the `index` order."

This increases the amount of repeating bytes between two given settings files in the same block.

For example, when packed as part of [Loadout][loadout].

[loadout]: ../../Server/Storage/Loadouts/About.md
[packagemetadatabin]: About.md#package-references
[config-schema]: ./Config-Schema.md
[setting-bool]: ./Config-Schema.md#boolean-setting
[setting-int]: ./Config-Schema.md#integer-setting
[setting-int-range]: ./Config-Schema.md#integer-range-setting
[setting-enum]: ./Config-Schema.md#choice-enum-setting
[setting-float]: ./Config-Schema.md#float-setting
[setting-float-range]: ./Config-Schema.md#float-range-setting
[setting-file]: ./Config-Schema.md#file-setting
[setting-folder]: ./Config-Schema.md#folder-setting
[setting-url]: ./Config-Schema.md#url-setting
[setting-color]: ./Config-Schema.md#color-setting