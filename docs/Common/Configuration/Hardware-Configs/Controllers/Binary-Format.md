# Controller Settings Binary Schema

!!! info "This section describes the binary schema for serializing controller settings efficiently."

The schema is designed to pack the settings data tightly to minimize storage space.

The data assumes it is not aligned.

## Schema Overview

The controller settings data is stored as a sequence of bytes, with each setting represented by a
group of bytes.

All multi-byte values are stored in little-endian format.
The file is 4 byte aligned.

!!! note "This file is not as aggressively packed as the other configs."

    The number of times a user rebinds is usually small.
    And we can still make use of SOLID compression.

## Header

| Field             | Type | Description                                 |
| ----------------- | ---- | ------------------------------------------- |
| `version`         | u8   | The file version. Currently 0.              |
| `num_controllers` | u8   | The number of controller specific settings. |
| `num_players`     | u8   | The number of player slots.                 |
| `reserved`        | u8   |                                             |

## Controller Entry

!!! info "This involves a sequence of settings for each controller."

| Field              | Type              | Description                                                                    |
| ------------------ | ----------------- | ------------------------------------------------------------------------------ |
| `controller_index` | u8                | The unique identifier for the controller.                                      |
| `reserved`         | u8                | Unused                                                                         |
| `config_size`      | u16               | The size of the embedded regular config in bytes.                              |
| `config_data`      | u8[`config_size`] | Config data serialized using [Standard Binary-Format.md][config-binary-format] |

## Player Entry

!!! info "This involves a sequence of settings for each player."

| Field          | Type | Description                               |
| -------------- | ---- | ----------------------------------------- |
| `file_size`    | u19  | The size of the file.                     |
| `num_settings` | u13  | The number of settings (for each player). |

!!! note "`file_size` is in lower bits, `num_settings` is in higher bits."

    `num_settings` is constrained to 8191.

    Hopefully that's sufficient.

Size: 4 bytes

### Binding Header

Each setting entry in the binary data follows this format:

| Field           | Type                                         | Description                             |
| --------------- | -------------------------------------------- | --------------------------------------- |
| `setting_index` | u16                                          | The unique index of the setting.        |
| `num_bindings`  | u8                                           | The number of bindings for the setting. |
| `padding`       | u8                                           | Currently unused.                       |
| `binding_data`  | [binding-entry][config-schema] | The serialized data for each binding.   |

Size: 4

#### Binding Entry

Each binding entry within a setting follows this format:

| Field              | Type | Description                                                                     |
| ------------------ | ---- | ------------------------------------------------------------------------------- |
| `controller_index` | u8   | The index of the gamepad to which the binding applies.                          |
| `type`             | u8   | The type of the binding ([0: button, 1: axis, 2: hat][available-bindings]).     |
| `value`            | u8   | The value of the binding ([button, axis, or hat constant][available-bin2dings]). |
| `comparison`       | u8   | The comparison operator for axis bindings (0: >=, 1: <=).                       |
| `threshold`        | f32  | The threshold value for axis bindings.                                          |
| `deadzone`         | f32  | The deadzone value for axis bindings.                                           |
| `radius`           | f32  | The radius value for axis bindings.                                             |
| `scale`            | f32  | The scale value for button bindings to emulate an axis.                         |

Size: 20 bytes

## Serialization Steps

1. Write the header.
2. For each controller:
      1. Write the `controller_index` as a 1-byte unsigned integer.
      2. Serialize the regular config data for the controller's settings according to the `Binary-Format.md` schema.
      3. Write the size of the serialized config data as a 2-byte unsigned integer (`config_size`).
      4. Write the serialized config data.
3. For each player:
      1. Write the `file_size` and `num_settings` as a 4-byte value, with `file_size` in the lower 19 bits and `num_settings` in the upper 13 bits.
      2. For each setting:
         1. Write the `setting_index` as a 2-byte unsigned integer.
         2. Write the `num_bindings` as a 1-byte unsigned integer.
         3. For each binding in the setting:
            1. Write the `controller_index` as a 1-byte unsigned integer.
            2. Write the `type` as a 1-byte unsigned integer.
            3. Write the `value` as a 2-byte unsigned integer.
            4. Write the `threshold` as a 4-byte floating-point value.
            5. Write the `comparison` as a 1-byte unsigned integer.
            6. Write the `deadzone` as a 4-byte floating-point value.
            7.  Write the `radius` as a 4-byte floating-point value.
            8.  Write the `scale` as a 4-byte floating-point value.

## Deserialization Steps

1. Read the header.
2. For each controller (repeated `num_controllers` times):
      1. Read the `controller_index` as a 1-byte unsigned integer.
      2. Read the `config_size` as a 2-byte unsigned integer.
      3. Read `config_size` bytes of serialized regular config data.
      4. Deserialize the regular config data according to the `Binary-Format.md` schema.
3. For each player (repeated `num_players` times):
      1. Read the `file_size` and `num_settings` as a 4-byte value.
      2. Extract `file_size` from the lower 19 bits and `num_settings` from the upper 13 bits.
      3. For each setting (repeated `num_settings` times):
         1. Read the `setting_index` as a 2-byte unsigned integer.
         2. Read the `num_bindings` as a 1-byte unsigned integer.
         3. For each binding (repeated `num_bindings` times):
            1. Read the `controller_index` as a 1-byte unsigned integer.
            2. Read the `type` as a 1-byte unsigned integer.
            3. Read the `value` as a 2-byte unsigned integer.
            4. Read the `threshold` as a 4-byte floating-point value.
            5. Read the `comparison` as a 1-byte unsigned integer.
            6. Read the `deadzone` as a 4-byte floating-point value.
            7.  Read the `radius` as a 4-byte floating-point value.
            8.  Read the `scale` as a 4-byte floating-point value.
            9.  Reconstruct the binding entry using the read values.
      4. Reconstruct the setting entry using the `setting_index`, `num_bindings`, and the list of binding entries.

[config-binary-format]: ../../Binary-Format.md
[config-schema`]: ./Config-Schema.md
[available-bindings]: ./Config-Schema.md#available-gamepad-bindings