!!! info "States how Reloaded3 Package Extends the [NX Archive Format via User Data][nx-user-data]"

## Data Types

- `String8` is assumed to be a 1 byte length prefixed UTF-8 string.
- `Align4` pads the data to the next 4 byte boundary.
- `Align8` pads the data to the next 8 byte boundary.

If the offset is already aligned, no padding is added.
The byte `00` is recommended for padding.

## Header (Standard)

!!! info "The user data format for standard packages has an [Extension ID] of `R3PK`"

    This is `0x5233504B` in big endian. For `Reloaded3PacKage`.

- `u8`: Version
- `String8`: [Package ID]
- `String8`: [Package Version]

## Header (Delta Update)

!!! info "The user data format for standard packages has an [Extension ID] of `R3DT`"

    This is `0x52334454` in big endian. For `Reloaded3DelTa`.

The ***header*** is the following:

- `u8`: Version
- `String8`: [Package ID]
- `String8`: [Package Version]
- `String8`: [Previous Package Version][Package Version]

### Patch Info

!!! info "Immediately follows the header."

First part lists the number of items which follow:

- `Align4`
- `u32`: NumPatches

- `u32[NumPatches]`: [PatchFileIndices]
- `Align8`
- [`XXH3[NumPatches]`][xxh3]: [PatchSources]
- `u32[NumPatches]`: [PatchTargetCounts]
- `String8[NumPatchTargets]`: PatchTargetPaths

!!! info "`NumPatchTargets` is calculated by summing all values of `PatchTargetCounts`."

The `PatchTargetPaths` are the paths of all files.

!!! example "An example"

    ```
    NumPatches: 3
    PatchTargetCounts: [2, 1, 3]
    PatchTargetPaths: [
        "textures/armor.dds",
        "textures/armor_normal.dds",
        "scripts/main.lua",
        "models/character.nif",
        "models/weapon.nif",
        "models/shield.nif"
    ]
    ```

    1. The output of `PatchSources[0]` + `PatchFileIndices[0]` produces 2 files:
        - "textures/armor.dds"
        - "textures/armor_normal.dds"

    2. The output of `PatchSources[1]` + `PatchFileIndices[1]` produces 1 file:
        - "scripts/main.lua"

    3. The output of `PatchSources[2]` + `PatchFileIndices[2]` produces 3 files:
        - "models/character.nif"
        - "models/weapon.nif"
        - "models/shield.nif"

#### PatchFileIndices

!!! info "These are the 0 based indexes of the patch files as they appear in the `NX` archive."

This is an array of `u32` values.

A value of 0 means the first file in the archive's file entries.

#### PatchSources

!!! info "These are the hashes of the source files"

The PatchSources and [PatchFileIndices] form tuples.

So `PatchSources[0]` has the hash of the file from the previous version of the package that
you should apply the patch at `PatchFileIndices[0]` to.

To find the original file, we check the original mod folder and find the file with the
corresponding [XXH3] hash using the [File Hash Cache].

#### PatchTargetCounts

!!! info "Each [PatchSources] and [PatchFileIndices] tuple can output multiple files."

When there are duplicate files in the new version of the package, we can reuse a pre-generated
patch for them. In this case, the `PatchTargetCounts` will be greater than 1; as this is the number
of files that the `source+patch` output will output to.

##### PatchTargetPaths

!!! info "These are the relative paths of the files that the [PatchSources] and [PatchFileIndices] tuples will output to."

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

## Discovering Deltas

!!! info "Deltas can be discovered by using the [Central Server]'s [Download Information API]."

To determine if you can apply the patch, use the [Delta Verification API].

[Central Server]: ../../../Services/Central-Server.md
[Delta Verification API]: ../../../Services/Central-Server.md#delta-verification-api
[Download Information API]: ../../../Services/Central-Server.md#download-information
[Extension ID]: https://nexus-mods.github.io/NexusMods.Archives.Nx/Specification/User-Data/#extensions
[Extract Info]: #extract-info
[File Hash Cache]: ../../../Common/Hash-Cache/File-Format.md
[nx-user-data]: https://nexus-mods.github.io/NexusMods.Archives.Nx/Specification/User-Data/
[Package ID]: ../Package-Metadata.md#id
[Package Version]: ../Package-Metadata.md#version
[Patch Info]: #patch-info
[PatchFileIndices]: #patchfileindices
[PatchSources]: #patchsources
[PatchTargetCounts]: #patchtargetcounts
[xxh3]: ../../../Common/Hashing.md#stable-hashing-for-large-data-with-many-files