# CoreCLR Backend

!!! info "Microsoft has a [guide for this][dotnet-hosting-guide]"

!!! note "Microsoft does not publish a statically linked library for this."

    However, after some editing to .NET sources [Reloaded-II][reloaded-ii-nethost]
    features a pre-built static lib for loading this runtime.

!!! warning "This backend is not available everywhere."

    For example, some platforms like a certain console with detachable controllers do not support this.

## Version Resolution Strategy

If the requested CLR version is already installed, use the one already installed on user PC:

- The function `get_hostfxr_path` in [hosting guide][dotnet-hosting-guide]
will fail if this is not possible.
- This reduces physical RAM and improves load speeds.

Otherwise load our own copy of the runtime.

- Download copy of [.NET SDK][dotnet-sdk-download], and include it in our mod.
- Pass folder path of the extracted SDK via `get_hostfxr_parameters.dotnet_root` to `get_hostfxr_path`.  [Documented Here.][native-hosting-locate-hostfxr]

!!! note "Note: These APIs are only supported in Core 3.X and above."

## Assembly Load Contexts

!!! warning "Coming Soon"

## Ready To Run

!!! warning "Coming Soon"

## Reloaded II

!!! info "Declares how backwards compatibility with Reloaded-II APIs is handled."

!!! warning "Coming Soon"

[dotnet-hosting-guide]: https://learn.microsoft.com/en-us/dotnet/core/tutorials/netcore-hosting
[dotnet-sdk-download]: https://dotnet.microsoft.com/en-us/download/dotnet/7.0
[native-hosting-locate-hostfxr]: https://github.com/dotnet/runtime/blob/main/docs/design/features/native-hosting.md#locate-hostfxr
[reloaded-ii-nethost]: https://github.com/Reloaded-Project/Reloaded-II/tree/master/source/Reloaded.Mod.Loader.Bootstrapper/nethost