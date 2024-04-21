# Signature Scanning

!!! info "Signature Scanning is a technique used to locate specific code or data patterns in a game's memory."

It allows modders to find and modify game functionality even when the game is updated,
without relying on fixed memory addresses.

As part of the Reloaded3 ecosystem, we need to provide a standard signature scanning library
and documentation. This will be exposed via a mod as that allows us to maximize performance and
interoperability between mods.

## Why Signature Scanning?

!!! question "Why do we need Signature Scanning?"

Modifying games that receive frequent updates can be challenging.

Each update can shuffle around code and data, breaking mods that rely on fixed memory addresses.

Signature Scanning helps mitigate this issue by searching for specific ***unique*** patterns of bytes rather
than relying on absolute addresses. This makes mods more resilient to game updates.

!!! example "An example signature"

      ```csharp
      "89 15 ??";
      ```

      This means: Find a byte with the value `0x89`, followed by a byte with the value `0x15`, followed by any byte.

## How It Works

!!! info "Signature Scanning works by searching the game's memory for a known sequence of bytes."

These bytes can represent a specific piece of code or a code reference to a variable.

The process involves the following steps:

1. **Identify the code or data you want to locate**: This could be a function you want to hook
   or code referencing a variable you want to access.

2. **Create a signature**: A signature is a string representation of the bytes you want to find,
   with wildcards for bytes that may change.

3. **Scan the game's memory**: Use a signature scanning library to search for the pattern
   of bytes specified by your signature.

4. **Calculate the memory address**: Once a match is found, calculate the actual memory address
   of the code or data based on the offset from the match location.

By using Signature Scanning, your mods can dynamically locate the required code or data even if
the game's memory layout changes in an update.

!!! warning "Signature scanning can be used to find code and read only data."

    It is NOT recommended to use signature scanning to find writable data.

## What's the Plan?

!!! tip "Port the original C# Signature Scanner Library [Reloaded.Memory.SigScan][reloaded-memory-sigscan] to Rust!! [(Existing R2 Mod)][r2-sigscan-mod]"

Improving it where necessary to meet the [requirements and goals for Reloaded3][requirements].

Hardware acceleration for AArch64 should also be added. Raytwo has already done the work there
[Reloaded.Memory.SigScan (Rust, AArch64)][lazysimd], with good results on the Nintendo Switch.

!!! tip "Fun fact"

    The aforementioned AArch64 port improved startup times of [ARCropolis][arcropolis] from 16.1s to 2.8s.

Some tricks from [Pattern16][pattern16] may also be used to improve performance further.

## Overview

- [Requirements][requirements]: Requirements & Goals for Reloaded3's signature scanning library & mod.
- [Creating Signatures](Creating-Signatures.md): [User Docs] Learn how to create signatures for code and data patterns.
- [Scanning for Signatures](Scanning-for-Signatures.md): [User Docs] Discover how to use Reloaded3's Signature Scanner library to locate patterns in game memory.

[arcropolis]: https://github.com/Raytwo/ARCropolis
[lazysimd]: https://github.com/Raytwo/lazysimd
[pattern16]: https://github.com/Dasaav-dsv/Pattern16
[requirements]: Requirements.md
[reloaded-memory-sigscan]: https://github.com/Reloaded-Project/Reloaded.Memory.SigScan
[r2-sigscan-mod]: https://github.com/Reloaded-Project/Reloaded.Memory.SigScan/blob/master/External/Reloaded.Memory.SigScan.ReloadedII/StartupScanner.cs