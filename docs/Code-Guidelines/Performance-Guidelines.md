## Optimizing for Binary Size

!!! info "These are the guidelines for writing compact code."

    In other words, building binaries with small sizes.

Consider this an extension of [johnthagen/min-sized-rust][min-sized-rust].

While the former is about how you can tweak compilation options to achieve a small binary,
this will give some guidance on how to structure new code to meet the
[code size guidelines for the mod loader][mod-loader-hw-requirements].

### When to *NOT* Apply these Guidelines

!!! tip "In some edge cases concessions must be made."

There's always a tradeoff in terms of what we can do.<br/>
Some systems are simply too complex to make replacements for.

For example:

- No sane person would make a full UI framework for R3.
- No sane person could make an SDL replacement for controllers.
    - You're not going to buy 100s of controllers to match SDL's [gamecontrollerdb.txt][gamecontrollerdb].
    - Having the user's gamepad pre-configured is much more valuable than the ~100kB of code size.

Before over-optimizing, always consider the tradeoffs involved.

Although Reloaded3 strives for maximum efficiency and 'perfectionism', sometimes having things
'just work' on the user machines can be just as 'perfect' as squeezing every byte out.

### When Applying These Guidelines is Encouraged

!!! tip "Apply this to any reusable code [that could possibly run inside a 32-bit environment][why-those-specs]."

Below are some examples.

***General Purpose Libraries/Code***:

Basically all universal 'Essential' mods in this wiki

- ✅ **DLL Injector**: Can be used to inject into child processes.
- ✅ **Code Hooking Library**: Used by all code mods.
- ✅ **[Virtual FileSystem][virtual-filesystem]**: Used by most games.
- ✅ **[File Emulation Framework][file-emulation-framework]**: Used by many games.

***Middleware/Engine Specific Code***:

- ✅ [**Middleware Handling Mods (Layer 1)**][middleware-mods]: Used in various games of various sizes.

***General Purpose Tools***:

- ⚠️ **Animated Texture Injector**:
    - Unlikely to be optimizing here for code size... BUT.
    - ***MAKE SURE*** users use optimized texture formats, otherwise 32-bit games will very quickly run out of address space.

***Game Specific Code***:

- ⚠️ [Game {X} Support (Layer 2)][game-support-layer2]
    - Unless the game's extremely simple, consider keeping the code small.
    - 'Simple' meaning 'no sane person would stuff it with 100s of stupidly sized textures'.

***Mod Management Specific Code***:

These can be ported to embedded systems, so should be optimized.

- ✅ Any code for the `launcher` UI.
- ✅ Any code for the `loader` server.

### Guidelines


#### Reduce use of `std` in libraries.



[min-sized-rust]: https://github.com/johnthagen/min-sized-rust
[middleware-mods]: ../Loader/Core-Architecture.md#middlewareos-handling-mods-layer-1
[game-support-layer2]: ../Loader/Core-Architecture.md#game-support-layer-2
[virtual-filesystem]: ../Mods/Essentials/Virtual-FileSystem/About.md
[file-emulation-framework]: ../Mods/Essentials/File-Emulation-Framework/About.md
[mod-loader-hw-requirements]: ./Hardware-Requirements.md#mod-loader
[why-those-specs]: ./Hardware-Requirements.md#why-these-specs
[server]: ../Server/About.md
[gamecontrollerdb]: https://github.com/mdqinc/SDL_GameControllerDB