!!! info "This page details a series of 'tricks' and 'advanced functionality' which can be added to emulators"

!!! note "Original code was C#"

    This code was translated to Rust via an LLM, and then updated by hand.

!!! note "The code below uses `format!` for clarity."

    In the real code, a different API should be used to avoid increasing the binary size
    by unreasonable amounts.

## Emulating Files inside Archives

!!! info "Sometimes you may want to emulate a file with the 'original' file being inside an archive."

Here is an example of an `IAwbEmulatorApi` service which does this.

It creates an emulated file with the 'original' file being the data at offset `offset` of the archive
at `sourcePath`. Assuming the data at `offset` is a valid file, and is not compressed, this API
should work just fine.

!!! note "Additional structs like `VirtualAwbHandle` are included for clarity."

```rust
use std::collections::HashMap;
use std::ffi::OsStr;

#[derive(Debug, Clone, Copy)]
struct VirtualAwbHandle(usize);

impl VirtualAwbHandle {
    fn invalid() -> Self {
        VirtualAwbHandle(0)
    }

    fn is_valid(&self) -> bool {
        self.0 != 0
    }
}

#[derive(Debug)]
enum CreateFromFileSliceError {
    Ok,
    CannotOpenFile,
    CannotSeekFile,
    CannotCreateEmulatedFile,
}

struct CreateFromFileSliceResult {
    virtual_awb_handle: VirtualAwbHandle,
    error: CreateFromFileSliceError,
}

struct VirtualAwbInfo {
    file_path: String,
    framework_handle: FileEmulationFrameworkHandle,
}

struct AwbEmulatorApi {
    logger: Logger,
    awb_emulator: AwbEmulator,
    framework: IFileEmulationFramework,
    handles: HashMap<VirtualAwbHandle, VirtualAwbInfo>,
}

impl AwbEmulatorApi {
    pub fn try_create_from_file_slice(
        &mut self,
        source_path: &OsStr,
        offset: u64,
        route: &Route,
        destination_path: &OsStr,
    ) -> CreateFromFileSliceResult {
        // Open a handle to the file which we want to use as the source.
        self.logger.info(&format!(
            "[AwbEmulatorApi] try_create_from_file_slice: {:?}, Ofs {}, Route {:?}",
            source_path, offset, route
        ));

        let file_handle = match open_file(source_path, FileOpenMode::Read) {
            Ok(handle) => VirtualAwbHandle(handle),
            Err(err) => {
                self.logger.error(&format!(
                    "[AwbEmulatorApi] try_create_from_file_slice: Failed to open base file with error: {}, Path {:?}",
                    err,
                    source_path
                ));
                return CreateFromFileSliceResult {
                    virtual_awb_handle: VirtualAwbHandle::invalid(),
                    error: CreateFromFileSliceError::CannotOpenFile,
                };
            }
        };

        // Move to the offset we want to emulate from.
        if let Err(err) = seek_file(file_handle.0, offset, SeekOrigin::Start) {
            self.logger.error(&format!(
                "[AwbEmulatorApi] try_create_from_file_slice: Failed to seek to offset {} with error: {}, Path {:?}",
                offset,
                err,
                source_path
            ));
            close_file(file_handle.0);
            return CreateFromFileSliceResult {
                virtual_awb_handle: VirtualAwbHandle::invalid(),
                error: CreateFromFileSliceError::CannotSeekFile,
            };
        }

        // Use the IEmulator to create an emulated file
        if let Some(emulated_file) = self.awb_emulator.try_create_emulated_file(file_handle.0, source_path, route) {
            // Register the file with FileEmulationFramework so it knows it exists.
            self.logger.info(&format!(
                "[AwbEmulatorApi] try_create_from_file_slice: Registering {:?}",
                destination_path
            ));
            let framework_handle = self.framework.register_virtual_file(destination_path, emulated_file);
            self.handles.insert(
                file_handle,
                VirtualAwbInfo {
                    file_path: destination_path.to_string_lossy().into_owned(),
                    framework_handle: FileEmulationFrameworkHandle(framework_handle),
                },
            );

            CreateFromFileSliceResult {
                virtual_awb_handle: file_handle,
                error: CreateFromFileSliceError::Ok,
            }
        } else {
            self.logger.error(&format!(
                "[AwbEmulatorApi] try_create_from_file_slice: Failed to Create Emulated File at Path {:?}",
                source_path
            ));
            close_file(file_handle.0);
            CreateFromFileSliceResult {
                virtual_awb_handle: VirtualAwbHandle::invalid(),
                error: CreateFromFileSliceError::CannotCreateEmulatedFile,
            }
        }
    }

    // API to cease emulating a file.
    // For very advanced users only, make sure the file is unloaded in underlying application first.
    pub fn invalidate_file(&mut self, virtual_awb_handle: VirtualAwbHandle) {
        if !virtual_awb_handle.is_valid() {
            return;
        }

        if let Some(entry) = self.handles.remove(&virtual_awb_handle) {
            self.awb_emulator.unregister_file(&entry.file_path);
            self.framework.unregister_virtual_file(&entry.file_path, entry.framework_handle.0);

            // Close the file handle associated with the invalidated file
            close_file(virtual_awb_handle.0);
        }
    }
}
```

!!! warning "Be very careful not to leak file handles here."

## Paired Files

!!! info "Sometimes files you may wish to emulate may come in pairs."

    Where one file needs to be modified based on the contents of another emulated file.
    Or some other mechanism exists where two files must match.

In our example, we have 2 files from CRI Middleware, an ACB and an AWB file.

We emulate the AWB, but the ACB file needs to contain a copy of the header from the AWB.

```rust
// ACBEmulator

fn try_create_emulated_file(&mut self, handle: RawHandle, filepath: &OsStr, route: &Route) -> Option<Box<dyn IEmulatedFile>> {
    // Checklist for ACB Emulator's try_create_emulated_file

    /*
        1. Check if the corresponding AWB has already been emulated.
           - If it has not yet been emulated, open a handle to the AWB file using `open_file()`.
           - This should trigger the AWB Emulator to emulate the AWB file.
           - Then re-check state to see if the AWB file has been emulated.
        2. Emulate the ACB file using the stored information.
           - i.e. Patch the ACB to have AWB header.
    */
}

fn unregister_file(&mut self, awb_path: &str) {
    // Unemulate the ACB file.
    // You may want to unregister the AWB+ACB in pairs.
    // As they are emulated in pairs.
}
```

There are different solutions from this problem, but the template above shows one way.
Basically the `AcbEmulator` has a check to ensure the AWB is emulated first, if it has not.

How this check is implemented, is up to the developer, as it is implementation details.
You can use events, shared state, or any other method.

The important parts are:

- The files can be opened in any order.
    - ***Never assume the files will be opened in a specific order***.
    - For two files/emulators like this, it's simple, for a case of N files, consider making a
      shared helper that can be called from any of the emulators.
- The files should be unregistered in same pairs they were created with.
    - In the case there is an API, to maintain consistency.