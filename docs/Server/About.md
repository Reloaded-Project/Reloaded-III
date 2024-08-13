# Server (Manager Backend)

!!! info "This section covers all information related to the design and architecture of the backend server powering the mod manager."

The server is responsible for various tasks such as mod packaging, configuration management,
diagnostics, load ordering, and more. This also covers the 'data model' of Reloaded3.

Basically all the actual work of a 'mod manager', but as a server.

## Sections

| Section                          | Description                                                                                  |
| -------------------------------- | -------------------------------------------------------------------------------------------- |
| [Packaging][packaging]           | Covers how mods are packaged and distributed, including the package structure and design.    |
| [Storage][storage]               | Covers where everything is stored on disk, including how files are managed.                  |
| [Diagnostics][diagnostics]       | Explains the diagnostic system that informs the frontend about issues with the user's setup. |
| [Load Ordering][load-ordering]   | Rules used for deprecation & automatic reordering of mods based on dependencies.             |
| [Workflows][workflows]           | Template system used to help make mod creation easier.                                       |

<!-- Links -->
[packaging]: ./Packaging/About.md
[storage]: ./Storage/About.md
[diagnostics]: ./Diagnostics.md
[load-ordering]: ./Load-Ordering.md
[workflows]: ./Workflows/About.md