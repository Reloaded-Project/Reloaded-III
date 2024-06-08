# Hardware Configurations

!!! info "Hardware settings are settings that are tied to your user."

    These are not carried as part of loadouts, but rather as part of the user/profile configuration.

!!! tip "To define hardware-specific settings, add an `[hardware]` section to the [config.toml][config-schema] file."

## Requirements

### Ability to configure `Windows` mod settings from `Linux`

!!! info "This involves running a helper program inside WINE"

    And communicating the results over inter-process-communication (IPC).

This will most likely involve sockets.

If possible, run the exact WINE/Proton version used to start the game.

### Ability to reorder Device Indexes

!!! warning "Sometimes you may not be able to uniquely identify a device."

    In those cases, you should be able to refer to devices by 'index' and reorder them.

!!! info "Sometimes you may not be able to uniquely identify a device."

For example, the user should be able to swap settings between 2 controllers in a trivial manner.

### Libraries should be usable outside of Reloaded3 Configs

!!! info "Some libraries here are 'unique' and should be reusable"

Let's be good citizens of the open source space.

## Sections

!!! tip "In reading order."

| Section                               | Description                            |
| ------------------------------------- | -------------------------------------- |
| [Displays](./Displays.md)             | Settings tied to a specific monitor.   |
| [Controllers](./Controllers/About.md) | SDL3 Based Cross Platform Controllers. |