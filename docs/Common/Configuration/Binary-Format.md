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

| Bits | Description                      |
| ---- | -------------------------------- |
| 0-2  | Version number, 0-7              |
| 3-5  | Reserved                         |
| 6-7  | Key size in bytes. 1, 2, 4, or 8 |

!!! note "The higher bits of the version number may be repurposed some day."

### Key-Value Pairs

Following the header, the file contains a sequence of key-value pairs.

#### Key

| Index (0-3) | ValueType (4-7) |
| ----------- | --------------- |
| `{XXXX}`    | `{YYYY}`        |

| Data Type | Name      | Label | Description                           |
| --------- | --------- | ----- | ------------------------------------- |
| `u4`      | Index     | X     | (0-15) Corresponds to [Index][config-schema] |
| `u4`      | ValueType | Y     | (0-15) Type of [Value](#value) stored.       |

The size of the key depends on the [header](#header), so if the key size is set to 2, the `Index`
will have 12 bits available.

## Value

| Type | Description   | Size (bytes) |
| ---- | ------------- | ------------ |
| 00   | Boolean (ON)  | 0            |
| 01   | Boolean (OFF) | 0            |
| 02   | i8            | 1            |
| 03   | u8            | 1            |
| 04   | i16           | 2            |
| 05   | u16           | 2            |
| 06   | i32           | 4            |
| 07   | u32           | 4            |
| 08   | i64           | 8            |
| 09   | u64           | 8            |
| 0A   | f32           | 4            |
| 0B   | f64           | 8            |
| 0C   | String        | Variable     |
| 0D   | StringList    | Variable     |
| 0E   | i24           | 3            |

The schema's settings map in the following way:

| Type                                                               | Value Type                             |
| ------------------------------------------------------------------ | -------------------------------------- |
| [Boolean][setting-bool]                                            | `00` or `01` (Bool ON/OFF)             |
| [Enum][setting-enum]                                               | `03`, `05`, `07` or `09` (u8/16/32/64) |
| [Integer][setting-int] & [Int Range][setting-int-range]            | `02` - `09` (i/u)(8/16/32/64)          |
| [Float][setting-float] & [Float Range][setting-float-range]        | `0A` or `0B` (f32/f64)                 |
| [File][setting-file], [Folder][setting-folder], [URL][setting-url] | `0C` (string)                          |
| [Color][setting-color]                                             | `0E` (i24) or `06`/`07` (i32/u32)      |

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