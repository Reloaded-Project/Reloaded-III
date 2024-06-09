# IPC Libraries

!!! info "Some binary size numbers for existing network based solutions for IPC."

    Note: A network based solution is needed for R3 because we need to communicate between
    a Wine client and the Linux host in some cases.

    Also a portable solution for those esoteric platforms, so ideally raw work over libc.

## Build Script

Build command for the solutions is

```bash
RUSTFLAGS="-C panic=abort -C lto=fat -C embed-bitcode=yes" cargo +nightly bloat -Z build-std=std,panic_abort -Z build-std-features=panic_immediate_abort --target x86_64-unknown-linux-gnu --profile profile
```

And the following `Cargo.toml`

```
# Profile Build
[profile.profile]
inherits = "release"
debug = true
codegen-units = 1
lto = true
strip = false  # No stripping!!

# Optimized Release Build
[profile.release]
codegen-units = 1
lto = true
strip = true  # Automatically strip symbols from the binary.
panic = "abort"
```

With an example specified, if available.

Use most slim example that talks client and server.
Use `-C linker-plugin-lto` when applicable.

## [ZeroMQ (libzmq Rust Bindings)](https://github.com/erickt/rust-zmq)

!!! error "A simple client-server has 500kB of code when built with minimum size settings."

    Automatic disqualification.

Also the cross-platform aspect is uncertain, for esoteric platforms without a guaranteed libc.


## [zmq.rs](https://github.com/zeromq/zmq.rs)

Same as the [native version above](#zeromq-libzmq-rust-bindings), builds to 1MiB by default,
but could potentially been brought down easily to 300-400KB by removing regex, and some other minor
things.

## [nanomsg-rs](https://github.com/thehydroimpulse/nanomsg.rs)

Builds with around 154KB of code. Mostly native C code.

Requires setting 'bundled' feature.

Portability with esoteric platforms is uncertain.

## [rust_tcp_ipc](https://github.com/voelklmichael/rust_tcp_ipc)

This is an ancient code base, so needed some fixing, as the built-in example
was commented out and out of date.

Once the example is fixed, we get the following for both client and server:

```
ile  .text    Size Crate
2.0%  41.8% 37.8KiB std
2.0%  40.6% 36.7KiB core
0.6%  12.5% 11.3KiB [Unknown]
0.1%   2.5%  2.2KiB alloc
0.1%   1.2%  1.1KiB rust_tcp_ipc
4.8% 100.0% 90.4KiB .text section size, the file size is 1.8MiB
```

```
0.6%  12.5% 11.3KiB    [Unknown] main
0.2%   4.8%  4.4KiB         core core::ops::function::FnOnce::call_once{vtable.shim}
0.2%   4.7%  4.2KiB         core <&T as core::fmt::Debug>::fmt
0.2%   4.3%  3.9KiB          std std::sync::mpmc::Sender<T>::send
0.2%   3.5%  3.2KiB         core core::ops::function::FnOnce::call_once{vtable.shim}
0.2%   3.4%  3.1KiB          std std::sync::mpmc::Sender<T>::send
0.2%   3.2%  2.9KiB          std std::sync::mpmc::Sender<T>::send
0.1%   2.9%  2.6KiB          std <str as std::net::socket_addr::ToSocketAddrs>::to_socket_addrs
0.1%   2.6%  2.3KiB         core <str as core::fmt::Debug>::fmt
0.1%   2.6%  2.3KiB         core <&T as core::fmt::Display>::fmt
0.1%   2.0%  1.8KiB         core core::ptr::drop_in_place<std::sync::mpsc::Receiver<reasonable_example::examp...
0.1%   1.9%  1.7KiB         core core::fmt::Formatter::pad
0.1%   1.9%  1.7KiB         core core::ptr::drop_in_place<std::sync::mpsc::Receiver<()>>
0.1%   1.9%  1.7KiB          std std::sync::mpmc::list::Channel<T>::read
0.1%   1.7%  1.5KiB          std std::sync::mpmc::zero::Channel<T>::send::{closure}
0.1%   1.6%  1.5KiB          std std::sync::mpmc::Receiver<T>::try_recv
0.1%   1.6%  1.5KiB          std std::sync::mpmc::zero::Channel<T>::send::{closure}
0.1%   1.6%  1.4KiB          std std::sync::mpmc::zero::Channel<T>::send::{closure}
0.1%   1.5%  1.3KiB         std? <std::sys_common::net::LookupHost as core::convert::TryFrom<(&str,u16)>>::tr...
0.1%   1.4%  1.3KiB          std <std::io::stdio::StdoutLock as std::io::Write>::write_all
0.1%   1.2%  1.1KiB rust_tcp_ipc rust_tcp_ipc::protocol_buffer::ProtocolBuffer<P>::process_new_buffer
0.1%   1.2%  1.0KiB          std std::sys::sync::once::futex::Once::call
0.1%   1.1%    999B         core <core::net::socket_addr::SocketAddr as core::fmt::Debug>::fmt
0.0%   1.0%    960B          std std::sync::mpmc::array::Channel<T>::send::{closure}
0.0%   1.0%    944B          std std::sync::mpmc::list::Channel<T>::recv::{closure}
0.0%   1.0%    925B         core core::net::parser::Parser::read_ipv4_addr
0.0%   1.0%    891B          std std::sync::mpmc::list::Channel<T>::start_recv
0.0%   0.9%    815B         core <core::str::pattern::CharSearcher as core::str::pattern::Searcher>::next_match
0.0%   0.8%    733B         core core::fmt::Formatter::pad_integral
0.0%   0.8%    720B          std std::sync::mpmc::zero::Channel<T>::disconnect
0.0%   0.8%    706B          std std::io::stdio::_print
0.0%   0.7%    624B          std std::sync::mpmc::waker::SyncWaker::notify
0.0%   0.6%    600B         core <core::fmt::builders::PadAdapter as core::fmt::Write>::write_str
0.0%   0.6%    591B          std std::io::buffered::bufwriter::BufWriter<W>::write_all_cold
0.0%   0.6%    566B         core core::ptr::drop_in_place<rust_tcp_ipc::tcp_ipc::TcpIpc<reasonable_example::e...
0.0%   0.6%    566B         core <&T as core::fmt::Debug>::fmt
0.0%   0.6%    543B          std std::sync::mpmc::list::Channel<T>::recv
0.0%   0.6%    530B         core core::fmt::write
0.0%   0.5%    508B         core core::net::parser::Parser::read_number
0.0%   0.5%    499B         core core::str::converts::from_utf8
0.0%   0.5%    494B         core core::fmt::num::<impl core::fmt::Debug for i32>::fmt
0.0%   0.5%    484B         core core::net::parser::Parser::read_ipv6_addr::read_groups
0.0%   0.5%    460B          std std::thread::park_timeout
0.0%   0.5%    445B          std std::sync::mpmc::waker::SyncWaker::disconnect
0.0%   0.5%    437B         core core::ptr::drop_in_place<std::sync::mpsc::Sender<reasonable_example::example...
0.0%   0.5%    433B         core core::ptr::drop_in_place<std::sync::mpsc::Sender<()>>
0.0%   0.5%    431B          std std::sys::pal::unix::stack_overflow::imp::make_handler
0.0%   0.5%    427B         core <core::str::lossy::Utf8Chunks as core::iter::traits::iterator::Iterator>::next
0.0%   0.5%    420B         core <&T as core::fmt::Debug>::fmt
0.0%   0.4%    407B          std std::sys::pal::unix::thread_local_dtor::register_dtor
0.0%   0.4%    386B          std std::sys::pal::unix::thread::Thread::new
0.0%   0.4%    384B          std std::sys::sync::once::futex::Once::call
0.0%   0.4%    369B          std std::sys::pal::common::small_c_string::run_with_cstr_allocating
0.0%   0.4%    366B          std std::sys::pal::unix::stack_overflow::imp::signal_handler
0.0%   0.4%    362B         core <core::net::ip_addr::Ipv4Addr as core::fmt::Display>::fmt
0.0%   0.4%    360B          std std::sys::sync::once::futex::Once::call
0.0%   0.4%    357B        alloc alloc::raw_vec::finish_grow
0.0%   0.4%    355B         core <&T as core::fmt::Debug>::fmt
0.0%   0.4%    354B         core <&T as core::fmt::Debug>::fmt
0.0%   0.4%    336B          std std::sys::sync::rwlock::futex::RwLock::read_contended
0.0%   0.4%    328B         core core::fmt::builders::DebugTuple::field
0.0%   0.3%    322B         core core::fmt::Write::write_char
0.0%   0.3%    307B          std std::thread::park
0.0%   0.3%    292B       alloc? <alloc::string::String as core::fmt::Write>::write_char
0.0%   0.3%    264B          std std::env::_var_os
0.0%   0.3%    264B         std? <std::io::Write::write_fmt::Adapter<T> as core::fmt::Write>::write_str
0.0%   0.3%    262B         core core::fmt::Write::write_char
0.0%   0.3%    262B         core core::fmt::num::imp::<impl core::fmt::Display for u32>::fmt
0.0%   0.3%    260B         core <core::result::Result<T,E> as core::fmt::Debug>::fmt
0.0%   0.3%    259B        alloc alloc::sync::Arc<T,A>::drop_slow
0.0%   0.3%    249B         core core::fmt::Write::write_char
0.0%   0.3%    249B         core core::fmt::Write::write_char
0.0%   0.3%    249B         core core::fmt::Write::write_char
0.0%   0.3%    249B         core core::fmt::Write::write_char
0.0%   0.3%    247B          std std::sys::sync::mutex::futex::Mutex::lock_contended
0.0%   0.3%    239B         core <&T as core::fmt::Debug>::fmt
0.0%   0.3%    238B          std std::sync::mpmc::context::Context::new
0.0%   0.2%    228B         core core::fmt::num::imp::<impl core::fmt::Display for u16>::fmt
0.0%   0.2%    217B          std std::io::error::Error::kind
0.0%   0.2%    215B         core core::fmt::Write::write_char
0.0%   0.2%    210B          std std::sys::sync::rwlock::futex::RwLock::wake_writer_or_readers
0.0%   0.2%    189B          std std::sys_common::thread_local_key::StaticKey::lazy_init
0.0%   0.2%    188B          std std::sys_common::thread_local_dtor::register_dtor_fallback::run_dtors
0.0%   0.2%    185B          std std::sys::pal::unix::time::Timespec::sub_timespec
0.0%   0.2%    170B        alloc alloc::raw_vec::RawVec<T,A>::grow_one
0.0%   0.2%    168B          std std::sys::pal::unix::thread::Thread::new::thread_start
0.0%   0.2%    168B          std std::thread::set_current
0.0%   0.2%    166B         core core::ptr::drop_in_place<core::result::Result<(reasonable_example::example_p...
0.0%   0.2%    163B          std std::sys::pal::unix::weak::DlsymWeak<F>::initialize
0.0%   0.2%    163B         core core::ptr::drop_in_place<std::sync::mpmc::waker::Waker>
0.0%   0.2%    158B          std std::io::error::Error::new
0.0%   0.2%    155B        alloc alloc::raw_vec::RawVec<T,A>::grow_one
0.0%   0.2%    150B          std std::io::error::Error::new
0.0%   0.2%    150B          std std::io::error::Error::new
0.0%   0.2%    149B        alloc alloc::raw_vec::RawVec<T,A>::reserve::do_reserve_and_handle
0.0%   0.2%    147B          std std::io::Write::write_fmt
0.0%   0.1%    137B         core core::fmt::num::imp::<impl core::fmt::Display for u8>::fmt
0.0%   0.1%    137B        alloc alloc::raw_vec::RawVec<T,A>::grow_one
0.0%   0.1%    134B         std? <std::io::Write::write_fmt::Adapter<T> as core::fmt::Write>::write_str
0.0%   0.1%    134B        alloc alloc::raw_vec::RawVec<T,A>::reserve::do_reserve_and_handle
0.1%   3.1%  2.8KiB              And 55 smaller methods. Use -n N to show more.
4.8% 100.0% 90.4KiB              .text section size, the file size is 1.8MiB
```

Getting good. Most of this is just monomorphisation and formatting, something like this can
easily be stripped down, maybe down to even 20KiB.

The underlying network library [mio][mio] is very portable and binds directly to libc.

## [message.io][message-io]

```
File  .text     Size             Crate Name
0.4%  11.5%  13.9KiB              core core::ops::function::FnOnce::call_once{vtable.shim}
0.4%  10.6%  12.8KiB         [Unknown] main
0.1%   2.5%   3.1KiB        message_io <message_io::network::driver::Driver<R,L> as message_io::network::driver::EventProcessor>::process
0.1%   2.2%   2.6KiB         multicast multicast::main::{closure}
0.1%   2.1%   2.5KiB             alloc alloc::collections::btree::remove::<impl alloc::collections::btree::node::Handle<alloc::collections::btr...
0.1%   1.9%   2.3KiB        message_io <message_io::network::driver::Driver<R,L> as message_io::network::driver::ActionController>::listen_with
0.1%   1.9%   2.3KiB             alloc <<alloc::boxed::Box<dyn core::error::Error+core::marker::Send+core::marker::Sync> as core::convert::From...
0.1%   1.8%   2.2KiB         hashbrown hashbrown::raw::RawTable<T,A>::reserve_rehash
0.1%   1.6%   2.0KiB        message_io <message_io::network::driver::Driver<R,L> as message_io::network::driver::ActionController>::connect_with
0.1%   1.5%   1.9KiB        message_io <message_io::network::driver::Driver<R,L> as message_io::network::driver::EventProcessor>::process
0.1%   1.4%   1.7KiB              core core::fmt::Formatter::pad
0.1%   1.4%   1.7KiB crossbeam_channel crossbeam_channel::select::run_select::{closure}
0.1%   1.4%   1.7KiB        message_io <message_io::network::driver::Driver<R,L> as message_io::network::driver::ActionController>::listen_with
0.1%   1.4%   1.6KiB              core core::ptr::drop_in_place<crossbeam_channel::channel::Receiver<std::time::Instant>>
0.1%   1.3%   1.6KiB        message_io message_io::network::transport::Transport::mount_adapter
0.1%   1.3%   1.6KiB              core core::ptr::drop_in_place<message_io::events::EventReceiver<()>>
0.0%   1.3%   1.5KiB crossbeam_channel crossbeam_channel::flavors::list::Channel<T>::read
0.0%   1.2%   1.5KiB crossbeam_channel <crossbeam_channel::channel::Receiver<T> as crossbeam_channel::select::SelectHandle>::register
0.0%   1.2%   1.5KiB crossbeam_channel <crossbeam_channel::channel::Receiver<T> as crossbeam_channel::select::SelectHandle>::register
0.0%   1.2%   1.5KiB              core core::ops::function::FnOnce::call_once{vtable.shim}
1.8%  47.8%  57.9KiB                   And 184 smaller methods. Use -n N to show more.
3.8% 100.0% 121.2KiB                   .text section size, the file size is 3.1MiB
```

The `multicast` example, with TCP (minor code edits required).

A bit too heavy, but this would be great for adding multiplayer to a game inside a mod.

## Conclusion

!!! info "Reloaded's IPC requirements are extremely minimal"

But everything is way too overkill, either in functionality or in binary size.

Build your own TCP based IPC, with mio. It's the most portable and the smallest.
We're talking extremely barebones, single thread per client, small stack

[mio]: https://github.com/tokio-rs/mio.git
[message-io]: https://github.com/lemunozm/message-io/