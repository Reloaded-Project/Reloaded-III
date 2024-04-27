# Optimizations

!!! note "Some parts of this section will compare against the [original unreleased C# implementation][original-impl]"

    This is to give an idea of where things can be improved while translating some existing code.

## Strings

!!! info "All strings internally are stored in the platform's native string format."

### Encoding

#### Unix-based Systems

!!! info "On Linux and other unix-based systems, a file or folder is usually represented by a sequence of bytes."

We'll assume UTF-8, as that's the case on pretty much all modern distros.

#### Windows

!!! info "On Windows, that is a sequence of 16-bit characters (UTF-16)."

Although Windows has ANSI (`A`) and Unicode (`W`) APIs side by side, under the hood, Windows
converts everything to UTF-16.

In order to speed things up, it is planned to use UTF-16 strings internally for non-ASCII input to
avoid re-encoding them like in the original C# implementation.

!!! note "This may change, in Rust version, we may investigate the tradeoff."

### Case Conversion

!!! info "In Windows, expect case insensitive paths."

We have to convert paths to uppercase inside various hooks.

!!! note "We choose uppercase because some languages e.g. greek have special rules for lowercase"

    This saves us from having to deal with those rules, improving performance.

#### Previous Implementation

In the C# implementation, we backported a `ToUpper` function from one of the .NET 8 Previews.
[Implementation Here][reloaded-memory-toupper]. (This function is faster than the one which
shipped in .NET 8 proper)

In said implementation, the code is optimized for 99% of the cases where the paths are pure
ASCII; with rare other cases falling to a slower implementation.

#### Rust Implementation

In Rust we can use the [make_ascii_uppercase][make-ascii-uppercase] function if we can trust
the paths to be ASCII for comparisons. Alternatively there's also functions like `to_uppercase`.

!!! note "We may want to copy out the implementation of `to_uppercase` to return result if string is ASCII"

    Rather than explicitly checking in another step, which is expensive.

These are not vectorised in the Rust source, but thanks to LLVM magic, they do get vectorised,
so there is generally no need to write our own. The `to_uppercase` function is generally limited
to unrolled SSE2, while `make_ascii_uppercase` will use rolled AVX2 if possible on CPU target.

### Hashing

!!! info "A hardware accelerated string hash function is used for file paths."

In the original C# implementation, this was a vectorized function which now lives here
[Reloaded.Memory String Hash][reloaded-memory-hash].

For the Rust implementation, it's recommended to use [AHash][ahash], it is the top performer
in the [smhasher][smhasher] benchmark suite for hashtables.

- All strings stored as Wide Strings.
    - Windows APIs use Wide Strings under the hood, even for ANSI APIs.
    - Therefore we save time by not having to widen them again.

### HashMaps

!!! info "HashMaps need to be able to query string slices."

In original C# implementation, it was necessary to use a custom dictionary that could query string
slices as keys, due to limitation of the built in one.

In Rust, this won't be needed; as thanks to the [Equivalent][equivalent] trait.
Hashbrown (Swisstable) is also faster.

### Memory Storage

!!! info "In the Rust implementation, we will pack strings together for efficiency."

In C#, some code was limited to the standard `String` type due to interoperability with
existing APIs. With some additional foresight and experience, we can do a bit better in Rust.

The idea is to use `string pooling` and custom string headers. Rather than having an allocation for
each string, we can perform a single memory allocation and then store all of the strings inline in
a single buffer.

```rust
// Pseudocode
pub struct StringEntry
{
    /// Truth Table for char_count_and_flag:
    ///
    /// | Bit Position (from LSB)        | 0 (IsAscii flag) | 1-15 (char_count)    |
    /// |--------------------------------|------------------|----------------------|
    /// | Value when ASCII               | 1                | ASCII char count     |
    /// | Value when non-ASCII (Windows) | 0                | UTF-16 char count    |
    /// | Value when non-ASCII (Unix)    | 0                | UTF-8 byte count     |
    ///
    /// - The least significant bit (LSB, position 0) is used as the `IsAscii` flag.
    ///   If it's 1, the string is ASCII. If it's 0, the string is non-ASCII.
    ///
    /// - The remaining 15 bits (positions 1-15) are used to store the character count.
    ///   If the string is ASCII, this is the count of ASCII characters.
    ///   If the string is non-ASCII, on Windows this is the count of UTF-16 characters,
    ///   and on Unix this is the count of UTF-8 bytes.
    char_count_and_flag: u16,

    // Inline in memory, right after header
    // Or u8 if using ANSI strings.
    data: u16[length]
}
```

String Widen is Cheap !!

### awa

!!! tip "And for `Hashbrown`'s low level [HashTable][hashtable] primitive."

```rust
pub struct TableEntry
{
    pub key: u64,
    pub value: &str
}

// To search (hash at minimum, as shown here)
table.find(KEY_HASH, |&val| val.key == KEY_HASH);
```

## Lookup Tree

!!! info "After creating the 'Redirection Tree' we create a 'Lookup Tree' for translating file paths"

[More details on both structures can be found in 'Implementation Details' section.][lookup-tree]

The `LookupTree` allows us to resolve file paths in O(3) time, at expense of some RAM.

[ahash]: https://github.com/tkaitchuck/aHash
[equivalent]: https://docs.rs/hashbrown/latest/hashbrown/trait.Equivalent.html
[lookup-tree]: ./Trees.md#lookup-tree
[make-ascii-uppercase]: https://github.com/rust-lang/rust/blob/80d1c8349ab7f1281b9e2f559067380549e2a4e6/library/core/src/num/mod.rs#L627
[original-impl]: https://github.com/Reloaded-Project/reloaded.universal.redirector/tree/rewrite-usvfs-read-features
[redirection-tree]: ./Trees.md#redirection-tree
[reloaded-memory-hash]: https://github.com/Reloaded-Project/Reloaded.Memory/blob/5d13b256c89ffa2b18bf430b6ef39925e4324412/src/Reloaded.Memory/Internals/Algorithms/UnstableStringHash.cs#L16
[smhasher]: https://github.com/rurban/smhasher
[reloaded-memory-toupper]: https://github.com/Reloaded-Project/Reloaded.Memory/blob/5d13b256c89ffa2b18bf430b6ef39925e4324412/src/Reloaded.Memory/Internals/Backports/System/Globalization/TextInfo.cs#L79
