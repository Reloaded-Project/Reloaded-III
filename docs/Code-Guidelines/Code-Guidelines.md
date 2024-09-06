{% raw %}
## Project Settings

!!! info "As a general rule of thumb, start with [reloaded-library-template][reloaded-library-template]."

Use the following settings:

- ✅ Include Documentation
- ✅ Cross Platform Testing Instructions & GitHub Actions Test Runs
- ✅ Run Automated Tests against Wine
    - 📔 When writing libraries that call OS APIs. (Including simple file reads, etc.)
- ✅ Build C Libraries in CI
- ✅ Std by Default (via STD feature)
    - 📔 [More on this below](#portability-guidelines)

## About Optimizing for Binary Size

!!! info "These are the guidelines for writing compact code."

    In other words, building binaries with small sizes.

Consider parts of this page as an extension of [johnthagen/min-sized-rust][min-sized-rust].

While the former is about how you can tweak compilation options to achieve a small binary,
this will give some guidance on how to structure new code to meet the
[code size guidelines for the mod loader][mod-loader-hw-requirements].

### When to *NOT* Over-Optimize for Size

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

### When Optimizing for Size is Encouraged

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

## Guidelines

### [Size & Perf] Be smart with library usage

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
    > - If `self` has a verbatim prefix (e.g. `\\?\C:\windows`) and `path` is not empty, the new path is normalized: all references to `.` and `..` are removed.

    In this context, because we are constructing a unix path, which is guaranteed to begin with `/`,
    and are always appending a directory.

    We don't need to handle any of these edge cases. The code for that is unnecessary, and will
    unnecessarily bloat the binary and make things slower.

!!! tip "Sometimes it's better to use `libc` rather than `std` for minimizing code size."

### [Size & Perf] Review (Vet) Library Source Code

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

### [Size] Use Feature Flags for Optional Functionality

!!! tip "Use feature flags to disable functionality which is not always a hard requirement."

As a practical example, consider an archive library like [C# Nx Archive Library][nx-library]
I wrote as part of my day-to-day job.

In the `Nx` library, multiple compression algorithms are supported, namely `Zstandard` and `LZ4`.

*However*, LZ4 is only used for ***very special cases***, 99% of the time, *Zstandard* is used. Therefore
it would be worthwhile to be able to disable LZ4 support.

#### 5.1 Cargo.toml

!!! tip "Put support for non-standard compression as a flag."

```toml
[dependencies]
lz4 = { version = "1.24", optional = true }
zstd = { version = "0.11", optional = true }

[features]
default = ["zstd-compression", "lz4-compression"]
zstd-compression = ["zstd"]
lz4-compression = ["lz4"]
```

#### 5.2 Usage

!!! tip "Users can now choose which compression algorithms to include"

```toml
# Include both LZ4 and Zstandard (default)
archive-lib = "0.1.0"

# Include only ZStd
archive-lib = { version = "0.1.0", default-features = false, features = ["zstd-compression"] }
```

#### Other Benefits

In addition to reducing binary size, this approach also reduces compilation time,
which for Rust projects can be extremely valuable.

## Portability Guidelines

!!! info "The modding framework strives to be [portable to even embedded systems][mod-loader-esoteric]."

    Below are guidelines to ensure your code is portable to a wide range of platforms.

Start with the [Reloaded Library Template](#project-settings).

### 1. Use `no_std` as a Foundation

When aiming for maximum portability, start with `no_std` as your base:

```rust
#![no_std]

// The template will take care of this for you.
```

This approach ensures your code doesn't rely on the standard library (`std`).
We will instead be leveraging subsets of `std` like `core` and `alloc`.

```rust
use core::fmt;
use core::ops::Add;
```

These are not platform-specific and can be used across all platforms.

!!! tip "Prefer `no_std` code and libraries where possible."

### 2. Abstraction Layers with Auto-Enabled Features

!!! tip "Create trait-based abstractions for platform-specific features"

This approach uses `build.rs` to automatically enable features based on the target platform,
allowing for clean separation of platform-specific code.

!!! note "We'll be using a `filesystem` as it is an easy to understand example."

    However do note, sometimes you can find libraries [(example)][pthread-3ds]
    that can supply missing `std` functionality.

#### 2.1 Project Structure

```
my_portable_lib/
├── Cargo.toml
├── build.rs
└── src/
    ├── lib.rs
    ├── fs.rs
    └── platforms/
        ├── std.rs
        ├── vita.rs
        └── switch.rs
```

#### 2.2 build.rs

!!! info "This automatically enables a feature based on the build target."

    This will make it easier to add conditional compiles like down the line.

    - `#[cfg(feature = "switch")]` is cleaner then
    - `#[cfg(all(target = "aarch64-nintendo-switch-freestanding", not(feature = "std")))]`

```rust
fn main() {
    let target = std::env::var("TARGET").unwrap();

    match target.as_str() {
        "armv7-sony-vita-newlibeabihf" => {
            println!("cargo:rustc-cfg=feature=\"vita\"");
        }
        "aarch64-nintendo-switch-freestanding" => {
            println!("cargo:rustc-cfg=feature=\"switch\"");
        }
        _ => {
            println!("cargo:rustc-cfg=feature=\"std\"");
        }
    }
}
```

- `vita` feature for `armv7-sony-vita-newlibeabihf` target.
- `switch` feature for `aarch64-nintendo-switch-freestanding` target.
- `std` feature for all other targets.

#### 2.3 Cargo.toml

!!! info "Make sure `Cargo.toml` includes the features."

```toml
[package]
name = "my_portable_lib"
version = "0.1.0"

[features]
default = []
std = []
vita = []
switch = []
```

#### 2.4 lib.rs

```rust
mod fs;
pub use fs::FileSystem;

#[cfg(feature = "std")]
mod platforms {
    mod std;
    pub use self::std::FS;
}

#[cfg(feature = "vita")]
mod platforms {
    mod vita;
    pub use self::vita::FS;
}

#[cfg(feature = "switch")]
mod platforms {
    mod switch;
    pub use self::switch::FS;
}

// This provides access to abstraction without
// knowing the specific implementation
pub use fs::FileSystem;
pub use platforms::Fs as FS;

// Platform-agnostic usage with zero-cost abstraction
pub fn use_file_system() {
    // Use FS::open(), FS::rename(), FS::delete()
    // without knowing the specific implementation
    let _ = FS::open("example.txt");
    let _ = FS::rename("old.txt", "new.txt");
    let _ = FS::delete("unwanted.txt");
}
```

#### 2.5 fs.rs

!!! info "Defines the `FileSystem` abstraction."

```rust
pub trait FileSystem {
    fn open(path: &str) -> Result<File, FileError>;
    fn rename(from: &str, to: &str) -> Result<(), FileError>;
    fn delete(path: &str) -> Result<(), FileError>;
}

// Define File and FileError here
```

#### 2.6 Platform-Specific Implementations

```rust
use crate::fs::{FileSystem, File, FileError};
pub struct FS;

impl FileSystem for FS {
    fn open(path: &str) -> Result<File, FileError> {
        // Implementation using std::fs
    }
    fn rename(from: &str, to: &str) -> Result<(), FileError> {
        // Implementation using std::fs
    }
    fn delete(path: &str) -> Result<(), FileError> {
        // Implementation using std::fs
    }
}
```

`platforms/vita.rs` and `platforms/switch.rs` would follow a similar pattern, implementing the
`FileSystem` trait for their respective platforms.

#### 2.7 Usage in External Crate

```rust
use my_portable_lib::FS;

fn main() {
    let _ = FS::open("example.txt");
}
```

This structure allows for:

1. Automatic feature selection based on the build target.
2. Clean separation of platform-specific code.
3. A common interface (`FileSystem` trait) for all platforms.
4. Platform-agnostic usage through the `FileSystem` type alias.

The `build.rs` script enables the appropriate feature based on the target, and the rest of the
code uses these features to conditionally compile the correct implementation.

### 3. Enable Alternative Allocators

!!! warning "This requires nightly Rust."

    However, you can use [allocator-api2][allocator-api2] to polyfill this for stable if desired.

When writing portable libraries, allow for use of alternative allocators to support various
memory management needs.

!!! tip "Sometimes switching the allocator can also bring performance benefits."

    Not just portability benefits! Therefore, it's a good idea to follow this guideline.
    For example you may want to use a separate allocator for small, short lived objects.

```rust
struct IndexBuffer<A: Allocator = Global> {
    data: Vec<u32, A>,
}

impl<A: Allocator> IndexBuffer<A> {
    // Constructor for custom allocator
    pub fn new_in(allocator: A) -> Self {
        Self {
            data: Vec::new_in(allocator),
        }
    }
}

impl IndexBuffer {
    // Constructor with default allocator
    pub fn new() -> Self {
        Self::new_in(Global)
    }
}

// And if working with manual memory
impl<A: Allocator> Drop for IndexBuffer<A> {
    fn drop(&mut self) {
        // Code here.
    }
}
```

This enables for usage like

```rust
// Using default allocator
let t1 = Tessellator::new();

// Using custom allocator
use std::alloc::System;
let t2 = Tessellator::new_in(System);
```

For custom allocators prefer static dispatch.
If possible, prefer using zero sized types for allocators, as to not incur overhead.


!!! warning "Adding an allocator parameter can affect inlining."

    Make sure to benchmark your code, even if the parameter is zero sized.

#### 3.1 Allocating uninitialized memory.

In place where you would use `alloc::alloc::alloc` or `alloc::alloc::dealloc`, consider using the provided allocator.

```rust
// Constructor for custom allocator
pub fn new_in(allocator: A) -> Self {
    let layout = Layout::array::<u32>(5).unwrap();

    // ❌ Don't use `alloc` (global allocator)
    let alloc = alloc(layout);

    // ✅ Instead use supplied allocator
    let alloc = allocator.allocate(layout);
}
```

When possible, avoid unsafe allocation and use safe constructs.

!!! example "Creating an array of 5 elements, in custom allocator, uninitialized."

    Requires Nightly Rust.

    ```rust
    let mut boxed_array = Box::<[i32], A>::new_uninit_slice_in(5, allocator);
    let mut boxed_array = unsafe {
        // Deferred initialization:
        boxed_array[0].as_mut_ptr().write(1);
        boxed_array[1].as_mut_ptr().write(2);
        boxed_array[2].as_mut_ptr().write(3);

        boxed_array.assume_init()
    };

    // More verbose alternative to first line (commented)
    // let mut boxed_array: Box<[MaybeUninit<i32>], A> = Box::new_uninit_slice_in(5, allocator);
    ```

### 4. Stack Memory Allocation

!!! info "When writing portable code, be aware of the varying thread stack sizes across different platforms"

Often you might want to allocate things on the stack for performance, but that can't always be done.

#### 4.1 Common Platform Stack Sizes

Note that these sizes can vary based on specific configurations:

- **Windows**:
    - Default: 1 MiB
    - Can be configured up to 8 MB
- **macOS**:
    - Default: 8 MiB
- **Linux**:
    - Default: 8 MiB

As a general rule of thumb, try to avoid allocating objects larger than 100K on the stack.

##### Esoteric and Embedded Platforms

!!! note "This is provided for completion."

    If you're an external contributor, you're not expected to keep these in mind.
    [More Info Here][mod-loader-esoteric]

For these sorts of platforms, such as sixth-generation consoles and embedded devices, assume the
stack size is around 64K on main thread and around 4K on non-main threads. For these platforms,
avoid >1000 byte stack allocations.

#### 4.2 Mixing Stack and Heap Allocation

!!! info "Sometimes it's possible to allocate on Stack with Heap fallback."

    For cases where you need fast allocation but it's possible the number of items
    is small.

[SmallVec][smallvec] is a vector-like container that stores a small number of elements on the stack,
falling back to the heap for larger allocations.

Example usage:

```rust
use smallvec::{SmallVec, smallvec};

// A SmallVec that can hold up to 4 elements on the stack
let mut vec: SmallVec<[u32; 4]> = smallvec![1, 2, 3];

vec.push(4); // Still on the stack
vec.push(5); // This will cause a heap allocation

assert_eq!(vec[0], 1);
assert_eq!(vec.len(), 5);
```

This helps boost performance by avoiding heap allocation for small collections.

### 5. Implement Abstractions for External Code

!!! tip "When interacting with external libraries or low-level systems, create safe Rust abstractions to manage unsafe operations."

    Don't trust that users downstream will manage memory correctly. Not even I trust myself.

!!! note "Most important libraries will already have bindings."

    But if you need to create new ones, follow the pattern below.

Consider a C library that provides functions to create and free an object (e.g. array):

```c
// C library functions
void* create_array(size_t size);
void free_array(void* ptr);
```

#### 5.1 Declare the C exports

!!! tip "This should be automated with [bindgen][bindgen]"

```rust
// FFI declarations
extern "C" {
    fn create_array(size: usize) -> *mut std::ffi::c_void;
    fn free_array(ptr: *mut std::ffi::c_void);
}
```

#### 5.2 Create a safe Rust wrapper

!!! tip "This wrapper ensures memory is not leaked."

```rust
pub struct SafeArray {
    ptr: *mut u8,
    len: usize,
}

impl SafeArray {
    pub fn new(size: usize) -> Option<Self> {
        let ptr = unsafe { create_array(size) as *mut u8 };
        if ptr.is_null() {
            None
        } else {
            Some(SafeArray { ptr, len: size })
        }
    }
}

impl Drop for SafeArray {
    fn drop(&mut self) {
        unsafe { free_array(self.ptr as *mut std::ffi::c_void) }
    }
}
```

In this specific example, implementing `Deref` for automatic conversion to a slice is useful:

```rust
use core::ops::{Deref, DerefMut};
impl Deref for SafeArray {
    type Target = [u8];
    fn deref(&self) -> &Self::Target {
        unsafe { std::slice::from_raw_parts(self.ptr, self.len) }
    }
}

impl DerefMut for SafeArray {
    fn deref_mut(&mut self) -> &mut Self::Target {
        unsafe { std::slice::from_raw_parts_mut(self.ptr, self.len) }
    }
}
```

#### 5.3 Use the safe Rust Abstraction

```rust
let array = SafeArray::new(10).expect("Failed to allocate array");
// Use array as a normal Rust slice
array[0] = 42;
// Memory is automatically freed when `array` goes out of scope
```

#### 5.4 Summary

1. The `SafeArray` struct encapsulates the raw pointer and length.
2. `Deref` and `DerefMut` implementations provide safe access to the array contents.
3. The `Drop` implementation ensures the memory is freed when the `SafeArray` is dropped.
4. All unsafe operations are contained within the implementation, providing a safe public API.
5. Error handling is implemented for allocation failures.

!!! note "Always document unsafe code and explain why it's necessary and how safety is upheld."

#### 5.5 How to Implement this Pattern

!!! tip "The standard for Rust is creating a `-sys` crate with the C exports, and a `-safe` crate with the safe Rust abstractions."

In other words:

- The `-sys` crate should contain the raw FFI declarations (`create_array` and `free_array`).
    - [This video can be used as a primer][creating-rust-ffi].
    - Combine with [bindgen docs][bindgen-docs] and [cc docs][cc-docs].
- The `-safe` crate should define the safe abstractions (`SafeArray` struct).
    - The end of [this guide][dwelo-guide] and its [part 2][dwelo-guide-2] give some good advice.
- The `-safe` crate depends on the `-sys` crate, providing a safe API for end-users.

This separation allows users to choose between raw bindings and safe abstractions, and facilitates maintenance and updates of the FFI layer.

!!! warning "Reloaded3 does not integrate with native package managers."

    Do not attempt to dynamic link to non-system libraries. There is not yet an available mechanism
    that says e.g. `dynamic link zstd if installed`. It is unlikely that there will be one
    any time soon.

### 6. Testing Across Different Platforms & Architectures

!!! info "To ensure correctness, please test your code on multiple platforms."

As a general rule of thumb, test your code against:

- At least 1 CPU architecture (e.g. x64 + ARM64)
- Different word sizes (e.g. 32-bit + 64-bit)
- Different endianess (e.g. little-endian + big-endian)
    - Do this if serializing data, e.g. doing networking or writing archive formats, etc.

!!! tip "The [reloaded-library-template][reloaded-library-template] is set up to do this out of the box."

    Provided you enabled cross-platform testing when creating the library.

!!! tip "Use `cross` for testing on different architectures."

    If you need to locally test, do use `cross`.
    Example: `cross test --target powerpc-unknown-linux-gnu` (32-bit, big-endian)

    You should find more detailed instructions in the [reloaded-library-template][reloaded-library-template].

### 7. Avoid Panic

!!! warning "Panic should be avoided where possible in portable reloaded3 libraries."

`panic!` in Rust can lead to several issues:

1. It creates unwind tables, increasing binary size.
2. It can negatively impact performance when mixed together with `Result<T, E>`.
3. It's inconvenient for C exports; because you have to catch it, which adds overhead and inconvenience.
    - If not caught, it leads to undefined behaviour.
4. You need to recursively document it in the docstrings; which is painful.

#### 7.1 Don't Panic unless Absolutely Necessary

!!! info "You should only panic on truly unrecoverable errors"

```rust
// Define a simple error enum
#[derive(Debug, PartialEq)]
enum ValidationError {
    TooSmall,
    TooBig,
}

// ❌ Don't use methods that can panic
fn risky_validate(num: i32) -> i32 {
    assert!(num >= 1, "Number too small");  // This can panic
    assert!(num <= 100, "Number too big");  // This can panic
    num
}

// ✅ Do use Result with an enum error type to handle potential errors
fn safe_validate(num: i32) -> Result<i32, ValidationError> {
    if num < 1 {
        Err(ValidationError::TooSmall)
    } else if num > 100 {
        Err(ValidationError::TooBig)
    } else {
        Ok(num)
    }
}
```

Here the validation panic is undesireable, as it can be handled gracefully by the caller.

Only panic if you have 100% unrecoverable errors where you absolutely
have to abort the program.

#### 7.2 Use `Result<T, E>` Instead of Panicking

!!! tip "Always prefer returning a `Result<T, E>` instead of using operations that might panic."

This allows the caller to handle errors gracefully, and also lets them be aware of all possible error cases.

```rust
// Define an error enum
#[derive(Debug, PartialEq)]
enum DivisionError {
    DivideByZero,
}

// ❌ Don't use methods that can panic
fn risky_divide(a: i32, b: i32) -> i32 {
    a / b // This will panic if b is zero
}

// ✅ Do use Result with an enum error type to handle potential errors
fn safe_divide(a: i32, b: i32) -> Result<i32, DivisionError> {
    if b == 0 {
        Err(DivisionError::DivideByZero)
    } else {
        Ok(a / b) // Compiler will infer it can't be 0
    }
}
```

!!! tip "If you can guarantee that `b` cannot be zero, use `unchecked_div`."

```rust
// ✅ Do use unchecked_div if you can guarantee b is not zero
fn divide(a: i32, b: i32) -> i32 {
    unsafe { a.unchecked_div(b) }
}
```

#### 7.3 Avoid Indexing (Use `Option<&T>`)

!!! info "Indexing with `[]` can panic if the index is out of bounds."

Instead, use `get()` which returns an `Option<&T>`.

```rust
// ❌ Don't use indexing
let first = my_vec[0]; // This can panic

// ✅ Do use get() and handle the None case
let first = my_vec.get(0).copied().unwrap_or_default();
```

!!! tip "If you can guarantee at compile time that the index is within bounds, use `unsafe` indexing"

```rust
// ✅ Do use unsafe indexing if bounds are guaranteed
let first = unsafe { *my_vec.get_unchecked(0) };
```

#### 7.4 Careful Use of `unwrap()` and `expect()`

Avoid using `unwrap()` or `expect()` in production code, as these will panic on `None` or `Err` values.

```rust
// ❌ Don't use unwrap() or expect()
let value = some_operation().unwrap();

// ✅ Do handle the error case explicitly
let value = match some_operation() {
    Ok(v) => v,
    Err(e) => handle_error(e),
};
```

!!! tip "If you can guarantee at compile time the result will be valid, use a debug only check."

    With the [debug unwraps] crate.

```rust
// ✅ Do use debug_unwrap_unchecked() if you can guarantee the result is valid
// This will only check result in debug builds.
let value = unsafe { some_operation().debug_unwrap_unchecked() };
```

Any use of this should be covered in tests, and ideally with a comment explaining why the guarantee is upheld
if needed.

#### 7.5 Safe Alternatives to Panicking Operations

!!! info "Some standard library functions can panic."

    Avoid panicking if possible, we don't want code bloat explained above.

For example, the `std` function `copy_from_slice`, panics if the slices have different lengths:

```rust
// ❌ Don't use copy_from_slice, which can panic
fn copy_data(destination: &mut [u8], source: &[u8]) {
    destination.copy_from_slice(source); // Panics if lengths differ
}

// ✅ Do implement a safe alternative
fn safe_copy_data(destination: &mut [u8], source: &[u8]) -> Result<(), SomeErrorType> {
    if destination.len() < source.len() {
        return Err(SomeErrorType::DestinationTooSmall);
    }
    let copy_len = source.len();
    unsafe { copy_nonoverlapping(source.as_ptr(), destination.as_mut_ptr(), copy_len); }
    Ok(())
}
```

#### 7.6 Use `#[no_panic]` Attribute

!!! tip "You can use the `#[no_panic]` attribute from the `no-panic` crate."

    This will cause a compile-time error if the function could potentially panic.

```rust
use no_panic::no_panic;

#[no_panic]
fn critical_function(x: u32) -> u32 {
    x + 1 // This function is guaranteed not to panic
}
```

<!-- Links -->
[file-emulation-framework]: ../Mods/Essentials/File-Emulation-Framework/About.md
[game-support-layer2]: ../Loader/Core-Architecture.md#game-support-layer-2
[gamecontrollerdb]: https://github.com/mdqinc/SDL_GameControllerDB
[min-sized-rust]: https://github.com/johnthagen/min-sized-rust
[middleware-mods]: ../Loader/Core-Architecture.md#middlewareos-handling-mods-layer-1
[mod-loader-hw-requirements]: ./Hardware-Requirements.md#mod-loader
[mod-loader-esoteric]: ./Hardware-Requirements.md#about-esoteric-and-experimental-platforms
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
[reloaded-library-template]: https://github.com/Reloaded-Project/reloaded-templates-rust
[pthread-3ds]: https://github.com/rust3ds/pthread-3ds
[allocator-api2]: https://crates.io/crates/allocator-api2
[smallvec]: https://github.com/servo/rust-smallvec
[nx-library]: https://nexus-mods.github.io/NexusMods.Archives.Nx/
[bindgen]: https://github.com/rust-lang/rust-bindgen
[creating-rust-ffi]: https://www.youtube.com/watch?v=KWrfxKUBIuo
[bindgen-docs]: https://docs.rs/bindgen
[cc-docs]: https://docs.rs/cc
[dwelo-guide]: https://medium.com/dwelo-r-d/using-c-libraries-in-rust-13961948c72a
[dwelo-guide-2]: https://medium.com/dwelo-r-d/wrapping-unsafe-c-libraries-in-rust-d75aeb283c65
[debug unwraps]: https://crates.io/crates/debug_unwraps
{% endraw %}
