This framework prioritises performance and compatibility first.

!!! warning "When writing Emulators, please stick to the following rules"

| Rule                                                            | Summary                                                                    |
| --------------------------------------------------------------- | -------------------------------------------------------------------------- |
| [Generated Files are Immutable](#generated-files-are-immutable) | Always serve the same content on subsequent requests/handle openings.      |
| [Never Disable The Emulator](#never-disable-the-emulator)       | An emulated file may also be created at any time, you cannot predict when. |

!!! note "Additional rules automatically handled or encouraged by framework provided abstractions"

| Rule                                                                    | Description                                                                              |
| ----------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| [Always Return All Requested Bytes](#always-return-all-requested-bytes) | Shield emulator against buggy software implementations.                                  |
| [Don't Assume Any Read Pattern](#dont-assume-any-read-pattern)          | Data can be accessed in any order; reads may begin from any offset and/or length.        |
| [Use Lazy Loading](#use-lazy-loading)                                   | Produce/initialize emulated files only when they are first requested by the application. |

!!! danger "Don't implement hacks!! Focus on compatibility."

    Do not implement hacks for things such as `hotswapping` files at runtime by serving
    different data on future loads; or writing to buffers passed by the application.

    Emulators should ***MAKE NO ASSUMPTIONS*** about the underlying program.

    Additional functionality such as 'hot reload' may instead be implemented on a per game or per
    middleware basis in additional mods. APIs to allow such advanced features
    (e.g. 'rebuild emulated file') can be provided by an emulator, but ***must not be enabled by default.***

## Generated Files are Immutable

!!! info "The file emulator should always serve the same file on subsequent requests/handle openings."

Generated files should always persist for whole application lifetime.

**Explanation:**

- An Emulator ***should not assume*** how the game/application will use the file.
- The target application may for example, read part of the file, such as the header and cache
  it in its own memory.
- Because we don't know what the application will do, we cannot safely change any part of the
  file after it has been read once.

## Never Disable The Emulator

!!! info "Enable the emulator at startup once and never disable it."

    Emulators should not be unloadable or suspendable mods.

An emulated file may also be created at any time, you cannot predict when.

And of course, emulators also work recursively, a mod may have a file your emulator might pick up.

## Always Return All Requested Bytes

!!! info "When a read request is made, the emulator should always return ***all*** requested bytes."

    A common programmer error is to issue a `Read()` command on a file stream and assume that
    all bytes requested will be given back.

!!! tip "[MultiStream][multistream] abstraction automatically handles this for you."

    If you're using this abstraction, you don't need to worry about this.

***Calling `Read()` will not always give you all your requested bytes!!***
But many developers (even myself included) have been guilty of this mistake for a very long time.

If possible, ***DO NOT*** return less than the number of bytes requested in order to shield
against buggy software implementations.

If you're using custom logic to resolve read requests that does not involve [MultiStream][multistream],
please ensure that you always return the requested number of bytes without fail. This may in some cases
require multiple calls to your own implementation of `Read()`.

## Don't Assume Any Read Pattern

!!! tip "Assume data can be accessed in any order, and reads may begin from any offset and/or length."

!!! tip "[MultiStream][multistream] abstraction automatically handles this for you."

## Use Lazy Loading

!!! info "Only produce/initialize emulated files when they are first requested by the application."

!!! tip "In other words, create your final files in `TryCreateFile` API."

    And up until that's called, just collect the data you need to create the file.

    e.g. Source folders.

[multistream]: ./implementation-utilities.md#multi-stream