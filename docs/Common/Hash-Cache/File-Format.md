The Hash Cache is stored in a binary file format for efficiency.
The file structure uses a structure of arrays approach for better compression.

## Notation

Assume any bit packed values are sequential, i.e. if `u4` then `u4` is specified, first `u4` is the `upper 4 bits`.

The file, including all packed fields is `little-endian`. It is written out when total number of
bits aligns with a power of 2.

- `u6` + `u12` is 2 bytes `little-endian`
- `u15` + `u17` is 4 bytes `little-endian`
- `u26` + `u22` + u16 is 8 bytes `little-endian`
- ***`u6` + `u11` + u17 is 4 bytes `little-endian`, not 2+2***

## File Layout

```
[Header]
[Partial Hashes Section]
[Full Hashes Section]
[Path Hashes Section]
[File Write Times Section]
[Paths Section] [Optional]
```

1. [**Header**](#header)
    - Describes the rest of the data in the file.

2. **Partial Hashes Section**
    - An array of `u64` values, each representing the [XXH3][hashing] hash of the first 4096 bytes (or whole file if smaller)
      for each file.

3. **Full Hashes Section**
    - An array of `u64` values, each representing the [XXH3][hashing] hash of the entire file for each file.

4. **Path Hashes Section**
    - An array of `u64` values, each representing the [XXH3][hashing] hash of the file path.
    - [File paths are sanitized.](#file-path-sanitization)

5. **Modify Times Section**
    - An array of `u64` values, each representing last write time of a file.
    - This uses the [Windows' FILETIME as the time stamp](#modify-time-format).

6. **Paths Section**
    - [Documented here.](#paths-section)

## Header

!!! info "The File Hash Cache begins with the following header."

Header (8 bytes):

- `u3`: Version Number
- `u5`: Flags
- `u24`: Number of Entries
- `u32`: Padding (Reserved)

!!! info "Current version is `0`"

### Bit Flags

Bits are in order `A0000`

- `A`: True if the `File Paths` section is present.

Other bits are currently unused.

## Modify Time Format

!!! info "This uses the Windows' [FILETIME][file-time] structure on all platforms."

This is the time in 100ns intervals since 12:00 A.M. January 1, 1601 Coordinated Universal Time (UTC).

The reasoning for using this on `nix` is a bit subtle. The native type on most `nix` systems is [timespec][timespec],
however this type can have inconsistent size. For example on 32-bit Linux systems it would likely be `8 bytes`,
and susceptible to the 2038 problem. On 64-bit systems it would be `16 bytes`; which is inconvenient for
space efficiency. etc.

Therefore we default to Windows' definition on all platforms.

```rust
// Constants for epoch difference and conversion
// EPOCH_DIFFERENCE is the number of seconds between the Windows epoch (1601-01-01)
// and the Unix epoch (1970-01-01)
const EPOCH_DIFFERENCE: i64 = 11_644_473_600;
const NANOS_PER_SEC: i64 = 1_000_000_000;
const WINDOWS_TICK: i64 = 100; // 100 nanoseconds

/// Converts a Unix timespec (seconds and nanoseconds) to a Windows timestamp
/// (100-nanosecond intervals since January 1, 1601 UTC)
///
/// This function handles both positive and negative timestamps, accounting for the difference
/// between Unix epoch (1970-01-01) and Windows epoch (1601-01-01).
///
/// Note: This function does not perform explicit overflow checks for performance reasons.
/// It should handle most practical timestamp values, but extreme values may cause overflow.
///
/// # Arguments
/// The unix timespec components.
///
/// * `seconds` - Signed seconds since Unix epoch (January 1, 1970)
/// * `nanoseconds` - Additional nanoseconds (always non-negative)
///
/// # Returns
///
/// The Windows timestamp as an i64 (FILETIME)
fn timespec_to_windows_timestamp(seconds: i64, nanoseconds: u32) -> i64 {
    // Convert seconds to Windows ticks
    let second_ticks = seconds * (NANOS_PER_SEC / WINDOWS_TICK);

    // Convert nanoseconds to Windows ticks
    let nano_ticks = (nanoseconds as i64) / WINDOWS_TICK;

    // Add epoch difference in ticks
    let epoch_diff_ticks = EPOCH_DIFFERENCE * (NANOS_PER_SEC / WINDOWS_TICK);

    // Combine all components
    second_ticks + nano_ticks + epoch_diff_ticks
}
```

On x86, this compiles down to around [7 instructions, without division][godbolt-time-conversion].
And around 11 on aarch64.

!!! warning "Above code is untested."

    But it should not overflow provided that the input values are within the bounds of Windows'
    timestamp format.

## Paths Section

!!! info "This section has the following layout"

    ```
    [Header]
    [Name Lengths Section]
    [Names Section]
    ```

The paths follow the [file path sanitization rules](#file-path-sanitization). They have no null terminators.

### Header

4 bytes:

- `u3`: Version Number
- `u5`: Flags
- `u24`: Compressed Size

The flags (`A0000`) for this section are:

- `A`: True if the [Name Lengths](#name-lengths-section) section uses `u16` instead of `u8`.

### Name Lengths Section

This is an array of path lengths in bytes expressed as `u8`(s).
(Or `u16` if the `A` flag [in header](#paths-section) is set)

Each array entry corresponds to a file at same index in previous sections.

So a value of 255 means the path is 255 bytes long.

### Names Section

This is a contiguous block of `UTF-8` encoded strings representing the relative paths of all files.
This block is compressed with `ZStd`, using single pass function, e.g. `ZSTD_compress` so decompressed
size is available in compressed payload.

## File Path Sanitization

!!! info "Each file path is sanitized using the following rules before being hashes."

1. Any trailing slashes are removed.
2. File paths are converted to upper case.
3. All slashes are forward slashes.

File paths are assumed to be case sensitive.

[hashing]: ../Hashing.md#hashing-algorithms
[file-time]: https://learn.microsoft.com/en-us/windows/win32/api/minwinbase/ns-minwinbase-filetime
[timespec]: https://www.gnu.org/software/libc/manual/html_node/Time-Types.html#index-struct-timespec
[godbolt-time-conversion]: https://godbolt.org/z/obrGYExYK