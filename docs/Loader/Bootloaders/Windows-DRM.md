# DRM Considerations for Windows Bootloaders

!!! failure "Fuck DRM"

## Steam

### Avoid Forced Reboot

!!! note

    Does not Apply to [DLL Hijack](./Windows-DllHijack.md).

!!! tip

    The Steam API forces games to reboot if they have not been launched via Steam; this can be problematic sometimes.  

1. Set `SteamAppID` env var.
2. Hook `steam_api.SteamAPI_RestartAppIfNecessary`.
3. Hook `steam_api.SteamAPI_IsSteamRunning`.

A combination of these has so far been sufficient; usually games' access to Steam Services are unaffected.   

## Steam (Embedded Stub)

!!! info

    For the purposes of reverse engineering; [Steamless](https://github.com/atom0s/Steamless) is able to automatically
    remove this DRM from most games.  

!!! info

    This DRM will deliberately crash the game process after attaching a debugger. It needs to be removed when debugging.  

!!! failure

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

!!! failure 

    GamePass titles encrypt their EXEs; making them unreadable, and don't even report correct location of EXE.

!!! note

    Actual path of EXE is usually something like `C:\Program Files\WindowsApps\SEGAofAmericaInc.F0cb6b3aer_1.10.23.0_x64_USEU+s751p9cej88mt\P5R.exe` 
    and changes every update...

!!! info

    For the purposes of Reverse Engineering; [UWPDumper](https://github.com/Wunkolo/UWPDumper) can often be used to get an unencrypted EXE.

!!! info

    Incompatible with [Inject into Suspended Process](./Windows-InjectIntoSuspended.md); because game EXE is redirected to some
    OS level launcher and thus the wrong program is hooked.

### Workaround

- We must either dump the EXE header from memory from a running game, or figure out appropriate 
  [DLL Hijacking](./Windows-DllHijack.md) DLL name from one of the other store releases.  

A reliable way to handle this DRM is not known. Getting user to launch game and dumping PE header from memory to figure out
an entry point is a method; but it's too hacky and poor UX.  

Worst offender by far.  

## Denuvo

!!! question "Some Denuvo titles have Anti-Debugging Measures"

    However it is unclear whether it is an optional Denuvo component or additional DRM from the publisher.  

!!! info

    Some SEGA games circa 2017 have an anti-debug measure where `ntdll.DbgUiRemoteBreakin` will constantly be rewritten with 
    `ret` (0xC3) on a background thread to prevent debugging.  

    It is usually easy to patch. Affected titles include Sonic Forces and Puyo Puyo Tetris.  

Surprisingly the least intrusive. That said, enjoy waiting 30 hours for game to disassemble...