# Tasks

!!! tip "The 'tasks' represent an array of actions that can be used to launch the game."

You can think of them like the `Tasks` you have in VSCode.

## Where Tasks can be Defined

- Per Game
    - These tasks are automatically created when you add a game to the launcher.
    - These are persisted in the user's preferences.
- Per Package
    - Packages can declare their own tasks to run.

## Structure

The `Tasks` field when present is an array of `Task` objects, where each `Task` is defined as:

```toml
[[Tasks]]
Type = "File"
VisualHint = "Game"
Name = "Launch Game"
GroupNames = ["GOG"]
Description = "Launches the game."
Path = "Game.exe"
IsPrimary = true
IsHidden = false
InjectLoader = true
Icon = "GameIcon.png"
RelativeWorkingDir = "Bin"
Arguments = ["-fullscreen", "-config", "{GameDir}/config.ini"]
```

| Type                      | Field                                     | Description                                                                                                           |
| ------------------------- | ----------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| [TaskType](#tasktype)     | [TaskType](#tasktype)                     | The type of the task (e.g., "File", "Url").                                                                           |
| [VisualHint](#visualhint) | [VisualHint](#visualhint)                 | Visual hint for the UIs.                                                                                              |
| string                    | Name                                      | A user-friendly name for the task.                                                                                    |
| string[]                  | [GroupNames](#group-names)                | A user-friendly name for 'group' containing this task.                                                                |
| string?                   | [Description](#description)               | A brief description of the task. Ideally limited to 2 short lines.                                                    |
| string                    | [Path](#path)                             | The relative path to the executable file or the URL to open. See [Path](#path) for details.                           |
| bool                      | [IsPrimary](#isprimary)                   | Indicates whether this task launches the game's main executable. Only one task should have `IsPrimary` set to `true`. |
| bool                      | [InjectLoader](#injectloader)             | Indicates whether the loader should be injected. Usually only true for the `IsPrimary` task.                          |
| string[]                  | [Arguments](#arguments)                   | An array of additional commandline arguments to pass to the executable. Can use placeholders like `{GameDir}`.        |
| bool?                     | IsHidden                                  | Indicates whether the task should be hidden from the user. Defaults to `false`.                                       |
| string?                   | [RelativeWorkingDir](#relativeworkingdir) | The working directory for the task. Defaults to the folder containing `Path`, otherwise is a folder relative to it.   |

### TaskType

!!! info "The `TaskType` can be one of the following"

- 0: `File`: Represents a task that launches an executable file.
- 1: `Url`: Launches an URL. [Path](#path) specifies the full URL to open.

### VisualHint

!!! info "This is a hint for the launcher and other UIs."

- 0: `Game`: Shows a GamePad. Used for game binary.
- 1: `Settings`: Shows a Gear. Used for launchers.
- 2: `Tool`: Shows a Wrench. Used for modding tools.
- 3: `Wiki`: Shows a Book. Used for documentation.
- 4: `Community`: Shows a Globe. Used for community links.

### Group Names

!!! info "A user-friendly name for 'groups' containing this task."

This field is used to group tasks together in the UI if the user to chooses to view
tasks by group.

Example group names include:

- `GOG`: All items imported from GOG.
- `Community`: All items imported from the community repository.

### Description

!!! info "A brief description of the task. Ideally limited to 2 short lines."

The `Description` field provides a brief description of the task.<br/>

It should ideally be limited to 2 short lines for conciseness and clarity.

**Example:**
```toml
Description = "Launches the configuration program."
```

### Path

!!! info "The relative path to the executable file or the URL to open."

The `Path` field specifies the relative path to the executable file or the URL to open when the task is executed.

- If the task is declared in a [Package][package], the `Path` is relative to the folder the package is located in.
- If the task is declared for a game, the `Path` is relative to the folder that contains the main executable of the game.
    - The one marked `IsPrimary`.

### IsPrimary

!!! info "Indicates whether this task launches the game's main executable."

    Only one task should have `IsPrimary` set to `true`.

The `IsPrimary` field indicates whether the task launches the game's main
executable, which is usually the primary EXE file assigned by the game store or the user.

!!! warning "When importing external tasks, there may be more than one 'default' task."

    In such cases, the local already defined task wins.

### InjectLoader

!!! info "Indicates whether the loader should be injected."

    Usually only true for the `IsPrimary` task.

The `InjectLoader` field is a boolean value that indicates whether the mod loader should be injected
when the task is executed.

!!! warning "This field is only used when the method of injecting is set to 'Code Injection'"

### RelativeWorkingDir

!!! info "The working directory for the task."

    Defaults to the folder containing `Path`, otherwise is a folder relative to it.

The `RelativeWorkingDir` field specifies the working directory for the task.

If not specified, it defaults to the folder containing the file specified in the `Path` field.<br/>
Otherwise, it is treated as a folder relative to the `Path`.

**Example:**
```toml
RelativeWorkingDir = ""
```

Gives you `C:/Games/MyGame/Bin` if the `Path` is `Bin/Game.exe` and game is at `C:/Games/MyGame`.

If you want to go one folder up from the `Path`, use double dots:
```toml
RelativeWorkingDir = ".."
```

This will set the working directory to `C:/Games/MyGame`.

### Commandline Placeholders

!!! info "These placeholders will be replaced with their corresponding values when the task is executed."

When specifying the `Path` or commandline `Arguments` for a task, you can use placeholders to
dynamically insert certain values.

The available placeholders are:

- `{GameDir}`: The absolute path to the directory containing the main executable file.

If the task is sourced from a package, the following variables are also available:

- `{PackageDir}`: The absolute path to the base folder of the package.
- `{PackageConfigDir}`: The absolute path to the config folder for the package.
    - [This is the `Package Configs` (`PackageConfigs/{packageId}`) folder.][items-to-store]
    - This folder allows for
- `{PackageUserCacheDir}`: The absolute path to the config folder for the package.
    - [This is the `Package Cache Files (User)` (`Cache/{packageId}`) folder.][items-to-store]
- `{PackageMachineCacheDir}`: The absolute path to the config folder for the package.
    - [This is the `Package Cache Files (Machine)` (`Cache/{packageId}`) folder.][items-to-store]

The intent is to allow for external tools to store their configuration files within loadouts.
By doing this, the user can cloud save their settings for their favourite tools.

### Arguments

!!! info "An array of additional commandline arguments to pass to the executable."

    Can use [Commandline Placeholders](#commandline-placeholders).

The `Arguments` field is an array of additional commandline arguments to pass to the executable
when the task is executed. It supports the use of [Commandline Placeholders](#commandline-placeholders)
like `{GameDir}` to dynamically insert values.

**Example:**

```toml
Arguments = ["-fullscreen", "-config", "{GameDir}/config.ini"]
```

When you execute the task, the following will run:

```
Game.exe -fullscreen -config C:/Games/MyGame/config.ini
```

## Tasks in Code

!!! tip "Some additional fields exist only in memory/code, on the actual implementation side"

| Type                      | Field               | Description                             |
| ------------------------- | ------------------- | --------------------------------------- |
| [TaskSource](#tasksource) | [Type](#tasksource) | Where the current task originated from. |

### TaskSource

- 0: `Game`: Task was defined for the game.
- 1: `Package`: Task was defined in a package.
- 2: `Community`: Task was imported from the community repository.
- 3: `Imported`: Task was imported from an external source (e.g., GOG).

## Importing from GOG

GOG Games have their 'tasks' defined inside the [goggame-{gameid}.info file][gog-info-file].

Example from file (truncated):

```json
"playTasks": [
    {
        "category": "game",
        "isPrimary": true,
        "languages": [
            "en-US"
        ],
        "name": "The Legend of Heroes: Trails in the Sky SC",
        "path": "ed6_win2_DX9.exe",
        "type": "File"
    },
    {
        "category": "launcher",
        "languages": [
            "en-US"
        ],
        "name": "Configuration Tool",
        "path": "Config2_DX9.exe",
        "type": "File"
    }
],
```

We should be able to import these tasks directly into the game configuration.

[gog-info-file]: ../Loadouts/Stores/GOG.md#goggame-gameidinfo
[images]: ../../../Common/Images.md
[package]: ../../Packaging/Package-Metadata.md
[items-to-store]: ../Locations.md#items-to-store