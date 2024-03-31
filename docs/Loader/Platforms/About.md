# Platform Support

!!! info "These pages contain miscellaneous notes regarding support on each platform."

| Operating System                    | Status                 |
| ----------------------------------- | ---------------------- |
| [Windows](./Windows.md)             | ✅                      |
| [Linux (Wine/Proton)](./Windows.md) | ✅                      |
| [Native Linux](./Linux.md)          | ⚡ Implement on Demand  |
| [Native OSX](./OSX.md)              | ⚡ Implement on Demand  |
| [Other](./Other.md)                 | 🔍 Investigation Needed |

`Implement on Demand` means; it'll be done when there's game to test.
The code will always be written with cross platform in mind; worry not.

## Minimum Requirements

As the core loader is written in Rust, it is theoretically possible to support any platform provided:

- You have access to sufficient amount of libc.
- LLVM supports the machine code for your target (e.g. ARM, x86 etc.).
- Executable format reverse engineered, so you can make linker produce libraries.
- You can dynamically load libraries.
- You can arbitrarily execute code in a game process ([write a Bootloader](../../Research/Bootloaders/About.md)).

## Categories Covered in Each Platform

!!! note "Note: Info on bootstrapping the loader itself is covered under [Bootloader](../Platforms/About.md)."

These topic instead include platform specific caveats and strategies, such as:

1. Running existing code mods (`.asi` and friends), if applicable.
2. Crash Handling
3. Intercepting Process Exit

And of course, anything else that's interesting.
The pages are more of a 'Cheat Sheet'.

## Crash Handling

!!! info "Each Platform should Make A Crash Dump"

After a crash has been encountered; the code should (if possible):

- Generate a Crash Dump.
- Dump Log to Same Location as Crash Dump.
- Display Crash Address (incl. Module/DLL name).
- Open a file manager in the location of the dump.

Dumps will be written out to [TODO: Link Pending] as:

- `dump.dmp` The crash dump.
- `log.txt` The log of the recent run.
- `info.json` Contextual information (e.g. Mod list game was started with).

The server should clean old crash dumps after some time (for instance, 7 days).

!!! note "Crash handling should be opt-out in loader, in case you want to use an external handler."