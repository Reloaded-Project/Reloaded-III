# Workflows: A Templating System for Easier Mod Creation

!!! info "'Workflows' are a templating system designed to simplify the mod creation process."

The primary goals are:

1. Identify common mod creation objectives
2. Provide streamlined assistance for these objectives

Most mods created by non-technical users typically involve simple modifications such as replacing models, textures, or audio.

By simplifying this process, we can help grow the modding community and potentially inspire some users to become more technically proficient over time.

## The Current User Journey

!!! example "You are an end user trying to make a [Persona 5 Royal][p5r] mod."

1. **Initial Search**:
    - User searches for phrases like `how to make a Persona 5 Royal mod`
    - Often leads to guides on how to *use* mods ‼️, not create them

2. **Finding the Right Resources**:
    - If lucky, user finds the [Persona Essentials][persona-essentials] documentation
    - And will also encounter [Reloaded-II Mod Creation Documentation][r2-mod-creation-docs]

3. **Manual Setup**:
    - User follows a series of manual steps from the [Persona Essentials][persona-essentials] documentation

While steps 1 and 2 are one-time experiences, step 3 must be repeated for each new mod.

## Current Challenges

!!! failure "The user experience for mod creation is often suboptimal"

1. **Discoverability Issues**:
    - General searches like `how to create mod` rarely yield relevant results
    - Proper documentation is often buried in search results

2. **Tedious Manual Processes**:
    - Once documentation is found, users face a series of repetitive, manual steps

## The Vision: An Ideal Workflow

!!! tip "Streamline the creation of common types of mods with a templating system"

1. **User Selects Workflow**:
    - User selects a workflow that matches their modding objective
    - For example:
        - Change a Character
        - Change an Object
        - Change a Music Track
        - Change a Stage

2. **Follow Steps Relevant to Workflow**:
    - Should we add a new item or replace an existing one?
    - For example:
        - Which character to replace?
        - Which object to replace?
        - Which music track to replace?
        - Which stage to replace?
    - This auto selects parts of [mod id][package-id], and other relevant details.

3. **Assist User with Replacement**:
    - Shipping tools as packages is really useful here.
    - For example:
        - Placing original files where new files should be (to help users understand the structure).
            - Maybe even converting them to user modifiable formats.
        - Helping the user loop an audio track. (e.g. with tools like [PyMusicLooper][pymusiclooper])
    - Some of these 'tasks' should maybe be reusable in right click context menus.

4. **Final Details**:
    - Setting up name, tags, and other metadata.

## Questions

1. **Should the user be able to select multiple workflows?**

    No. Reloaded3 encourages modularity, ideally mods should do only one thing, and do it well.
    Users can then mix mods by choosing which mods to enable and which to disable.

    Therefore it is advised to only allow users to create with one workflow.

[p5r]: https://store.steampowered.com/app/1687950/Persona_5_Royal/
[persona-essentials]: https://sewer56.dev/p5rpc.modloader/usage/
[r2-mod-creation-docs]: https://reloaded-project.github.io/Reloaded-II/CreatingMods/
[package-id]: ../Packaging/Package-Metadata.md#id
[pymusiclooper]: https://github.com/arkrow/PyMusicLooper