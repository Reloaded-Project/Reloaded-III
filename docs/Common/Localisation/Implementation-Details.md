# Parsing & Implementation Details

!!! info "To quickly parse this file, do it in a linear fashion."

    In other words, don't split the string by NewLine

Parsing of this file can be done quickly by making clever knowledge of UTF-8 and SIMD.

Note the UTF-8 encoding table:

|  Code point range  |  Byte 1  |  Byte 2  |  Byte 3  |  Byte 4  | Code points |
|:------------------:|:--------:|:--------:|:--------:|:--------:|:-----------:|
|  U+0000 - U+007F   | 0xxxxxxx |          |          |          |     128     |
|  U+0080 - U+07FF   | 110xxxxx | 10xxxxxx |          |          |    1920     |
|  U+0800 - U+FFFF   | 1110xxxx | 10xxxxxx | 10xxxxxx |          |    61440    |
| U+10000 - U+10FFFF | 11110xxx | 10xxxxxx | 10xxxxxx | 10xxxxxx |   1048576   |

Each character in the ASCII range `U+0000 - U+007F` can't be the final byte of a multi-byte
character. Therefore we can efficiently search for characters like `0x0A` (newline) and `0x23` (`#`),
rather than having to parse character by character.

## Fast Finding Keys

!!! tip "Number of keys can be very quickly determined with the use of SIMD."

The idea is the following:

- Match a repeated pattern of `\n[[`

- MoveMask the result
    - If result is 0, no match. Skip to next `<REGISTER_LENGTH> - 3` bytes.

- If result is not zero, keep shift by number of trailing zeroes.
    - Check if `111` (all bytes match). If not, shift by 3 and repeat till result 0.

Untested Pseudocode:

```
function FastFindKeys(data):
    simd_register = LoadSIMDRegister("\n[[")
    i = 0
    while i < length(data) - (REGISTER_LENGTH - 1):
        substring = data[i : i + REGISTER_LENGTH]
        comparison = CompareStringSIMD(substring, simd_register)
        mask = MoveMask(comparison)

        if mask == 0:
            i += REGISTER_LENGTH
        else:
            while mask != 0:
                trailing_zeroes = CountTrailingZeroes(mask)
                i += trailing_zeroes

                if (mask & 0b111) == 0b111:
                    # Found a key at index i
                    ProcessKey(data, i)
                    # Move past the found pattern.
                    i += 3
                    break

                # Else if not all match, shift to next bit.
                # On next loop, we'll try from first match again
                mask >>= 1
                i += 1

    # Process remaining data (less than REGISTER_LENGTH) using a non-SIMD approach
    # ...
```

## Fast Value Lookup

!!! tip "We can accelerate looking up values by looking up the hash of the key."

    This is done by computing the hash of every key at compile time, and looking up
    the value by key at runtime.

    Requirements:

    - Endian Agnostic
    - Stable/Same Hash
    - Fast

The standard implementation will do this with [xxh3][xxh3], which was chosen based
on [smhasher][smhasher] & [smhasher3][smhasher3] results.

In almost all most cases, the number of keys should be small enough such that we can reasonably
expect that there will never be a hash collision between 2 keys.

Chances are most translation files will have <100 keys, and bigger projects <1000 keys.

!!! warning "In the rare event a hash collision technically exists..."

    The library should first error out during the parse process.
    And the user should rename the new colliding variable.

### Implementing This

!!! tip "The trick in Rust is to use `Hashbrown`'s [HashTable][hashtable]."

You could store every localizable string as such:

```rust
pub struct TableEntry
{
    pub key: u64,
    pub value: &str
}
```

And query with:

```rust
table.find(KEY_HASH, |&val| val.key == KEY_HASH);
```

Now we just did a hash-only value fetch.

## Memory Layout Recommendation

!!! info "An implementing library may perform fast formats by caching some data."

To maximize perf and minimize memory usage, implementations here should prefer to do a copy
approach rather than a zero-copy approach.

Sum up the size of all strings. Perform a `malloc`, and copy the strings to the new buffer.

In the elements inside `TableEntry` above, can then point to the unified buffer.

!!! note

    While this will mean slightly increased parse time, it will also mean that long term, operations
    will be more efficient and less memory will be used.

<!-- Links -->
[hashtable]: https://docs.rs/hashbrown/latest/hashbrown/struct.HashTable.html#method.find
[smhasher]: https://github.com/rurban/smhasher?tab=readme-ov-file
[smhasher3]: https://gitlab.com/fwojcik/smhasher3
[xxh3]: https://github.com/Cyan4973/xxHash