# Workflow Scripting

!!! info "Reloaded3 workflows use [Rhai] scripts for adding additional arbitrary logic to templates."

This document outlines the scripting capabilities available in Reloaded3 workflows.

<!-- Note: Material MkDosc doesn't highlight `rhai`, so we used `rust` as a substitute in code blocks. -->

## Script Location

Rhai scripts are specified in the `workflow.toml` file under the `[metadata]` section:

```toml
[metadata]
rhai_script = "scripts/my_workflow_script.rhai"
```

## Execution Timing

!!! tip "See: [Workflow Execution Steps] for the full details."

Rhai scripts are executed after all workflows in a chain have been completed, but before the final
template substitution step. This allows scripts to modify or add variables based on user inputs from
multiple workflows.

## Available Modules and Functions

Reloaded3 extends Rhai with custom modules and functions tailored for workflow operations.
Here are the available modules:

### Variable Module

!!! info "Allows for interaction with variables set during workflow execution."

!!! example "An Example"

    ```rust
    // Check if a variable is set
    let is_set = variable::is_set("my_variable");

    // Get a variable value
    let value = variable::get("my_variable");

    // Set a variable
    variable::set("new_variable", "new value");

    // Prompt user for input
    let user_input = variable::prompt("Enter a value:");
    let bool_input = variable::prompt("Do you agree?", true);
    let choice = variable::prompt("Select an option:", "Option 1", ["Option 1", "Option 2", "Option 3"]);
    ```

* **`variable::is_set(name: &str) -> bool`**: Returns `true` if the variable `name` has been set, `false` otherwise.

* **`variable::get(name: &str) -> value`**: Retrieves the value of the variable `name`.
  Returns `null` if the variable doesn't exist.

* **`variable::set(name: &str, value: (&str|bool))`**: Sets the variable `name` to `value`.
  If the variable already exists, it will be overwritten.

* **`variable::prompt(text: &str) -> value`**: Prompts the user with `text` and returns their input as a string.

* **`variable::prompt(text: &str, default_value: bool) -> value`**: Prompts the user with `text`,
  offering `default_value` as the default option. Returns a boolean.

* **`variable::prompt(text: &str, default_value: &str) -> value`**: Prompts the user with `text`,
  offering `default_value` as the default option. Returns a string.

* **`variable::prompt(text: &str, default_value: &str, choices: Array) -> value`**: Prompts the user
  to choose from the given `choices` array, with `default_value` as the default option.

### File Operations

!!! info "Allows you to read/write/create files."

!!! warning "Be careful about casing in file operations."

    File operations are case-sensitive on some platforms.
    Be sure to use the correct casing when working with files.

    If the case does not match, the template system will try doing a non-case sensitive search
    as a fallback. That may mean a different file is found than the one you intended.

!!! example "An Example"

    ```rust
    // Check if a file exists in the output directory
    let exists_in_output = output::exists("config.txt");

    // Write content to a file in the output directory
    output::write("output.txt", "File content");

    // Read a file from the game directory
    let game_file_content = game::read("data/levels.dat");

    // Check if a file exists in the workflow directory
    let exists_in_workflow = workflow::exists("templates/config.txt");

    // Read a file from the workflow directory
    let workflow_file_content = workflow::read("templates/stage_template.txt");
    ```

#### Output File Operations

!!! info "This lets you work with [files] declared in [workflow metadata][files], prior to [template substitution]."

* **`output::exists(relativepath: &str) -> bool`**: Returns `true` if the file or directory at `relativepath` exists in the output directory, `false` otherwise.

* **`output::rename(from: &str, to: &str)`**: Renames the file or directory from `from` to `to` in the output directory.

* **`output::delete(relativepath: &str)`**: Deletes the file or directory at `relativepath` in the output directory.

* **`output::write(relativepath: &str, content: &str)`**: Writes `content` to the file at `relativepath` in the output directory.

* **`output::write(relativepath: &str, content: Array)`**: Writes each element of the `content` array to a new line in the file at `relativepath` in the output directory.

* **`output::read(relativepath: &str) -> Array<u8>`**: Reads the contents of the file at `relativepath` in the output directory and returns it as a byte array.

#### Game File Operations

!!! info "Allows for read-only access to files in the game folder."

    These operations provide access to the game files that the mod is being created for.

    You are ***NOT*** supposed to write anything to this folder.

* **`game::exists(relativepath: &str) -> bool`**: Returns `true` if the file or directory at `relativepath` exists in the game directory, `false` otherwise.

* **`game::read(relativepath: &str) -> Array<u8>`**: Reads the contents of the file at `relativepath` in the game directory and returns it as a byte array.

#### Workflow File Operations

!!! info "Allows for read-only access to files in the workflow folder."

    These operations provide access to the files that are part of the workflow itself.

    You are ***NOT*** supposed to write anything to this folder.

* **`workflow::exists(path: &str) -> bool`**: Returns `true` if the file or directory at `path` exists in the workflow directory, `false` otherwise.

* **`workflow::read(path: &str) -> Array<u8>`**: Reads the contents of the file at `path` in the workflow directory and returns it as a byte array.

### System Module

!!! info "These functions allow you to interact with the underlying operating system."

!!! example "An Example"

    ```rust
    // Execute a system command
    let result = system::command("echo", ["Hello, World!"]);

    // Get current date
    let date = system::date();
    print(`Year: ${date.year}, Month: ${date.month}, Day: ${date.day}`);
    ```

* **`system::command(cmd: &str, args: Array) -> value`**: Executes the system command `cmd` with the given `args` array. Returns the command's output as a string.

* **`system::date() -> Date`**: Returns a `Date` object representing the current date in UTC. The `Date` object has `year`, `month`, and `day` properties.

## Example Rhai Script

Here's an example of a Rhai script that might be used in a Reloaded3 workflow:

```rust
// New API functions for getting full system paths
fn game_path(relative_path) {
    return system::game_path(relative_path);
}

fn workflow_path(relative_path) {
    return system::workflow_path(relative_path);
}

fn output_path(relative_path) {
    return system::output_path(relative_path);
}

// Get user inputs from previous workflow steps
let selected_zone = variable::get("selected_zone");
let stage_name = variable::get("stage_name");
let add_or_replace = variable::get("add_or_replace");

// Determine the stage ID based on the selected zone and stage
let stage_id = switch selected_zone {
    "ZONE_SEASIDE" => variable::get("seaside_stage"),
    "ZONE_CITY" => variable::get("city_stage"),
    "ZONE_CASINO" => variable::get("casino_stage"),
    _ => "UNKNOWN_STAGE"
};

// Map stage IDs to their corresponding numbers
let stage_number_map = #{
    "STAGE_SEASIDEHILL": "01",
    "STAGE_OCEANPALACE": "02",
    "STAGE_EGGHAWK": "20",
    "STAGE_GRANDMETROPOLIS": "03",
    "STAGE_POWERPLANT": "04",
    "STAGE_TEAMBATTLE1": "21",
    "STAGE_CASINOPARK": "05",
    "STAGE_BINGOHIGHWAY": "06",
    "STAGE_ROBOTCARNIVAL": "22"
};

// Get the stage number
let stage_number = stage_number_map[stage_id];

if stage_number == () {
    print(`Error: Unknown stage ID ${stage_id}`);
    return;
}

// Determine if we're adding a new stage or replacing an existing one
let is_new_stage = (add_or_replace == "SETTING_STAGE_ADD");

// If adding a new stage, find the next available stage number
let target_stage_number;
if is_new_stage {
    // Logic to find the next available stage number
    // This is a placeholder and should be implemented based on your specific requirements
    target_stage_number = "90"; // Example: using 90 as the first new stage number
} else {
    target_stage_number = stage_number;
}

// Set the target stage ID for file operations
variable::set("target_stage_id", target_stage_number);

// Copy the files
copy_stage_files(stage_number, target_stage_number);

// Update the stage name in the appropriate files
// This is a placeholder and should be implemented based on your specific requirements
let stage_name_file = output_path(`dvdroot/s${target_stage_number}_stagename.bin`);
if output::exists(stage_name_file) {
    output::write(stage_name_file, stage_name);
    print(`Updated stage name in ${stage_name_file}`);
}

print(`Stage "${stage_name}" (s${target_stage_number}) has been ${is_new_stage ? "created" : "replaced"}.`);

// Function to copy files with both 's' and 'stg' prefixes
fn copy_stage_files(source_number, target_number) {
    let prefixes = ["s", "stg"];
    let file_list = [
        "${prefix}${num}_ptcl.bin",
        "${prefix}${num}_PB.bin",
        "${prefix}${num}_P1.bin",
        "${prefix}${num}_P2.bin",
        "${prefix}${num}_P3.bin",
        "${prefix}${num}_P4.bin",
        "${prefix}${num}_P5.bin",
        "${prefix}${num}obj.one",
        "${prefix}${num}obj_h.one",
        "${prefix}${num}obj_flyer.one",
        "${prefix}${num}ind.rel",
        "${prefix}${num}OBJ.one",
        "${prefix}${num}MRG.one",
        "${prefix}${num}_sp.spl",
        "${prefix}${num}_light.bin",
        "${prefix}${num}_indinfo.dat",
        "${prefix}${num}_DB.bin",
        "${prefix}${num}_cam.bin",
        "${prefix}${num}_blk.bin",
        "${prefix}${num}.one",
        "${prefix}${num}_h.one",
        "${prefix}${num}_h.txc",
        "${prefix}${num}.dmo",
        "se_${prefix}${num}_tbl.bin",
        "BGM/SNG_STG${num}.adx",
        "collisions/${prefix}${num}.cl",
        "collisions/${prefix}${num}_wt.cl",
        "collisions/${prefix}${num}_xx.cl",
        "stgtitle/${prefix}${num}title_disp.one",
        "stgtitle/${prefix}${num}title_dispEX.one",
        "stgtitle/${prefix}${num}title_dispSH.one",
        "stgtitle/mission/${prefix}${num}CE00.bmp",
        "stgtitle/mission/${prefix}${num}CExE00.bmp",
        "textures/${prefix}${num}.txd",
        "textures/${prefix}${num}_indirect.txd",
        "textures/${prefix}${num}_effect.txd"
    ];

    for prefix in prefixes {
        for file in file_list {
            let source_path = game_path(`dvdroot/${file.replace("${prefix}${num}", "${prefix}${source_number}")}`);
            let target_path = output_path(`dvdroot/${file.replace("${prefix}${num}", "${prefix}${target_number}")}`);

            if game::exists(source_path) {
                let content = game::read(source_path);
                output::write(target_path, content);
                print(`Copied ${source_path} to ${target_path}`);
            }
        }
    }
}
```

[rhai]: https://rhai.rs/book/
[minijinja]: https://github.com/mitsuhiko/minijinja
[Workflow Execution Steps]: ./About.md#workflow-execution-steps
[files]: ./About.md#workflow-schema
[template substitution]: ./Templates.md