# Config Binary Format

!!! info "This page describes the binary format used for serializing and deserializing the [config.toml][config-toml] file."

The binary format is designed to be compact and efficient for storing and loading configuration settings.

## Format Overview

The binary format consists of a header followed by a series of key-value pairs representing the
configuration settings.

### Header

The header is a single byte containing version and key size information.

| Bits | Description                      |
| ---- | -------------------------------- |
| 0-5  | Version number, 0-61             |
| 6-7  | Key size in bytes. 1, 2, 4, or 8 |

### Key-Value Pairs

Following the header, the file contains a sequence of key-value pairs.
Each pair consists of a key and its corresponding value.

The key is represented as an unsigned integer with the size specified in the header (1, 2, 4 or 8 bytes).

The value format depends on the data type of the setting.

## Setting Serialization

### Boolean Setting

A boolean setting is serialized as a single byte.

| Value   | Byte |
| ------- | ---- |
| `false` | 0x00 |
| `true`  | 0x01 |

### Choice (Enum) Setting

A choice setting is serialized as a single byte representing the index of the selected choice.

### Integer Setting

An integer setting is serialized as a signed 32-bit integer (4 bytes) in little-endian byte order.

### Integer Range Setting

An integer range setting is serialized as a signed 32-bit integer (4 bytes) in little-endian byte
order, representing the selected value within the range.

### Float Setting

A float setting is serialized as a 32-bit IEEE 754 floating-point number (4 bytes) in little-endian
byte order.

### Float Range Setting

A float range setting is serialized as a 32-bit IEEE 754 floating-point number (4 bytes) in
little-endian byte order, representing the selected value within the range.

### File Setting

A file setting is serialized as a null-terminated UTF-8 string representing the file path.

### Folder Setting

A folder setting is serialized as a null-terminated UTF-8 string representing the folder path.

### Color Setting

A color setting is serialized as 4 bytes in RGBA order.

| Byte | Channel |
| ---- | ------- |
| 0    | Red     |
| 1    | Green   |
| 2    | Blue    |
| 3    | Alpha   |

### String Setting

A string setting is serialized as a null-terminated UTF-8 string.

### String List Setting

A string list setting is serialized as a series of null-terminated UTF-8 strings, followed by an
additional null byte to indicate the end of the list.

### URL Setting

A URL setting is serialized as a null-terminated UTF-8 string representing the URL.

## Example

Given the following `config.toml` file:

```toml
[[settings]]
index = 0
type = "bool"
name = "SETTING_ENABLE_FEATURE"
description = "SETTING_ENABLE_FEATURE_DESC"
default = true

[[settings]]
index = 1
type = "int"
name = "SETTING_COUNT"
description = "SETTING_COUNT_DESC"
default = 42
```

The corresponding binary representation would be:

```
Header (1 byte):
0b00010001 (version 1, key size 1 byte)

Settings:
0x00 0x01 (key 0, value true)
0x01 0x2A 0x00 0x00 0x00 (key 1, value 42)
```

In this example, the header indicates version 1 and a key size of 1 byte. The two settings are then
serialized as key-value pairs.

The boolean setting with key 0 is serialized as a single byte (0x01) representing `true`.

The integer setting with key 1 is serialized as a 32-bit integer (0x2A 0x00 0x00 0x00) in
little-endian byte order, representing the value 42.

## Optimizing Compression Efficiency

!!! tip "To maximize compression efficiency, we use a couple of tricks."

To optimize for SOLID compression, we write the values in the `index` order.

This increases the amount of repeating bytes between two given settings files.

## Versioning

!!! info "The binary format includes a version number to allow for future extensions and modifications."

When making changes to the binary format, increment the version number in the header.
This allows older versions of the software to detect and handle the configuration files accordingly.

If a newer version of the software encounters an older version of the configuration file, it should
still be able to parse and use the available settings, ignoring any missing or unknown settings.
```

This `Config-Binary-Format.md` page describes the binary format used for serializing and
deserializing the configuration settings defined in the `config.toml` file. It provides an overview
of the format, including the header and key-value pair structure. It also explains how each setting
type from the `Config-Schema.md` file is serialized in the binary format.

The example section demonstrates how a sample `config.toml` file would be represented in the binary
format, making it easier to understand the serialization process.

Finally, the versioning section mentions the importance of including a version number in the binary
format to handle future changes and ensure backward compatibility.

[def]: ./Config-Schema.md