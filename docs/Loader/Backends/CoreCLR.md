# CoreCLR Backend

!!! info "Microsoft has a [guide for this][dotnet-hosting-guide]."

!!! note "Microsoft does not publish a statically linked library for this."

    However, after some editing to .NET sources [Reloaded-II][reloaded-ii-nethost]
    features a pre-built static lib for loading this runtime.

!!! warning "This backend is not available everywhere."

    For example, some platforms like a certain console with detachable controllers do not support this.

## Shipping the Runtime

!!! info "In Reloaded3, the Runtime is shipped as a regular Package (Mod) that the Backend mod depends on."

In the interest of making installation of Reloaded3 as easy as possible on:

- Users without admin privileges.
- Users on Linux and other WINE-supported platforms.

We will ship a full copy of the [.NET SDK][dotnet-sdk-download] as a Reloaded package and use it
from our mod.

### Packaging

!!! info ".NET Based Reloaded3 mods all set a dependency on `reloaded3.backend.coreclr` in the mod template."

The .NET Runtime package is shipped the following [package id(s)][package-id]:

- `reloaded3.backend.coreclr`: Latest .NET Runtime
- `reloaded3.backend.coreclr.nightly`: Nightly .NET Runtime (Daily Builds)

The main `reloaded3.backend.coreclr` packages contains all full and preview releases of the Runtime.

The nightly package `reloaded3.backend.coreclr.nightly` contains daily runtime versions, and is separate
from the main package to avoid spamming release versions.

### Runtime Version Selection

!!! info "To change runtime version, simply change the current version of the package."

If they want to test the latest .NET nightly version, simply enable the package
`reloaded3.backend.coreclr.nightly`, this will use the [Deprecation System][deprecation-system] to
override the main `reloaded3.backend.coreclr` package.

### Feature Selection

!!! into "The above mentioned packages are meta packages."

    We use the [Features][features] system to target the relevant package.

These meta packages use features to target the actual required packages with the use
[default auto-enabled features][default-features].

For example, if the features `win` and `x86` are set, the package `reloaded3.backend.coreclr.win-x86`
will be used.

## Runtime Version Resolution Strategy

!!! info "If the requested runtime is already installed, prefer the one on user's PC."

- The function `get_hostfxr_path` in [hosting guide][dotnet-hosting-guide]
will fail if this is not possible.
- This reduces physical RAM and improves load speeds.

If this is not possible, we load our own copy of the runtime.

- Use our own embedded in-mod copy of the .NET SDK.
- Pass folder path of the extracted SDK via `get_hostfxr_parameters.dotnet_root` to `get_hostfxr_path`.  [Documented Here.][native-hosting-locate-hostfxr]

!!! note "Note: These APIs are only supported in Core 3.X and above."

## Assembly Load Contexts

!!! note "We're using exactly same approach as Reloaded-II here."

!!! info "AssemblyLoadContext(s) Provide a way to load mods in isolation."

When loading individual mods in Reloaded3, we use a separate [AssemblyLoadContext][alc] for each mod.

This means that each mod can have its own dependencies. For example, Mod A can use `Library 12.0.0`,
while Mod B can use `Library 13.0.0` without conflict.

Implications of this include:

- `ModA` cannot use any code from `ModB`.
    - Mods can perform IL trimming to strip away unused code safely.
- If both `ModA` and `ModB` use `Library 12.0.0`, they will still be separate instances.
    - They will both be loaded in memory, and separately JIT'd. Costing RAM and JIT time.

### Dependency Injection

!!! tip "This explains how we conditionally break isolation to allow mods to communicate."

[Moved to its own subsection.][dependency-injection-api-docs]

### Use Case: I want mods to communicate without breaking isolation.

!!! info "Use the [Dependency Injection][dependency-injection-api-docs] mechanism described above."

Essentially it boils down to following:

- Producer creates `LibraryA` containing only interfaces unique to it and no dependencies.

```csharp
/// <summary>
/// Represents an individual scanner that can be used to scan for byte patterns.
/// </summary>
public interface IScanner : IDisposable
{
    /// <summary>
    /// Attempts to find a given pattern inside the memory region this class was created with.
    /// The method used depends on the available hardware; will use vectorized instructions if available.
    /// </summary>
    /// <param name="pattern">
    ///     The pattern to look for inside the given region.
    ///     Example: "11 22 33 ?? 55".
    ///     Key: ?? represents a byte that should be ignored, anything else if a hex byte. i.e. 11 represents 0x11, 1F represents 0x1F
    /// </param>
    /// <returns>A result indicating an offset (if found) of the pattern.</returns>
    PatternScanResult FindPattern(string pattern);
}
```

- Producer shares `LibraryA`.

```csharp
public class Exports : IExports
{
    public Assembly[] GetSharedAssemblies() => new[] { typeof(SomeTypeFromInterfacesDllToShare).Assembly };
}
```

```csharp
var _scanner_ = new Scanner(); // Implements IScanner
_injector.AddOrReplaceService<IScanner>(this, _scanner);
```

- Consumer uses `LibraryA`, and their instance at runtime is exactly same as producer's.

```csharp
_scanner = _injector.GetService<IScanner>();
```

For the exact details and caveats, please do read the docs.

### Use Case: I want to share a DLL Between Mods

!!! info "Sometimes you may want to share a DLL between mods."

!!! danger "Only share DLLs with stable APIs"

    Use [public API analyzer][api-analyzer] to ensure no breaking changes are made.

```csharp
public class Exports : IExports
{
    public Assembly[] GetSharedAssemblies() => new[] { typeof(SomeTypeFromDllToShare).Assembly };
}
```

To share a DLL, simply return the Assembly (DLL) you want to share as an export.

!!! danger "Remember, that this also shares all dependencies transitively."

    If `ModA` uses `Library 12.0.0` and `SomeTypeFromDllToShare` uses `Library 13.0.0`, then
    `ModA` will use `Library 13.0.0` as well.

    Extra special care must be taken to ensure that this does not happen. Therefore it's recommended
    that this functionality is used to share ONE DLL ONLY, and that DLL should have a stable API.

Breaking isolation is very, very heavily discouraged.

!!! warning "Log shared DLLs to console, to help with debugging."

## Ready To Run

!!! info "Mods which have a lot of code executed at startup may use `ReadyToRun` to reduce the startup time"

R2R is a file format that ships lower quality Tier0 native code alongside standard .NET IL code.

This reduces startup time by eliminating the need to JIT some code at boot time, but slightly
increases memory usage and DLL size.

More reading:

- [Conversation about ReadyToRun][conversation-about-r2r]
- [ReadyToRun Compilation][r2r-compilation]

## Assembly Trimming Support

!!! warning "Trimming framework-dependent code is ***not an officially supported .NET feature***"

    Trimming in Reloaded is a custom feature that uses existing .NET SDK components under the hood.
    This is made available by a custom [trimming target][trimming-target].

!!! danger "Incorrect use of trimming *can* and *will* break your mods."

    When using trimming you should test your mods thoroughly.

*Assembly trimming* allows you to remove unused code from your mods (and their dependencies), often
significantly shrinking the size of the generated DLLs. This in turn improves load times, download
size and runtime memory use.

In Reloaded-II, both loader itself and all 1st party mods use trimming.

### Testing Trimming

!!! info "Testing trimming is performed with included `BuildLinked.ps1` script."

    This is part of the Reloaded-II mod template, and will likely be part of Reloaded3's as well.

This script will fully wipe the mod output folder and build with trimming.
When the build is done, go test your mod.

Sample output:
```
Input Assembly: Reloaded.Hooks.Definitions [Mode: link]
Input Assembly: Reloaded.Mod.Interfaces [Mode: link]
Input Assembly: Reloaded.Hooks.ReloadedII.Interfaces [Mode: link]
Input Assembly: Reloaded.Mod.Template [Mode: link]
```

`link` indicates the assembly is being trimmed.
`` (empty) means trim if `IsTrimmable` == true, else use default trimmer setting [copy].

### Configuring Trimming

Trimming can be configured by modifying your `.csproj` file. The following properties can be used to control the trimming process.

| Reloaded Property      | Purpose                                                   | Replacement for.      |
| ---------------------- | --------------------------------------------------------- | --------------------- |
| ReloadedILLink         | Enables trimming at publish time.                         | PublishTrimmed        |
| ReloadedLinkRoots      | Specifies a DLL/Assembly to be preserved in its entirety. | TrimmerRootAssembly   |
| ReloadedLinkAssemblies | Specifies a DLL/Assembly to be force trimmed.             | ManagedAssemblyToLink |

Other officially supported properties can be used. For example you could supply an
[XML Root Descriptor][xml-root-descriptor] with `TrimmerRootDescriptor` for more granular control.

### Default Trimming Behaviour

!!! info "The default trimming behaviour used in Reloaded mods replicates the behaviour from .NET 6"

    And NOT .NET 7+. We instead choose to err on the side of caution.

The following general rules apply:

- Only assemblies marked `IsTrimmable` are trimmed by default.
- Default trimming mode (`TrimMode`) is `link` (remove unused assemblies + code).

### General Trimming Guidance

!!! tip

    This is general guidance from personal experience with developing Reloaded.

Doing the following steps is advised for enabling trimming:

- Build with `BuildLinked.ps1`.
- Add all assemblies with trim warnings to `ReloadedLinkAssemblies`.
- Build again and test.

!!! note

    If you have marked an assembly to not be trimmed with `ReloadedLinkAssemblies`, but it still displays a trim warning, feel free to ignore the warning.

Basic trimming now works.

#### Trimming the Remainder

To further optimise your mod, you can now force trimming on individual libraries.
To do so, perform the following.

- Inspect the build output:
```
# Sample Output
Input Assembly: Reloaded.Hooks.Definitions [Mode: link]
Input Assembly: Reloaded.Mod.Interfaces [Mode: link]
Input Assembly: Deez.Nutz.Library [Mode: copy]
```

- For each library where `Mode != link`.
  - Enable trimming for library (using `ReloadedLinkAssemblies`).
  - Build and test the mod.
  - If the mod does not run correctly, remove library from `ReloadedLinkAssemblies`.

## Reloaded II

!!! info "Declares how backwards compatibility with Reloaded-II APIs is handled."

!!! warning "Coming Soon"

A mod translates Reloaded-II APIs to Reloaded3 APIs. That's about it.

[alc]: https://learn.microsoft.com/en-us/dotnet/fundamentals/runtime-libraries/system-runtime-loader-assemblyloadcontext
[api-analyzer]: https://github.com/dotnet/roslyn-analyzers/blob/main/src/PublicApiAnalyzers/PublicApiAnalyzers.Help.md
[conversation-about-r2r]: https://devblogs.microsoft.com/dotnet/conversation-about-ready-to-run/
[default-features]: ../../Server/Features.md#default-features
[dependency-injection-api-docs]: ./CoreCLR-Dependency-Injection.md
[deprecation-system]: ../../Server/Load-Ordering.md#mods-can-deprecate-other-mods-by-overriding-dependencies
[dotnet-hosting-guide]: https://learn.microsoft.com/en-us/dotnet/core/tutorials/netcore-hosting
[dotnet-sdk-download]: https://dotnet.microsoft.com/en-us/download/dotnet/7.0
[features]: ../../Server/Features.md
[native-hosting-locate-hostfxr]: https://github.com/dotnet/runtime/blob/main/docs/design/features/native-hosting.md#locate-hostfxr
[package-id]: ../../Server/Packaging/Package-Metadata.md#id
[reloaded-ii-nethost]: https://github.com/Reloaded-Project/Reloaded-II/tree/master/source/Reloaded.Mod.Loader.Bootstrapper/nethost
[r2-alc]: https://reloaded-project.github.io/Reloaded-II/DependencyInjection_Consumer/
[r2r-compilation]: https://docs.microsoft.com/en-us/dotnet/core/deploying/ready-to-run
[trimming-target]: https://github.com/Reloaded-Project/Reloaded-II/blob/master/source/Reloaded.Mod.Template/templates/configurable/Reloaded.Trimming.targets
[xml-root-descriptor]: https://github.com/dotnet/linker/blob/main/docs/data-formats.md#descriptor-format