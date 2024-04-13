# Loader

!!! info "These sections cover all information related to the design of the mod loader."

Specifically, these sections focus on everything related to the actual 'mod loader' lives inside of
the game process and powers your mods.

From getting it running, to how mods are booted up.

## Sections

!!! tip "It is suggested you read the following first."

| Section                                | Description                                                         |
| -------------------------------------- | ------------------------------------------------------------------- |
| [Core Architecture][core-architecture] | Describes how the overall system composes together at a high level. |

Other sections:

| Section                                | Description                                                    |
| -------------------------------------- | -------------------------------------------------------------- |
| [Platform Support][platform-support]   | Important notes & information for different Operating Systems. |
| [Backends][backends]                   | How support for different runtimes can be added to Reloaded3.  |
| [Copy Protection][copy-protection]     | How to deal with DRM and DRM-things to be aware of.            |
| [Loader API][loader-api]               | Functionality to mods provided by the loader.                  |
| [Loader Deployment][loader-deployment] | How the actual loader DLL is deployed to game folder.          |
| [Breaking Changes][breaking-changes]   | Things Reloaded3 fundamentally does different to Reloaded-II.  |

Important Reads:

| Section                        | Description                                                                      |
| ------------------------------ | -------------------------------------------------------------------------------- |
| [Load Ordering][load-ordering] | Rules used for deprecation & automatic reordering of mods based on dependencies. |

<!-- Links -->
[backends]: ./Backends/About.md
[breaking-changes]: ./Breaking-Changes.md
[copy-protection]: ./Copy-Protection/About.md
[core-architecture]: ./Core-Architecture.md
[loader-api]: ./Loader-API/About.md
[load-ordering]: ../Server/Load-Ordering.md
[loader-deployment]: ./Deployment.md
[platform-support]: ./Platforms/About.md