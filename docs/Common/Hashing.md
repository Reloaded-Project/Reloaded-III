# Hashing Algorithms

!!! info "An overview of the recommended hash algorithms for various use cases in Reloaded3."

## Unstable Hashing for Small Data

!!! info "'Unstable' meaning, the hash may be different across different machines or versions."

    i.e. These hashes are never persisted anywhere.

For hashing small data (less than 128 bytes), such as dictionary keys or short strings, we use [AHash][ahash].

This is a high performance hash algorithm designed for hash tables.
It has been chosen based on its performance in the [smhasher][smhasher] and [smhasher3][smhasher3] benchmark suites.

It uses AES-NI hardware accelerated instructions for high performance on modern CPUs.

## Stable Hashing for Large Data with Many Files

!!! info "For when you need to persist hashes and there may be millions of files."

    Or when you have some space to waste.

For this Reloaded3 uses [XXH128][xxh3].

XXH128 is an insanely fast non-cryptographic hash algorithm utilising SIMD instructions for
high performance on modern CPUs. It approaches RAM speed limits.

!!! tip "When used with hash tables (`hashbrown`) we truncate this to 64-bits."

    Also known as `xxh128low`. We check the full hash during the equality check.

## Stable Hashing for General-Purpose Use

!!! info "For any other use cases."

For general-purpose hashing scenarios that don't fall into the above categories, we recommend using
[XXH3][xxh3].

XXH3 is a variant of XXH128 that produces a 64-bit hash value. It offsets the same
characteristics as XXH128 but is recommended when the number of file hashes is not expected to be
that big.

## Rationale

- AHash for small data:
    - Designed specifically for hash tables and optimized for performance.
    - Pretty much #1 in hash table benchmarks.
    - Provides good distribution and collision resistance for small data within a single run.

- XXH128 for large data with many files:
    - Extremely fast performance, optimized for modern CPUs.
    - Stable hash function, ensuring consistent hash values across runs and versions.
    - Suitable for file integrity checks, caching, and deduplication scenarios.

- XXH3 for general-purpose use:
    - Variant of XXH128 that produces a 64-bit hash value.
    - Offers the same stability and performance characteristics as XXH128.
    - More suitable when there's less hashes to go around.

The recommendations provided here are based on general best practices and the needs of Reloaded3.
When choosing a hash algorithm, consider the specific requirements of your use case, such as data
size, stability, and performance.

!!! info "Reloaded3 does not currently utilize cryptographic hashing algorithms"

    The focus is on performance and general-purpose use cases rather than cryptographic security.

## Additional Content

- [Collisions Tester][collision-tester]: A brute force program to test hash functions for collisions.
- [SMHasher3][smhasher3]: A fork of the original SMHasher with more tests and better support for modern CPUs.
- [SMHasher][smhasher]: A comprehensive test suite for hash functions.

[ahash]: https://docs.rs/ahash
[collision-tester]: https://fossies.org/linux/xxHash/tests/collisions/README.md
[smhasher]: https://github.com/rurban/smhasher
[smhasher3]: https://gitlab.com/fwojcik/smhasher3
[xxh3]: https://github.com/Cyan4973/xxHash