# Programmer Usage

!!! warning "All APIs shown here are for reference only, not final."

The Redirector uses the Reloaded Dependency Injection [TODO: Link Pending] system to expose an API.

To use the Redirector API:

1. Add the `reloaded3.api.windows.vfs.interfaces.s56` (or equivalent for your language) package to your project.

2. Add the dependency `reloaded3.api.windows.vfs.s56` to your mod's dependencies.

3. In your mod's entry point, acquire the Controller:

=== "C#"
    ```csharp
    IRedirectorController _redirectorController;

    public void Start(IModLoaderV1 loader)
    {
        _redirectorController = _modLoader.GetService<IRedirectorController>();
    }
    ```

=== "Rust"
    ```rust
    struct MyMod {
        redirector_controller: Option<IRedirectorController>,
    }

    impl MyMod {
        fn new(loader: &mut IModLoader) -> Self {
            Self {
                redirector_controller: loader.get_service::<IRedirectorController>().ok(),
            }
        }
    }
    ```

=== "C++"
    ```cpp
    class MyMod {
    private:
        IRedirectorController* _redirectorController;

    public:
        MyMod(IModLoader* loader)
        {
            _redirectorController = loader->GetService<IRedirectorController>();
        }
    };
    ```

## IRedirectorController API

!!! info "Using basic C# types for easier understanding. Actual types may vary."


### Redirecting Individual Files

- `AddRedirect(string sourcePath, string targetPath)`: Redirects an individual file path from
  `sourcePath` (original game path) to `targetPath` (mod file path).

- `RemoveRedirect(string sourcePath, string targetPath)`: Removes redirection for an individual file
  path from `sourcePath` to `targetPath`.

### Redirecting All Files in Folder

- `AddRedirectFolder(string sourceFolder, string targetFolder)`: Adds a new redirect folder.
  Files in `targetFolder` will overlay files in `sourceFolder`.

- `RemoveRedirectFolder(string sourceFolder, string targetFolder)`: Removes a redirect folder where
  files in `targetFolder` were overlaying `sourceFolder`.

### Registering Virtual Files

!!! info "For file emulation framework. [TODO: Link Pending]"

    These APIs allow you to inject virtual files into search results, such that they appear
    alongside real files when game folders are being searched.

- `RegisterVirtualFile(string filePath, VirtualFileMetadata metadata)`: Registers a new virtual
  file at `filePath` with the provided metadata. This allows the virtual file to be seen during file searches.

- `UnregisterVirtualFile(string filePath)`: Unregisters a previously registered virtual file at `filePath`.

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

### Setting Adjustment

!!! info "Toggling settings flags."

- `GetRedirectorSetting(VfsSettings setting)`: Gets the current value of a redirector setting.
  See `VfsSettings` enum for options.

- `SetRedirectorSetting(bool enable, VfsSettings setting)`: Enables or disables a specific redirector setting.

### Debugging

- `Enable()` / `Disable()`: Enables or disables the VFS entirely.

## Examples

Redirect an individual file:

=== "C#"
    ```csharp
    _redirectorController.AddRedirect(@"dvdroot\bgm\SNG_STG26.adx", @"mods\mybgm.adx");
    ```

=== "Rust"
    ```rust
    redirector_controller.add_redirect(r"dvdroot\bgm\SNG_STG26.adx", r"mods\mybgm.adx");
    ```

=== "C++"
    ```cpp
    _redirectorController->AddRedirect(R"(dvdroot\bgm\SNG_STG26.adx)", R"(mods\mybgm.adx)");
    ```

Add a new redirect folder:

=== "C#"
    ```csharp
    _redirectorController.AddRedirectFolder(@"game\data", @"mods\mymod\data");
    ```

=== "Rust"
    ```rust
    redirector_controller.add_redirect_folder(r"game\data", r"mods\mymod\data");
    ```

=== "C++"
    ```cpp
    _redirectorController->AddRedirectFolder(R"(game\data)", R"(mods\mymod\data)");
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

    _redirectorController.RegisterVirtualFile(@"game\virtualfile.txt", metadata);
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

    redirector_controller.register_virtual_file(r"game\virtualfile.txt", metadata);
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

    _redirectorController->RegisterVirtualFile(R"(game\virtualfile.txt)", metadata);
    ```

Print file redirections to console:

=== "C#"
    ```csharp
    _redirectorController.SetRedirectorSetting(true, VfsSettings.PrintRedirect);
    ```

=== "Rust"
    ```rust
    redirector_controller.set_redirector_setting(true, VfsSettings::PrintRedirect);
    ```

=== "C++"
    ```cpp
    _redirectorController->SetRedirectorSetting(true, VfsSettings::PrintRedirect);
    ```