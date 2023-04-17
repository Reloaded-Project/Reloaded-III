# Dll Hijacking/Import Table Hooking

!!! info

    This is probably by far the most common method used by mod loaders everyone knows; but I'll throw in a very, very quick recap just in case.

A quick summary of how it works is like this:  

- An EXE can define number of DLLs to import (via `IMAGE_IMPORT_DESCRIPTOR`).  
- The OS (PE Loader) will load those DLLs when the process is created.  
- This will load our loader DLL.  
- In the loader we load the original DLL and redirect all exports to it.  
- If the game calls one of the exports, we initialize the `mod loader` (only once).  

## Considerations

!!! info

    If the mod loader is loaded from a hijacker like [Ultimate ASI Loader](https://github.com/ThirteenAG/Ultimate-ASI-Loader/releases), 
    it might have already worked around Steam DRM.

## Technical Issues

!!! info

    This can conflict with legacy injectors because there's only finite amount of DLLs you can stub. You risk running out.

!!! danger "Issues with Microsoft DRM"

    See [Microsoft DRM](./Windows-DRM.md#microsoft-ms-storegame-pass); it's not known how to automatically determine which
    DLL name to stub in a reliable fashion.  

!!! danger

    Generally [Ultimate ASI Loader](https://github.com/ThirteenAG/Ultimate-ASI-Loader/releases) is used for this, but has issues
    with certain games like 64-bit Persona Ports or UWP San Andreas; need to make own loader for these cases.

## Implementation

Read the PE header for the names of the DLLs that are imported at boot; and pick an appropriate one that's not already used in the game folder.

Using [Ultimate ASI Loader](https://github.com/ThirteenAG/Ultimate-ASI-Loader/releases) is probably a decent temporary solution, 
but overkill for our use case. The occasional compatibility issue also leaves a bit to be desired, especially since it's not being maintained
(issues receive not even a response for months on end).  