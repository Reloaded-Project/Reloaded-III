# Creating Signatures

!!! note "This is user documentation."

    This document explains how to create signatures for code and data patterns in games.

!!! info "Signatures are string representations of the bytes you want to locate in a game's memory."

They consist of hex bytes and wildcards that match bytes.

## Signature Format

!!! example "A signature looks like this (hex)"

    ```
    89 15 ?? ?? ?? ?? EB ?? A3 ?? ?? ?? ??
    ```

- Each `byte` is represented by its hexadecimal value (e.g. `89`, `15`).
- Wildcards are represented by `??`, which matches any byte.

### Signature Format (Bit-Level)

!!! example "A signature can also be defined at the bit level:"

    ```
    10001001 ???????? ???????? 11101011 ???????? 10100011 ???????? ????????
    ```

Where `?` represents a bit that can be either `0` or `1`.

## Identifying Signatures

!!! info "To create a signature, you need to identify the bytes that make up the code or data you want to find."

This usually involves the following steps:

1. **Locate the code or data in a disassembler**: Use a tool like IDA Pro, Ghidra,
   or Binary Ninja to find the function or variable you're interested in.

2. **Identify unique bytes**: Find a unique sequence of code bytes at that address.

This process can be automated with with [Signature Creation Tools](#signature-creation-tools).

The theory is to find a sequence of bytes that is unique to the code or data you want to locate,
and while masking out the bytes that may change between different game builds from the assembly,
i.e. memory addresses, jump targets, etc.

!!! warning "It's suggested to only use this technique to scan read only memory."

    This can mean one of the following:

    - Code (usually in `.text` segment)
    - Read-only data (usually in `.rdata` segment)

    Most commonly, you will use this to create a signature for the start of a
    function you intend to hook.<br/>
    However, it can also be used to find variables in memory.

## Signature Creation Tools

!!! tip "There are tools available to help automate the process of creating signatures"

- **[SigMaker for IDA](#sigmaker-for-ida)**: A plugin for IDA Pro that can generate and test signatures.
- **[SigMakerEx for IDA](#sigmaker-for-ida)**: An alternative plugin for IDA Pro that generates signatures.
    - Creates signatures only, but is more flexible than SigMaker for that purpose.
- **[MakeSig for Ghidra](#makesig-for-ghidra)**: A script for Ghidra that creates signatures for functions and code snippets.

### SigMaker for IDA

!!! note "We have merged SigMaker and SigMakerEx docs into a single section."

    Since using these two plugins is very similar.

[You can find SigMaker for IDA here][sigmaker-x64]. You can find [SigMakerEx here][sigmaker-ex].

To install, simply drop the plugin into the `plugins` directory.
You can then access `SigMaker`(Ex) via `Edit -> Plugins -> SigMaker`(Ex) or by pressing `Ctrl + Alt + S`.

!!! tip "We recommend using `SigMakerEx` for creating signatures and older `SigMaker` for testing them."

To create a function signature perform the following steps

=== "SigMakerEx"

    1. Navigate to the code you want to create a signature for.
    2. Press `Ctrl + Alt + S` to open SigMakerEx.
    3. Click `Function`.
    4. Copy the signature from the `Output` window.
    5. Test the pattern in original SigMaker (non-EX) by clicking `Test IDA Pattern`.

=== "SigMaker"

    1. Select the code you want to create a signature for.
    2. Press `Ctrl + Alt + S` to open SigMaker.
    3. Click `Create IDA Pattern from Selection`.
    4. Copy the signature from the `Output` window.
    5. Test the pattern by clicking `Test IDA Pattern`.
    6. If there are multiple results, select more code and repeat the process until there is only one result.

### MakeSig for Ghidra

[You can find MakeSig for Ghidra here][makesig].

To install, drop the `makesig.py` script into your `ghidra_scripts` directory.

To create a signature:

1. Open the `Script Manager` window by clicking `Window -> Script Manager` or using the Script Manager button in the toolbar.
2. Find the `makesig` script and double-click it to run.
3. Select the function or instruction you want to create a signature for.
4. The signature will be printed to the console output.

## Example of Finding a Static Variable via Signature Scanning

!!! info "An example of finding a variable in memory with signature scanning."

    More specifically, we want to find a variable `levelId` in read-write memory (`.data`).

The assembly code (commented below) accesses the `levelId` variable.

```csharp
// Instruction              // Bytes
mov levelId, edx            // 89 15 [?? ?? ?? ??] <= Level ID Address
jmp loc_4354A1 	            // EB ??
mov someOtherVariable, eax  // A3 ?? ?? ?? ??
```

The bytes make up the signature `89 15 ?? ?? ?? ?? EB ?? A3 ?? ?? ?? ??`, with the
4 bytes after `89 15` being the static address of the `levelId` variable.

We scan for the above signature, and add `2` to the found address to get the location of where
`levelId` is stored in memory. We then read from that location to find out where `levelId` is:

=== "C#"
    ```csharp
    // Scan for the signature
    var result = scanner.FindPattern("89 15 ?? ?? ?? ?? EB ?? A3 ?? ?? ?? ??");
    if (!result.Found)
        throw new Exception("Signature not found");

    // Get the address of the instruction
    var instructionAddress = (byte*)result.Address;

    // Get the address of the levelId variable
    var levelIdAddress = (int*)(instructionAddress + 2);

    // Read the value of levelId
    var levelId = *levelIdAddress;
    ```

=== "Rust"
    ```rust
    // Scan for the signature
    let result = scanner.find_pattern("89 15 ?? ?? ?? ?? EB ?? A3 ?? ?? ?? ??");
    if !result.found {
        panic!("Signature not found");
    }

    // Get the address of the instruction
    let instruction_address = result.address as *const u8;

    // Get the address of the levelId variable
    let level_id_address = unsafe { instruction_address.offset(2) as *const i32 };

    // Read the value of levelId
    let level_id = unsafe { *level_id_address };
    ```

=== "C++"
    ```cpp
    // Scan for the signature
    auto result = scanner.FindPattern("89 15 ?? ?? ?? ?? EB ?? A3 ?? ?? ?? ??");
    if (!result.Found)
        throw std::runtime_error("Signature not found");

    // Get the address of the instruction
    auto instructionAddress = reinterpret_cast<uint8_t*>(result.Address);

    // Get the address of the levelId variable
    auto levelIdAddress = reinterpret_cast<int*>(instructionAddress + 2);

    // Read the value of levelId
    auto levelId = *levelIdAddress;
    ```

[makesig]: https://github.com/YaLTeR/ghidra_scripts
[sigmaker-x64]: https://github.com/ajkhoury/SigMaker-x64
[sigmaker-ex]: https://github.com/kweatherman/sigmakerex