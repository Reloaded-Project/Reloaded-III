!!! info "Game config stores all of the user's preferences for launcher/loader behaviour related to a game."

## Background Knowledge

Before reading this, read the basics over at the [Loadouts page][event-sourcing].

The approach and requirements here are generally the same.
Likewise, storing App configurations also makes use of *Event Sourcing* for backups.

## File Format

!!! info "A config for an application has the following file format."

| Data Type | Name   | Label | Description                                                                                                      |
| --------- | ------ | ----- | ---------------------------------------------------------------------------------------------------------------- |
| `u8`      | Length | X     | [0-255] Length of new commandline parameters in [commandline-parameter-data.bin][commandline-parameter-data.bin] |

!!! tip "Games in Reloaded3 use the concept of 'events' to track and manage changes over time."

Consider reading more about this in the

- ❌ [Create Shortcut]
- ❌ [Show Console]
- ❌ [Deployment Type (e.g. ASI Loader)]
- ❌ [Extra Commandline Arguments]

[event-sourcing]: ../Loadouts/About.md#event-sourcing