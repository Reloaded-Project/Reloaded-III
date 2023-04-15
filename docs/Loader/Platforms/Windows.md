# Windows

## Native Mods with Dynamic Linking

!!! info

    Some older native mods might want to dynamically link to libraries 
    (.dlls) they ship with their mods. We need to register the mod's directory
    as a possible path for loading DLLs.

```csharp
// Reference C# code from Reloaded-II.
var builder = new StringBuilder(4096); // ought to be enough characters given most programs break at 260 anyway. 
GetDllDirectoryW(builder.Length, builder);
SetDllDirectoryW(Path.GetDirectoryName(dllPath));
_moduleHandle = LoadLibraryW(dllPath);
SetDllDirectoryW(builder.ToString());
```

## Error Reporting

!!! warning

    Assume the user does not have any sort of crash dump/error reporting enabled. 
    We must generate dumps ourselves when our process dies.

```rust
use winapi::um::winnt::{EXCEPTION_POINTERS, LONG};

unsafe extern "system" fn my_unhandled_exception_filter(exception_info: *mut EXCEPTION_POINTERS) -> LONG {
    // Finish Logging and Generate a Crash Dump...
    // ...
    
    // Return 0 because our exception was not handled; we only generated a dump.
    0
}
```

And register it elsewhere:

```rust
unsafe {
    SetUnhandledExceptionFilter(Some(my_unhandled_exception_filter));
}
```

After the crash dump has been generated; the code should:  

- Generate a Crash Dump.  
- Dump Log to Same Location as Crash Dump.  
- Display Crash Address (incl. Module/DLL name).  
- Open an explorer window in the location of the dump.  

Dumps will be written out to `%temp%/Reloaded-III/process.exe` as:  

- `dump.dmp` The crash dump.  
- `log.txt` The log of the recent run.  
- `info.json` Contextual information (e.g. Mod list game was started with).  

A compatible mod manager should clean the `%temp%/Reloaded-III` folder on each boot.

!!! question

    Open for suggestions as to where place the dumps; if anyone has any other preference.

## Process Exit Hook

!!! info

    To ensure all logs have been successfully written out to disk; it's necessary to hook
    `kernel32.ExitProcess` to get a notification for when the process exits.

## Wine 

!!! info 

    To detect wine, check if `ntdll` exports `wine_get_version`.  
    Always note that Wine is in constant development; in the future workarounds might become obsolete.

!!! important

    We really should open up tickets for this once the loader port is done.

```rust
// Translated from C# Reloaded-II via GPT3.5, untested.
use winapi::um::libloaderapi::{GetModuleHandleA, GetProcAddress};
use winapi::shared::minwindef::{HMODULE, FARPROC};
use std::ffi::CString;

pub static ENVIRONMENT: Environment = Environment::new();

pub struct Environment {
    pub is_wine: bool,
}

impl Environment {
    const fn new() -> Self {
        let is_wine = is_wine();
        Self { is_wine }
    }
}

fn is_wine() -> bool {
    unsafe {
        // Get the handle to the ntdll.dll module.
        let ntdll: HMODULE = GetModuleHandleA(CString::new("ntdll.dll").unwrap().as_ptr());

        // Check if the wine_get_version function exists in ntdll.dll.
        let wine_get_version: FARPROC = GetProcAddress(ntdll, CString::new("wine_get_version").unwrap().as_ptr());
        wine_get_version != std::ptr::null_mut()
    }
}
```

And to check:

```rust
println!("Is running under Wine: {}", ENVIRONMENT.is_wine);
```

### Console

Within Wine, the function `Kernel32.GetConsoleWindow` might not correctly evaluate in some cases, 
or be stubbed entirely.

!!! error "Do not do just this."

```rust
if !console_exists() {
    alloc_console();
}
```

!!! success "Do this instead."

```rust
if ENVIRONMENT.is_wine {
    // Wine doesn't support GetConsoleWindow, so we need to allocate a new console window.
    alloc_console();
    return;
}

if !console_exists() {
    alloc_console();
}
```

## DRM

!!! info

    Refer to section [Windows DRM](../Bootloaders/Windows-DRM.md)

## Emulation Support

| Architecture   | Supported   |
|----------------|-------------|
| WINE x86/x64   | ✅          |
| Windows on ARM | ❓ Unknown. |