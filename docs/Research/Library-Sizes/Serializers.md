# Serialization Solutions

!!! info "Binary size used by various serialization solutions."

[Full Git Repo with Random Lib Tests](https://github.com/Reloaded-Project/Reloaded-III/files/14900675/postcard_test.zip)

Sample data used:

```rust
#![feature(optimize_attribute)]

extern crate alloc;
use std::io::{prelude::Read, Cursor};

use byteorder::{LittleEndian, ReadBytesExt};
use rkyv::{Archive, Deserialize, Serialize};

#[derive(Archive, Deserialize, Serialize, Debug, Eq, PartialEq)]
struct Credit {
    name: String,
    role: String,
    url: Option<String>,
}

#[derive(Archive, Deserialize, Serialize, Debug, Eq, PartialEq)]
struct UpdateInfo {
    item_type: String,
    item_id: u32,
}

#[derive(Archive, Deserialize, Serialize, Debug, Eq, PartialEq)]
struct DependencyInfo {
    id: String,
    name: String,
    author: String,
    // Additional fields for UpdateData can be added here
}

#[derive(Archive, Deserialize, Serialize, Debug, Eq, PartialEq)]
struct GalleryItem {
    file_name: String,
    caption: Option<String>,
}

#[derive(Archive, Deserialize, Serialize, Debug, Eq, PartialEq)]
struct PackageConfig {
    id: String,
    name: String,
    summary: String,
    author: String,
    docs_file: Option<String>,
    version: String,
    tags: Vec<String>,
    source_url: Option<String>,
    project_url: Option<String>,
    published: String,
    icon: String,
    is_library: bool,
    supported_games: Vec<String>,
    credits: Vec<Credit>,
    update_data: UpdateInfo,
    dependencies: Vec<DependencyInfo>,
    gallery: Vec<GalleryItem>,
    // Additional fields for Targets can be added here
}

#[no_mangle]
pub extern "C" fn deserialize_package_config(data: &[u8]) -> PackageConfig {
    let archived = unsafe { rkyv::archived_root::<PackageConfig>(data) };
    archived.deserialize(&mut rkyv::Infallible).unwrap()
}
```

## Observations

- Most solutions, which based on `serde` tend to introduce varying levels of code bloat.
    - This is unfortunately not always serde's fault, but just something that happens.

## Manual (Unoptimized)

```
21.7%  55.0% 2.1KiB     [Unknown] deserialize_package_config
 6.4%  16.2%   633B postcard_test postcard_test::deserialize_string
 2.2%   5.5%   213B         alloc alloc::raw_vec::finish_grow
 1.9%   4.7%   185B         alloc alloc::raw_vec::RawVec<T,A>::grow_one
 1.9%   4.7%   185B         alloc alloc::raw_vec::RawVec<T,A>::grow_one
 1.9%   4.7%   184B         alloc alloc::raw_vec::RawVec<T,A>::grow_one
 0.9%   2.3%    89B postcard_test postcard_test::deserialize_option_string
 0.5%   1.4%    54B     [Unknown] __rust_alloc
 0.0%   0.0%     1B           std std::sys::pal::unix::args::imp::ARGV_INIT_ARRAY::init_wrapper
 0.0%   0.0%     0B               And 0 smaller methods. Use -n N to show more.
39.5% 100.0% 3.8KiB               .text section size, the file size is 9.6KiB
```

With optimization, should pretty much match rkyv; but with copying.
Except for extra drop/grow vector.

## [Rkyv][rkyv]

!!! info "[rkyv][rkyv] is by far the winner."

    It's pretty much on par with manual deserialization by hand.

```
35.2%  88.8% 2.8KiB [Unknown] deserialize_package_config
 1.2%   3.1%   100B     alloc alloc::slice::<impl alloc::borrow::ToOwned for [T]>::to_owned
 0.7%   1.7%    54B [Unknown] __rust_alloc
 0.0%   0.0%     1B       std std::sys::pal::unix::args::imp::ARGV_INIT_ARRAY::init_wrapper
 0.0%   0.0%     0B           And 0 smaller methods. Use -n N to show more.
39.7% 100.0% 3.2KiB           .text section size, the file size is 8.0KiB
```

!!! note "Drop does not show up here because rkyv uses custom collection types"

    And the actual data is sourced from the buffer storing the data.

## [Postcard][postcard]

Postcard is quite alright.

Some deserialization logic is inlined adding to code size but that's within expectation.

```
39.0%  68.2% 5.6KiB [Unknown] deserialize_package_config
 4.5%   7.8%   657B     serde serde::de::impls::<impl serde::de::Deserialize for alloc::string::String>::deserialize
 4.2%   7.3%   615B     serde serde::de::SeqAccess::next_element
 1.4%   2.5%   213B     alloc alloc::raw_vec::finish_grow
 1.3%   2.2%   185B     alloc alloc::raw_vec::RawVec<T,A>::grow_one
 1.3%   2.2%   185B     alloc alloc::raw_vec::RawVec<T,A>::grow_one
 1.3%   2.2%   184B     alloc alloc::raw_vec::RawVec<T,A>::grow_one
 1.0%   1.8%   152B      core core::ptr::drop_in_place<alloc::vec::Vec<postcard_test::Credit>>
 0.9%   1.5%   126B      core core::ptr::drop_in_place<alloc::vec::Vec<postcard_test::DependencyInfo>>
 0.6%   1.1%    94B      core core::ptr::drop_in_place<alloc::vec::Vec<alloc::string::String>>
 0.4%   0.6%    54B [Unknown] __rust_alloc
 0.0%   0.0%     1B       std std::sys::pal::unix::args::imp::ARGV_INIT_ARRAY::init_wrapper
 0.0%   0.0%     0B           And 0 smaller methods. Use -n N to show more.
57.2% 100.0% 8.2KiB           .text section size, the file size is 14.4KiB
```

## [Bincode][bincode]

Bincode somehow brought `core::fmt` along.

```
 File  .text    Size     Crate Name
18.5%  37.0%  4.7KiB [Unknown] deserialize_package_config
 6.3%  12.6%  1.6KiB     alloc <<alloc::boxed::Box<dyn core::error::Error+core::marker::Sync+core::marker::Send> as core::...
 3.7%   7.5%    975B     alloc <<alloc::boxed::Box<dyn core::error::Error+core::marker::Sync+core::marker::Send> as core::...
 3.1%   6.3%    822B     serde serde::de::impls::<impl serde::de::Deserialize for alloc::string::String>::deserialize
 2.8%   5.5%    724B      core core::fmt::num::imp::<impl core::fmt::Display for u64>::fmt
 2.0%   4.1%    533B     alloc core::fmt::Write::write_fmt
 1.7%   3.5%    451B     serde serde::de::SeqAccess::next_element
 0.9%   1.9%    246B     serde serde::de::Error::invalid_length
 0.9%   1.7%    228B    alloc? <alloc::string::String as core::fmt::Write>::write_char
 0.8%   1.6%    213B     alloc alloc::raw_vec::finish_grow
 0.7%   1.4%    185B     alloc alloc::raw_vec::RawVec<T,A>::grow_one
 0.7%   1.4%    185B     alloc alloc::raw_vec::RawVec<T,A>::grow_one
 0.7%   1.4%    184B     alloc alloc::raw_vec::RawVec<T,A>::grow_one
 0.6%   1.3%    165B      core core::unicode::printable::check
 0.6%   1.3%    164B      core core::char::EscapeUnicode::new
 0.6%   1.2%    152B      core core::ptr::drop_in_place<alloc::vec::Vec<postcard_test::Credit>>
 0.6%   1.1%    145B     alloc alloc::raw_vec::RawVec<T,A>::grow_amortized
 0.5%   1.0%    126B      core core::ptr::drop_in_place<alloc::vec::Vec<postcard_test::DependencyInfo>>
 0.4%   0.9%    114B     alloc alloc::raw_vec::RawVec<T,A>::try_allocate_in
 0.4%   0.9%    112B      core core::fmt::Formatter::padding
 2.5%   5.0%    658B           And 16 smaller methods. Use -n N to show more.
49.9% 100.0% 12.8KiB           .text section size, the file size is 25.5KiB
```

## [Bitcode](https://github.com/SoftbearStudios/bitcode)

```
13.4%  23.9%  3.4KiB [Unknown] deserialize_package_config
12.5%  22.4%  3.2KiB   bitcode bitcode::derive::decode_inline_never
 4.2%   7.6%  1.1KiB   bitcode <bitcode::length::LengthDecoder as bitcode::coder::View>::populate
 3.4%   6.0%    878B   bitcode <bitcode::str::StrDecoder as bitcode::coder::View>::populate
 2.0%   3.7%    533B      core core::fmt::write
 1.9%   3.3%    486B   bitcode <bitcode::derive::option::OptionDecoder<T> as bitcode::coder::View>::populate
 1.8%   3.3%    476B   bitcode std::sys::thread_local::fast_local::Key<T>::try_initialize
 1.8%   3.2%    471B      core core::ptr::drop_in_place<postcard_test::_::PackageConfigDecoder>
 1.2%   2.2%    325B   bitcode bitcode::pack::unpack_bytes
 1.1%   1.9%    281B   bitcode bitcode::pack::unpack_arithmetic
 1.1%   1.9%    281B   bitcode bitcode::pack::unpack_arithmetic
 0.9%   1.6%    234B   bitcode bitcode::pack::unpack_arithmetic
 0.9%   1.6%    232B   bitcode bitcode::pack::unpack_arithmetic
 0.8%   1.5%    213B     alloc alloc::raw_vec::finish_grow
 0.8%   1.4%    199B   bitcode bitcode::pack::unpack_arithmetic
 0.7%   1.3%    191B       std std::sys_common::thread_local_key::StaticKey::key
 0.7%   1.3%    188B       std core::fmt::Write::write_char
 0.7%   1.2%    175B       std <std::io::Write::write_fmt::Adapter<T> as core::fmt::Write>::write_str
 0.6%   1.1%    166B       std alloc::raw_vec::RawVec<T,A>::grow_one
 0.6%   1.1%    164B     alloc alloc::vec::Vec<T,A>::reserve
 4.0%   7.1%  1.0KiB           And 17 smaller methods. Use -n N to show more.
55.9% 100.0% 14.3KiB           .text section size, the file size is 25.5KiB
```

Bitcode might have a lot of code, but it has a cool benefit that it's very compression friendly.

The data is laid out in a way that benefits lossless compression.

Bit of a bummer, `core::fmt` got involved, but aside from that, this would actually scale well with
more structures to serialize, since a lot of the logic is lifted out to the methods.

## Takeaways

### It's mostly Monomorphization

For example:

- `alloc::raw_vec::RawVec<T,A>::grow_one`
- `core::ptr::drop_in_place<alloc::vec::Vec<T>>`

Commonly see multiple implementation.

!!! note "It might be possible to contribute to the `standard library` to improve this."

Technically speaking the code shouldn't differ much, you're growing or deallocing an
X number of bytes.

The generics could be pointed at a shared implementation using `u8` as the type, like malloc/free
in C. Though it may incur an additional jmp instruction of overhead.

### Use `rkyv` for serializing read-only data.

It performs the best in deserialization and has the smallest binary size.

An example of where using `rkyv` is suitable therefore is for saving loader settings from the
server.

### Use `bitcode` for serializing data where copy may be beneficial

It's a bit heavier on code size than `rkyv` but tends to
serialize structured data faster, and it's very compression friendly.

A good usage for a library like `bitcode` is for serializing loadout `snapshots` that require
mutating *after* they are loaded.

[rkyv]: https://rkyv.org/motivation.html
[postcard]: https://github.com/jamesmunns/postcard
[bincode]: https://github.com/bincode-org/bincode