# Scanning for Signatures

!!! note "This is user documentation."

    This document explains how to use the Signature Scanner library in a Reloaded3 mod.

!!! info "Once you have created a signature, you can use Reloaded3's Signature Scanner library to locate it in the game's memory."

In Reloaded3, this will be done via the mod, which provides the latest library version, allows for
parallelism across mods, and provides a stable API.

!!! warning "TODO: None of the API names or examples here are final."

    These are a placeholder and will be updated once the library is implemented.

## Common Setup

1. **Add the appropriate library or header file to your project**.
    - C#: `Reloaded.Memory.SigScan.Reloaded3.Interfaces` NuGet package
    - Rust: `reloaded_memory_sigscan_reloaded3` crate.
    - C++: `reloaded_memory_sigscan_reloaded3.h` header file.

2. **Get an instance of `IScannerLibrary`**: Use the mod loader's `GetService<IScannerLibrary>()`
   method to get an instance of `IScannerLibrary`.

## IScannerLibrary Interface

The `IScannerLibrary` interface provides access to the `IStartupScanner` and `IScannerFactory`
interfaces through the following methods:

- `GetStartupScanner()`: Returns an instance of `IStartupScanner` for performing startup scans.
- `GetScannerFactory()`: Returns an instance of `IScannerFactory` for creating scanner instances
  for arbitrary scans.

Below is an example of how to obtain instances of `IStartupScanner` and `IScannerFactory` using
`IScannerLibrary`:

=== "C#"
    ```csharp
    private IScannerLibrary _scannerLibrary;
    private IStartupScanner _startupScanner;
    private IScannerFactory _scannerFactory;

    public void Start()
    {
        // Get an instance of IScannerLibrary
        _modLoader.GetService<IScannerLibrary>().TryGetTarget(out _scannerLibrary);

        // Get instances of IStartupScanner and IScannerFactory
        _startupScanner = _scannerLibrary.GetStartupScanner();
        _scannerFactory = _scannerLibrary.GetScannerFactory();
    }
    ```

=== "Rust"
    ```rust
    struct MyMod {
        scanner_library: Option<IScannerLibrary>,
        startup_scanner: Option<IStartupScanner>,
        scanner_factory: Option<IScannerFactory>,
        // ...
    }

    impl MyMod {
        fn start(&mut self, mod_loader: &mut IModLoader) {
            // Get an instance of IScannerLibrary
            self.scanner_library = mod_loader.get_service::<IScannerLibrary>().ok();

            // Get instances of IStartupScanner and IScannerFactory
            if let Some(library) = &self.scanner_library {
                self.startup_scanner = Some(library.get_startup_scanner());
                self.scanner_factory = Some(library.get_scanner_factory());
            }
        }
    }
    ```

=== "C++"
    ```cpp
    class MyMod {
    private:
        IScannerLibrary* _scannerLibrary;
        IStartupScanner* _startupScanner;
        IScannerFactory* _scannerFactory;

    public:
        void Start(IModLoader* modLoader)
        {
            // Get an instance of IScannerLibrary
            modLoader->GetService<IScannerLibrary>()->TryGetTarget(&_scannerLibrary);

            // Get instances of IStartupScanner and IScannerFactory
            _startupScanner = _scannerLibrary->GetStartupScanner();
            _scannerFactory = _scannerLibrary->GetScannerFactory();
        }
    };
    ```

## Startup Scans (IStartupScanner)

!!! tip "To perform startup scans using `IStartupScanner`, follow these steps:"

1. **Queue your signature scans**: Call the appropriate methods on the `IStartupScanner` instance,
   passing in your signature as a string and a callback function to handle the scan result.
    - `AddMainModuleScan(signature, handler)` scans the whole EXE/ELF.
    - `AddArbitraryScan(signature, range, handler)` scans a custom range.
    - `AddMainModuleSegmentScan(signature, permissions, handler)` scans all segments of EXE/ELF that
      match the specified `permissions` flags (Execute/Read/Write).

2. **Handle the scan result**: In your callback function, check the `Found` property of the
   `PatternScanResult` object to determine if the pattern was found, and use the `Address` property
   to calculate the memory address where the pattern was found. You can also use `Offset` property
   to calculate the offset from the start of the scan range.

Below is an example.

=== "C#"
    ```csharp
    private IStartupScanner _startupScanner;

    public void Start()
    {
        // Get an instance of IStartupScanner
        _startupScanner = _scannerLibrary.GetStartupScanner();

        // Queue a signature scan
        _startupScanner.AddMainModuleScan("89 15 ?? ?? ?? ?? EB ?? A3 ?? ?? ?? ??", OnLevelIdScan);

        // Queue a 'null' scan to execute a callback after previous scans
        _startupScanner.AddMainModuleScan("", OnScanComplete);
    }

    private void OnLevelIdScan(PatternScanResult result)
    {
        if (!result.Found)
        {
            _logger.WriteLine("Signature for getting LevelId not found.");
            return;
        }

        // Get the address of the levelId variable
        var levelIdAddress = result.Address + 2;

        // Read the value of levelId
        var levelId = *(int*)levelIdAddress;
        _logger.WriteLine($"LevelId: {levelId}");
    }

    private void OnScanComplete(PatternScanResult result)
    {
        _logger.WriteLine("All scans completed.");
    }
    ```

=== "Rust"
    ```rust
    struct MyMod {
        startup_scanner: Option<IStartupScanner>,
        // ...
    }

    impl MyMod {
        fn start(&mut self, mod_loader: &mut IModLoader) {
            // Get an instance of IStartupScanner
            if let Some(library) = &self.scanner_library {
                self.startup_scanner = Some(library.get_startup_scanner());
            }

            // Queue a signature scan
            if let Some(scanner) = &self.startup_scanner {
                scanner.add_main_module_scan("89 15 ?? ?? ?? ?? EB ?? A3 ?? ?? ?? ??", Self::on_level_id_scan);

                // Queue a 'null' scan to execute a callback after previous scans
                scanner.add_main_module_scan("", Self::on_scan_complete);
            }
        }

        fn on_level_id_scan(result: PatternScanResult) {
            if !result.found {
                println!("Signature for getting LevelId not found.");
                return;
            }

            // Get the address of the levelId variable
            let level_id_address = result.address + 2;

            // Read the value of levelId
            let level_id = unsafe { *(level_id_address as *const i32) };
            println!("LevelId: {}", level_id);
        }

        fn on_scan_complete(_result: PatternScanResult) {
            println!("All scans completed.");
        }
    }
    ```

=== "C++"
    ```cpp
    class MyMod {
    private:
        IStartupScanner* _startupScanner;

    public:
        void Start(IModLoader* modLoader)
        {
            // Get an instance of IStartupScanner
            _startupScanner = _scannerLibrary->GetStartupScanner();

            // Queue a signature scan
            _startupScanner->AddMainModuleScan("89 15 ?? ?? ?? ?? EB ?? A3 ?? ?? ?? ??", std::bind(&MyMod::OnLevelIdScan, this, std::placeholders::_1));

            // Queue a 'null' scan to execute a callback after previous scans
            _startupScanner->AddMainModuleScan("", std::bind(&MyMod::OnScanComplete, this, std::placeholders::_1));
        }

    private:
        void OnLevelIdScan(const PatternScanResult& result)
        {
            if (!result.Found)
            {
                std::cout << "Signature for getting LevelId not found." << std::endl;
                return;
            }

            // Get the address of the levelId variable
            auto levelIdAddress = result.Address + 2;

            // Read the value of levelId
            auto levelId = *(int*)levelIdAddress;
            std::cout << "LevelId: " << levelId << std::endl;
        }

        void OnScanComplete(const PatternScanResult& result)
        {
            std::cout << "All scans completed." << std::endl;
        }
    };
    ```

!!! warning "Using `IStartupScanner` is mandatory"

    - Avoids conflicts in case multiple mods are scanning for the same signature.
    - Ensures that all scans are performed in parallel, improving startup time.
    - Provides caching of scan results between runs.

Scans submitted to `IStartupScanner` are returned in the order they are submitted, so there's no
need to worry about conflicts, load order or race conditions.

!!! tip "Using Results of Multiple Scans at Once"

    In some rare cases, you may want to do something only after scanning a couple of signatures in
    a group.

    For example, scan 5 signatures, and only do something if all 5 signatures match.

    To do this, first submit the 5 signatures, and collect the results of these scans to a shared
    location, e.g. a shared vector. Then, submit a 'null' scan with an empty string as the signature.

    This 'null' scan will be used to execute the callback after all previous scans are complete.

## Arbitrary Scans (IScannerFactory)

!!! tip "To perform arbitrary scans using `IScannerFactory`, follow these steps:"

1. **Get an instance of `IScannerFactory`**: Use the `GetScannerFactory()` method of the
   `IScannerLibrary` instance to get an instance of `IScannerFactory`.

2. **Create a scanner instance**: Call one of the `CreateScanner` methods on the `IScannerFactory`
   instance, passing in the appropriate parameters based on your scanning needs.
    - `CreateScanner(data)` creates a scanner for an arbitrary slice of data (slice type native to
      the language).
    - `CreateScanner(data, length)` creates a scanner for a pointer to data and its length.

3. **Perform the scan**: Call the `FindPattern` method on the scanner instance, passing in your
   signature as a string.

4. **Check the result**: The `FindPattern` method returns a `PatternScanResult` object, which
   contains a `Found` property indicating whether the pattern was found, and an `Address` property
   giving the memory address where the pattern was found. You can also use `Offset` property to
   calculate the offset from the start of the scan range.

Below is an example.

=== "C#"
    ```csharp
    private IScannerFactory _scannerFactory;

    public void Start()
    {
        // Get an instance of IScannerFactory
        _scannerFactory = _scannerLibrary.GetScannerFactory();
    }

    public void ScanForPattern(byte[] data)
    {
        // Create a scanner instance for the provided data
        var scanner = _scannerFactory.CreateScanner(data);

        // Perform the scan
        var result = scanner.FindPattern("89 15 ?? ?? ?? ?? EB ?? A3 ?? ?? ?? ??");

        if (!result.Found)
        {
            _logger.WriteLine("Pattern not found.");
            return;
        }

        // Get the address where the pattern was found
        var patternAddress = result.Address;

        _logger.WriteLine($"Pattern found at address: {patternAddress:X}");
    }
    ```

=== "Rust"
    ```rust
    struct MyMod {
        scanner_factory: Option<IScannerFactory>,
        // ...
    }

    impl MyMod {
        fn start(&mut self, mod_loader: &mut IModLoader) {
            // Get an instance of IScannerFactory
            if let Some(library) = &self.scanner_library {
                self.scanner_factory = Some(library.get_scanner_factory());
            }
        }

        fn scan_for_pattern(&self, data: &[u8]) {
            if let Some(factory) = &self.scanner_factory {
                // Create a scanner instance for the provided data
                let scanner = factory.create_scanner(data);

                // Perform the scan
                let result = scanner.find_pattern("89 15 ?? ?? ?? ?? EB ?? A3 ?? ?? ?? ??");

                if !result.found {
                    println!("Pattern not found.");
                    return;
                }

                // Get the address where the pattern was found
                let pattern_address = result.address;

                println!("Pattern found at address: {:X}", pattern_address);
            }
        }
    }
    ```

=== "C++"
    ```cpp
    class MyMod {
    private:
        IScannerFactory* _scannerFactory;

    public:
        void Start(IModLoader* modLoader)
        {
            // Get an instance of IScannerFactory
            _scannerFactory = _scannerLibrary->GetScannerFactory();
        }

        void ScanForPattern(const uint8_t* data, size_t length)
        {
            // Create a scanner instance for the provided data
            auto scanner = _scannerFactory->CreateScanner(data, length);

            // Perform the scan
            auto result = scanner->FindPattern("89 15 ?? ?? ?? ?? EB ?? A3 ?? ?? ?? ??");

            if (!result.Found)
            {
                std::cout << "Pattern not found." << std::endl;
                return;
            }

            // Get the address where the pattern was found
            auto patternAddress = result.Address;

            std::cout << "Pattern found at address: " << std::hex << patternAddress << std::endl;
        }
    };
    ```

!!! note "Arbitrary scans using `IScannerFactory` are not cached or parallelized."

    If you need to perform scans that benefit from caching and parallelization, consider using
    `IStartupScanner` instead.

## Error Handling

!!! warning "It's important to handle cases where a signature is not found, as this may indicate that the game has been updated and the pattern has changed."

In the callback function or after performing a scan, you can check the `Found` property of the
`PatternScanResult` to determine if the pattern was located, and log an error or take appropriate
action if it was not.