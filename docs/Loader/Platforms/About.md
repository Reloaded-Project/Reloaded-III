# Platform Support

As the core loader is written in Rust, it is theoretically possible to support any platform provided:  

- You have access to libc.  
- LLVM supports the machine code for your target (e.g. ARM, x86 etc.).  
- Executable format reverse engineered, so you can make linker produce libraries.  
- You can dynamically load libraries.  
- You can arbitrarily execute code in a game process ([write a Bootloader](../Bootloaders/About.md)).  

| Operating System                    | Status                  |
|-------------------------------------|-------------------------|
| [Windows](./Windows.md)             | ✅                       |
| [Linux (Wine/Proton)](./Windows.md) | ✅                       |
| [Switch](./Switch.md)               | 🔍 Investigation Needed |
| [Native Linux](./Linux.md)          | ⚡ Implement on Demand   |
| [Native OSX](./OSX.md)              | ⚡ Implement on Demand   |
| Other                               | ❓ Unknown.              |

`Implement on Demand` means; it'll be done when there's game to test.  
The code will always be written with cross platform in mind; worry not.  