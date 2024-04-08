# Dependency Injection (CoreCLR Backend)

!!! tip "This explains how we conditionally break isolation to allow mods to communicate in the [CoreCLR Backend][coreclr-backend]."

We do this by selectively sharing instances of `Assemblies` (DLLs), between mods.

Mods can nominate which `Assemblies` (DLLs) they wish to share with other mods. If a mod contains
an assembly it wishes to share, the backend will:

- Load that mod.
- Load the shared assemblies into a shared `AssemblyLoadContext`.
- Unload the mod.

When the Publisher and Subscriber mods are then loaded, the backend will force both of them to
use the already loaded `Assembly` instance from the **shared** `AssemblyLoadContext`.

Thus both mods operate on the same instance of the `Assembly`.

## Step by Step Walkthrough

![Example][dependency-injection-internal]

1. Gathering Shared Assemblies
    1. Backend loads `Redirector` (Publisher).
    2. Backend loads all shared Assemblies into Shared `AssemblyLoadContext`.
    3. Backend unloads `Redirector` (Publisher).

2. Loading Mods
    1. Backend loads `Redirector`, sharing its own `Assemblies` with itself (from 1.b).
    2. Backend loads `RedirectorMonitor` (Consumer).
        1. `RedirectorMonitor` specified `Redirector` in its `ModDependencies` field.
        2. Therefore Backend shares all of `Redirector`'s exports with `RedirectorMonitor`.
 
3. Executing Mods
    1. ***Mod Loader*** rearranges mod load order to account for mod dependencies.
    2. `Redirector` code executes. Redirector publishes `IRedirector` (from Reloaded.Mod.Interfaces.IRedirector.dll) to Backend.
    3. `Monitor` code executes. Monitor obtains `IRedirector` from Backend.

## API Documentation

!!! info "This is the user facing API documentation for this feature."

    To be pasted to actual Reloaded3 docs (not this specification), once production begins.

The technical details will stay here, while text below will go to Reloaded3 docs once finalized.

### How it Works

!!! info "A publisher and subscriber share a common DLL containing only interfaces and no dependencies."

The concept is that the [backend mod][coreclr-backend] acts as a middleman between .NET mods.

This middleman allows mods to communicate by passing implementations of interfaces between each other.

An illustration:

![Example][dependency-injection]

*An example with Reloaded-II's [File Redirector][file-redirector].*

- Mod A (Redirector) publishes an interface `IRedirector` to the Mod Loader.
- Mod B (Other Mod) asks the Mod Loader for the `IRedirector` interface.

This is done via the backend mod's `IDependencyInjector`interface.

### How to Consume Services

!!! note "A specific mod load order is ***not*** required when consuming services."

Reloaded will [automatically rearrange load order][load-ordering] when required to ensure
dependencies are loaded before their consumers without affecting the order of other mods.

#### Set a Dependency on the Other Mod

!!! tip "First, set a dependency on the mod whose API you want to consume."

To do this, update your Mod Configuration,
to include the id of the mod you are consuming.

#### Add NuGet Reference to Other Mod

Every mod that publishes an interface will have something called an `Interfaces` library,
which contains a collection of all the interfaces that the mod publishes.

By convention, this library is usually named `<ModId>.Interfaces` and comes in the form of a NuGet package.

Examples (Reloaded-II):

- [Reloaded Hooks Shared Lib][hooks-shared-lib] [(NuGet)][reloaded-shared-lib-nuget]
- [Memory SigScan Shared Lib][reloaded-sigscan]  [(NuGet)][reloaded-sigscan-nuget]

#### Consume Services

Use the `IDependencyInjector` API to get an instance of the interface you want to consume.
This interface should be available at the entry point (`Start`) of the mod you are consuming.

```csharp
WeakReference<IRedirector> _redirector;
void GetService()
{
    _redirector = _injector.GetService<IRedirector>();
}
```

✅ Always check the service is valid and hasn't been disposed before usage.
```csharp
void DoSomethingWithService()
{
    // If the mod we got IRedirector from is unloaded, `TryGetTarget` will fail.
	if (_redirector != null && _redirector.TryGetTarget(out var redirector))
    {
        // Do something with `redirector`
    }
}
```

#### Life Cycle & Disposal

!!! info "Some Reloaded mods support real-time loading and unloading."

    As such, you must be careful with how you consume interfaces from other mods.

!!! note "You can find out if a mod is unloadable by checking that mod's config file."

In order to ensure unloading of publishers can correctly happen in the runtime, Reloaded uses "Weak References" (`WeakReference<T>`).

Here is guidance on how to use them:

✅ Storing Weak References on the Heap is OK
```csharp
WeakReference<IRedirector> _reference;
void AcquireService()
{
	_reference = _injector.GetService<IRedirector>();
}
```

✅ Storing referenced objects on the Stack is OK
```csharp
void AcquireService()
{
	IRedirector redirector = _injector.GetService<IRedirector>().Target;
    // redirector is no longer referenced outside of the scope of the method.
}
```

❌ Storing referenced objects on the Heap is NOT OK.
```csharp
IRedirector _redirector;
void AcquireService()
{
	_redirector = _injector.GetService<IRedirector>().Target;
    // This prevents the mod loader from being unable to dispose the service.
}
```

### How to Publish Services

!!! info "Publishing Services in Reloaded is done through something called `Interfaces` libraries."

`Interfaces` libraries are simply libraries that contain interfaces exposing a mod's public API.

!!! danger "These libraries should not contain any external dependencies."

    Unless you really, really know what you're doing.

#### Create an Interfaces Library

Create a separate `Class Library` project in your solution named, `<YOUR_MOD_ID>.Interfaces` (by convention).

Add a `Project Reference` from to this new library in your main mod.

Your `Solution Explorer` (or equivalent) should look something like this:

![][project-dependency]

##### Create a NuGet Package

!!! warning "Once you upload a package to NuGet.org, you cannot delete it"

    You can only hide it from search results.

To make your interfaces library more accessible, it is preferable to make it a NuGet package
and publish it to NuGet.org.

To do so, add and fill the following lines to your interface project's `.csproj` file (inside the first `PropertyGroup`):

```xml
<!-- Create NuGet Package and include your Documentation/comments inside. -->
<GenerateDocumentationFile>true</GenerateDocumentationFile>
<GeneratePackageOnBuild>True</GeneratePackageOnBuild>

<!-- Set to the same as your project name/namespace -->
<PackageId>Your.Namespace.Here.Interfaces</PackageId>

<!-- Use Semantic Versioning -->
<Version>1.0.0</Version>
<Authors>YourNameHere</Authors>

<!-- Description of your Package -->
<Description>Description of your mod.</Description>

<!-- Link to your Source Code [GitHub Page, etc.] -->
<PackageProjectUrl></PackageProjectUrl>
<RepositoryUrl></RepositoryUrl>

<!-- URL to the icon seen for your package in NuGet Search -->
<PackageIconUrl>https://avatars1.githubusercontent.com/u/45473408</PackageIconUrl>

<!-- SPDX License Identifier: https://spdx.org/licenses/ -->
<PackageLicenseExpression>LGPL-3.0-or-later</PackageLicenseExpression>
<PackageRequireLicenseAcceptance>True</PackageRequireLicenseAcceptance>
```

Then build the project in `Release` mode.

When you build the interfaces project, you should now see an accompanying `.nupkg` file in the `bin` folder.
You can then upload this file to NuGet.org.

!!! note

    If you are using an IDE like Visual Studio, you'll most likely be able to edit these properties from a `Properties` / `Project Settings` window.

#### Create Interfaces

Create the interfaces for each of the public APIs that you wish to expose to other mods.

A quick way to do this (in many IDEs) is to hover your text cursor over a class name and apply the `Extract Interface` Quick Fix/option.

![][extract-interface]

An example interface:

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

!!! danger "Your interfaces library SHOULD NOT contain any external references/NuGet packages/3rd party libraries."

    You risk breaking others' mods if they end up using the same libraries.

#### Publish the Interfaces Library

All that's left is for you to publish the interfaces library.
To do this, two steps are required.

##### Export the Interfaces

Create a class which inherits from `IExports`.
In `GetTypes`, return an array of interfaces to be consumed by other mods.

```csharp
public class Exports : IExports
{
    // Export the DLL with `IScanner` inside.
    public Assembly[] GetSharedAssemblies() => new[] { typeof(IScanner).Assembly };
}
```

##### Share it with Backend

During initialization (`Mod.cs`), register your interface with the Backend using the `IModLoader` instance.

```csharp
void PublishInterface()
{
    var scanner = new Scanner(); // Implements IScanner
    _injector.AddOrReplaceService<IScanner>(this, scanner);
}
```

#### Disposing (Publisher)

Reloaded will automatically dispose your services when your mod is unloaded.
You can however, still manually (if desired) dispose/replace your dependency instances with the `RemoveService` method.

```csharp
void Unload()
{
    _injector.RemoveService<IScanner>();
}
```

#### Upgrading Interfaces

!!! tip "The [Public API Analyzer][public-api-analyzer] is very highly recommended."

    When combined with source control, e.g. 'git' it will help you keep track of the APIs your mod exposes.

You are free to **ADD** anything to your existing interfaces at any time.

However, after you publish an interface, you should **NEVER**:

- Remove any parts of it.
- Change any existing parts of it (names, parameters).

Failure to do so will break any mods which use those methods.

#### Examples (Reloaded-II)

The following (Reloaded-II) mods can be used as examples.

**Universal Mods**

- [Reloaded Universal File Redirector][reloaded-file-redirector]
    - Producer: `Reloaded.Universal.Redirector`
    - Contract: `Reloaded.Universal.Redirector.Interfaces`
    - Consumer(s): `Reloaded.Universal.Monitor`, `Reloaded.Universal.RedirectorMonitor`

**Application Specific**

- [Sonic Heroes Controller Hook][heroes-controller-hook] (Allows other mods to receive/send game inputs.)
    - Producer: `Riders.Controller.Hook`
    - Contract: `Riders.Controller.Hook.Interfaces`
    - Consumer(s): `Riders.Controller.Hook.Custom`, `Riders.Controller.Hook.XInput`, `Riders.Controller.Hook.PostProcess`

- [Sonic Riders Controller Hook][riders-controller-hook] (Allows other mods to receive/send game inputs.)
    - Producer: `Heroes.Controller.Hook`
    - Contract: `Heroes.Controller.Hook.Interfaces`
    - Consumer(s): `Heroes.Controller.Hook.Custom`, `Heroes.Controller.Hook.XInput`, `Heroes.Controller.Hook.PostProcess`

**Libraries as Dependencies**

- [PRS Compressor/Decompressor][prs-compressor]
- [Reloaded.Hooks (Function Hooking/Detour Library)][reloaded-hooks]

## TODO

- [ ] C# Template for `Interfaces` Library.
  - [ ] Including CI/CD Pipelines, like GitHub Actions, GitLab
- [ ] Add Link to 'Mod Configuration' Page when ready. [here](#set-a-dependency-on-the-other-mod)
- [ ] Add instructions on setting a dependency in Reloaded3. [here](#set-a-dependency-on-the-other-mod)
- [ ] Update Diagrams with Reloaded-III Examples.
- [ ] Update linked mods in [Add NuGet Reference to Other Mod](#how-to-use-library) with Reloaded-III Examples.
- [ ] Rename `IDependencyInjector` (based on feedback).
- [ ] Show which field to check in [Life Cycle & Disposal](#life-cycle--disposal) for determining if unloadable.

[coreclr-backend]: ./CoreCLR.md#assembly-load-contexts
[dependency-injection]: ../../Images/DependencyInjection.png
[dependency-injection-internal]: ../../Images/DependencyInjection-Internal.png
[extract-interface]: ../../Images/ExtractInterface.png
[file-redirector]: https://github.com/Reloaded-Project/reloaded.universal.redirector
[heroes-controller-hook]: https://github.com/Sewer56/Heroes.Controller.Hook.ReloadedII
[hooks-shared-lib]: https://github.com/Sewer56/Reloaded.SharedLib.Hooks.ReloadedII
[load-ordering]: ../../Server/Load-Ordering.md
[project-dependency]: ../../Images/ProjectDependency.png
[prs-compressor]: https://github.com/Sewer56/Reloaded.SharedLib.Csharp.Prs.ReloadedII
[public-api-analyzer]: https://github.com/dotnet/roslyn-analyzers/blob/main/src/PublicApiAnalyzers/PublicApiAnalyzers.Help.md
[reloaded-file-redirector]: https://github.com/Reloaded-Project/Reloaded.Mod.Universal.Redirector
[reloaded-hooks]: https://github.com/Sewer56/Reloaded.SharedLib.Hooks.ReloadedII
[reloaded-shared-lib-nuget]: https://www.nuget.org/packages/Reloaded.SharedLib.Hooks
[reloaded-sigscan]: https://github.com/Reloaded-Project/Reloaded.Memory.SigScan
[reloaded-sigscan-nuget]: https://www.nuget.org/packages/Reloaded.Memory.SigScan.ReloadedII.Interfaces
[riders-controller-hook]: https://github.com/Sewer56/Riders.Controller.Hook