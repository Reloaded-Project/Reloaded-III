# About Bootloaders

!!! info

    'Bootloader' in the spec refers to the component used to acquire arbitrary code execution inside the 
    game's target process.

Basically, how we get our loader running.  

In some cases, it is important to support a variety of bootloaders on a given target OS.  

The inclusion of DRM (some of which is [Operating System Level](./Windows-DRM.md#microsoft-ms-storegame-pass)) can make
certain injection methods incompatible, in which case we must work around these issues.