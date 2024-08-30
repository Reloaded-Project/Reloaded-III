
!!! info "The Static CDN API provides offline access to package metadata, configurations, compatibility reports, and other essential information."

!!! info "The API is hosted on BackBlaze with CloudFlare CDN."

    Or directly on CloudFlare R2, we'll see when we get there.

The API uses a file structure designed to efficiently handle lookups for over 1 million packages, with packages split into multiple files based on the first three bytes of their XXH3 hash, calculated from the package ID.

!!! note "Hashes in this API are returned as little endian numbers"

    To convert to a string, use the hexadecimal representation of the number
    after converting to little endian.

## Lookup Process

To look up a package, translation, or other hash based data:

1. Calculate the XXH3 hash of the package ID.
2. Take the first two bytes of the hash.
3. Navigate to the corresponding directory based on the first byte and second byte.
4. Load the corresponding `.msgpack.zstd` file (or folder) within that directory.
5. Search for the package entry with the matching full hash within that file.

This file structure provides benefits such as scalability, fast lookups, and balanced distribution
of packages across files, while accommodating the potential for accessing around 16.8 million unique mods.

(In a manner where 1 file == 1 mod)

## Download Information API

Each `.msgpack.zstd` file in the `download-info` directory contains an array of package entries.

```
.
└── download-info
    ├── 00
    │   ├── 00
    │   │   ├── {packageIdHash}.msgpack.zstd
    │   │   ├── {packageIdHash}.msgpack.zstd
    │   │   ...
    │   │   └── {packageIdHash}.msgpack.zstd
    │   ├── 01
    │   │   ├── {packageIdHash}.msgpack.zstd
    │   │   ├── {packageIdHash}.msgpack.zstd
    │   │   ...
    │   │   └── {packageIdHash}.msgpack.zstd
    │   ...
    │   └── ff
    │       ├── {packageIdHash}.msgpack.zstd
    │       ├── {packageIdHash}.msgpack.zstd
    │       ...
    │       └── {packageIdHash}.msgpack.zstd
    ...
    └── ff
        ├── 00
        │   ├── {packageIdHash}.msgpack.zstd
        │   ├── {packageIdHash}.msgpack.zstd
        │   ...
        │   └── {packageIdHash}.msgpack.zstd
        ...
        └── ff
            ├── {packageIdHash}.msgpack.zstd
            ├── {packageIdHash}.msgpack.zstd
            ...
            └── {packageIdHash}.msgpack.zstd
```

Here's an example of the decoded MessagePack content:

```json
[
  {
    "packageIdHash": XXH3(UTF8(packageId)),
    "packageId": "reloaded3.utility.reloadedhooks.s56",
    "version": "1.1.0",
    "updateData": {
      "GameBanana": {
        "ItemType": "Mod",
        "ItemId": 408376
      },
      "GitHub": {
        "UserName": "Sewer56",
        "RepositoryName": "reloaded3.gamesupport.persona5royal"
      },
      "Nexus": {
        "GameDomain": "persona5",
        "Id": 789012
      }
    },
    "downloadInfo": [
      {
        "type": "GameBanana",
        "idRow": 610939,
        "fileSize": 1048576
      },
      {
        "type": "NexusMods",
        "uid": "7318624808113",
        "fileSize": 1048576
      },
      {
        "type": "GitHub",
        "userName": "Sewer56",
        "repositoryName": "persona5royal-modloader",
        "assetId": 160499684,
        "fileSize": 495
      }
    ],
    "deltaUpdates": [
      {
        "fromVersion": "1.0.0",
        "downloadInfo": [
          {
            "type": "GameBanana",
            "idRow": 610940,
            "fileSize": 102400
          },
          {
            "type": "NexusMods",
            "uid": "7318624808114",
            "fileSize": 102400
          },
          {
            "type": "GitHub",
            "userName": "Sewer56",
            "repositoryName": "persona5royal-modloader",
            "assetId": 160499685,
            "fileSize": 102400
          }
        ]
      }
    ]
  },
  ...
]
```

!!! note "Expect only contents for 1 package per file"

The contents of this API mirror those in the [Download Information] API, so use that API for reference.

## Package Metadata API

Each `.msgpack.zstd` file in the `package-metadata` directory contains an array of package entries.

```
.
└── package-metadata
    ├── 00
    │   ├── 00
    │   │   ├── {packageIdHash}.msgpack.zstd
    │   │   ├── {packageIdHash}.msgpack.zstd
    │   │   ...
    │   │   └── {packageIdHash}.msgpack.zstd
    │   ├── 01
    │   │   ├── {packageIdHash}.msgpack.zstd
    │   │   ├── {packageIdHash}.msgpack.zstd
    │   │   ...
    │   │   └── {packageIdHash}.msgpack.zstd
    │   ...
    │   └── ff
    │       ├── {packageIdHash}.msgpack.zstd
    │       ├── {packageIdHash}.msgpack.zstd
    │       ...
    │       └── {packageIdHash}.msgpack.zstd
    ...
    └── ff
        ├── 00
        │   ├── {packageIdHash}.msgpack.zstd
        │   ├── {packageIdHash}.msgpack.zstd
        │   ...
        │   └── {packageIdHash}.msgpack.zstd
        ...
        └── ff
            ├── {packageIdHash}.msgpack.zstd
            ├── {packageIdHash}.msgpack.zstd
            ...
            └── {packageIdHash}.msgpack.zstd
```

Here's an example of the decoded MessagePack content:

```json
[
  {
    "packageIdHash": XXH3(UTF8(packageId)),
    "packageId": "reloaded3.utility.reloadedhooks.s56",
    "version": "1.1.0",
    "packageToml": "Id = \"reloaded3.utility.reloadedhooks.s56\"\nName = \"Reloaded3 Hooking Library\"...",
    "configToml": "...",
    "languageFiles": [
      {
        "path": "languages/en-GB.toml",
        "data": "..."
      },
      {
        "path": "languages/fr-FR.toml",
        "data": "..."
      }
    ]
  },
  ...
]
```

## Translations API

Each `.msgpack.zstd` file in the `translations` directory corresponds to a single package.

```
└── translations
    ├── 00
    │   ├── 00
    │   │   ├── {packageIdHash}.msgpack.zstd
    │   │   ├── {packageIdHash}.msgpack.zstd
    │   │   ...
    │   ├── 01
    │   │   ├── {packageIdHash}.msgpack.zstd
    │   │   ├── {packageIdHash}.msgpack.zstd
    │   │   ...
    │   ...
    │   └── ff
    │       ├── {packageIdHash}.msgpack.zstd
    │       ├── {packageIdHash}.msgpack.zstd
    │       ...
    ...
    └── ff
        ├── 00
        │   ├── {packageIdHash}.msgpack.zstd
        │   ├── {packageIdHash}.msgpack.zstd
        │   ...
        ...
        └── ff
            ├── {packageIdHash}.msgpack.zstd
            ├── {packageIdHash}.msgpack.zstd
            ...
```

Here's an example of the decoded MessagePack content:

```json
[
  {
    "packageId": "reloaded3.utility.examplemod.s56.de",
    "languageCode": "de-DE",
    "friendlyName": "Deutsch (Deutschland)"
  },
  {
    "packageId": "reloaded3.utility.examplemod.s56.fr",
    "languageCode": "fr-FR",
    "friendlyName": "Français (France)"
  },
  ...
]
```

***Typical Use Cases:***

- Discover available translations for a package.
- Download and install translations for a package.

For more information on how translations are structured and added to packages, refer to the
[Adding Localisations][adding-localisations] documentation.

### Translation Packages API

!!! info "This API stores the raw `.nx` package files for translation mods"

The actual translation content is stored separately from the translation metadata for efficiency.

```
.
└── translation-data
    ├── 00
    │   ├── 00
    │   │   ├── {translationPackageIdHash}.nx
    │   │   ├── {translationPackageIdHash}.nx
    │   │   ...
    │   ├── 01
    │   │   ├── {translationPackageIdHash}.nx
    │   │   ├── {translationPackageIdHash}.nx
    │   │   ...
    │   ...
    └── ff
        ├── 00
        │   ├── {translationPackageIdHash}.nx
        │   ├── {translationPackageIdHash}.nx
        │   ...
        ...
        └── ff
            ├── {translationPackageIdHash}.nx
            ├── {translationPackageIdHash}.nx
            ...
```

Each `.nx` file is the full translation mod package.

This API only stores ***only*** packages under `1MiB`, which should hopefully
satisfy 100% of all text based translation mods. Otherwise you'll need to delegate
to the original site where the mod was uploaded.

!!! warning "If downloading from here results in failure, use the [Download Information] API to get the proper download sources."

## Compatibility Reports API

!!! tip "This is a backup endpoint and may contain slightly outdated compatibility reports"

    To get the latest values, query the server proper.
    This is just a fallback in case main server is dead.

    To save on costs, this is a backup updated every 24 hours.
    This makes for approx `256*30` -> `7680` files updated a month.

The compatibility reports are grouped by the first byte of the `packageId` hash
to efficiently handle updates for a large number of mods.

This allows us to update multiple mods in batch every time interval.

```
.
└── compatibility-reports
    ├── 00.msgpack.zstd
    ├── 01.msgpack.zstd
    └── fd.msgpack.zstd
    └── fe.msgpack.zstd
    └── ff.msgpack.zstd
```

Here's an example of the decoded MessagePack content:

```json
[
  {
    "packageId": "reloaded3.gamesupport.persona5royal.s56",
    "packageVersion": "1.0.1",
    "gameCompatibility": {
      "persona5royal": [
        {
          "gameVersionId": 1,
          "successCount": 42,
          "failureCount": 3
        },
        ...
      ],
      "persona4golden": [
        {
          "gameVersionId": 2,
          "successCount": 10,
          "failureCount": 1
        },
        ...
      ]
    }
  },
  {
    "packageId": "reloaded3.utility.reloadedhooks.s56",
    "packageVersion": "2.3.0",
    "gameCompatibility": {
      "sonicheroes": [
        {
          "gameVersionId": 2,
          "successCount": 20,
          "failureCount": 1
        },
        ...
      ]
    }
  },
  ...
]
```

!!! info "The `gameVersionId` field is sourced from the [Community Repository][community-repository-versions]."

## Search API

!!! note "This API does not have a hosted endpoint."

    This is a CDN only API.

!!! info "Retrieves the entire list of mods for a specific game"

    We download this and can then search locally.

The searchable mod data is grouped by the `game` prefix, which is the first part of the package ID
as declared in `Package-Metadata.md`. All mods with the same `game` prefix are stored within a
single `.msgpack.zstd` file.

```
.
└── search
    ├── game1.msgpack.zstd
    ├── game2.msgpack.zstd
    ...
    └── reloaded3.msgpack.zstd
```

In this structure, each `.msgpack.zstd` file represents a `game` prefix and contains an
array of searchable mod entries for all mods with that prefix.

Here's an example of the decoded MessagePack content for a `.msgpack.zstd` file:

```json
[
  {
    "packageId": "game1.mods.mod1.s56",
    "name": "Mod 1",
    "summary": "A cool mod for Game 1",
    "bannerImages": [
      {
        "imageHash": 1234567890,
        "resolutions": [
          {
            "width": 440,
            "height": 220
          },
          {
            "width": 880,
            "height": 440
          }
        ]
      }
    ]
  },
  {
    "packageId": "game1.mods.mod2.s56",
    "name": "Mod 2",
    "summary": "Another awesome mod for Game 1",
    "bannerImages": [
      {
        "imageHash": 2345678901,
        "resolutions": [
          {
            "width": 440,
            "height": 220
          },
          {
            "width": 880,
            "height": 440
          }
        ]
      }
    ]
  },
  ...
]
```

Each entry in the array represents a searchable mod and includes the following fields:

- `packageId`: The unique identifier of the mod package.
- `name`: The name of the mod.
- `summary`: A brief one-line summary of the mod, extracted from the mod metadata.
- `bannerImages`: An array of banner images for the mod.
    - `imageHash`: The XXH3 hash of the banner image, stored as an integer to minimize size.
    - `resolutions`: An array of available resolutions for the banner image.
        - `width`: The width of the image in pixels.
        - `height`: The height of the image in pixels.

### Banner Files

!!! info "All banner files are stored in a separate folder structure based on the XXH3 hash of the image."

    We use XXH3 here because MessagePack doesn't natively support 16 byte integers.
    Also to save space.

```
.
└── banner-files
    ├── 12
    │   └── 34
    │       ├── 1234{restofImageHash}
    │       │   ├── 0.jxl
    │       │   └── 1.jxl
    │       └── 1234{restofImageHash}
    │           ├── 0.jxl
    │           └── 1.jxl
    ├── 56
    │   └── 78
    │       ├── 5678{restofImageHash}
    │       │   ├── 0.jxl
    │       │   └── 1.jxl
    │       └── 5678{restofImageHash}
    │           ├── 0.jxl
    │           └── 1.jxl
    ...
```

The logic is same as in directories above. The only caveat is we now have a folder named after the hash, and multiple files inside of it.

For the file name, use the index of the array entry. So first entry is `0.jxl`, second entry is `1.jxl`, and so on.

!!! tip "See [Mod Metadata: Icon (Search)][mod-metadata-search-image] for more information."

### Searching Mods

To perform a search, users can follow these steps:

1. Download the `.msgpack.zstd` file for the desired `game` prefix from the static endpoint.
2. Decompress and load the `.msgpack.zstd` file into memory.
3. Perform local searches based on the desired criteria:
      - Mod Name: Search for mods whose `name` field contains the specified keywords.
      - Mod ID: Search for mods whose `packageId` field matches the specified ID.
      - Summary: Search for mods whose `summary` field contains the specified keywords.
4. Display the search results to the user, including the banner images.
      - To display a banner image, retrieve the banner file using the `imageHash` and `resolutions` array from the `bannerImages` field of the mod entry.
      - Load the appropriate banner file based on the user's display resolution.

By default, I recommend searching by substring. In Name and ModId. Summary can be opt in.

## Delta Verification API

!!! info "This API determines the information needed to determine if you are eligible to apply a delta update."

Each file contains a list of hashes that must exist in the previous version of the package.

If any file does not exist, you will be unable to apply the delta update.

### File Structure

```
.
└── delta-headers
    ├── 00
    │   ├── 00
    │   │   ├── {deltaHeaderHash}.bin
    │   │   ├── {deltaHeaderHash}.bin
    │   │   ...
    │   │   └── {deltaHeaderHash}.bin
    │   ├── 01
    │   │   ├── {deltaHeaderHash}.bin
    │   │   ├── {deltaHeaderHash}.bin
    │   │   ...
    │   │   └── {deltaHeaderHash}.bin
    │   ...
    │   └── ff
    │       ├── {deltaHeaderHash}.bin
    │       ├── {deltaHeaderHash}.bin
    │       ...
    │       └── {deltaHeaderHash}.bin
    ...
    └── ff
        ├── 00
        │   ├── {deltaHeaderHash}.bin
        │   ├── {deltaHeaderHash}.bin
        │   ...
        │   └── {deltaHeaderHash}.bin
        ...
        └── ff
            ├── {deltaHeaderHash}.bin
            ├── {deltaHeaderHash}.bin
            ...
            └── {deltaHeaderHash}.bin
```

### Delta Header Hash Calculation

!!! info "To determine which file you need to open (generate `deltaHeaderhash`), follow these steps"

1. Create a string by concatenating `packageId`, `oldVersion`, and `newVersion`, separated by null bytes:
    ```
    {packageId}\0{oldVersion}\0{newVersion}\0
    ```
2. Encode this string as UTF-8.
    - Note: *In most cases, this will be ASCII and result in 1 byte per character.*
3. Calculate the [XXH3] hash of this UTF-8 encoded string.
    - Including the final null terminator.
4. Use the string name of the hash (in hexadecimal) to determine the file location.

For example, if the [XXH3] hash is `12ab3c4d5e6f7890`, the file would be located at:

```
delta-headers/12/ab/12ab3c4d5e6f7890.bin
```

This follows the same pattern as other files.

### Delta Header File Content

!!! info "The `.bin` file contains a list of XXH3 hashes."

    These hashes represent the files required in the previous/original mod folder to apply the
    delta update.

    ***If a file with any of the hashes is not present, the delta update cannot be applied.***

- `u8`: Version
- `u24`: Reserved
- `u32`: Number of hashes
- `XXH3[Number of hashes]`: List of file hashes

[adding-localisations]: ../../Common/Localisation/Adding-Localisations.md
[community-repository]: ../Community-Repository.md
[community-repository-versions]: ../Community-Repository.md#version
[community-repository-id]: ../../Server/Storage/Games/About.md#whats-inside-an-game-configuration
[game-id]: ../../Server/Storage/Games/About.md#id
[package-metadata]: ../../Server/Packaging/Package-Metadata.md
[update-data]: ../../Server/Packaging/Package-Metadata.md#update-source-data
[steam-grid-db]: ../../Research/External-Services/SteamGridDB.md
[r2-all-deps-idx]: https://github.com/Reloaded-Project/Reloaded-II.Index/blob/main/AllDependencies.json.br
[pages-limits]: https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages#usage-limits
[package-id]: ../../Server/Packaging/Package-Metadata.md#id
[sync-loadout]: ../../Server/Storage/Loadouts/File-Format/Unpacked.md#restoring-actual-package-files
[package-reference-ids]: ../../Server/Storage/Loadouts/File-Format/Unpacked.md#package-idsbin
[hashing]: ../../Common/Hashing.md#stable-hashing-for-general-purpose-use
[mod-metadata-search-image]: ../../Server/Packaging/Package-Metadata.md#icon-search
[Download Information]: ./Online-API.md#download-information
[delta-update-header]: ../../Server/Packaging/File-Format/Archive-User-Data-Format.md#header-delta-update
[XXH3]: ../../Common/Hashing.md#stable-hashing-for-general-purpose-use