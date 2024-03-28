# Load Ordering

!!! info

    This page shows the rules used when ordering mods to be loaded.

!!! note

    Mods loaded last are assumed to be of highest priority.

## Backends are Rearranged as First

!!! info

    Backends are placed first in the mod load order before any other sorting occurs.

!!! tip

    This is a safeguard in case individual developers forget to set a dependency on the required backend.

!!! abstract "Log this as warning to console."

Suppose a following mod order:

```mermaid
flowchart LR
    NetMod[".NET Mod"] --> B
    B --> Backend[".NET Backend"]
    Backend --> D
```

The `".NET Mod"` should have a dependency on `".NET Backend"`, but it is missing.

To resolve this, the load order should be set to:

```mermaid
flowchart LR
    Backend[".NET Backend"] --> NetMod[".NET Mod"]
    NetMod --> B
    B --> D
```

## Dependencies Must be Loaded First

!!! info

    If Mod A sets Dependency on Mod B, then Mod B must be loaded first.

Suppose the following load order.

```mermaid
flowchart LR
    A --> B
    B --> C
    C --> D

    A -. Depends On .-> C
```

The mods must be arranged such that `ModC` is available by the time `ModA` is loaded.

i.e. The resulting load order should be...

```mermaid
flowchart LR
    C --> A
    A --> B
    B --> D

    A -. Depends On .-> C
```

## Mods can Disable Incompatible Mods During Startup

!!! info

    Mod A can mark Mod B as incompatible, leading to Mod B being disabled at startup.

!!! warning "Experimental"

    This is intended with the purpose of disabling mods in known guaranteed game-breaking scenarios.

!!! abstract "Log this as warning to console."

Consider the following scenario:

```mermaid
flowchart LR
    %% Define
    VK["Vulkan Support"]
    RT["RayTracing Mod"]
    9E["D3D9Ex Support"]

    9E --> VK
    VK --> RT
    RT -. Dependency .-> VK

    9E <-. Incompatible ..-> VK
```

You have one mod which upgrades game to `Direct3D9Ex` and one that upgrades the game to `Vulkan`.

!!! question "You can only use one Graphics API at a time; so what happens?"

Proposed solution is to destruct the mod with the lower priority, in this case the `D3D9Ex` mod.

```mermaid
flowchart LR
    %% Define
    VK["Vulkan Support"]
    RT["RayTracing Mod"]

    RT -. Dependency .-> VK
    VK --> RT
```

Additional Rationale:

- Incompatible mods may be implicitly loaded via dependencies with no way of user explicitly disabling them.

### Edge Case: Mod Dependency was Filtered Out

!!! danger

    In some cases destroying the mod with lower priority means that the dependencies of another mod are no longer
    resolvable.

!!! abstract "Display in MessageBox. Abort loading."

Consider the following:

```mermaid
flowchart LR
    %% Define
    VK["Vulkan Support"]
    RT["RayTracing Mod"]
    9E["D3D9Ex Support"]

    VK --> RT
    RT -. Dependency .-> VK
    RT --> 9E

    9E <-. Incompatible .-> VK
```

When `Vulkan Support` is filtered out due to being lower priority, the dependencies of `RayTracing Mod` are no longer
satisfied; thus game cannot be safely started.

To handle error case; simply check if all dependencies are satisfied after doing all operations.

### Edge Case: Recursive Incompatibility

!!! info

    If Mod A disables Mod B which disables Mod C; Mod C should stay.

!!! abstract "Log this case in console under 'info' level."

Consider the following:

```mermaid
flowchart LR
    %% Define
    A --> B
    B --> C

    C -. Incompatible .-> B
    B -. Incompatible .-> A
```

If higher priority `Mod C` marks `Mod B` as incompatible, `Mod A` can stay as it is no longer incompatible.

i.e. After removing items; this load order should be...

```mermaid
flowchart LR
    %% Define
    A --> C
```

### Edge Case: Recursive Destruction With Dependency

!!! info

    If Mod A disables Mod B which depends on Mod C; **BUT** Mod C was not part of original group of mods to load, discard Mod C too.

!!! abstract "Log this case in console under 'info' level."

```mermaid
flowchart LR
    %% Define
    A -- Via Dependency --> B
    B --> C

    C -. Incompatible .-> B
```

If mod B is removed, there is no longer reason to include Mod A; therefore it is removed.

```mermaid
flowchart LR
    C
```

## Mods can Deprecate Other Mods by Overriding Dependencies

!!! info

    Mod A can mark Mod B as deprecated in the context of dependency resolution.
    In this case, all Dependencies to Mod A are re-routed to Mod B during the mod loading procedure.

!!! danger "Dangerous"

    This is intended to allow communities to pick up the work if a maintainer of one critical dependency goes missing;
    however risks the possibility of abuse. This should be seen as last resort.

!!! abstract "Log this as warning to console."

```mermaid
flowchart LR
    %% Define
    A["Old Game Support"]
    B["New Game Support"]
    C["Costume Mod"]

    A --> C
    C --> B
    C -. Dependency .-> A
```

If Mod B declares itself as successor of Mod A [deprecates Mod A], dependencies to Mod A are rerouted to Mod B.

And since there is no longer a dependency on `Old Game Support`; the mod is excluded entirely.

```mermaid
flowchart LR
    %% Define
    B["New Game Support"]
    C["Costume Mod"]

    C -. Dependency .-> B
    B --> C
```