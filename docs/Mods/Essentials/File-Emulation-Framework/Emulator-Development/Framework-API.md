
!!! info "Sometimes you may need to interact with the File Emulation Framework directly."

    Simply to register your emulator, or for more advanced use cases.

## register

```rust
fn register(&mut self, emulator: Box<dyn IEmulator>);
```

Registers an emulator with the framework.

- `emulator`: The emulator instance implementing the `IEmulator` trait.

## register_virtual_file

!!! tip "This is often used to create a virtual file backed by a slice of another file."

```rust
fn register_virtual_file(&mut self, file_path: &OsStr, file: Box<dyn IEmulatedFile>) -> FileEmulationFrameworkHandle;
```

Registers a virtual file with the framework.

- `file_path`: The path of the virtual file.
- `file`: The emulated file instance implementing the `IEmulatedFile` trait.
- Returns: A handle to the registered virtual file.

This is used to make the framework recognise an arbitrary virtual file.

Sometimes this is useful in the case that you manually want to create an emulated file without
having to wait for the game/application to open it.

## unregister_virtual_file

Removes a registration for a previously registered virtual file.

```rust
fn unregister_virtual_file(&mut self, file_path: &OsStr);
```

- `file_path`: The path of the virtual file to unregister.

Sometimes this is handy when you want to implement more advanced functionality such as 'hot reload'
in mods that use emulators under the hood.

## try_create_from_file_slice

!!! info "Tries to create an emulated file from a specific file slice."

```rust
fn try_create_from_file_slice(
    &mut self,
    file_path: &OsStr,
    offset: u64,
    length: FileLength,
    route: &Route
) -> EmulatedFileResult;
```

- `file_path`: The path of the file to open.
- `offset`: The file offset from which to start emulating.
- `route`: The route associated with the emulated file.
- `destination_path`: The destination path where the emulated file will be registered.
- Returns: An `EmulatedFileResult` struct containing the result of the operation.

This API allows emulators to create an emulated file from a specific file slice.
This is useful if you want to create a file based on the slice of uncompressed data within an archive.

[Example in Emulator Cookbook][cookbook-example].

The difference between what's in the cookbook and this API is how they are invoked.
In the cookbook, the invoker of an API is expected to be an external mod that is not an emulator.

This API on the other hand is intended to be instead invoked from within an emulator, as the emulator
is building the emulated file. (In the `Build` function)

For example, when you create an emulated `.AFS` archive (which is a container of uncompressed files)
, calling `try_create_from_file_slice` for every unmodified (non-injected) file will allow for another
emulator to pick up the file and emulate it. This avoids the necessity for extracting anything from
the archive and allows for emulators to stay recursive.

!!! note "The lifetime of the result of `try_create_from_file_slice` is tied to the lifetime of the file with matching `file_path`"

    In other words, when original emulated is destroyed/unloaded, the emulated file here will be unloaded too.

[cookbook-example]: ./Emulator-Cookbook.md#emulating-files-inside-archives