# CoreCLR Backend

!!! info

    Microsoft has a [guide for this](https://learn.microsoft.com/en-us/dotnet/core/tutorials/netcore-hosting).

!!! note

    Microsoft does not publish a statically linked library for this; however, after some editing to .NET sources
    [Reloaded-II](https://github.com/Reloaded-Project/Reloaded-II/tree/master/source/Reloaded.Mod.Loader.Bootstrapper/nethost)
    features a pre-built static lib for loading this runtime.

!!! warning

    This backend is unavailable on `Switch`.

## Version Resolution Strategy

If the requested CLR version is already installed, use the one already installed on user PC:

- The function `get_hostfxr_path` in [hosting guide](https://learn.microsoft.com/en-us/dotnet/core/tutorials/netcore-hosting)
will fail if this is not possible.
- This reduces physical RAM and improves load speeds.

Otherwise load our own copy of the runtime.

- Download copy of [.NET SDK](https://dotnet.microsoft.com/en-us/download/dotnet/7.0), and include it in our mod.
- Pass folder path of the extracted SDK via `get_hostfxr_parameters.dotnet_root` to `get_hostfxr_path`.  [Documented Here.](https://github.com/dotnet/runtime/blob/main/docs/design/features/native-hosting.md#locate-hostfxr)

!!! note

    These APIs are only supported in Core 3.X and above.

## Assembly Load Contexts

!!! warning "Coming Soon"

## Ready To Run

!!! warning "Coming Soon"

## Reloaded II

!!! info "Declares how backwards compatibility with Reloaded-II APIs is handled."