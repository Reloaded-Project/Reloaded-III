!!! info "This page describes the logic performed to generate and apply delta patches."

## Applying Deltas

!!! info "The delta update logic is as follows."

1. Check all [`PatchSources`][PatchSources] and [`FilesToCopy`][FilesToCopy] against existing files.
    - Find item in [File Hash Cache] with same hash.
        - ***Abort if not found.***
    - Check hash of actual file obtained from [File Hash Cache].
        - If file on disk has same write time, use cached hash.
        - If file has different write time, recompute the hash. ***Don't update cache however!!***
        - ***Abort if hash mismatches.***
    - Get file path to file with hash.

2. Apply delta patches for all files.
    - Writing them directly to temp directory.

3. Extract all files in [`FilesToExtract`][FilesToExtract] to temp directory.
    - Find file in archive by matching hash.

4. Copy all files in [`FilesToCopy`][FilesToCopy] to temp directory.
5. Rename temp directory to output directory.

!!! danger "In order to prevent data loss, the ***delta update logic will NOT run in place***."

    In the case of sudden termination of the process or power loss, the original folder
    must remain unchanged. Therefore the output will always be to a new directory, then
    we'll simply swap the directories once operation is complete.

    Temp directory should be on the same mount as the output directory, ideally in parent folder.

## Generating Deltas

!!! info "These are the steps to generate a single delta patch."

This follows a 3 step process:

1. [Pack New Version]
2. [Get Previous Versions]
3. [Process Files]

Intermediate `.patch` files (patches) are stored in RAM.
<!-- TODO: For embedded devices we want disk too -->

### Pack New Version

!!! info "Pack the `NewVersion` of the mod (non-delta)."

This can be used as the reference `.nx` file from which we source the data in the later steps.

This is useful, because the packing step also provides us with ***hashes*** of the final files (for free),
and ***pre-compressed data*** (for [Repacking][nx-repacking] feature of `.nx`) to accelerate the
delta generation process.

### Get Previous Version(s)

!!! info "Obtain the previous versions to create deltas from."

User should be able to select the previous versions they wish to create deltas from.

The original inputs can be sourced from:

- Disk (if [File Hash Cache] matches disk state)
- Download (otherwise)

### Process Files

!!! info "Process all files to we need to generate"

    Each file has a 'state' which can be one of the following:

    - Unprocessed
    - Processed

***For each delta to generate do the following.***

Iterate over all of the files in `NewVersion`.

- If the file is in the `Original` mod folder and is the same, add it to the copy list.
    - **Mark** the file as **Processed**.

- Else If the file is not the same, generate a patch for it.
    - GetOrCreate patch for `original` -> `new` file.
        - If a patch was already made for `hash(original)` then reuse it.
        - By appending to `PatchTargetPaths` list for that specific patch.
    - Link the generated patch to the `original` file hash, for all output files.
    - **Mark** the file as **Processed**.

Then iterate again, to cover remaining files:

- If the file is new (not in `Original` folder), add it to the extract list.
    - **Mark** the file as **Processed**.

Now all files should be processed.

!!! info "Now you can generate the [delta header] and pack the delta files."

## Delta Patch Format

!!! info "There are many formats with which you can generate deltas."

    Which do we use?

I've tried several formats:

- [VCDiff]: Good for general purpose.
- [HDiffPatch]: Extremely competitive, low memory footprint.
- [xdelta3]: General purpose, sacrifices ratio for speed.
- [ZStandard Patching Engine]: Very fast decompression.

After trying several solutions, I decided to use the [ZStandard Patching Engine]. [HDiffPatch] was
generally the best for executable data and used little memory. On the other hand, the
[ZStandard Patching Engine] was slightly better for binary data (e.g. 3D Model Files).

The main reason for going with ZStandard comes down to decompression speed. Decompression speed
on my machine was hitting around 1GiB/s, approximately double that of [HDiffPatch].

This also blends well with the fact that is simply the fact that the dependency is already in use
within the the `.nx` archive container; therefore it brings no additional dependency.

[delta header]: ./Archive-User-Data-Format.md#header-delta-update
[File Hash Cache]: ../../../Common/Hash-Cache/File-Format.md
[FilesToCopy]: ./Archive-User-Data-Format.md#copy-info
[FilesToExtract]: ./Archive-User-Data-Format.md#extract-info
[Get Previous Versions]: #get-previous-versions
[Hash Target Files]: #hash-target-files
[HDiffPatch]: https://github.com/sisong/HDiffPatch
[nx-repacking]: https://nexus-mods.github.io/NexusMods.Archives.Nx/Usage/#repacking
[Pack New Version]: #pack-new-version
[PatchSources]: ./Archive-User-Data-Format.md#patch-info
[Process Files]: #process-files
[VCDiff]: https://github.com/google/open-vcdiff
[xdelta3]: https://github.com/jmacd/xdelta.git
[zstd-patch-from]: https://github.com/facebook/zstd/issues/2835
[ZStandard Patching Engine]: https://github.com/facebook/zstd/wiki/Zstandard-as-a-patching-engine