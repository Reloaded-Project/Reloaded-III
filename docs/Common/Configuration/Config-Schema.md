# Mod Configurations

!!! warning "TODO: Enabling 'features' in configs."

!!! info "This file specifies the schema for the `config.toml` file that defines package configuration settings."

The `config.toml` file is used to declare a list of configurable settings for a package (e.g. mod).

It allows authors to expose various options to users, with Reloaded3 automatically generating
an appropriate UI for adjusting these settings based on their types and specified constraints.

## File Structure

The `config.toml` file has the following structure:

```toml
[general]
name = "Mod Name"
language_folder = "config"
default_language = "en-GB.toml"

[[settings]]
type = "bool"
name = "SETTING_BOOL"
description = "SETTING_BOOL_DESC"
default = true

[[settings]]
type = "choice"
name = "SETTING_CHOICE"
description = "SETTING_CHOICE_DESC"
choices = ["OPTION_1", "OPTION_2", "OPTION_3"]
default = "OPTION_2"

# Additional setting definitions...
```

The file is divided into two main sections:

- `[general]`: Contains general metadata about the mod and its configuration.
- `[[settings]]`: An array of setting definitions, with each setting enclosed in double brackets `[[]]`.

## General Metadata

The `[general]` section contains the following fields:

| Field              | Type   | Description                                                          |
| ------------------ | ------ | -------------------------------------------------------------------- |
| `name`             | string | The name of the mod configuration. May be used in the UI.            |
| `language_folder`  | string | The subfolder containing the language files for the config.          |
| `default_language` | string | The default language file to use, relative to the `language_folder`. |

### File Locations

!!! example "An example of how various files are set."

Given a mod folder structured like

```
reloaded3.utility.examplemod.s56
├── config
│   └── config.toml
├── languages
│   └── config
│       ├── en-GB.toml
│       └── uwu-en.toml
├── modfiles
│   └── mod.dll
├── package
│   └── images
│       └── config-image-1.jxl
└── package.toml
```

Setting `language_folder = "config"` and `default_language = "en-GB.toml"` would use the `en-GB.toml` file.

Setting an image field to `config-image-1.jxl` would use the image located in `package/images/config-image-1.jxl`.

For more details regarding why the files are separated in this way, see the note in [Packaging: Images][packaging-images].

## Common Setting Fields

All setting types share the following common fields:

| Field         | Type      | Description                                                                               |
| ------------- | --------- | ----------------------------------------------------------------------------------------- |
| `index`       | number    | Index of the setting. Make this a unique number and never change it.                      |
| `type`        | string    | The data type of the setting. See individual setting types.                               |
| `name`        | string    | The localization key for the setting name.                                                |
| `description` | string    | The localization key for the setting description.                                         |
| `default`     | varies    | The default value for the setting. Type depends on `type`.                                |
| `apply_on`    | string    | When to apply setting changes. One of "restart", "save", "instant".                       |
| `variable`    | string    | Optional variable name to reference the setting in conditionals.                          |
| `client_side` | bool      | [Optional] Indicates if the setting should not be overwritten by the host in multiplayer. |
| `show_if`     | condition | See: [Conditional Settings](#conditional-settings)                                        |

The `name` and `description` fields should reference localization keys as described in the
[Localisation Format][localisation-format] page.

### Field Types

- `type`, `name`, `description`, `apply_on`, `variable`: string
- `default`: varies based on the setting type

### apply_on

- `restart`: Requires a restart of application/game to apply changes.
- `save`: Applies settings when you hit `save` button.
- `instant`: Applies settings in real-time.

### client_side

!!! info "If true, this config won't be overwritten when joining an online multiplayer lobby."

This allows for mods such as UI mods to be used in mods that add online play without forcibly being disabled.

By default this value is false. So config would get overwritten.

## How are Settings Displayed?

!!! tip "The settings are displayed in the exact order they are defined in the `config.toml` file."

What the Launcher UI displays should match 1:1 with the order of settings in the `config.toml` file.

## Setting Types

!!! info "Declares the type of settings you can display."

### Boolean Setting

!!! info "A boolean value, presented as a checkbox."


| Field       | Type   | Description                                      |
| ----------- | ------ | ------------------------------------------------ |
| `image_on`  | string | [Optional] Image to display when value is true.  |
| `image_off` | string | [Optional] Image to display when value is false. |

Shown as: `[✓] Enable Feature X` or `Enable Feature X ( O)`

Example:

```toml
[[settings]]
index = 0
type = "bool"
name = "SETTING_ENABLE_X"
description = "SETTING_ENABLE_X_DESC"
default = false
image_on = "enable_x_on.jxl"
image_off = "enable_x_off.jxl"
# apply_on =
# variable =
# client_side =
# show_if =
```

This allows the user to enable or disable a setting

### Choice (Enum) Setting

!!! info "A multiple-choice setting, presented as a dropdown."

Additional Fields:

| Field           | Type     | Description                                                                          |
| --------------- | -------- | ------------------------------------------------------------------------------------ |
| `choices`       | [string] | An array of localization keys for the available options.                             |
| `choice_images` | [string] | [Optional] An array of images for each choice, corresponding to the `choices` array. |

!!! example "Example: A 'render quality' dropdown."

    This setting allows the user to choose between different rendering resolutions for shadows.

```toml
[[settings]]
index = 1
type = "choice"
name = "SHADOW_RESOLUTION"
description = "SHADOW_RESOLUTION_DESC"
choices = ["LOW_QUALITY", "MEDIUM_QUALITY", "HIGH_QUALITY"]
choice_images = ["shadow_low.jxl", "shadow_medium.jxl", "shadow_high.jxl"]
default = "MEDIUM_QUALITY"
# apply_on =
# variable =
# client_side =
# show_if =
```

Shown as: `Render Quality: [Medium Quality ▼]`

!!! danger "It's a breaking change to remove an entry from `choices`."

    You can hide a choice by replacing it with a blank string, `""`, this will hide it from the user UI.

    ```toml
    choices = ["LOW_QUALITY", "", "HIGH_QUALITY", "ULTRA_QUALITY"]
    ```

    Here, `MEDIUM_QUALITY` was hidden.

### Integer Setting

!!! info "An integer value, presented as a number input."

Additional Fields:

| Field        | Type     | Description                                     |
| ------------ | -------- | ----------------------------------------------- |
| `min`        | int      | (Default: -2^63) The minimum allowed value.     |
| `max`        | int      | (Default: -2^63) The maximum allowed value.     |
| `formatters` | [string] | [Formatters][formatters] to apply to the value. |

!!! example "Example: Changing the size of an inventory"

    This setting allows the user to set the max number of items in their inventory, from 0 to 100.

```toml
[[settings]]
index = 2
type = "int"
name = "INVENTORY_SIZE"
description = "INVENTORY_SIZE_DESC"
default = 5
min = 0
max = 100
formatters = ["FRIENDLY"]
# apply_on =
# variable =
# client_side =
# show_if =
```

Shown as: `Inventory Size: [50]`

### Integer Range Setting

!!! info "An integer value within a range, presented as a slider."

Additional Fields:

| Field          | Type             | Description                                     |
| -------------- | ---------------- | ----------------------------------------------- |
| `min`          | int              | (Default: -2^63) The minimum allowed value.     |
| `max`          | int              | (Default: 2^63) The maximum allowed value.      |
| `step`         | int              | The increment step for the slider.              |
| `labels`       | [string, string] | Localization keys for min and max value labels. |
| `formatters`   | [string]         | [Formatters][formatters] to apply to the value. |
| `range_images` | [[int, string]]  | [Optional] The image to display for each value. |

!!! example "Example: Changing the intensity of a visual effect"

    This setting controls the intensity of a visual effect, from 0% (low) to 100% (high), with
    images showing the effect at different levels.

```toml
[[settings]]
index = 3
type = "int_range"
name = "SETTING_INTENSITY"
description = "SETTING_INTENSITY_DESC"
min = 0
max = 100
step = 5
default = 50
labels = ["LABEL_LOW", "LABEL_HIGH"]
formatters = ["PERCENTAGE"]
range_images = [
    [0, "intensity_low.jxl"],
    [50, "intensity_medium.jxl"],
    [80, "intensity_high.jxl"]
]
# apply_on =
# variable =
# client_side =
# show_if =
```

Shown as:

```
                           50%
Effect Intensity: [••••••••••--------]
                 LOW                HIGH
```

!!! note "About `range_images`"

    The values specified here are minimums.
    So in this example, `intensity_low.jxl` will be used for values 0-49, and `intensity_medium.jxl` for 50-79.

### Float Setting

!!! info "A floating-point value, presented as a number input."

Additional Fields:

| Field        | Type     | Description                                     |
| ------------ | -------- | ----------------------------------------------- |
| `min`        | float    | The minimum allowed value.                      |
| `max`        | float    | The maximum allowed value.                      |
| `places`     | int      | The number of decimal places (0-5).             |
| `formatters` | [string] | [Formatters][formatters] to apply to the value. |

!!! example "Example: Change the boss health multiplier"

    This setting allows the user to adjust the health of boss HP between 0.1x and 10.0x,
    with two decimal places of precision.

```toml
[[settings]]
index = 4
type = "float"
name = "SETTING_BOSS_HEALTH_SCALE"
description = "SETTING_BOSS_HEALTH_SCALE_DESC"
default = 1.0
min = 0.1
max = 10.0
places = 2
formatters = ["ROUNDED"]
# apply_on =
# variable =
# client_side =
# show_if =
```

Shown as: `Boss Health: [1.50]`

### Float Range Setting

!!! info "A floating-point value within a range, presented as a slider."

Additional Fields:

| Field          | Type             | Description                                     |
| -------------- | ---------------- | ----------------------------------------------- |
| `min`          | float            | The minimum allowed value.                      |
| `max`          | float            | The maximum allowed value.                      |
| `step`         | float            | The increment step for the slider.              |
| `labels`       | [string, string] | Localization keys for min and max value labels. |
| `formatters`   | [string]         | [Formatters][formatters] to apply to the value. |
| `range_images` | [[int, string]]  | [Optional] The image to display for each value. |

!!! example "Example: Change the boss health multiplier"

    This setting allows the user to adjust the health of boss HP between 0.1x and 10.0x,
    with two decimal places of precision.

```toml
[[settings]]
index = 5
type = "float_range"
name = "SETTING_VOLUME"
description = "SETTING_VOLUME_DESC"
min = 0.0
max = 1.0
step = 0.1
default = 0.5
labels = ["LABEL_MUTE", "LABEL_MAX"]
formatters = ["PERCENTAGE"]
range_images = [
    [0.0, "volume_mute.jxl"],
    [0.5, "volume_medium.jxl"],
    [0.8, "volume_high.jxl"]
]
# apply_on =
# variable =
# client_side =
# show_if =
```

Shown as:

```
                        50%
Master Volume: [••••••••••--------]
              MUTE                MAX
```

!!! note "About `range_images`"

    The values specified here are minimums.
    So in this example, `volume_mute.jxl` will be used for `x < 0.5`, and `intensity_medium.jxl` for x `>0.5` and `<0.8`.

### File Setting

!!! info "A file path, presented as a file picker dialog."

Additional Fields:

| Field      | Type   | Description                                               |
| ---------- | ------ | --------------------------------------------------------- |
| `filter`   | string | File extension filter (e.g. `"*.png"`).                   |
| `default`  | string | Default file path (relative to a package folder).         |
| `title`    | string | Localization key for the title of the file picker dialog. |
| `multiple` | bool   | If `true`, allows selecting multiple files.               |

!!! warning

    Use of absolute paths or paths outside of a Reloaded3 package folder is discouraged as it breaks
    reproducibility. The setting cannot be shared across different machines or installations.

    Whenever possible, we will auto convert to [Special Location References](#special-location-references).

!!! example "Example: Select a custom 3D model file"

    This setting allows the user to select a custom 3D model file for their character.

```toml
[[settings]]
index = 6
type = "file"
name = "SETTING_MODEL"
description = "SETTING_MODEL_DESC"
default = "models/custom.obj"
filter = "*.obj"
title = "TITLE_SELECT_MODEL"
multiple = false
# apply_on =
# variable =
# client_side =
# show_if =
```

Shown as: `Custom Model: [models/custom.obj] [Browse...]`

### Folder Setting

!!! info "A folder path, presented as a folder picker dialog."

Additional Fields:

| Field     | Type   | Description                                                 |
| --------- | ------ | ----------------------------------------------------------- |
| `default` | string | Default folder path (relative to a package folder).         |
| `title`   | string | Localization key for the title of the folder picker dialog. |

!!! warning

    Use of absolute paths or paths outside of a Reloaded3 package folder is discouraged as it breaks
    reproducibility. The setting will not be shared across different machines or installations.

    Whenever possible, we will auto convert to [Special Location References](#special-location-references).

!!! example "Example: Selecting a custom folder for Replay Backups"

    This setting allows the user to choose a custom folder for saving replays of online races.
    These could later be played back.

```toml
[[settings]]
index = 7
type = "folder"
name = "SETTING_REPLAY_FOLDER"
description = "SETTING_REPLAY_FOLDER_DESC"
default = "output"
title = "TITLE_SELECT_REPLAY_FOLDER"
# apply_on =
# variable =
# client_side =
# show_if =
```

Shown as: `Output Folder: [C:\Users\Username\Documents\MyGame\Output] [Select Folder...]`

### Color Setting

!!! info "A color value, presented as a color picker."

Additional Fields:

| Field   | Type | Description                       |
| ------- | ---- | --------------------------------- |
| `alpha` | bool | Whether to include alpha channel. |

!!! example "Example: Select a colour for car nitro"

    This setting allows the user to pick a custom color for a car's nitrous exhaust.

```toml
[[settings]]
index = 8
type = "color"
name = "SETTING_NITRO_COLOR"
description = "SETTING_NITRO_COLOR_DESC"
default = "#FF0000"
alpha = true
# apply_on =
# variable =
# client_side =
# show_if =
```

!!! note "The default is specified as `RGBA`"

Shown as: `[■] #FF5500AA [Pick Color...]`

### String Setting

!!! info "A string value, presented as a text input."


| Field       | Type | Description                     |
| ----------- | ---- | ------------------------------- |
| `hide_text` | bool | Hides the text (password input) |

!!! example "Example: Rename Player"

    This setting allows the user to rename their player in multiplayer games.

```toml
[[settings]]
index = 9
type = "string"
name = "SETTING_PLAYERNAME"
description = "SETTING_PLAYERNAME_DESC"
default = "LABEL_DEFAULT_PLAYERNAME"
hide_text = false
# apply_on =
# variable =
# client_side =
# show_if =
```

Shown as: `Player Name: [PlayerOne]`

### String List Setting

!!! info "A list of strings, presented as a comma-separated text input."

!!! example "Example: Specify excluded file extensions"

    This setting allows the user to specify a list of file extensions to exclude
    from an operation.

```toml
[[settings]]
index = 10
type = "string_list"
name = "SETTING_EXCLUDED_EXT"
description = "SETTING_EXCLUDED_EXT_DESC"
default = ["dll", "exe"]
# apply_on =
# variable =
# client_side =
# show_if =
```

Shown as: `Excluded Extensions: [dll, exe, tmp]`

### URL Setting

!!! info "A read-only setting that opens a URL when clicked."

!!! example "Example: Homepage URL"

    This setting displays a link to the mod's homepage.

```toml
[[settings]]
index = 11
type = "url"
name = "SETTING_HOMEPAGE"
description = "SETTING_HOMEPAGE_DESC"
default = "https://example.com"
# apply_on =
# variable =
# client_side =
# show_if =
```

Shown as: `Mod Homepage: [Visit Website]`

## Conditional Settings

!!! info "Settings can be conditionally displayed based on the values of other settings."

To conditionally display a setting, add a `show_if` field with an array of condition expressions.
Each condition expression has the following format:

```toml
{
    variable = "<variable_name>",
    comparator = "<comparator>",
    value = "<value>"
}
```

Where:

- `<variable_name>` is the variable name of the setting to check.
- `<comparator>` is one of: `=`, `!=`, `>`, `>=`, `<`, `<=`.
- `<value>` is the value to compare against, always represented as a string.
- `<op>` is either `AND` or `OR`, specifying how this condition combines with the previous one.

Example:
```toml
[[settings]]
index = 12
type = "bool"
name = "SETTING_ENABLE_LOGGING"
description = "SETTING_ENABLE_LOGGING_DESC"
default = false
variable = "enable_logging"

[[settings]]
index = 13
type = "choice"
name = "SETTING_LOG_LEVEL"
description = "SETTING_LOG_LEVEL_DESC"
choices = ["LOG_LEVEL_DEBUG", "LOG_LEVEL_INFO", "LOG_LEVEL_WARNING", "LOG_LEVEL_ERROR"]
default = "LOG_LEVEL_INFO"
variable = "log_level"
show_if = [
    { variable = "enable_logging", comparator = "=", value = "true" },
    { op = "AND", variable = "enable_advanced_settings", comparator = "=", value = "true" }
]
```

In this example, the `SETTING_LOG_LEVEL` setting will only be displayed if both `enable_logging` and
`enable_advanced_settings` are set to `true`.

!!! note "This can be applied to individual settings as well as groups."

## Setting Groups

!!! info "Settings can be organized into collapsible groups for better readability."

To create a group, add a `[group]` section before the settings you want to include.

Example:
```toml
[group]
name = "GROUP_GRAPHICS"
description = "GROUP_GRAPHICS_DESC"
show_global = true

[[settings]]
index = 14
type = "int"
name = "SETTING_WIDTH"
description = "SETTING_WIDTH_DESC"
default = 1920

[[settings]]
index = 15
type = "int"
name = "SETTING_HEIGHT"
description = "SETTING_HEIGHT_DESC"
default = 1080

[group]
name = "GROUP_AUDIO"
description = "GROUP_AUDIO_DESC"

[[settings]]
index = 16
type = "float"
name = "SETTING_VOLUME"
description = "SETTING_VOLUME_DESC"
default = 0.5
```

This creates two groups, "Graphics" and "Audio", each containing their respective settings.
The group's `name` and `description` fields should reference localization keys.

| Field         | Type   | Description                                                                                            |
| ------------- | ------ | ------------------------------------------------------------------------------------------------------ |
| `name`        | string | The localization key for the setting name.                                                             |
| `description` | string | The localization key for the setting description.                                                      |
| `show_global` | bool   | Display the setting as [Globally Configurable Across Loadouts](./About.md#ux-for-configuration-layers) |

## Variables and Special Locations

The `file` and `folder` settings support the use of special location references in their `default` field.

### Special Location References

!!! warning "TODO: Move these to a 'standard' mods can also use."

Special location references can be used to point to predefined directories. The available references are:

- `$ModFolder`: The root folder of the current mod.
- `$Desktop`: The user's desktop folder.
- `$Documents`: The user's documents folder.
- `$Downloads`: The user's downloads folder.
- `$Music`: The user's music folder.
- `$Pictures`: The user's pictures folder.
- `$Videos`: The user's videos folder.
- `${mod:<ModId>}`: The folder of another mod (e.g. `${mod:reloaded3.utility.examplemod.s56}`).

Example:
```toml
[[settings]]
index = 14
type = "file"
name = "SETTING_CONFIG_FILE"
description = "SETTING_CONFIG_FILE_DESC"
default = "$ModFolder/config.ini"
filter = "*.ini"
title = "TITLE_SELECT_CONFIG_FILE"
```

In this example, the `SETTING_CONFIG_FILE` setting uses the mod's root folder as the default
location to look for the configuration file.

## Value Formatters

Value formatters can be applied to settings like `int`, `int_range`, `float`, and `float_range`
to modify how the value is displayed in the UI.

The available formatters are:

- `FRIENDLY`: Displays large numbers in a friendly format (e.g. `1000000` -> 1M).
- `USE_CULTURE`: Displays numbers in user's language culture (e.g. `1000000` -> `1,000,000`).
- `SIZE_FRIENDLY`: Displays value in KB, MB or GB (etc.) for readability.
- `SIZE_FRIENDLY_RATE`: Same as `SIZE_FRIENDLY` but appends rate, e.g. `MB/s`.
- `PERCENTAGE`: Displays value as percentage (0-100).
- `ROUNDED`: Rounds value to the nearest integer.

Multiple formatters can be combined by specifying them in an array.

Example:
```toml
[[settings]]
index = 20
type = "int"
name = "SETTING_FILE_SIZE_LIMIT"
description = "SETTING_FILE_SIZE_LIMIT_DESC"
default = 1048576
min = 0
max = 10737418240
formatters = ["SIZE_FRIENDLY"]
```

In this example, the `SETTING_FILE_SIZE_LIMIT` setting will display its value in MB or GB for
better readability.

!!! note "Formatting is ***NOT*** culture specific."

    Writing the number `1000000` as a string, will always be printed as `1000000`, and not
    `1,000,000` or `1.000.000`. User's locale is not considered unless opted into.

## Simulating Multiple Config Files

!!! info "In Reloaded-II, it was possible to create multiple config files."

    However, this feature no longer exists in the current configuration system.

Instead, to achieve a similar effect, you can duplicate the fields within a single `config.toml`
file and place the settings into appropriate groups.

You can then use the `show_if` field to conditionally display or hide entire groups based on
specific conditions.

Here's an example of enabling settings for Player 1 and Player 2:

```toml
[[settings]]
index = 0
type = "bool"
name = "SETTING_ENABLE_P1"
description = "SETTING_ENABLE_P1_DESC"
default = true
variable = "enable_p1"

[[settings]]
index = 1
type = "bool"
name = "SETTING_ENABLE_P2"
description = "SETTING_ENABLE_P2_DESC"
default = false
variable = "enable_p2"

[group]
name = "GROUP_PLAYER_1"
description = "GROUP_PLAYER_1_DESC"
show_if = [{ variable = "enable_p1", comparator = "=", value = "true" }]

[[settings]]
index = 2
type = "string"
name = "SETTING_P1_NAME"
description = "SETTING_P1_NAME_DESC"
default = "Player 1"

# ... Additional Player 1 settings ...

[group]
name = "GROUP_PLAYER_2"
description = "GROUP_PLAYER_2_DESC"
show_if = [{ variable = "enable_p2", comparator = "=", value = "true" }]

[[settings]]
index = 10
type = "string"
name = "SETTING_P2_NAME"
description = "SETTING_P2_NAME_DESC"
default = "Player 2"

# ... Additional Player 2 settings ...
```

In this example, we have two settings (`SETTING_ENABLE_P1` and `SETTING_ENABLE_P2`) that
control the visibility of the Player 1 and Player 2 settings, respectively.

This is done via the [show_if](#conditional-settings) field, and the `enable_p1` and `enable_p2`
variables.

!!! tip "Careful with the copy-paste."

    Remember to update setting names, descriptions, and group names to reflect the correct player.

## Source Generation

!!! info "For details on generating source code from the `config.toml` schema file, see the [Source Generation][source-generation] page."

## Configuration Versioning

!!! info "When versioning configuration files, follow these rules"

!!! danger

    - ❌ Avoid changing the type of a setting
    - ❌ Avoid changing the meaning of a setting

    If you need to do any of the following, please make a new setting and remove the old setting.<br/>
    That way, setting files from older versions of the package will still work.

    Slightly tweaking settings in compatible ways of course, such as adjusting min-max ranges is fine.

!!! tip

    ✅ Provide default values for new settings

## Hardware Settings

!!! info "[See: Hardware Settings][hardware-settings]"

[localisation-format]: ../Localisation/File-Format.md
[formatters]: #value-formatters
[source-generation]: ./Source-Generation.md
[hardware-settings]: ./Hardware-Configs/About.md
[packaging-images]: ../../Server/Packaging/About.md#images