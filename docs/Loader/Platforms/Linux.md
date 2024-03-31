# Linux

!!! note "Wine is covered under [Windows](./Windows.md)."

!!! question "This May be Improved"

    Native Linux games are not often modded.<br/>
    There may be some better methods to do the things here.

!!! info

    This will be implemented when the need to support a cross-platform game arises. Always open for PRs 💜.

## Bootstrapping

Covered in [Linux Preload Bootloader](../../Research/Bootloaders/Linux-Preload.md).

## Native Mods with Dynamic Linking

Basically N/A. 

Almost nobody has been modding native Linux games before, aside some cross platform titles.

## Crash Handler & Process Exit Hook

!!! warning

    Assume the user does not have any sort of crash dump/error reporting enabled.
    We must generate dumps ourselves when our process dies.

```rust
use libc::{c_int, c_void, sigaction, siginfo_t, SIGSEGV, SA_SIGINFO};

extern "C" fn crash_handler(sig: c_int, info: *mut siginfo_t, _ucontext: *mut c_void) {
    let signal_name = match sig {
        SIGSEGV => "SIGSEGV",
        SIGABRT => "SIGABRT",
        SIGILL => "SIGILL",
        SIGFPE => "SIGFPE",
        SIGBUS => "SIGBUS",
        SIGSYS => "SIGSYS",
        _ => "Unknown",
    };

    // Generate a crash dump or perform any necessary logging
    // ...

    // Optionally, you can exit the process here
    // std::process::exit(1);
}
```

And register it elsewhere:

```rust
unsafe {
    // Run custom crash handler on equivalent of a Windows 'Access Violation'.
    let mut action: sigaction = core::mem::zeroed();
    action.sa_sigaction = crash_handler as usize;
    action.sa_flags = SA_SIGINFO;
    sigaction(SIGSEGV, &action, core::ptr::null_mut());
}
```

Signals Quick Reference:

- `SIGSEGV`: Basically `Bad Memory Read/Write`.
- `SIGABRT`: Called by `abort()` or on fatal error.
- `SIGILL`: Called when bad instruction executed.
- `SIGFPE`: Called on bad arithmetic, e.g. Division by 0.
- `SIGBUS`: Called on memory read misalign usually.
- `SIGSYS`: Called on bad system call.

Others (Know but don't handle these):

- `SIGTRAP`: Called on breakpoint.

## Console

!!! warning "This is extremely tricky, and options aren't very good."

Traditionally if you want terminal output, you should simply start your
program in a terminal emulator. That may not always be possible, however.

Here's some known options for console output below.

### Adjusting External Launcher Configurations

!!! info "We adjust external launcher start options to run the game in a terminal emulator."

!!! tip "Start Here!"

Sometimes it's possible to get the game to boot with a terminal by adjusting the configuration
of an external launcher.

Say for instance, an older Linux game may need to be launched via the Steam Linux Runtime to run 
at all on a modern distro.

For Steam this can be solved by overwriting `Launch Options`:

```
alacritty -e %command%
```

This spawns the game with its `stdout` in alacritty.

!!! warning "The Problem with This Approach"

    You have no idea how the user will want to run their game. They may run it through Steam,
    through some other Launcher, or even through a script. God knows.

### Emulating AllocConsole on Linux

!!! info "Alternative Solution: Can we spawn a terminal and pass stdout/stdin/stderr via it?"

A [useful blog post](https://poor.dev/blog/terminal-anatomy/).<br/>
Another [useful blog post](https://stackoverflow.com/a/65377109).

With `xterm` or a terminal that allows you to specify a pseudoterminal, you
can do it like this:

```rust
use std::env;
use std::ffi::CString;
use std::fs::File;
use std::io::{self, Read, Write};
use std::os::unix::io::{AsRawFd, FromRawFd, IntoRawFd};
use std::process::Command;

fn main() {
    // Example ptname_str: "/dev/pts/3"
    // xterm: "xterm -S{}/{} &"

    // Open a pseudo terminal
    let pt = unsafe { libc::posix_openpt(libc::O_RDWR) };
    if pt == -1 {
        eprintln!("Could not open pseudo terminal.");
        std::process::exit(1);
    }

    // Get the pseudo terminal device name
    let ptname = unsafe { libc::ptsname(pt) };
    if ptname.is_null() {
        eprintln!("Could not get pseudo terminal device name.");
        unsafe { libc::close(pt) };
        std::process::exit(1);
    }

    // Unlock the pseudo terminal
    if unsafe { libc::unlockpt(pt) } == -1 {
        eprintln!("Could not unlock pseudo terminal.");
        unsafe { libc::close(pt) };
        std::process::exit(1);
    }

    // Convert pseudo terminal device name to a string
    let ptname_str = unsafe { CString::from_raw(ptname).into_string().unwrap() };

    // Spawn the xterm process
    let xterm_cmd = format!(
        "xterm -S{}/{} &",
        &ptname_str[ptname_str.rfind('/').unwrap() + 1..],
        pt
    );
    let _ = Command::new("sh").arg("-c").arg(&xterm_cmd).spawn();

    // Open the pseudo terminal device
    let mut xterm_file = unsafe { File::from_raw_fd(libc::open(ptname, libc::O_RDWR)) };

    // Wait for xterm to start
    let mut buf = [0; 1];
    while buf[0] != b'\n' {
        xterm_file.read_exact(&mut buf).unwrap();
    }
    
    // Redirect standard output and error to the pseudo terminal
    let stdout_fd = io::stdout().as_raw_fd();
    let stderr_fd = io::stderr().as_raw_fd();
    if unsafe { libc::dup2(pt, stdout_fd) } < 0 {
        eprintln!("Could not redirect standard output.");
        unsafe { libc::close(pt) };
        std::process::exit(1);
    }
    if unsafe { libc::dup2(pt, stderr_fd) } < 0 {
        eprintln!("Could not redirect standard error output.");
        unsafe { libc::close(pt) };
        std::process::exit(1);
    }

    // Print to the xterm
    println!("This should appear on the xterm.");
    eprintln!("So should this.");

    // Wait for user input
    io::stdin().read_exact(&mut buf).unwrap();

    // Close the pseudo terminal
    unsafe { libc::close(pt) };
}
```

This gets us the behaviour of Windows' AllocConsole on Linux, but unfortunately not all terminal
emulators allow us to specify a custom pseudoterminal. 

#### Emulating AllocConsole (Alternative Method)

!!! info "This is essentially what software like `screen` and `tmux` do."

We can write a program that passes messages to/from a specified pseudoterminals
and then run that inside the user's terminal emulator.

Here's an example with `tio`:

```rust
use std::ffi::CString;
use std::io;
use std::os::unix::prelude::AsRawFd;
use std::process::Command;

use libc::{sleep, tcgetattr, tcsetattr, termios, TCSANOW};

fn main() {
    // Open a pseudo terminal
    let pt = unsafe { libc::posix_openpt(libc::O_RDWR) };
    if pt == -1 {
        eprintln!("Could not open pseudo terminal.");
        std::process::exit(1);
    }

    // Get the pseudo terminal device name
    let ptname = unsafe { libc::ptsname(pt) };
    if ptname.is_null() {
        eprintln!("Could not get pseudo terminal device name.");
        unsafe { libc::close(pt) };
        std::process::exit(1);
    }

    // Unlock the pseudo terminal
    if unsafe { libc::unlockpt(pt) } == -1 {
        eprintln!("Could not unlock pseudo terminal.");
        unsafe { libc::close(pt) };
        std::process::exit(1);
    }

    // Convert pseudo terminal device name to a string
    let ptname_str = unsafe { CString::from_raw(ptname).into_string().unwrap() };

    // Configure terminal settings
    // If we ever use something different than 'tio'.
    // We enable ONLCR to ensure newline characters also move cursor left when sending commands back.
    // We enable OPOST to ensure output processing is enabled.
    // We enable INLCR to ensure messages sent from host/parent wrap.
    /*
    unsafe {
        let mut termios = std::mem::zeroed::<termios>();
        tcgetattr(pt, &mut termios);
        termios.c_oflag |= libc::ONLCR | libc::OPOST;
        termios.c_iflag |= libc::INLCR; | libc::ICRNL; // Can you combine these?
        tcsetattr(pt, TCSANOW, &termios);
    }
    */

    // Spawn the screen process
    // https://github.com/tio/tio
    let _ = Command::new("alacritty")
        .arg("-e")
        .arg("tio")
        .arg("--mute") // Don't display tio header.
        .arg("-m")
        .arg("INLCRNL") // make sure cursor wraps to start on newline
        .arg(ptname_str.as_str())
        .spawn();

    // Wait for screen to spawn and connect
    // TODO: Find a decent way to do this.
    unsafe {
        sleep(5);
    }

    // Redirect standard output and error to the pseudo terminal
    let stdout_fd = io::stdout().as_raw_fd();
    let stderr_fd = io::stderr().as_raw_fd();
    if unsafe { libc::dup2(pt, stdout_fd) } < 0 {
        eprintln!("Could not redirect standard output.");
        unsafe { libc::close(pt) };
        std::process::exit(1);
    }
    if unsafe { libc::dup2(pt, stderr_fd) } < 0 {
        eprintln!("Could not redirect standard error output.");
        unsafe { libc::close(pt) };
        std::process::exit(1);
    }

    // Print to the screen terminal
    println!("This should appear on the screen terminal.");
    eprintln!("So should this.");
    unsafe {
        sleep(1);
    }

    // Close the pseudo terminal
    // unsafe { libc::close(pt) };
}
```

This seems to work fine.

!!! warning "This example code introduces a lot of binary bloat."

    `Command::new().arg()` pulls in a whole `btree` and `core::fmt`.

    These amount to ~35kB of binary size. Unacceptable for Reloaded's loader.

To better match Reloaded conventions, write it like this:

```rust
// Convert pseudo terminal device name to a C string
let ptname_cstr = unsafe { CStr::from_ptr(ptname) };

// Construct the tio command as a C string array
let tio_cmd = [
    "alacritty\0".as_ptr() as *const i8,
    "-e\0".as_ptr() as *const i8,
    "tio\0".as_ptr() as *const i8,
    "--mute\0".as_ptr() as *const i8,
    "-m\0".as_ptr() as *const i8,
    "INLCRNL\0".as_ptr() as *const i8,
    ptname_cstr.as_ptr(),
];

// Spawn the alacritty process with the tio command
let pid = unsafe { libc::fork() };

if pid == 0 {
    // Child process
    unsafe {
        libc::execvp("alacritty\0".as_ptr() as *const i8, tio_cmd.as_ptr());
        libc::exit(1);
    }
} else if pid < 0 {
    // Fork failed
    eprintln!("Failed to fork the process.");
    unsafe {
        libc::exit(1);
    }
}
```

This reduces the code size to less than 20%.
In fact, in isolation, the user code is less than 0.5kB, if you also replace`println!` to external logger calls.

!!! note "Remember that this is example code."

    This code needs cleanup. It's not production ready, and has some edge cases.