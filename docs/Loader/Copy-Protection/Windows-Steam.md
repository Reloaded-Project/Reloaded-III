Steam specific DRM considerations.

## Steam (DRM Wrapper)

!!! failure

    This DRM presents is a problem because the game code is encrypted at boot, if you try to modify the game code at that point
    you'll hit the encrypted data and run into issues.

This is a lightweight form of DRM that encrypts the original binary in-place and decrypts the data at boot.
The stub responsible for the decryption is likely written in x86/x64 Assembly.

Resources:

- [Technical Information about this DRM][steamstub-info].
- [Official SteamWorks Documentation](steamstub-official-docs).

### Dangers

!!! failure

    This DRM will deliberately crash the game process after attaching a debugger. It needs to be removed when debugging.

For the purposes of debugging or reverse engineering; [Steamless][steamless]
is able to automatically remove this DRM from most games.

### Detection

Parse the PE header of the executable in memory.
If this DRM is present, there is an `IMAGE_SECTION_HEADER` with the name `.bind`.

This holds true for all currently known versions of SteamStub.

!!! tip "Use `get_section_names` method of [min-pe-parser][min-pe-parser]."

### Common Workaround(s)

Most loaders use either of the two approaches:

- [DLL Hijack][dll-hijack] a known DLL and init in one of the library's Init functions e.g. `d3d9.CreateDevice`.
- Hook a library's init function (e.g. `d3d9.CreateDevice`), load Reloaded in the hook, and unhook.

!!! danger "We can't do this in R3, we should assume no knowledge of target game."

### What R3 Should Do

#### Phase 0: Strip Stream Wrapper if Possible with Steamless

!!! warning "We remove Steam DRM Wrapper when possible for interoperability and compatibility purposes."

    ***THE MAIN PURPOSE OF THIS ACTION IS TO ACHIEVE INTEROPERABILITY BETWEEN THE EXISTING
    GAME SOFTWARE, MOD LOADER AND 3RD PARTY LOADER MODS.***

    - Reloaded performs this mainly to allow debugging crashes experienced by end users.
    - Reloaded will never remove SteamWorks API integration. (i.e. `steam_api.dll`)
    - Reloaded will never include or distribute any emulator for the Steamworks API integration.
    - Reloaded will never promote, encourage or assist with piracy.
    - Reloaded will never assist with bypassing anti-cheats or online protections.

    In practice, almost all Steam games will retain their existing copy protection
    through their integration/use of the SteamWorks API (`steam_api.dll`).

    IMPORTANT: This needs to be communicated in the final software.

1. Build [Steamless][steamless] with modern .NET (i.e. .NET Core).
   - Produce native Reloaded Packages (TODO: LINK PENDING) that bundle Steamless as a Tool.
2. Run `Steamless.CLI` with `--keepbind`, `--exp`.
   - This is necessary because some games have an [edge case][edge-case].

#### Phase 1: Strip Stream Wrapper if Possible with Steamless

!!! tip "This is used as a fallback in case Phase 0 fails."

The solution here is to mass hook APIs [listed here][r2-delay-inject-hooks];
and safely unhook after one of the targets has been hit.

This has historically worked well and has only overhead of 3 x86 instructions post unhooking with
[Reloaded.Hooks][reloaded-hooks].

!!! note "The preferred workaround for this (currently employed by `Reloaded-II` and `Ultimate-ASI-Loader`)."

## Tricks

!!! info "Some tricks you can do in order to work around certain limitations"

### Avoid Forced Reboot

!!! tip

    The SteamWorks API forces games to reboot if they have not been launched via Steam; this can be problematic
    for [DLL Injection](../../Research/Bootloaders/Windows-InjectIntoSuspended.md).

1. Set `SteamAppID` env var.
2. Hook `steam_api.SteamAPI_RestartAppIfNecessary`.
3. Hook `steam_api.SteamAPI_IsSteamRunning`.

A combination of these has so far been sufficient; usually games' access to Steam Services are unaffected.

This should only be done if ***DLL Injection is THE ONLY WAY*** to get the loader running. Currently no known games require this.

!!! note "This should be avoided if possible, because launching outside of the Steam client leads to Cloud Saves not immediately syncing."

<!-- Links -->

[dll-hijack]: ../../Research/Bootloaders/Windows-DllHijack.md
[edge-case]: https://github.com/atom0s/Steamless/issues/80
[min-pe-parser]: https://github.com/Sewer56/min-pe-parser
[r2-delay-inject-hooks]: https://github.com/Reloaded-Project/Reloaded-II/blob/master/source/Reloaded.Mod.Loader/DelayInjectHooks.json
[reloaded-hooks]: https://github.com/Reloaded-Project/Reloaded.Hooks
[steamless]: https://github.com/atom0s/Steamless
[steamstub-info]: https://www.pcgamingwiki.com/wiki/User:Cyanic/Steam_DRM#Typical_reasons_for_using_Steam_DRM