# Mod Configurations

!!! info "This file specifies the schema for the `config.toml` file that defines package configuration settings."

The `config.toml` file is used to declare a list of configurable settings for a package (e.g. mod).

It allows authors to expose various options to users, with Reloaded3 automatically generating
an appropriate UI for adjusting these settings based on their types and specified constraints.

## File Structure

The `config.toml` file has the following structure:

```toml
[general]
name = "Mod Name"
author = "Author Name"
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
| `name`             | string | The name of the mod. Used in the UI.                                 |
| `author`           | string | The author of the mod.                                               |
| `language_folder`  | string | The subfolder containing the language files for the config.          |
| `default_language` | string | The default language file to use, relative to the `language_folder`. |

### Language Location

!!! example "An example of how language files are set."

Given a mod folder structured like

```
reloaded3.utility.examplemod.s56
├── modfiles
│   └── mod.dll
├── languages
│   └── config
│       ├── en-GB.toml
│       └── uwu-en.toml
├── config.toml
└── package.toml
```

Setting `language_folder = "config"` and `default_language = "en-GB.toml"` would use the `en-GB.toml` file.

## Common Setting Fields

All setting types share the following common fields:

| Field         | Type   | Description                                                                               |
| ------------- | ------ | ----------------------------------------------------------------------------------------- |
| `index`       | number | Index of the setting. Make this a unique number and never change it.                      |
| `type`        | string | The data type of the setting. See individual setting types.                               |
| `name`        | string | The localization key for the setting name.                                                |
| `description` | string | The localization key for the setting description.                                         |
| `default`     | varies | The default value for the setting. Type depends on `type`.                                |
| `apply_on`    | string | When to apply setting changes. One of "restart", "save", "instant".                       |
| `variable`    | string | Optional variable name to reference the setting in conditionals.                          |
| `client_side` | bool   | [Optional] Indicates if the setting should not be overwritten by the host in multiplayer. |

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

Example:
```toml
[[settings]]
index = 0
type = "bool"
name = "SETTING_ENABLE_X"
description = "SETTING_ENABLE_X_DESC"
default = false
```

### Choice (Enum) Setting

!!! info "A multiple-choice setting, presented as a dropdown."

Additional Fields:

| Field     | Type     | Description                                              |
| --------- | -------- | -------------------------------------------------------- |
| `choices` | [string] | An array of localization keys for the available options. |

Example:
```toml
[[settings]]
index = 1
type = "choice"
name = "SETTING_RENDER_MODE"
description = "SETTING_RENDER_MODE_DESC"
choices = ["RENDER_MODE_A", "RENDER_MODE_B", "RENDER_MODE_C"]
default = "RENDER_MODE_B"
```

!!! danger "It's a breaking change to remove an entry from `choices`."

    You can hide a choice by replacing it with a blank string, `""`, this will hide it from the user UI.

    ```toml
    choices = ["RENDER_MODE_A", "", "RENDER_MODE_C", "RENDER_MODE_D"]
    ```

    Here, `MODE_B` was hidden.

### Integer Setting

!!! info "An integer value, presented as a number input."

Additional Fields:

| Field        | Type     | Description                                     |
| ------------ | -------- | ----------------------------------------------- |
| `min`        | int      | (Default: -2^63) The minimum allowed value.     |
| `max`        | int      | (Default: -2^63) The maximum allowed value.     |
| `formatters` | [string] | [Formatters][formatters] to apply to the value. |

Example:
```toml
[[settings]]
index = 2
type = "int"
name = "SETTING_COUNT"
description = "SETTING_COUNT_DESC"
default = 5
min = 0
max = 100
formatters = ["FRIENDLY"]
```

### Integer Range Setting

!!! info "An integer value within a range, presented as a slider."

Additional Fields:

| Field        | Type             | Description                                     |
| ------------ | ---------------- | ----------------------------------------------- |
| `min`        | int              | (Default: -2^63) The minimum allowed value.     |
| `max`        | int              | (Default: 2^63) The maximum allowed value.      |
| `step`       | int              | The increment step for the slider.              |
| `labels`     | [string, string] | Localization keys for min and max value labels. |
| `formatters` | [string]         | [Formatters][formatters] to apply to the value. |

Example:
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
```

### Float Setting

!!! info "A floating-point value, presented as a number input."

Additional Fields:

| Field        | Type     | Description                                     |
| ------------ | -------- | ----------------------------------------------- |
| `min`        | float    | The minimum allowed value.                      |
| `max`        | float    | The maximum allowed value.                      |
| `places`     | int      | The number of decimal places (0-5).             |
| `formatters` | [string] | [Formatters][formatters] to apply to the value. |

Example:
```toml
[[settings]]
index = 4
type = "float"
name = "SETTING_SCALE"
description = "SETTING_SCALE_DESC"
default = 1.0
min = 0.1
max = 10.0
places = 2
formatters = ["ROUNDED"]
```

### Float Range Setting

!!! info "A floating-point value within a range, presented as a slider."

Additional Fields:

| Field        | Type             | Description                                     |
| ------------ | ---------------- | ----------------------------------------------- |
| `min`        | float            | The minimum allowed value.                      |
| `max`        | float            | The maximum allowed value.                      |
| `step`       | float            | The increment step for the slider.              |
| `labels`     | [string, string] | Localization keys for min and max value labels. |
| `formatters` | [string]         | [Formatters][formatters] to apply to the value. |

Example:
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
```

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
    reproducibility. The setting will not be shared across different machines or installations.

Example:
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
```

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

Example:
```toml
[[settings]]
index = 7
type = "folder"
name = "SETTING_OUTPUT"
description = "SETTING_OUTPUT_DESC"
default = "output"
title = "TITLE_SELECT_OUTPUT"
```

### Color Setting

!!! info "A color value, presented as a color picker."

Additional Fields:

| Field   | Type | Description                       |
| ------- | ---- | --------------------------------- |
| `alpha` | bool | Whether to include alpha channel. |

Example:
```toml
[[settings]]
index = 8
type = "color"
name = "SETTING_BG_COLOR"
description = "SETTING_BG_COLOR_DESC"
default = "#FF0000"
alpha = true
```

!!! note "The default is specified as `RGBA`"

### String Setting

!!! info "A string value, presented as a text input."


| Field       | Type | Description                     |
| ----------- | ---- | ------------------------------- |
| `hide_text` | bool | Hides the text (password input) |

Example:
```toml
[[settings]]
index = 9
type = "string"
name = "SETTING_USERNAME"
description = "SETTING_USERNAME_DESC"
default = "LABEL_DEFAULT_USER"
hide_text = false
```

### String List Setting

!!! info "A list of strings, presented as a comma-separated text input."

Example:
```toml
[[settings]]
index = 10
type = "string_list"
name = "SETTING_EXCLUDED_EXT"
description = "SETTING_EXCLUDED_EXT_DESC"
default = ["dll", "exe"]
```

Internally, the value is stored as a single string with elements separated by `|`.

### URL Setting

!!! info "A read-only setting that opens a URL when clicked."

Example:
```toml
[[settings]]
index = 11
type = "url"
name = "SETTING_HOMEPAGE"
description = "SETTING_HOMEPAGE_DESC"
default = "https://example.com"
```

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

## Setting Groups

!!! info "Settings can be organized into collapsible groups for better readability."

To create a group, add a `[group]` section before the settings you want to include.

Example:
```toml
[group]
name = "GROUP_GRAPHICS"
description = "GROUP_GRAPHICS_DESC"

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

## Variables and Special Locations

The `file` and `folder` settings support the use of special location references in their `default` field.

### Special Location References

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

- `FRIENDLY`: Displays large numbers in a friendly format (e.g. 1,000,000 -> 1M).
- `SIZE_FRIENDLY`: Displays value in MB or GB for readability.
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

## Source Generation

!!! tip "The configuration schema is designed to be source generation friendly."

In the future, I hope to use C# Source Generators and Rust `proc_macro` to automatically generate
the schema file based on the configuration settings defined in the code.
This will keep the schema and code in sync.

Here's the current idea.

### Basic Example

=== "C#"

    ```csharp
    [Config(Name = "Mod Name", Author = "Author Name", LanguageFolder = "config", DefaultLanguage = "en-GB.toml")]
    public partial class MyModConfig
    {
        [Setting(Index = 0, Name = "SETTING_ENABLE_LOGGING", Description = "SETTING_ENABLE_LOGGING_DESC")]
        private bool enableLogging = false;

        [Setting(Index = 1, Name = "SETTING_LOG_LEVEL", Description = "SETTING_LOG_LEVEL_DESC", DefaultValue = "INFO")]
        private string logLevel = "INFO";

        [Setting(Index = 2, Name = "SETTING_MAX_LOG_FILES", Description = "SETTING_MAX_LOG_FILES_DESC", Min = 1, Max = 100)]
        private int maxLogFiles = 10;
    }
    ```

    This could generate the following code:

    ```csharp
    public partial class MyModConfig
    {
        public bool GetEnableLogging(ISettingsSource source);
        public string GetLogLevel(ISettingsSource source);
        public int GetMaxLogFiles(ISettingsSource source);
    }
    ```

=== "Rust"

    ```rust
    #[config(name = "Mod Name", author = "Author Name", language_folder = "config", default_language = "en-GB.toml")]
    pub struct MyModConfig {
        #[setting(index = 0, name = "SETTING_ENABLE_LOGGING", description = "SETTING_ENABLE_LOGGING_DESC")]
        enable_logging: bool,

        #[setting(index = 1, name = "SETTING_LOG_LEVEL", description = "SETTING_LOG_LEVEL_DESC", default_value = "INFO")]
        log_level: String,

        #[setting(index = 2, name = "SETTING_MAX_LOG_FILES", description = "SETTING_MAX_LOG_FILES_DESC", min = 1, max = 100)]
        max_log_files: i32,
    }
    ```

    This could generate the following code:

    ```rust
    impl MyModConfig {
        pub fn get_enable_logging(&self, source: &dyn ISettingsSource) -> bool;
        pub fn get_log_level(&self, source: &dyn ISettingsSource) -> &str;
        pub fn get_max_log_files(&self, source: &dyn ISettingsSource) -> i32;
    }
    ```

### Advanced Example

=== "C#"

    ```csharp
    [Config(Name = "Mod Name", Author = "Author Name", LanguageFolder = "config", DefaultLanguage = "en-GB.toml")]
    public partial class MyModConfig
    {
        [Setting(Index = 0, Name = "SETTING_ENABLE_FEATURE", Description = "SETTING_ENABLE_FEATURE_DESC")]
        private bool enableFeature = true;

        [Group(Prefix = "General", Name = "GROUP_GENERAL", Description = "GROUP_GENERAL_DESC")]
        private GeneralSettings generalSettings;

        [Group(Prefix = "Advanced", Name = "GROUP_ADVANCED", Description = "GROUP_ADVANCED_DESC")]
        private AdvancedSettings advancedSettings;

        [Setting(Index = 9, Name = "SETTING_LOG_FEATURE", Description = "SETTING_LOG_FEATURE_DESC")]
        private bool logFeature = true;

        private class GeneralSettings
        {
            [Setting(Index = 1, Name = "SETTING_UPDATE_INTERVAL", Description = "SETTING_UPDATE_INTERVAL_DESC", Min = 1, Max = 60)]
            private int updateInterval = 5;

            [Setting(Index = 2, Name = "SETTING_ENABLE_NOTIFICATIONS", Description = "SETTING_ENABLE_NOTIFICATIONS_DESC")]
            private bool enableNotifications = true;
        }

        private class AdvancedSettings
        {
            [Setting(Index = 5, Name = "SETTING_ADVANCED_FEATURE", Description = "SETTING_ADVANCED_FEATURE_DESC")]
            private bool advancedFeature = false;
        }
    }
    ```

    This could generate the following methods:

    ```csharp
    public partial class MyModConfig
    {
        public bool GetEnableFeature(ISettingsSource source);
        public int GetGeneralUpdateInterval(ISettingsSource source);
        public bool GetGeneralEnableNotifications(ISettingsSource source);
        public bool GetAdvancedFeature(ISettingsSource source);
        public bool GetLogFeature(ISettingsSource source);
    }
    ```

=== "Rust"

    ```rust
    #[config(name = "Mod Name", author = "Author Name", language_folder = "config", default_language = "en-GB.toml")]
    pub struct MyModConfig {
        #[setting(index = 0, name = "SETTING_ENABLE_FEATURE", description = "SETTING_ENABLE_FEATURE_DESC")]
        enable_feature: bool,

        #[group(prefix = "general", name = "GROUP_GENERAL", description = "GROUP_GENERAL_DESC")]
        general_settings: GeneralSettings,

        #[group(prefix = "advanced", name = "GROUP_ADVANCED", description = "GROUP_ADVANCED_DESC")]
        advanced_settings: AdvancedSettings,

        #[setting(index = 9, name = "SETTING_LOG_FEATURE", description = "SETTING_LOG_FEATURE_DESC")]
        log_feature: bool,
    }

    pub struct GeneralSettings {
        #[setting(index = 1, name = "SETTING_UPDATE_INTERVAL", description = "SETTING_UPDATE_INTERVAL_DESC", min = 1, max = 60)]
        update_interval: i32,

        #[setting(index = 2, name = "SETTING_ENABLE_NOTIFICATIONS", description = "SETTING_ENABLE_NOTIFICATIONS_DESC")]
        enable_notifications: bool,
    }

    pub struct AdvancedSettings {
        #[setting(index = 5, name = "SETTING_ADVANCED_FEATURE", description = "SETTING_ADVANCED_FEATURE_DESC")]
        advanced_feature: bool,
    }
    ```

    This could generate the following methods:

    ```rust
    impl MyModConfig {
        pub fn get_enable_feature(&self, source: &dyn ISettingsSource) -> bool;
        pub fn get_general_update_interval(&self, source: &dyn ISettingsSource) -> i32;
        pub fn get_general_enable_notifications(&self, source: &dyn ISettingsSource) -> bool;
        pub fn get_advanced_feature(&self, source: &dyn ISettingsSource) -> bool;
        pub fn get_log_feature(&self, source: &dyn ISettingsSource) -> bool;
    }
    ```

### Groups

The group properties, such as `Prefix`, `Name`, and `Description`, are defined on the group itself
using the `Group` attribute (C#) or `#[group]` attribute (Rust).

They are included into the parent via fields however, this helps express order that closer matches
the config file.

### Ordering

!!! info "The settings in the derived `config.toml` are sorted by the `index` attribute."

When dealing with groups, the order is determined by the lowest `index` inside the group struct.

For example:

```csharp
[Config(Name = "Mod Name", Author = "Author Name", LanguageFolder = "config", DefaultLanguage = "en-GB.toml")]
public partial class MyModConfig
{
    [Setting(Index = 0, Name = "SETTING_ENABLE_FEATURE", Description = "SETTING_ENABLE_FEATURE_DESC")]
    private bool enableFeature = true;

    [Group(Prefix = "General", Name = "GROUP_GENERAL", Description = "GROUP_GENERAL_DESC")]
    private GeneralSettings generalSettings;

    [Group(Prefix = "Advanced", Name = "GROUP_ADVANCED", Description = "GROUP_ADVANCED_DESC")]
    private AdvancedSettings advancedSettings;

    [Setting(Index = 9, Name = "SETTING_LOG_FEATURE", Description = "SETTING_LOG_FEATURE_DESC")]
    private bool logFeature = true;

    private class GeneralSettings
    {
        [Setting(Index = 1, Name = "SETTING_UPDATE_INTERVAL", Description = "SETTING_UPDATE_INTERVAL_DESC", Min = 1, Max = 60)]
        private int updateInterval = 5;

        [Setting(Index = 2, Name = "SETTING_ENABLE_NOTIFICATIONS", Description = "SETTING_ENABLE_NOTIFICATIONS_DESC")]
        private bool enableNotifications = true;
    }

    private class AdvancedSettings
    {
        [Setting(Index = 5, Name = "SETTING_ADVANCED_FEATURE", Description = "SETTING_ADVANCED_FEATURE_DESC")]
        private bool advancedFeature = false;
    }
}
```

This would result in the following indexes:

```
0: enableFeature
1: generalSettings.updateInterval
2: generalSettings.enableNotifications
3: reserved
4: reserved
5: advancedSettings.advancedFeature
6: reserved
7: reserved
8: reserved
9: logFeature
```

Which means the groups can be extended.

!!! tip "Please keep indexes within the range 0-65535 if possible, and ideally within 0-255."

    So we can compress better.

### Number Sizes

The sizes of integers in the generated code depend on the `max` value set in the `Setting` attribute.

By default, if no `max` value is specified, a 32-bit integer is used.

### Accessors

!!! info "The fields in the configuration struct are private."

The source generator will generate public accessor methods for each field, taking an `ISettingsSource` as a parameter.

The `ISettingsSource` is responsible for providing the actual values of the settings.

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

[localisation-format]: ../Localisation/File-Format.md
[formatters]: #value-formatters