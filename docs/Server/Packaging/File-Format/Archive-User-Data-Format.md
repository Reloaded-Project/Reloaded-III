!!! info "States how Reloaded3 Package Extends the [NX Archive Format via User Data][nx-user-data]"

!!! info ""

    This is shorthand for `Reloaded3PacKage`.

## Data Types

- `String8` is assumed to be a 1 byte length prefixed UTF-8 string.
- `Align4` pads the data to the next 4 byte boundary.
- `Align8` pads the data to the next 8 byte boundary.

If the offset is already aligned, no padding is added.
The byte `00` is recommended for padding.

## Header (Standard)

!!! info "The user data format for standard packages has an [Extension ID] of `R3PK`"

    This is `0x5233504B` in big endian. For `Reloaded3PacKage`.

- `String8`: [Package ID]
- `String8`: [Package Version]

## Header (Delta Update)

!!! info "The user data format for standard packages has an [Extension ID] of `R3DT`"

    This is `0x52334454` in big endian. For `Reloaded3DelTa`.

The ***header*** is the following:

- `String8`: [Package ID]
- `String8`: [Package Version]

### Patch Info

!!! info "Immediately follows the header."

First part lists the number of items which follow:

- `Align4`
- `u32`: NumPatches

After this is the `patch file indices` section:

- [PatchFileIndex[NumPatches]](#patchfileindex): PatchFileIndices

After this is the `patch source hashes` section:

- `Align8`
- [TargetCount[NumPatches]](#targetcount): PatchSources

!!! tip "The `PatchFileIndices` and `PatchSources` form tuples."

Then follows the `patch target count` section:

- [TargetCount[NumPatches]](#patchfileindex): PatchTargetCounts

And lastly are the patch targets:

- `String8[NumPatchTargets]`: PatchTargetPaths

The `NumPatchTargets` are calculated by summing all values of `PatchTargetCounts`.

Each member of `PatchTargetCounts` represents the number of output files for the corresponding
[PatchSource] and [PatchFileIndex] tuple. This allows to

The `PatchTargetPaths` are the paths of all files.

### Extract Info

!!! info "Immediately follows [Patch Info]"

    This is a list of files to extract from the `NX` archive to output directory raw.

    The files are extracted to paths that are the same as in the archive.

- `Align4`
- `u32`: NumFilesToExtract
- `u32[NumFilesToExtract]`: FilesToExtract

!!! tip "This is the list of files that's not in previous version but is in new version."

### Copy Info

!!! info "Immediately follows [Extract Info]"

    This is a list of files that need to be copied (verbatim) from the previous version
    of the package to the new version.

- `Align4`
- `u32`: NumFilesToCopy
- [XXH3[NumFilesToCopy]][xxh3]: FilesToCopy
- `String8[NumFilesToCopy]`: RelativeOutputPaths

### Data Types

#### TargetCount

!!! info "Represents the number of targets for a specified [PatchSource] and [PatchFileIndex] tuple."

This is a `u32` value.

#### PatchSource

!!! info "This structure contains the source file in the previous version of the package"

    The actual patch file is at [PatchFileIndex].

The structure has single member:

- [XXH3][xxh3]: SourceHash

We check the original mod folder and find the file with the corresponding [XXH3] hash
using the [File Hash Cache].

#### PatchFileIndex

!!! info "This structure contains the index of the patch file for the corresponding [Source Files](#patchsource)"

    The actual patch file is at [PatchFileIndex].

The structure has single member:

- `u32`: Index

## Delta Apply Logic

!!! info "The delta update logic is as follows."

1. Check all [`PatchSources`](#patch-info) and [`FilesToCopy`](#copy-info) against existing files.
    - Find item in [File Hash Cache] with same hash.
        - ***Abort if not found.***
    - Check hash of actual file obtained from [File Hash Cache].
        - If file on disk has same write time, use cached hash.
        - If file has different write time, recompute the hash. ***Don't update cache however!!***
        - ***Abort if hash mismatches.***
    - Get file path to file with hash.

2. Apply delta patches for all files.
    - Writing them directly to temp directory.

3. Extract all files in [`FilesToExtract`](#extract-info) to temp directory.
    - Find file in archive by matching hash.

4. Copy all files in [`FilesToCopy`](#copy-info) to temp directory.
5. Rename temp directory to output directory.

!!! danger "In order to prevent data loss, the ***delta update logic will NOT run in place***."

    In the case of sudden termination of the process or power loss, the original folder
    must remain unchanged. Therefore the output will always be to a new directory, then
    we'll simply swap the directories once operation is complete.

    Temp directory should be on the same mount as the output directory, ideally in parent folder.

## Discovering Deltas

Deltas can be discovered by using the [Central Server].

[Central Server]: ../../../Services/Central-Server.md
[nx-user-data]: https://nexus-mods.github.io/NexusMods.Archives.Nx/Specification/User-Data/
[Extension ID]: https://nexus-mods.github.io/NexusMods.Archives.Nx/Specification/User-Data/#extensions
[Package ID]: ../Package-Metadata.md#id
[Package Version]: ../Package-Metadata.md#version
[xxh3]: ../../../Common/Hashing.md#stable-hashing-for-large-data-with-many-files
[File Hash Cache]: ../../../Common/Hash-Cache/File-Format.md
[PatchSource]: #patchsource
[PatchFileIndex]: #patchfileindex
[Patch Info]: #patch-info
[Extract Info]: #extract-info