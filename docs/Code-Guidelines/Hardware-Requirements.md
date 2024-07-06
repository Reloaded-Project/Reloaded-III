# Target Hardware and OS Specifications

!!! note "This page is heavily opinionated."

!!! info "The following specs below are targets only."

    There are some exceptions.

    For example if you're writing game mods that run only on modern 64-bit
    machines, then pay no mind to this section.

This page simply provides an insight into my (Sewer's) personal targets.

## Minimum Requirements

!!! info "Below are the minimum requirements for running Reloaded3."

For reference:

- **Server**: The backend server that handles all of the mod management logic
- **Loader**: Everything that runs inside game code

### Full Experience (Launcher + Server)

!!! info "For running the UI and Backend Server on one machine"

- **CPU**: Pentium III
- **RAM**:
    - 128MB (Desktop) [Avalonia, NativeAOT]
    - 32MB (Embedded) [Not Currently Planned]
- **Storage**: A 5400 RPM hard drive.

Something around the specs of an original Xbox.

### Server Only

!!! info "For running just the backend server."

    To manage mods, a client can externally collect via TCP.<br/>
    TODO: Link the Networking Page

- **RAM**:
    - **Idle:** 4MB of RAM
    - **Active:** 16MB of RAM

Something like the Dreamcast.

Motivation: User could leave the server running standalone in the background, and connect to it from
another machine. When idle, it should not eat up too much memory so power users could be confident
about letting it run.

### Mod Loader

!!! info "For running just the mod loader."

- **RAM**:
    - **Target**: 0.5MB
    - **Max**: 1MB

The loader should ideally fit in the remaining available unused RAM of a GameCube era game.
The max meanwhile targets a cross-platform title running on the original Xbox.

## Why These Specs?

!!! question "Reloaded3 is not targeting these platforms, so why are the min specs so low?"

    I will be honest, there is no 'good reason'.

    Reloaded3 is purely about perfectionism. As my last modding framework, I simply want to
    see how much I can push things in both effiency and innovation.

    A crazy experiment to run this in embedded environments would just be cherry on the cake.

Anyway, idealism aside. Even on the PC, there are still plenty memory constrained environments
once you are dealing with older 32-bit games.

Notably, 32-bit games are restricted to 2GiB of memory out of the box, and due to fragmentation,
***this is actually closer to 1.5GiB***.

When games are heavily modded, you may find yourselves in a situation where you get very close
to hitting that limit.

!!! tip "Large Address Aware a.k.a. '4GB Patch'"

    Many games can be patched to extend memory to 4GiB.<br/>
    Reloaded3 will offer this, but it's not always guaranteed every game will work.

But guess what... ***it's not even 1.5GiB***.<br/>
***We have even less memory.***

### Address Space Usage Induced by 3rd Party Software

!!! info "Third party injected code further limit our available memory."

And this situation isn't getting any better, in fact, everyday we have less and less
memory, as our software becomes increasingly ~~shit~~ bloated and unoptimized.

See: [Software Disenchantment][software-disenchantment]

Below are some example numbers of memory usage by various common software
that gets injected and can runs from inside a common 32-bit game.

This was measured with VMMap, on 10th of June 2024, on a 1080p screen and all
software on default settings.

#### Software Overlays

| Software                                      | Virtual Memory Use (Committed Bytes) |
| --------------------------------------------- | ------------------------------------ |
| Steam Overlay                                 | 25MiB                                |
| Steam Overlay (After Opening Once)            | 65MiB                                |
| RivaTuner Statistics Server (RTSS) 'Disabled' | 63MiB                                |
| RivaTuner Statistics Server (RTSS)            | 67MiB                                |
| GeForce Experience                            | UNKNOWN ⚠                            |
| Nvidia App                                    | UNKNOWN ⚠                            |

Notes:

- RivaTuner Statistics Server is the software bundied with MSI Afterburner
    - Disabling it only hides the UI, it still kicks in.
- ⚠ Driver magic involved with Nvidia, so the memory cost is being absorbed by driver.

#### General Purpose Tools

| Software                 | Committed Bytes |
| ------------------------ | --------------- |
| Special K                | 189MiB          |
| Special K (Overlay Open) | 197MiB          |
| ReShade                  | 25MiB           |
| ReShade (Open)           | 27MiB           |
| DXVK D3D9 ⚠              | 4.9MiB          |
| Ultimate ASI Loader      | 2.2MiB          |

⚠ DXVK can sometimes [save a bit of memory too][dxvk-mmf].

#### FrameBuffer Access

!!! info "Certain operations require copying the pixels from GPU to CPU"

    a.k.a. Copying the framebuffer.

Examples:

- Screenshots
- Video Capture
- CPU based post-processing (rare, but it happens)

If a user has an 8K 16:9 display, ***132MB of RAM*** is required (`7680 * 4320 * 4 bytes`)
to store a frame.

#### High Resolution Textures

!!! info "Some end users throw absurdly large textures at games."

And don't compress them using optimal formats, meaning they get 4 bytes per pixel.
This is understandable, as non-developers are not expected to know the intricacies of texture compression.

The other aspect is that many casual modders are often not aware of setting appropriate texture
sizes in their mods. Often the expected viewing distance and target resolution are not considered
when determining the texture size. In this case, you end up seeing a lot of 1024x1024 textures
for items that are displayed.

!!! example "An image is displayed in a size of 128x128 (96 DPI) on screen."

    A modder may upscale that to 512x512, for a '4K Texture Pack' when that in fact
    is the appropriate size for an 8K display, not a 4K one.

    !!! note "We'll try to prevent this with [Diagnostics][diagnostics]"

#### Conclusion

!!! info "We're running dry of memory in 32-bit processes."

As each of these software becomes more and more complex, they use more and more RAM.

A power-user with `Special K`, `ReShade` and `RivaTuner Statistics Server` running their game through Steam
is going to have ***an memory overhead of 350MiB***. Now slap some demanding 32-bit game and HD mods
on top of that.

You might have a mod setup that works today, but tomorrow, software gets updated, it becomes more bloated,
and your game runs out of RAM 😿 💀.

As a general purpose modding framework, ***Reloaded3 must be able to handle all sorts of eventualities***.

!!! tip "[Reloaded3 is actively pushing back against Wirth's Law][wirth-law]"

### How the Specs will be Applied

!!! tip "We will not limit ourselves to these specs."

    We should instead focus on providing the 'knobs' to allow the code to be
    scaled down to these constraints.

For example; this means allowing the user to extract archives on a single thread only.

It does not mean that the whole thing should be designed fully around old hardware in mind.
More memory can be used if required; for example, to display images.

### About Esoteric & Experimental Platforms

!!! info "Consoles, Embedded Systems, etc."

!!! warning "Having a standard dynamically linked library is considered an essential requirement."

Reloaded3 is a plugin based system. (i.e. Mods are Plugins)

Without a standard/system library to link plugins to, R3 mods will be too
large to efficiently run on super niche targets; such as embedded inside
a GameCube game. (<1 MB RAM free)

While I have no intention of targeting these platforms personally, the architecture will be
nonetheless designed in a way that does not explicitly lock out such targets.

Namely this boils down to:

- Merging mods into a single compilation will be possible.
    - This avoids wasting memory on multiple copies of the same common code.
    - So user's mods may be compiled on the fly.
    - But you may need to install a compilation toolchain in this crazy workflow.
- Allowing loading code in custom formats.
    - This is covered under [Custom Backends (Layer 0)][custom-backends].
    - A custom backend could be used to load Position Independent Code (PIC) from a custom format.

If anyone's crazy enough to try these sorts of experiments, let me know.

I'd love to lend a hand in the unexpected.

### Misc Notes

!!! note "It may be useful to allow mods to boot the server from within a game."

    In the case mods involving online multiplayer need to download additional mods on the fly,
    etc. They can connect to server through IPC.

[dxvk-mmf]: https://github.com/doitsujin/dxvk/pull/2663
[software-disenchantment]: https://tonsky.me/blog/disenchantment/
[diagnostics]: ../Server/Diagnostics.md
[wirth-law]: https://en.wikipedia.org/wiki/Wirth%27s_law
[custom-backends]: ../Loader/Core-Architecture.md#custom-backends-layer-0