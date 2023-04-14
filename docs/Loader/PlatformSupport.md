# Platform Support

As the core loader is written in Rust, it is theoretically possible to support any platform provided:  

- You have access to libc.  
- LLVM supports the machine code for your target (e.g. ARM, x86 etc.).  
- Executable format reverse engineered, so you can make linker produce libraries.  
- You can dynamically load libraries.  
- You can arbitrarily execute code in a game process.  

| Operating System                             | Status                  |
|----------------------------------------------|-------------------------|
| [Windows](./Platform-Windows.md)             | ✅                       |
| [Linux (Wine/Proton)](./Platform-Windows.md) | ✅                       |
| [Switch](./Platform-Switch.md)               | 🔍 Investigation Needed |
| Native Linux                                 | 🔍 Investigation Needed |
| Native OSX                                   | 🔍 Investigation Needed |
| Other                                        | ❓ Unknown.              |

