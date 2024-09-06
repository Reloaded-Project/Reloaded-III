!!! info "This describes the file format used to share packages in Reloaded3"

## Rationale

!!! tip "The following are some of the points to consider for the file format."

### Modularity

!!! info "Reloaded3 packages heavily encourage ***modularity***"

    That means breaking your big mod into smaller, focused mods.

This means creating separate mods for your individual music track, characters, stages,
or whatever you got going on. As opposed to a large monolithic mod.

With that in mind, it's generally ***expected for Reloaded3 packages to be under 20MB*** (uncompressed)
in size, ideally. The only notable exceptions are for ***stage/level mods, which may reach around 100MB***,
depending on texture size used.

***What this means*** is that even in the absence of [Delta Patching][delta-patching], ***grabbing an
update will not download many files that are not needed***.

### Package Structure

!!! info "A more-complex `Reloaded3` package looks something like this."

```
reloaded3.utility.examplemod.s56
├── config
│   └── config.toml
├── languages
│   ├── config
│   │   ├── en-GB.toml
│   │   └── uwu-en.toml
│   └── dll
│       ├── en-GB.toml
│       └── uwu.toml
├── modfiles
│   ├── redirector
│   │   └── skill-game-asset.bin
│   └── mod.dll
├── package
│   ├── docs
│   │   ├── changelog
│   │   │   └── 1.0.0.md
│   │   └── index.html
│   ├── images
│   │   ├── config-image-1.jxl
│   │   ├── skill-1.jxl
│   │   ├── skill-2.jxl
│   │   └── skill-3.jxl
│   ├── description.md
│   └── license.md
└── package.toml
```

A thing to consider noting here is that most of the files are already optimally compressed, i.e.
`JPEG XL` (`.jxl`) or are small (`.md`). The only big files to consider are those in the `modFiles`
directory, where the main mod content lies.

#### NxVFS

!!! info "Contents of `modFiles` may already be compressed due to `NxVFS` (TODO: Link Pending)"

NxVFS transforms a part of file tree from:

```
modfiles
├── vfs
│   └── redirector
│       └── skill-game-asset.bin
└── mod.dll
```

into

```
modfiles
├── redirector
│   └── skill-game-asset.bin
└── mod.dll
```

In this case, we should avoid recompressing the `.nx` archive.

## Packaging Solution

!!! info "R3 packages use the [NX (Nexus) Archive format][nx-format] as its native format for packaging."

This is a minimal archive format that I (Sewer56) designed, created and implemented for high performance
storage of mods.

Using following settings:

- Hashing: [XXH3].
- Compression: ZStandard
- Compression Level: 22
- Block Size: 16MB
- Padding: None
- `package.toml` and `config.toml` are ***NOT*** SOLID compressed.
    - This helps indexing in [Central Server].

!!! tip "Any inner `.nx` archives are ***NOT*** re-compressed."

!!! note "Implementation Status"

    XXH3 hashing is not yet implemented in NX Archive Format.
    Removing padding is also not yet implemented.

### Nx Over Zip

!!! info "Certain websites may be reluctant to allow the hosting of `.nx` archives."

!!! tip "To do this, we can wrap the `.nx` archives over `.zip` containers."

Recall that the `.zip` archive format is a list of the following:

```c
// Defines a file record
typedef struct {
    // Header for the file
    char     frSignature[4]; // 0x04034b50
    ushort   frVersion;
    ushort   frFlags;
    COMPTYPE frCompression;
    DOSTIME  frFileTime;
    DOSDATE  frFileDate;
    uint     frCrc;
    uint     frCompressedSize;
    uint     frUncompressedSize;
    ushort   frFileNameLength;
    ushort   frExtraFieldLength;
    if( frFileNameLength > 0 )
        char     frFileName[ frFileNameLength ];
    if( frExtraFieldLength > 0 )
        uchar    frExtraField[ frExtraFieldLength ];

    // Compressed data
    if( frCompressedSize > 0 )
        uchar    frData[ frCompressedSize ];

} ZIPFILERECORD;
```

With the file data being in `frCompressedSize`.

This effectively means that if you embed a single `.nx` archive named `data.nx` into a `.zip` file
and with no compression, you can expect the contained `.nx` archive to always start at offset 0x25.

We can exploit this, and use this to workaround upload restrictions.

!!! warning "Do not use this format for local disk access."

    Only for web access, `.nx` is specifically aligned to have blocks be multiple of 4096 to optimize
    for disk access. Therefore having misaligned files will cause performance issues.

!!! warning "Unaligned access on some CPU architectures may cause runtime errors."

    We will therefore name the file `data-r3.nx` instead. This will shift the start offset to `0x28`.
    That makes the start of the archive aligned on an 8 byte boundary.

[nx-format]: https://nexus-mods.github.io/NexusMods.Archives.Nx/
[XXH3]: https://github.com/Cyan4973/xxHash
[delta-patching]: ./Archive-User-Data-Format.md#header-delta-update
[Central Server]: ../../../Services/Central-Server/Online-API.md