!!! warning "This documentation is a translation of the existing C# documentation into Rust"

    Final APIs may slightly differ. The translation was done by an LLM.

## Core API

!!! info "This is the API that's most commonly used inside emulator implementations."

### File I/O APIs

!!! info "FileEmulatorFramework provides a very minimal, simple API for reading existing file content"

!!! Note "`POSIX` covers Linux, macOS, and other Unix-like systems."

These APIs abstract away the platform-specific details and provide a consistent interface for file
I/O operations that map to low level native API calls.

!!! tip "By using these functions, emulator code can be written in a platform-independent manner."

    So you can write and test your emulator on Linux, and it'll automatically work on Windows
    (and vice versa).

#### read_file

!!! info "Reads data from a file, advancing the current file pointer by the number of bytes read."

It maps to different APIs depending on the platform:

| Platform | API                                                 |
| -------- | --------------------------------------------------- |
| Windows  | `ReadFile`                                          |
| POSIX    | `read` from `libc`                                  |

```rust
let mut buffer = vec![0; 1024];
let bytes_read = read_file(file_handle, &mut buffer).unwrap();
```

#### read_struct

!!! info "Reads a struct from the current position of the file handle."

This function provides a convenient way to read a struct directly from a file handle.

```rust
#[repr(C)]
struct MyStruct {
    field1: u32,
    field2: u16,
}

let my_struct: MyStruct = read_struct(file_handle).unwrap();
```

#### seek_file

!!! info "Changes the file pointer (offset) of the specified file handle."

| Platform | API                                                 |
| -------- | --------------------------------------------------- |
| Windows  | `SetFilePointerEx`                                  |
| POSIX    | `lseek` from `libc`                                 |

```rust
// Seek to the beginning of the file
seek_file(file_handle, 0, SeekOrigin::Start).unwrap();
```

#### get_file_pointer

!!! info "Retrieves the current value of the file pointer (position) of the specified file handle."

| Platform | API                                                 |
| -------- | --------------------------------------------------- |
| Windows  | `SetFilePointerEx` with `FILE_CURRENT`              |
| POSIX    | `lseek` from `libc` with `SEEK_CUR`                 |

```rust
let current_position = get_file_pointer(file_handle).unwrap();
println!("Current file pointer: {}", current_position);
```

#### open_file

!!! info "Opens a file for reading and returns a file handle."

| Platform | API                                                 |
| -------- | --------------------------------------------------- |
| Windows  | `CreateFileW`                                       |
| POSIX    | `open` from `libc`                                  |

```rust
let file_handle = open_file("path/to/file.bin").unwrap();
```

### Route

!!! info "A utility struct that represents a path to a file within the context of the FileEmulationFramework."

The `Route` struct is used to match files that should be emulated based on their paths.
It provides methods to check if a given path matches the route.

```rust
let route = Route::new("path/to/file.bin");
```

#### matches_no_subfolder

!!! info "Checks if the given `group.Route` matches the end of the current `Route`, without considering subfolders."

This method is commonly used when checking if a file should be emulated based on its path.

```rust
let route = Route::new("path/to/file.bin");
let group_route = Route::new("file.bin");
let matches = route.matches_no_subfolder(&group_route); // true
```

#### matches_with_subfolder

!!! info "Checks if the given `group.Route` matches the current `Route`, considering subfolders."

This method is used when dealing with emulated files that have a hierarchy of internal files or nested folders.

```rust
let route = Route::new("parent.bin");
let group_route = Route::new("parent.bin/child/child.dds");
let matches = route.matches_with_subfolder(&group_route); // true
```

For more detailed information on how the `Route` struct and its methods work, please refer
to the [Routing][routing] page.

### Streams

#### MultiStream

!!! info "`MultiStream` combines multiple streams into a single stream with read and seek support."

The `MultiStream` is the primary abstraction used in building emulators. Most emulators simply
build a `MultiStream` and use that to resolve read calls directly.

This abstraction is very highly optimised, and is the recommended way to build emulators.

```rust
// Build a Stream.
let streams = vec![
    StreamOffsetPair::new(File::open("file1.bin").unwrap(), OffsetRange::from_start_and_length(0, 1024)),
    StreamOffsetPair::new(File::open("file2.bin").unwrap(), OffsetRange::from_start_and_length(1024, 2048)),
];

let multi_stream = MultiStream::new(streams);

// Read data spanning both streams
let mut data = vec![0; 2048];
multi_stream.read(&mut data).unwrap();
```

#### PaddingStream

!!! info "Stream that fills the read buffer with a single, user specified byte."

Emulated files will very often have padding bytes, for example, padding between the end of one file
and the start of another file.

`PaddingStream` is used to supply that padding, when used in conjunction with [MultiStream](#multistream).

```rust
// Create 1024 bytes of 0x00 padding
let padding_stream = PaddingStream::new(0x00, 1024);
```

#### FileSliceStream

!!! info "A `Stream` abstraction that wraps a [FileSlice](#fileslice)."

These structs allow you to read data from a [FileSlice](#fileslice) as if it were a stream.

Example:

```rust
let slice = FileSlice::new(1024, 4096, "file.bin");
let stream = FileSliceStream::new(slice);
```

### Primitives

#### FileSlice

!!! info "An abstraction that allows you to read a region of a given file."

When building emulators, you will often provide a mixture of the original data and new data.
This struct will allow you to more easily fetch the original data when needed.

```rust
// Create a slice for the first 1024 bytes of a file
let slice = FileSlice::new(0, 1024, "path/to/file.bin");
```

##### Merging File Slices

!!! tip "Slices of the same file that touch each other can be merged into singular, larger slices."

!!! tip "This is usually automatically handled by [MultiStream](#multistream) under the hood."

For example, `0-4095` and `4096-65536` can be merged into a single slice of `0-65536`.

In practice, this is sometimes possible when working with archives containing
file data whereby multiple files are laid out side by side.

```rust
let first = FileSlice::new(0, 4096, "file.bin");
let second = FileSlice::new(4096, 4096, "file.bin");

if let Some(merged) = FileSlice::try_merge(first, second) {
    // Successfully merged into 'merged'
}
```

If you are using streams backed by `FileSlice`, you can merge them
using `FileSliceStream::try_merge` for individual streams or
`FileSliceStream::merge_streams` when you have multiple streams.

#### OffsetRange

!!! info "A utility struct that stores a start and end offset [inclusive]."

Can be used for testing for overlaps, testing if an address is in range, etc.

```rust
let range = OffsetRange::from_start_and_length(1024, 512);
let is_in_range = OffsetRange::contains_point(&range, 1536); // true
```

##### `OffsetRangeSelector`

!!! info "Utility for quickly finding the offset range that contains a given offset."

The `OffsetRangeSelector` is used to quickly find the index of an `OffsetRange` that contains a
given offset. It assumes that the provided `OffsetRange`s are sorted in ascending order and
without gaps.

Internally, the selector uses binary search to efficiently locate the correct range index.

Example usage:

```rust
let ranges = vec![
    OffsetRange::from_start_and_length(0, 1024),
    OffsetRange::from_start_and_length(1024, 2048),
    OffsetRange::from_start_and_length(2048, 4096),
];

let selector = OffsetRangeSelector::new(ranges);
let index = selector.select(1500); // Returns 1
```

The data should be internally represented as `0`, `1024`, `2048`, `4096`,
with the ranges joined.

## Utility API

### `Mathematics` Struct

This struct has some common mathematics related operations, such as rounding up numbers to add padding to files.

```rust
let rounded_up = Mathematics::round_up(1234, 512); // 1536
```

### `DirectorySearcher` Struct

!!! info "The `DirectorySearcher` struct can be used for extremely fast searching of files on the filesystem."

On Windows, this uses a custom implementation which uses the `NtQueryDirectoryFile` under the hood.
For Linux, this uses the standard Rust library as that is already efficient.

Expect a considerable speedup over the built-in Rust implementation.

```rust
let (files, directories) = DirectorySearcher::get_directory_contents_recursive("C:/MyFolder");
```

[routing]: ./Routing.md