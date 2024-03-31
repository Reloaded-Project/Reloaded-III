# Dll Hijacking/Import Table Hooking

!!! info

    Probably by far the most common method used by mod loaders; but I'll throw in a very, very quick recap just in case.

A quick summary of how it works is like this:

- An EXE can define number of DLLs to import (via `IMAGE_IMPORT_DESCRIPTOR`).
- The OS (PE Loader) will load those DLLs when the process is created.
- This will load our loader DLL.
- In the loader we load the original DLL and redirect all exports to it.
- If the game calls one of the exports, we initialize the `mod loader` (only once).

## When to Use

!!! info "Any service with an integrated 'Cloud Save' option that runs outside of the game."

This applies to most launchers, e.g. `GOG`, `Microsoft Store`, `Steam`. Some exceptions apply, for instance, games
can use external SDKs to handle cloud saves manually, in which case using [DLL Injection into Suspended](./Windows-InjectIntoSuspended.md)
is preferred.

## Technical Issues

- [Microsoft Store Titles are Encrypted](../../Loader/Copy-Protection/Windows-MSStore.md)
    - We must use one of the workarounds to get the stub name.

- [Steam DRM Wrapper](../../Loader/Copy-Protection/Windows-Steam.md)
    - We must delay the initialization of the mod loader until after the Steam DRM Wrapper code runs.
    - Otherwise mods will try hooking encrypted code and fail miserably.
    - Or strip the wrapper in name of interoperability.

- Possibility game might not have many available DLLs to stub.
    - i.e. You risk running out of shims.
    - We can work around this by loading via existing shim, if found to be installed in game directory.

## Considerations

!!! danger

    Generally [Ultimate ASI Loader](https://github.com/ThirteenAG/Ultimate-ASI-Loader/releases) is used for this, but is not lightweight
    enough to meet the performance requirements of R3. Could only be used as last resort.

## Implementation

Read the PE header for the names of the DLLs that are imported at boot; and pick an appropriate one that's not already used in the game folder.

Using [Ultimate ASI Loader](https://github.com/ThirteenAG/Ultimate-ASI-Loader/releases) is probably a decent temporary solution,
but overkill for our use case. The occasional compatibility issue also leaves a bit to be desired, especially since it's not being maintained
(issues receive not even a response for months on end).