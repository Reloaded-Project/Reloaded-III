# Configuration

!!! info "This page describes Reloaded3's configuration file format details."

!!! warning "TODO: Ingest for settings outside of Reloaded3 origin"

!!! warning "TODO: How we store global configuration in Application Profiles"

## Requirements

!!! info "These are the requirements for Reloaded3 configurations."

- Layer Support
    - Ability to have 'layers', such as hardware-specific settings.
    - Example: You don't want to boot the game in wrong resolution when syncing loadout between devices.
- Minimal Size
    - Must be as tiny as possible, since we need to [store them in loadouts][loadouts].
- Live Editing
    - Must be able to edit settings live.
- Netplay Support
    - Must be able to be synced over the network.
    - This entails small configs, and a standardized way to apply them.
- Source Generation Friendly
    - Must be able to generate source code from the configuration.
    - Or the Configuration from the source code.
- Cross-Language Support
    - Must be able to be used in any language.
    - Not just language with native source generation support (e.g. C# and Rust).
- Grouping of Configuration Items
    - For example, all settings related to a specific feature.
    - Or all settings related to a 'player' in a local multiplayer game.
- Sensible Defaults
    - Mods and Packages should be able to ship sensible defaults.
- Conditional Settings
    - For example, showing setting B only if setting A is enabled.

## Non-Requirements

- Support for every possible kind of data.
    - Some very domain specific configurations may still use separate binaries.

## UX for Configuration 'Layers'

!!! info "The UX around this is stupidly complicated."

The planned UX for the time being is the following.

- Package settings UI is scoped per loadout.
- Package configs can declare groups.
- Groups can opt in to be 'globally configurable' (a.k.a. `show_global`)
    - This automatically puts them in a 'Global' section in the UI.
    - Alternatively a user may manually add them to the global section.
        - That is saved in the [Game Config][game-config].

## Sections

!!! tip "In reading order."

| Section                         | Description                                            |
| ------------------------------- | ------------------------------------------------------ |
| [Config Schema][config-schema]  | How configuration options are defined.                 |
| [Source Generation][source-gen] | How we generate source code from config schema.        |
| [Binary Format][binary-format]  | How Reloaded3 configuration files are written to disk. |

[binary-format]: ./Binary-Format.md
[config-schema]: ./Config-Schema.md
[loadouts]: ../../Server/Storage/Loadouts/About.md
[source-gen]: ./Source-Generation.md
[game-config]: ../../Server/Storage/Games/About.md