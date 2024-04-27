# Programmer Usage

!!! warning "The presented API is just for reference."

    It may be modified ahead of release.

## Using the API

The Redirector uses [Reloaded Dependency Injection](https://reloaded-project.github.io/Reloaded-II/DependencyInjection_HowItWork/) to expose an API.

To use the Redirector API:

1. Add the `Reloaded.Universal.Redirector.Interfaces` NuGet package to your project.

2. Add the dependency `reloaded.universal.redirector` to `ModDependencies` in your `ModConfig.json`.

3. In your `Mod()` entry point, acquire the Controller:

```csharp
IRedirectorController _redirectorController;

public void Start(IModLoaderV1 loader)
{
    _redirectorController = _modLoader.GetController<IRedirectorController>();
}
```

## IRedirectorController API

The `IRedirectorController` interface provides the following methods:

- `AddRedirect(string oldPath, string newPath)`: Redirects an individual file path.

- `RemoveRedirect(string oldPath)`: Removes redirection for an individual file path.

- `AddRedirectFolder(string folderPath)`: Adds a new redirect folder. Files in this folder will overlay files in the game directory.

- `AddRedirectFolder(string folderPath, string sourceFolder)`: Adds a new redirect folder with a custom source folder. Files in `folderPath` will overlay files in `sourceFolder`.

- `RemoveRedirectFolder(string folderPath)`: Removes a redirect folder.

- `RemoveRedirectFolder(string folderPath, string sourceFolder)`: Removes a redirect folder with a specific source folder.

- `GetRedirectorSetting(RedirectorSettings setting)`: Gets the current value of a redirector setting. See RedirectorSettings enum for options.

- `SetRedirectorSetting(bool enable, RedirectorSettings setting)`: Enables or disables a specific redirector setting.

- `Enable()` / `Disable()`: Enables or disables the redirector entirely.

## Examples

Redirect an individual file:

```csharp
_redirectorController.AddRedirect(@"dvdroot\bgm\SNG_STG26.adx", @"mods\mybgm.adx");
```

Add a new redirect folder:

```csharp
_redirectorController.AddRedirectFolder(@"mods\mymod");
```

Print file redirections to console:

```csharp
_redirectorController.SetRedirectorSetting(true, RedirectorSettings.PrintRedirect);
```