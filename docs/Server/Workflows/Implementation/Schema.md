# Workflow Schema

!!! info "This file specifies the format of the `workflow.toml` files used to define workflow metadata and behaviour."

TODO: A way to run external tools in workflows.

## Example File

!!! info "A typical `workflow.toml` has the following structure"

```toml
[metadata]
format-version = 0
name = "WORKFLOW_NAME"
summary = "WORKFLOW_SUMMARY"
gameId = "sonicheroes"
version = "1.0.0"
author = "Sewer56" # Who created this workflow.
files = [
    "files/package.toml",
]
language-subfolder = "create-a-character"
default_language = "en-GB.toml"

# Author [Special Variable] via Setting
# Name via Setting
# Summary via Setting
# character_name [in ID] via Setting
# character_name [Full] via Setting
# license via Choice Setting
# tags via Setting
# allow 'extra tags' via Setting
# add or replace via Selection

# A way to set dependencies between steps.
# A way to link the script to the workflow.
# A way to specify whether to replace voices.
# A way to specify whether to replace sound effects.

[[settings]]
index = 0
type = "choice"
name = "SETTING_CHARACTER"
description = "SETTING_CHARACTER_DESC"
choices = ["CHARACTER_SONIC", "CHARACTER_TAILS", "CHARACTER_KNUCKLES"]
choice_images = ["sonic_icon.jxl", "tails_icon.jxl", "knuckles_icon.jxl"]
default = "CHARACTER_SONIC"
variable = "selected_character"
```

## Special Variables

!!! info "Some variables are 'special' and may have predetermined default values based on the environment."



## Metadata Section

The `[metadata]` section contains information about the workflow itself:

| Field                | Type   | Description                                                              |
| -------------------- | ------ | ------------------------------------------------------------------------ |
| `format-version`     | int    | The version of the workflow format. (Currently `0`)                      |
| `name`               | string | Localization key for the name of the workflow.                           |
| `summary`            | string | Localization key for the 1 line description summary.                     |
| [`gameId`][game-id]  | string | The [game][game-id] this workflow is for.                                |
| `version`            | string | The version of the workflow.                                             |
| `author`             | string | The (primary) author or group behind the workflow.                       |
| `files`              | string | The files where variable substitutions should be performed.              |
| `language-subfolder` | string | The name of the subfolder in the `languages` folder used for localizing. |
| `default_language`   | string | The default language file to use, relative to the `language_folder`.     |

!!! tip "The `language-subfolder` field is used when you're shipping multiple workflows within one package."

## Package Section

!!! info "The `[package]` section defines default values for the package metadata"

| Field                          | Type        | Description                                        |
| ------------------------------ | ----------- | -------------------------------------------------- |
| id_template                    | string      | Template for generating the package ID.            |
| name_template                  | string      | Localization key for the package name template.    |
| summary_template               | string      | Localization key for the package summary template. |
| author                         | string      | Author of the package (can use `{user_input}`).    |
| [package_type][package-type]   | PackageType | Type of the package (e.g., `"Mod"`).               |
| [is_dependency][is-dependency] | bool        | Whether the package is a dependency.               |
| version                        | string      | Version of the package.                            |
| license_id                     | string      | SPDX License Identifier for the package.           |
| tags                           | string[]    | Tags for the package.                              |

## Steps Section

The `[[steps]]` section defines the steps of the workflow:

| Field       | Type     | Description                                                   |
| ----------- | -------- | ------------------------------------------------------------- |
| type        | string   | Type of step (e.g., "selection", "text_input", "file_input"). |
| id          | string   | Unique identifier for the step.                               |
| prompt      | string   | Localization key for the prompt or question.                  |
| options     | array    | For "selection" type, the list of options.                    |
| file_types  | string[] | For "file_input" type, the allowed file extensions.           |
| target_path | string   | For "file_input" type, where to place the file.               |
| show_if     | array    | Conditions for displaying this step.                          |

For "selection" type steps, each option in the `options` array has the following fields:

| Field | Type   | Description                            |
| ----- | ------ | -------------------------------------- |
| key   | string | Localization key for the option text.  |
| value | string | The value associated with this option. |

## Automation Section

The `[automation]` section defines automated tasks to be performed:

| Field         | Type     | Description                                        |
| ------------- | -------- | -------------------------------------------------- |
| type          | string   | Type of automation task.                           |
| source_format | string[] | Source file formats for conversion tasks.          |
| target_format | string   | Target file format for conversion tasks.           |
| apply_to      | string   | ID of the step this automation applies to.         |
| action        | string   | Specific action for the automation (e.g., "loop"). |
| tool          | string   | Tool to use for the automation task.               |

## Settings Section

!!! info "The `[[settings]]` entry defines [configuration settings][configuration-settings] for the package."

Each setting must specify a [`variable` name][configuration-settings-common-fields], for example:

```toml
[[settings]]
type = "choice"
name = "SETTING_CHARACTER"
description = "SETTING_CHARACTER_DESC"
choices = ["CHARACTER_SONIC", "CHARACTER_TAILS", "CHARACTER_KNUCKLES"]
default = "CHARACTER_SONIC"
variable = "selected_character"
```

The results of these settings are substituted into the package metadata.

The `[config]` section defines the configuration settings for the package:

## Package Subsections

### Update Data

The `[package.update_data]` section defines update information for the package:

| Field           | Type   | Description                               |
| --------------- | ------ | ----------------------------------------- |
| user_name       | string | GitHub username (can use `{user_input}`). |
| repository_name | string | GitHub repository name (can use `{id}`).  |

### Gallery

The `[[package.gallery]]` section defines gallery items for the package:

| Field     | Type   | Description                                    |
| --------- | ------ | ---------------------------------------------- |
| file_name | string | Name of the image file.                        |
| caption   | string | Localization key for the gallery item caption. |

### Targets

The `[package.targets]` section defines the target files for different platforms:

| Field | Type   | Description                        |
| ----- | ------ | ---------------------------------- |
| any   | string | The main DLL file for the package. |

## Variable Substitution

Throughout the schema, you can use curly braces `{}` to denote variables that will be substituted with actual values during the workflow execution. For example:

- `{game}`: Will be replaced with the game name.
- `{character_name}`: Will be replaced with the character name input by the user.
- `{user_input}`: Indicates that the user will be prompted for this information.
- `{id}`: Will be replaced with the generated package ID.

These variables allow for dynamic generation of package metadata and file paths based on user input and selections made during the workflow.

## Localization

!!! info "Workflows use the [Reloaded3 localization system][r3-localization-system]."

All user-facing text uses localization keys instead of direct text.

These keys will be resolved using the appropriate language file based on the user's settings.

Localization files should be placed in the [`languages` folder of the package][where-to-add-locales],
following the Reloaded3 localization file format. For example:

```toml
## languages/create-a-character-/en-GB.toml
[[WORKFLOW_NAME]]
Change a Character

[[WORKFLOW_SUMMARY]]
Allows you to add or replace a character in the game.



```

The workflow system will use these localization keys to display text in the user's preferred language,
falling back to the default language if a translation is not available.

[game-id]: ../../Storage/Games/About.md#id
[r3-localization-system]: ../../../Common/Localisation/About.md
[package-type]: ../../Packaging/Package-Metadata.md#packagetype
[is-dependency]: ../../Packaging/Package-Metadata.md#is-dependency
[configuration-settings]: ../../../Common/Configuration/Config-Schema.md
[configuration-settings-common-fields]: ../../../Common/Configuration/Config-Schema.md#common-setting-fields
[where-to-add-locales]: ../../../Common/Localisation/Adding-Localisations.md#where-to-add-localisations