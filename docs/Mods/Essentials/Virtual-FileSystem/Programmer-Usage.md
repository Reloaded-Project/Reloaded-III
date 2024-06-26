# Programmer Usage

!!! warning "All APIs shown here are for reference only, not final."

The Redirector uses the Reloaded Dependency Injection [TODO: Link Pending] system to expose an API.

To use the Redirector API:

1. Add the `reloaded3.api.windows.vfs.interfaces.s56` (or equivalent for your language) package to your project.

2. Add the dependency `reloaded3.api.windows.vfs.s56` to your mod's dependencies.

3. In your mod's entry point, acquire the necessary services:

=== "C#"
    ```csharp
    IRedirectorService _redirectorService;
    IVfsService _vfsService;
    IVfsSettingsService _vfsSettingsService;

    public void Start(IModLoaderV1 loader)
    {
        _redirectorService = _modLoader.GetService<IRedirectorService>();
        _vfsService = _modLoader.GetService<IVfsService>();
        _vfsSettingsService = _modLoader.GetService<IVfsSettingsService>();
    }
    ```

=== "Rust"
    ```rust
    struct MyMod {
        redirector_service: Option<IRedirectorService>,
        vfs_service: Option<IVfsService>,
        vfs_settings_service: Option<IVfsSettingsService>,
    }

    impl MyMod {
        fn new(loader: &mut IModLoader) -> Self {
            Self {
                redirector_service: loader.get_service::<IRedirectorService>().ok(),
                vfs_service: loader.get_service::<IVfsService>().ok(),
                vfs_settings_service: loader.get_service::<IVfsSettingsService>().ok(),
            }
        }
    }
    ```

=== "C++"
    ```cpp
    class MyMod {
    private:
        IRedirectorService* _redirectorService;
        IVfsService* _vfsService;
        IVfsSettingsService* _vfsSettingsService;

    public:
        MyMod(IModLoader* loader)
        {
            _redirectorService = loader->GetService<IRedirectorService>();
            _vfsService = loader->GetService<IVfsService>();
            _vfsSettingsService = loader->GetService<IVfsSettingsService>();
        }
    };
    ```

## IRedirectorService API

!!! info "Using basic C# types for easier understanding. Actual types may vary."

### Redirecting Individual Files

- `RedirectHandle AddRedirect(string sourcePath, string targetPath)`: Redirects an individual file path from
  `sourcePath` (original game path) to `targetPath` (mod file path). Returns a handle to the redirection.

- `void RemoveRedirect(RedirectHandle handle)`: Removes the redirection associated with the given `handle`.

### Redirecting All Files in Folder

- `RedirectFolderHandle AddRedirectFolder(string sourceFolder, string targetFolder)`: Adds a new redirect folder.
  Files in `targetFolder` will overlay files in `sourceFolder`. Returns a handle to the redirect folder.

- `void RemoveRedirectFolder(RedirectFolderHandle handle)`: Removes the redirect folder associated with the given `handle`.

## IVfsService API

!!! info "Using basic C# types for easier understanding. Actual types may vary."

### Registering Virtual Files

!!! info "For file emulation framework. [TODO: Link Pending]"

    These APIs allow you to inject virtual files into search results, such that they appear
    alongside real files when game folders are being searched.

- `VirtualFileHandle RegisterVirtualFile(string filePath, VirtualFileMetadata metadata)`: Registers a new virtual
  file at `filePath` with the provided metadata. This allows the virtual file to be seen during file searches.
  Returns a handle to the virtual file.

- `void UnregisterVirtualFile(VirtualFileHandle handle)`: Unregisters the virtual file associated with the given `handle`.

The `VirtualFileMetadata` structure should look something like:

```csharp
// This may differ for Unix. That's to be determined.
public struct VirtualFileMetadata
{
    public long CreationTime;
    public long LastAccessTime;
    public long LastWriteTime;
    public long ChangeTime;
    public long EndOfFile;
    public long AllocationSize;
    public FileAttributes FileAttributes;
}
```

Actually reading the files etc. is handled by the file emulation framework itself.

!!! note "This API is intended to be called by the framework"

    And not by individual 'File Emulators' using the framework.
    i.e. The end user of the framework should not be calling this API.

## IVfsSettingsService API

!!! info "Using basic C# types for easier understanding. Actual types may vary."

### VFS Settings

- `GetVfsSetting(VfsSettings setting)`: Gets the current value of a VFS setting.
  See `VfsSettings` enum for options.

- `SetVfsSetting(bool enable, VfsSettings setting)`: Enables or disables a specific VFS setting.

The `VfsSettings` enum provides the following options:

```csharp
[Flags]
public enum VfsSettings
{
    None = 0,                   // Default value.
    PrintRedirect = 1 << 0,     // Prints when a file redirect is performed.
    PrintOpen = 1 << 1,         // Prints file open operations. (debug setting)
    DontPrintNonFiles = 1 << 2, // Skips printing non-files to the console.
    PrintGetAttributes = 1 << 3 // Prints operations that get file attributes (debug setting)
}
```

### Debugging

- `Enable()` / `Disable()`: Enables or disables the VFS entirely.

## Examples

Redirect an individual file:

=== "C#"
    ```csharp
    var handle = _redirectorService.AddRedirect(@"dvdroot\bgm\SNG_STG26.adx", @"mods\mybgm.adx");
    // ...
    _redirectorService.RemoveRedirect(handle);
    ```

=== "Rust"
    ```rust
    let handle = redirector_service.add_redirect(r"dvdroot\bgm\SNG_STG26.adx", r"mods\mybgm.adx");
    // ...
    redirector_service.remove_redirect(handle);
    ```

=== "C++"
    ```cpp
    auto handle = _redirectorService->AddRedirect(R"(dvdroot\bgm\SNG_STG26.adx)", R"(mods\mybgm.adx)");
    // ...
    _redirectorService->RemoveRedirect(handle);
    ```

Add a new redirect folder:

=== "C#"
    ```csharp
    var handle = _redirectorService.AddRedirectFolder(@"game\data", @"mods\mymod\data");
    // ...
    _redirectorService.RemoveRedirectFolder(handle);
    ```

=== "Rust"
    ```rust
    let handle = redirector_service.add_redirect_folder(r"game\data", r"mods\mymod\data");
    // ...
    redirector_service.remove_redirect_folder(handle);
    ```

=== "C++"
    ```cpp
    auto handle = _redirectorService->AddRedirectFolder(R"(game\data)", R"(mods\mymod\data)");
    // ...
    _redirectorService->RemoveRedirectFolder(handle);
    ```

Register a virtual file (dummy example):

=== "C#"
    ```csharp
    var metadata = new VirtualFileMetadata
    {
        CreationTime = DateTime.Now.Ticks,
        LastAccessTime = DateTime.Now.Ticks,
        LastWriteTime = DateTime.Now.Ticks,
        ChangeTime = DateTime.Now.Ticks,
        EndOfFile = 1024,
        AllocationSize = 1024,
        FileAttributes = FileAttributes.Normal
    };

    var handle = _vfsService.RegisterVirtualFile(@"game\virtualfile.txt", metadata);
    // ...
    _vfsService.UnregisterVirtualFile(handle);
    ```

=== "Rust"
    ```rust
    let metadata = VirtualFileMetadata {
        creation_time: SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_nanos() as i64,
        last_access_time: SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_nanos() as i64,
        last_write_time: SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_nanos() as i64,
        change_time: SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_nanos() as i64,
        end_of_file: 1024,
        allocation_size: 1024,
        file_attributes: FileAttributes::Normal,
    };

    let handle = vfs_service.register_virtual_file(r"game\virtualfile.txt", metadata);
    // ...
    vfs_service.unregister_virtual_file(handle);
    ```

=== "C++"
    ```cpp
    VirtualFileMetadata metadata;
    metadata.CreationTime = std::chrono::system_clock::now().time_since_epoch().count();
    metadata.LastAccessTime = std::chrono::system_clock::now().time_since_epoch().count();
    metadata.LastWriteTime = std::chrono::system_clock::now().time_since_epoch().count();
    metadata.ChangeTime = std::chrono::system_clock::now().time_since_epoch().count();
    metadata.EndOfFile = 1024;
    metadata.AllocationSize = 1024;
    metadata.FileAttributes = FileAttributes::Normal;

    auto handle = _vfsService->RegisterVirtualFile(R"(game\virtualfile.txt)", metadata);
    // ...
    _vfsService->UnregisterVirtualFile(handle);
    ```

Change VFS settings:

=== "C#"
    ```csharp
    // Enable printing of file redirects
    _vfsSettingsService.SetVfsSetting(true, VfsSettings.PrintRedirect);

    // Disable the VFS entirely
    _vfsSettingsService.Disable();
    ```

=== "Rust"
    ```rust
    // Enable printing of file redirects
    vfs_settings_service.set_vfs_setting(true, VfsSettings::PrintRedirect);

    // Disable the VFS entirely
    vfs_settings_service.disable();
    ```

=== "C++"
    ```cpp
    // Enable printing of file redirects
    _vfsSettingsService->SetVfsSetting(true, VfsSettings::PrintRedirect);

    // Disable the VFS entirely
    _vfsSettingsService->Disable();
    ```