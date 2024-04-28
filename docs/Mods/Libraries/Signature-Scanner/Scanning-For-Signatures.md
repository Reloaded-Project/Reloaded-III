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
    - C#: `reloaded3.utility.sigscan.interfaces.s56` NuGet package
    - Rust: `reloaded3_utility_sigscan_interfaces_s56` crate.
    - C++: `reloaded3_utility_sigscan_interfaces_s56.h` header file.

2. **Get instances of the scanner services**: Use the mod loader's `GetService<T>()` method to get instances of
   `IStartupScanner` and `IScannerFactory`.

Below is an example of how to obtain instances of the scanner services:

=== "C#"
    ```csharp
    private IStartupScanner _startupScanner;
    private IScannerFactory _scannerFactory;

    public void Start()
    {
        _startupScanner = _modLoader.GetService<IStartupScanner>();
        _scannerFactory = _modLoader.GetService<IScannerFactory>();
    }
    ```

=== "Rust"
    ```rust
    struct MyMod {
        startup_scanner_service: Option<IStartupScanner>,
        scanner_factory_service: Option<IScannerFactory>,
        // ...
    }

    impl MyMod {
        fn start(&mut self, mod_loader: &mut IModLoader) {
            self.startup_scanner_service = mod_loader.get_service::<IStartupScanner>().ok();
            self.scanner_factory_service = mod_loader.get_service::<IScannerFactory>().ok();
        }
    }
    ```

=== "C++"
    ```cpp
    class MyMod {
    private:
        IStartupScanner* _startupScanner;
        IScannerFactory* _scannerFactory;

    public:
        void Start(IModLoader* modLoader)
        {
            _startupScanner = modLoader->GetService<IStartupScanner>();
            _scannerFactory = modLoader->GetService<IScannerFactory>();
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
    public void Start()
    {
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
    fn start(&mut self, mod_loader: &mut IModLoader) {
        // Queue a signature scan
        if let Some(scanner_service) = &self.startup_scanner_service {
            scanner_service.add_main_module_scan("89 15 ?? ?? ?? ?? EB ?? A3 ?? ?? ?? ??", Self::on_level_id_scan);

            // Queue a 'null' scan to execute a callback after previous scans
            scanner_service.add_main_module_scan("", Self::on_scan_complete);
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
    ```

=== "C++"
    ```cpp
    void Start(IModLoader* modLoader)
    {
        // Queue a signature scan
        _startupScanner->AddMainModuleScan("89 15 ?? ?? ?? ?? EB ?? A3 ?? ?? ?? ??", std::bind(&MyMod::OnLevelIdScan, this, std::placeholders::_1));

        // Queue a 'null' scan to execute a callback after previous scans
        _startupScanner->AddMainModuleScan("", std::bind(&MyMod::OnScanComplete, this, std::placeholders::_1));
    }

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

1. **Create a scanner instance**: Call one of the `CreateScanner` methods on the `IScannerFactory`
   instance, passing in the appropriate parameters based on your scanning needs.
    - `CreateScanner(data)` creates a scanner for an arbitrary slice of data (slice type native to
      the language).
    - `CreateScanner(data, length)` creates a scanner for a pointer to data and its length.

2. **Perform the scan**: Call the `FindPattern` method on the scanner instance, passing in your
   signature as a string.

3. **Check the result**: The `FindPattern` method returns a `PatternScanResult` object, which
   contains a `Found` property indicating whether the pattern was found, and an `Address` property
   giving the memory address where the pattern was found. You can also use `Offset` property to
   calculate the offset from the start of the scan range.

Below is an example.

=== "C#"
    ```csharp
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
    fn scan_for_pattern(&self, data: &[u8]) {
        if let Some(factory_service) = &self.scanner_factory_service {
            // Create a scanner instance for the provided data
            let scanner = factory_service.create_scanner(data);

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
    ```

=== "C++"
    ```cpp
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
    ```

!!! note "Arbitrary scans using `IScannerFactory` are not cached or parallelized."

    If you need to perform scans that benefit from caching and parallelization, consider using
    `IStartupScanner` instead.

## Error Handling

!!! warning "It's important to handle cases where a signature is not found, as this may indicate that the game has been updated and the pattern has changed."

In the callback function or after performing a scan, you can check the `Found` property of the
`PatternScanResult` to determine if the pattern was located, and log an error or take appropriate
action if it was not.

That covers the key aspects of using the Signature Scanner services in Reloaded3 mods. Let me know if you have any further questions!