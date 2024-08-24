!!! info "This describes the format of the [.nx files][location] containing packed loadouts."

Reloaded3 uses the [NX (Nexus) Archive format][nx-format] to pack loadout files.

This is a minimal archive format that I (Sewer56) designed, created and implemented for high performance
storage of mods.

With some tweaks, it can also be used as an incredibly lightweight archive format for storing minimal
data like loadouts.

### Packing Configuration

The loadout files are packed using the NX format with the following configuration:

- All padding between files is removed to maximize space efficiency.
- Hashing is disabled for further optimization.
- Everything is packed into a single SOLID block.

!!! note "Implementation Status"

    Both of these features are *not yet* implemented in the NX Archive Format.
    They are however planned.

These will be present in a future native port of the library.

### Packed Files

The following tree structure represents the files included in the packed .nx archive:

```
├── header.bin
├── events.bin
├── timestamps.bin
├── commit-parameter-types.bin
├── commit-parameters-versions.bin
├── commit-parameters-lengths-8.bin
├── commit-parameters-lengths-16.bin
├── commit-parameters-lengths-32.bin
├── commit-parameters-text.bin
├── commit-parameters-timestamps.bin
├── commit-parameters-backrefs-8.bin
├── commit-parameters-backrefs-16.bin
├── commit-parameters-backrefs-24.bin
├── commit-parameters-backrefs-32.bin
├── commit-parameters-lists.bin
├── config.bin
├── config-data.bin
├── external-config.bin
├── external-config-data.bin
├── external-config-paths.bin
├── external-config-refs.bin
├── package-ids.bin
├── package-versions-len.bin
├── package-versions.bin
├── stores.bin
├── store-data.bin
└── commandline-parameter-data.bin
```

!!! note "Additional Files"

    The packed archive may include more files if the unpacked loadout structure is updated.
    Always refer to the latest [Unpacked.md][unpacked] documentation for the most up-to-date file list.

[location]: ../About.md#location
[nx-format]: https://nexus-mods.github.io/NexusMods.Archives.Nx/
[unpacked]: ./Unpacked.md