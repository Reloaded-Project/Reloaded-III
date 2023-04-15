# DRM Considerations for Windows Bootloaders

!!! failure "Fuck DRM"

## Steam

### Avoid Forced Reboot

1. Set `SteamAppID` env var.
2. Hook `steam_api.SteamAPI_RestartAppIfNecessary`.
3. Hook `steam_api.SteamAPI_IsSteamRunning`.

todo

## Steam (Embedded Stub)

!!! info

    For the purposes of reverse engineering; [Steamless](https://github.com/atom0s/Steamless) is able to automatically
    remove this DRM from most games.  

!!! warning

    This DRM presents is a problem because the game code is encrypted at boot, if you try to modify the game code at that point
    you'll hit the encrypted data and run into issues.

This is a lightweight form of DRM that encrypts the original binary in-place and decrypts the data at boot. 
The stub responsible for the decryption is likely written in x86/x64 Assembly.  

[More information about this DRM here](https://www.pcgamingwiki.com/wiki/User:Cyanic/Steam_DRM#Typical_reasons_for_using_Steam_DRM).  

### Detection

Parse the PE header of the executable in memory.  
If this DRM is present, there is an `IMAGE_SECTION_HEADER` with the name `.bind`.  

### Workaround

Most loaders use either of the two approaches:  

- [DLL Hijack](./Windows-DllHijack.md) a known DLL and init in one of the library's Init functions e.g. `CreateDevice`.  
- Hook said API (e.g. `d3d9.CreateDevice`) explicitly, and unhook on unload.  

We can't do this in R3 however, we should assume no knowledge of target game.  

The preferred workaround for this (currently employed by Reloaded-II and Ultimate-ASI-Loader) is to mass hook APIs 
[listed here](https://github.com/Reloaded-Project/Reloaded-II/blob/master/source/Reloaded.Mod.Loader/DelayInjectHooks.json);
and safely unhook after one of the targets has been hit. 

This has historically worked well and has only overhead of 3 x86 instructions post unhooking with 
[Reloaded.Hooks](https://github.com/Reloaded-Project/Reloaded.Hooks).

## Microsoft (MS Store/Game Pass)

uwu