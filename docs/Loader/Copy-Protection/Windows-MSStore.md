!!! important "The information on this page is accurate for Project Centennial apps, i.e. Win32 apps converted to UWP."
    
    It is not currently known how much of this applies to pure UWP Apps.

This also includes games installed via the Xbox App, or 'Gamepass games'.

## Microsoft (MS Store/Game Pass)

!!! info

    For the purposes of Reverse Engineering; [UWPDumper](https://github.com/Wunkolo/UWPDumper) can often be used to get an unencrypted EXE.

### Dangers

#### Binaries are Encrypted

!!! failure "EXEs are Encrypted and Unreadable"

    This appears to not be a copy-protection measure per se, but a leftover from UWP's security model.

Many actions performed by Reloaded require access to the EXE, such as:  

- Workflows (Link Pending)
- App Icon Extraction
- Determining DLL Name for [DLL Hijacking](../Bootloaders/Windows-DllHijack.md)

#### Binary Path at Runtime Doesn't Match Real Location

!!! note

    Actual path of EXE reported at runtime is something like `C:\Program Files\WindowsApps\SEGAofAmericaInc.F0cb6b3aer_1.10.23.0_x64_USEU+s751p9cej88mt\P5R.exe` 
    and can change every update.

In other words, do not use the path of the EXE at runtime to check anything critical.  
Use only for cache purposes at best.  

#### Do not use DLL Injection

!!! warning "Although it is technically possible to do so, [DLL Injection](../Bootloaders/Windows-InjectIntoSuspended.md) should be avoided for MS Store games."

Launching many centennial games will invoke a binary called `gamelaunchhelper.exe`.  

This binary is responsible for, among other things, syncing cloud saves. Therefore, it should not be skipped.  

### Common Workarounds

!!! info "Or at least the possible ones I can think of"

**1. Dumping the EXE from memory of a running game:**  
- We could do this, but it'd be very poor User Experience.  

**2. Using a known DLL name with [DLL Hijacking](../Bootloaders/Windows-DllHijack.md):**  
- Possible via [Community Repository](../../Services/Community-Repository.md), but this is not a good solution for unknown apps.  
- Possible via dumping the EXE from memory, but leads to poor UX.  
- Does not fix the issue of the binary being encrypted, leading to limited functionality.  

**3. DLL Injection into Suspended Process**  
- i.e. Force skipping `gamelaunchhelper.exe` to boot into the game directly.  
- Can be done via `Invoke-CommandInDesktopPackage` in PowerShell.  
- Does not fix the issue of the binary being encrypted, leading to limited functionality.  
- Causes issues with cloud saves.  

**4. Replacing the main game EXE with DLL Injector Stub**  
- DLL Injection by renaming `P5R.exe` to `P5R-orig.exe` and placing DLL Injector as `P5R.exe`, which then runs and injects into `P5R-orig.exe`.  
- Basically it leads to `gamelaunchhelper.exe` running our injector.  
- Fixes cloud save issue.  
- Does not fix the issue of the binary being encrypted, leading to limited functionality.  

**5. Decrypting the EXE**  
- Basically removing the leftover UWP security model functionality.  
- When executing code inside the AppX container, the EXE can be read decrypted.  
- So when we make a copy of the EXE inside the game, the copied file is decrypted.  
- Can be performed using official `Invoke-CommandInDesktopPackage` applet in PowerShell, and launching a custom EXE to do the copy.  
- Does not technically circumvent copy protection (to best of my knowledge).  

### What R3 Should Do

Basically, decrypt the EXE. 

This is a multi-step process which involves:  

- Finding `AppxManifest.xml`, which may be in EXE folder or in some folder above.  
- Parsing `AppxManifest.xml` to extract `Application.Id` and `PackageFamilyName`.  
    - `PackageFamilyName` is generally derived as `{Identity.Name}-{hash(Identity.Publisher)}`.  
    - Consider using [package-family-name](https://github.com/russellbanks/package-family-name) library directly.  
- Finding all unreadable files (just `.exe` files currently).  
- Launching a custom EXE inside the AppX container which does a copy onto itself (this decrypts).
    - This custom EXE can be launched using official `Invoke-CommandInDesktopPackage` in PowerShell.  
    - Or unofficially with COM Interfaces detailed in [launching-a-centennial-app](#launching-a-centennial-app).  
    - Reloaded-II uses [replace-files-with-itself](https://github.com/Sewer56/replace-files-with-itself) as the binary.  
    - In Reloaded3, consider using current (server) binary with a `--copy` flag.  

Although not a stable API, prefer the COM interface. With it you can get a process handle, which in turn lets you use
[WaitForSingleObject](https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-waitforsingleobject?redirectedfrom=MSDN) 
to wait for the target process to finish.

Refer to [Reloaded-II's code](https://github.com/Reloaded-Project/Reloaded-II/blob/3b800957b5b919ebba42b92e9cf859dbbe1c9926/source/Reloaded.Mod.Launcher.Lib/Utility/TryUnprotectGamePassGame.cs#L14) for some existing reference code. 

!!! note "Re-launching the server binary is preferable to using a custom EXE. It increases our resilience to false antivirus detections."

    The whole app not working at all is preferable to a tiny amount not working.  
    More EXEs also mean more potential for false positives.  

### Launching a Centennial App

!!! info "This tells you how to use internal COM interfaces to launch a Centennial App (emulate `Invoke-CommandInDesktopPackage`)."

C++ Definitions Below:

```cpp
typedef enum _DESKTOP_APPX_ACTIVATE_OPTIONS
{
    DAXAO_NONE = 0,
    DAXAO_ELEVATE = 1,
    DAXAO_NONPACKAGED_EXE = 2,
    DAXAO_NONPACKAGED_EXE_PROCESS_TREE = 4,
    DAXAO_NONPACKAGED_EXE_FLAGS = 6,
    DAXAO_NO_ERROR_UI = 8,
    DAXAO_CHECK_FOR_APPINSTALLER_UPDATES = 16,
    DAXAO_CENTENNIAL_PROCESS = 32,
    DAXAO_UNIVERSAL_PROCESS = 64,
    DAXAO_WIN32ALACARTE_PROCESS = 128,
    DAXAO_RUNTIME_BEHAVIOR_FLAGS = 224,
    DAXAO_PARTIAL_TRUST = 256,
    DAXAO_UNIVERSAL_CONSOLE = 512,
    DAXAO_APP_SILO = 1024,
    DAXAO_TRUST_LEVEL_FLAGS = 1280
} DESKTOP_APPX_ACTIVATE_OPTIONS, * PDESKTOP_APPX_ACTIVATE_OPTIONS;

// Windows 11
// ClsId: 168EB462-775F-42AE-9111-D714B2306C2E
interface DECLSPEC_UUID("F158268A-D5A5-45CE-99CF-00D6C3F3FC0A") IDesktopAppxActivator : IUnknown {
    IDesktopAppxActivator();

    IDesktopAppxActivator(const IDesktopAppxActivator&) = delete;
    IDesktopAppxActivator& operator=(const IDesktopAppxActivator&) = delete;

    HRESULT STDMETHODCALLTYPE QueryInterface(REFIID riid, void** ppvObj) override final;
    ULONG   STDMETHODCALLTYPE AddRef() override final;
    ULONG   STDMETHODCALLTYPE Release() override final;

    void STDMETHODCALLTYPE Activate(
        _In_ PWSTR ApplicationUserModelId, 
        _In_ PWSTR PackageRelativeExecutable, 
        _In_ PWSTR Arguments,
        _Out_ PHANDLE ProcessHandle);

	void STDMETHODCALLTYPE ActivateWithOptions(
        _In_ PWSTR ApplicationUserModelId, 
        _In_ PWSTR Executable, 
        _In_ PWSTR Arguments,
        _In_ ULONG ActivationOptions, 
        _In_opt_ ULONG ParentProcessId, 
        _Out_ PHANDLE ProcessHandle);

    void STDMETHODCALLTYPE ActivateWithOptionsAndArgs(
        _In_ PWSTR ApplicationUserModelId,
        _In_ PWSTR Executable,
        _In_ PWSTR Arguments,
        _In_opt_ ULONG ParentProcessId,
        _In_opt_ PVOID ActivatedEventArgs,
        _Out_ PHANDLE ProcessHandle);

    void STDMETHODCALLTYPE ActivateWithOptionsArgsWorkingDirectoryShowWindow(
        _In_ PWSTR ApplicationUserModelId,
        _In_ PWSTR Executable,
        _In_ PWSTR Arguments,
        _In_ ULONG ActivationOptions,
        _In_opt_ ULONG ParentProcessId,
        _In_opt_ PVOID ActivatedEventArgs,
        _In_ PWSTR WorkingDirectory,
        _In_ ULONG ShowWindow,
        _Out_ PHANDLE ProcessHandle);
}

// Windows 10
// ClsId: 168EB462-775F-42AE-9111-D714B2306C2E
interface DECLSPEC_UUID("72e3a5b0-8fea-485c-9f8b-822b16dba17f") IDesktopAppxActivator : IUnknown {
    IDesktopAppxActivator();

    IDesktopAppxActivator(const IDesktopAppxActivator&) = delete;
    IDesktopAppxActivator& operator=(const IDesktopAppxActivator&) = delete;

    HRESULT STDMETHODCALLTYPE QueryInterface(REFIID riid, void** ppvObj) override final;
    ULONG   STDMETHODCALLTYPE AddRef() override final;
    ULONG   STDMETHODCALLTYPE Release() override final;

    void STDMETHODCALLTYPE Activate(
        _In_ PWSTR ApplicationUserModelId, 
        _In_ PWSTR PackageRelativeExecutable, 
        _In_ PWSTR Arguments,
        _Out_ PHANDLE ProcessHandle);

	void STDMETHODCALLTYPE ActivateWithOptions(
        _In_ PWSTR ApplicationUserModelId, 
        _In_ PWSTR Executable, 
        _In_ PWSTR Arguments,
        _In_ ULONG ActivationOptions, 
        _In_opt_ ULONG ParentProcessId, 
        _Out_ PHANDLE ProcessHandle);
}
```

This code was translated back to C++ and Windows API types from the C# source.  

- Windows11: Create COM object with ClsId `168EB462-775F-42AE-9111-D714B2306C2E`, IId `F158268A-D5A5-45CE-99CF-00D6C3F3FC0A`.  
- Windows10: Create COM object with ClsId `168EB462-775F-42AE-9111-D714B2306C2E`, IId `72e3a5b0-8fea-485c-9f8b-822b16dba17f`.  

Using these interfaces looks something like this:

```cpp
// NOTE: This code is untested, and I don't usually write C++
// please correct this if compile error.
HRESULT hRes;
class IDesktopAppxActivator *appxActivate = nullptr;
HANDLE processHandle = nullptr;

hRes = CoInitialize(nullptr); // Init COM
hRes = CoCreateInstance( // Make COM interface
    "168EB462-775F-42AE-9111-D714B2306C2E", // ClsId
    nullptr,
    CLSCTX_INPROC_SERVER,
    "F158268A-D5A5-45CE-99CF-00D6C3F3FC0A", // IId (Win11)
    (void **)&appxActivate);

hRes = appxActivate->ActivateWithOptions(
    packageFamilyName, // Derived in an above step.
    pathToExe, // Path to EXE used to do the copying, i.e. `replace-files-with-itself` for Reloaded-II
    arguments, // Args to pass to `replace-files-with-itself`
    _DESKTOP_APPX_ACTIVATE_OPTIONS::DAXAO_CENTENNIAL_PROCESS | _DESKTOP_APPX_ACTIVATE_OPTIONS::DAXAO_NONPACKAGED_EXE_PROCESS_TREE, // Centennial Process and `PreventBreakaway` from `Invoke-CommandInDesktopPackage`
    0,
    &processHandle);

if (SUCCEEDED(hRes) && processHandle != nullptr) {
    // Wait for the process to exit
    WaitForSingleObject(processHandle, INFINITE);
    CloseHandle(processHandle);
}

appxActivate->Release();
CoUninitialize(); // Release COM
return processHandle;
```

That's about it.

Actual implementation may require more error handling, i.e. to ensure process doesn't run forever, that it started correctly, etc.

There's no telling when a future Windows version may change something, as we're using an internal API.

#### Deriving this Information

!!! tip "In the event the COM interface changes, you can do the following steps to update."

!!! note "This information is derived from the official `Invoke-CommandInDesktopPackage` applet in PowerShell."

1. Open `PowerShell` that comes with Windows.
2. Run `Get-Command Invoke-CommandInDesktopPackage | Format-List *`.
3. Find the C# Class Name and DLL.
4. Open the DLL in a decompiler (e.g. dnSpy).

You should get some fairly readable C# code, so if the COM interface ever changes, you can find the new interface quickly.