<div align="center">
	<h1>Reloaded3 File Emulation Framework</h1>
	<img src="../Images/Icon.png" Width=200/><br/>
	<strong>🎈 Let's screw with binaries 🎈</strong>
    <p>A framework for creating virtual files at runtime.</p>
</div>

## About The Framework

!!! note "[This is Reloaded-II's FileEmulationFramework documentation, but in Rust][r2-fef]."

The file emulation framework is a framework for intercepting Operating System API calls related to the
reading of files from disk; in order to trick games into loading files that don't really exist.

It builds on top of previous experiments with Reloaded-II:

- [Reloaded-II FileEmulationFramework][r2-fef]: The reimagining and original C# implementation of this.
- [Persona 4 Golden (32-bit) PC modloader][p4gpc-modloader]: The slightly improved derivative.
- [ONE Redirector][one-redirector]: The other original.
- [AFS Redirector][afs-redirector]: The original.

## A User Friendly Example

Replacing files inside big archives without creating new ones.

![][afs-example]

![][afs-original-file]

In this case, the following files would replace the 7th, 8th, 9th and 10th file in the
`SH_VOICE_E.afs` archive.

## How It Works

!!! tip "By hooking API calls used to open files, get their properties and read from them, we can create files 'on the fly'"

This allows us to perform various forms of post processing such as merging archives in a way
where we require zero knowledge of the application (game) running under the hood.

!!! note "File Emulation therefore works with just about anything."

	This includes regular tools/programs reading files, and even emulators.<br/>
	As long as the emulated file you output is understood by the target applicetion.

Projects using this framework are referred to as 'emulators' hence the name `File Emulation Framework`.

This is because they simulate files that don't really exist on disk.

## When to Use File Emulation

!!! tip "Use File Emulation rather than [Merged File Cache][merged-file-cache] if all/most following criteria hold true"

- Emulated Files are Large (>32MB)
- Emulated Files don't have many small (<1MB) files from many sources
- Generated file can reuse existing data in existing files. (e.g. chunks of existing file/archive)

For more info, see [Read Performance of SOLID Files][read-performance].

## Performance Impact

!!! tip "In most use cases, emulators have negligible performance impact."

All numbers listed here are on a 5900X with CL16 3000MHz RAM.
Numbers below are for original C# implementation, Rust will improve some things very slightly.

Performance varies with a lot of factors, including...

### File Open Time

!!! tip "Usually first access to an emulated file may be delayed for a small amount of time"

In the original C# emulators, this is:

- `0.5ms` - `1ms` per emulated file for most realistic inputs.

In addition, the original .NET implementations will roughly have:

- `1ms` JIT time, for creating first emulated file of a given type

This will improve a bit in Rust, since JIT time is not a factor and we get a high quality
compilation off the bat, rather than tiered JIT compilation.

### Read Overhead

!!! tip "Read speed/overhead is negligible in most cases."

A single typical read operation involves the following:

- A dictionary lookup to find emulated file.
	- `8ns`, constant.
	- This will be faster in Rust, because Swisstable (Hashbrown) is faster.

- A binary search to determine correct stream/source for the data to be read.
    - `2.5ns` - `5.5ns` for typical files (under 64 streams).
        - Example: Inject a few textures into a texture archive.
    - or `35ns` for a read of a huge file with 16384 streams.
        - Example: Replace 25% of a 65536 file archive.

- Remaining code/other overheads.
    - Approx `1` - `2ns`, constant.

Generally sub `15ns` overhead for each read call in existing implementation.
And `8ns` for non-emulated files.

For non-SOLID archives, the original use case for this framework, this is basically it.
Completely negligible.

!!! warning "For files that are read entirely in 1 go, with multiple sources, additional caveats apply."

	Load performance may improve or degrade depending on storage medium used.<br/>
	For more information, see [Read Performance of SOLID Files][read-performance].

## Credits, Attributions

- Header icon created by <a href="https://www.flaticon.com/free-icons/settings" title="settings icons">Freepik - Flaticon</a>

[afs-example]: ./Images/Afs/Afs-Example.png
[afs-original-file]: ./Images/Afs/Afs-Original-File.png
[afs-redirector]: https://github.com/Sewer56/AfsFsRedir.ReloadedII
[merged-file-cache]: ../../Libraries/Merged-File-Cache/About.md
[one-redirector]: https://github.com/Sewer56/Heroes.Utils.OneRedirector.ReloadedII
[p4gpc-modloader]: https://github.com/tge-was-taken/p4gpc.modloader
[r2-fef]: https://sewer56.dev/FileEmulationFramework/
[read-performance]: ./Read-Performance.md