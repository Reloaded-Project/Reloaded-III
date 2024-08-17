!!! info "This page provides more info on [Microarchitecture Levels][microarchitecture-levels] in Reloaded3."

## Determining Supported Instruction Set on Local Machine

Start with [core-detect][core-detect] crate, and make a separate library with helper methods to
determine which category the current CPU falls under.

You can use `rustc --print=cfg -C target-cpu=x86-64-v3` to print the specific `target_feature`(s)
available to a CPU.

## Emulating Instruction Sets for x86 (32-bit) Targets

!!! warning "x86-64-v* don't have equivalents for 32-bit targets in LLVM."

    But we can derive them!

To derive them, use the Rust compiler like so `rustc --print=cfg -C target-cpu=x86-64-v4`.
This will print a list of details for the target, alongside, most importantly, ***target features***.

!!! example "Example for x86-64-v2"

    ```
    target_feature="avx"
    target_feature="avx2"
    target_feature="avx512bw"
    target_feature="avx512cd"
    target_feature="avx512dq"
    target_feature="avx512f"
    target_feature="avx512vl"
    ```

From there, we have to filter out features which are not available in 32-bit mode.

- `avx512bw`, `avx512cd`, `avx512dq`, `avx512f`, `avx512vl`: These AVX-512 extensions are 64-bit only.
- `cmpxchg16b`: This extension is only available in 64-bit mode. May be possible to use in 32-bit programs but atomic read/write of 128-bit values is not guaranteed in 32-bit mode.

Therefore we can derive the following:

| Type   | Name   | Features                                                                       |
| ------ | ------ | ------------------------------------------------------------------------------ |
| string | x86-v2 | `fxsr` `lahfsahf` `popcnt` `sse` `sse2` `sse3` `sse4.1` `sse4.2` `ssse3`       |
| string | x86-v3 | all previous + `avx` `avx2` `bmi1` `bmi2` `f16c` `fma` `lzcnt` `movbe` `xsave` |

The microarch level `i686-v4` is redundant, because all new features in `x86-64-v4` are not
supported in 32-bit mode.

These features come from LLVM, so can also be used with Clang, etc.


[core-detect]: https://docs.rs/core_detect/latest/core_detect/
[microarchitecture-levels]: https://en.wikipedia.org/wiki/X86-64#Microarchitecture_levels