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
- No sane person would make an SDL replacement for controllers.
    - You're not going to buy 100s of controllers to match SDL's [gamecontrollerdb.txt][gamecontrollerdb].
    - Having the user's gamepad pre-configured is much more valuable than the ~100kB of code size.

Before over-optimizing, always consider the tradeoffs involved.<br/>
Sometimes the extra space used by a non-specialized off the shelf library may be acceptable.

Although Reloaded3 strives for maximum efficiency and 'perfectionism', sometimes having things
'just work' on the user machines can be just as 'perfect' as squeezing every byte out.

!!! note "Sometimes you can just improve the existing solution."

    Replacing `gamecontrollerdb.txt` with a binary version for example, would save binary size,
    and disk space.

### When Applying These Guidelines is Encouraged

!!! tip "Apply this to any ***reusable code*** [that could possibly run inside a 32-bit environment][why-those-specs]."

Below are some examples of good places to optimize.

***General Purpose Libraries/Code***:

Basically all universal 'Essential' mods in this wiki, and the libraries they may use.

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

- ✅ Any code for the `loader` server.
- ✅ Any code that can be used inside mods.

### Guidelines

#### Be smart with library usage

!!! info "Sometimes you can be a bit smarter than libraries."

    This includes the standard library.

Below is an example.

Suppose you want to take an action on every directory up to a certain file path.
For example, to ensure that all directories in a path exist.

The standard 'idiomatic' way would be to write it like this:

```rust
fn process_path(path: &str) {
    let mut current_path = PathBuf::with_capacity(path.len());
    current_path.push("/");

    for component in path.split('/') {
        if !component.is_empty() {
            current_path.push(component);

            // Do something with directory
            handle_directory(&current_path);
        }
    }
}
```

However, you can do better. You can work with a raw string directly?

```rust
unsafe fn process_path(path: &str) {
    let mut current_path = String::with_capacity(path.len());
    current_path.push('/');
    for component in path.split('/') {
        if !component.is_empty() {
            current_path.push_str(component);

            // Do something with directory.
            handle_directory(&current_path);

            current_path.push('/');
        }
    }
}
```

!!! question "But how is this better?"

    Consider the [implementation of push][push-impl] in `PathBuf` and note all the edge cases:

    > - If `path` is absolute, it replaces the current path
    > - If `path` has a root but no prefix (e.g., `\windows`), it replaces everything except for the prefix (if any) of `self`.
    > - If `path` has a prefix but no `root`, it replaces `self`.
    > - If `self` has a verbatim prefix (e.g. `\\?\C:\windows`) and `path` is not empty, the new path is normalized: all references to . and `..` are removed.

    In this context, because we are constructing a unix path, which is guaranteed to begin with `/`,
    and are always appending a directory.

    We don't need to handle any of these edge cases. The code for that is unnecessary, and will
    unnecessarily bloat the binary.

#### Review (Vet) Library Source Code

!!! info "Have a peek into implementation of 3rd party libraries."

    In particular small libraries that likely haven't had many eyes on them.

When writing code, especially C# code where the barrier of entry is low, it's easy for authors
to write code which is far from optimal.

Take for example [A Semi-Popular Avalonia Icon Library][projectanker-avalonia-icons].<br/>
To load a material design icon from this library...

- [You Embed all 7447 Icons Inside your Binary (+ ~3.5MB binary size)][projectanker-icon-assets]
- [Load an Icon from Embedded Resource][projectanker-icon-load]
- [Parse Icon SVG for Properties using Uncompiled Regex][projectanker-parse-svg]
- [Parse Icon SVG Path to create Icon][projectanker-parse-svg-path]

The loading process restarts every single time you want to load an icon. If you have
10 buttons with the same icon, the that entire loading process (from extracting embedded resource)
repeats 10 times.

Also [changing the colour of the icon repeats all of the loading steps again][projectanker-icon-reload].

This is a bit of a more extreme example, but it is very easy to take a dependency on something
that may not be very optimal. A lot of stars on GitHub does not necessarily always have to speak
on the quality of the code.

!!! tip "For smaller libraries, consider a quick run down through their source code."

    If you see something that could be optimized, consider making a PR.
    Or write your own alternative.

<!-- Links -->
[file-emulation-framework]: ../Mods/Essentials/File-Emulation-Framework/About.md
[game-support-layer2]: ../Loader/Core-Architecture.md#game-support-layer-2
[gamecontrollerdb]: https://github.com/mdqinc/SDL_GameControllerDB
[min-sized-rust]: https://github.com/johnthagen/min-sized-rust
[middleware-mods]: ../Loader/Core-Architecture.md#middlewareos-handling-mods-layer-1
[mod-loader-hw-requirements]: ./Hardware-Requirements.md#mod-loader
[projectanker-avalonia-icons]: https://github.com/Projektanker/Icons.Avalonia
[projectanker-icon-assets]: https://github.com/Projektanker/Icons.Avalonia/tree/main/src/Projektanker.Icons.Avalonia.MaterialDesign/Assets
[projectanker-icon-load]: https://github.com/Projektanker/Icons.Avalonia/blob/509a9741321da5be8a9a585cb0ab3a94378712ff/src/Projektanker.Icons.Avalonia.MaterialDesign/MaterialDesignIconProvider.cs#L55-L76
[projectanker-parse-svg]: https://github.com/Projektanker/Icons.Avalonia/blob/509a9741321da5be8a9a585cb0ab3a94378712ff/src/Projektanker.Icons.Avalonia.MaterialDesign/MaterialDesignIconProvider.cs#L39-L53
[projectanker-parse-svg-path]: https://github.com/Projektanker/Icons.Avalonia/blob/509a9741321da5be8a9a585cb0ab3a94378712ff/src/Projektanker.Icons.Avalonia/IconImage.cs#L94
[projectanker-icon-reload]: https://github.com/Projektanker/Icons.Avalonia/blob/509a9741321da5be8a9a585cb0ab3a94378712ff/src/Projektanker.Icons.Avalonia/Icon.axaml.cs#L56
[push-impl]: https://doc.rust-lang.org/std/path/struct.PathBuf.html#method.push
[server]: ../Server/About.md
[virtual-filesystem]: ../Mods/Essentials/Virtual-FileSystem/About.md
[why-those-specs]: ./Hardware-Requirements.md#why-these-specs