# Central Server

!!! info "The Central Server is a web API that provides various services to support the Reloaded3 ecosystem."

It is responsible for the tasks listed below.

!!! note "API returns ***Zstandard compressed MessagePack by default***."

    But we will use JSON in the examples for readability.

    This is to reduce bandwidth usage and improve performance.

    Gotta remember that Reloaded is funded out of pocket, at a loss, so we need to keep costs low.

## Mod Compatibility Tracking

!!! info "The Central Server keeps a database of user submitted mod compatibility reports."

Users can anonymously report whether a specific mod version worked with a specific game version.

!!! note "Game versions are sourced from the [Community Repository][community-repository-versions]."

This information can be used to provide compatibility insights to other users.

### Submit Compatibility Report

- `POST /api/compatibility`

***Description:*** Submit a compatibility report.

***Request Body:***

```json
{
  "packageId": "reloaded3.gamesupport.persona5royal.s56",
  "packageVersion": "1.0.1",
  "gameId": "persona5royal",
  "gameVersionId": 1
}
```

***Response:***

- `200 OK` if the compatibility information was successfully recorded.
- `400 Bad Request` if the request body is invalid.
- `404 Not Found` if any of the following is true:
    - The `gameId` is not recognized. Response body: `{ "error": "Unrecognized gameId" }`
    - The `gameVersionId` is not recognized. Response body: `{ "error": "Unrecognized gameVersionId" }`
    - The `packageId` is not recognized. Response body: `{ "error": "Unrecognized packageId" }`
    - The `packageVersion` is not recognized. Response body: `{ "error": "Unrecognized packageVersion" }`

### Query Compatibility Reports

- `GET /api/compatibility`

***Description:*** Query compatibility reports.

***Parameters:***

- `packageId`: The ID of the package. [(Package Metadata)][package-metadata].
- `packageVersion`: The version of the package. [(Package Metadata)][package-metadata].
- `gameId`: The ID of the game. ([Community Repository][community-repository]) [(Documented Here)][community-repository-id].
- `gameVersionId`: The ID of the game version. [(`ID` field in Community Repository `Version`)][community-repository-versions].

***Example Response Body:***
```json
{
  "packageId": "reloaded3.gamesupport.persona5royal.s56",
  "packageVersion": "1.0.1",
  "gameId": "persona5royal",
  "gameVersionId": 1,
  "successCount": 42,
  "failureCount": 3
}
```

### Submit Multiple Compatibility Reports

- `POST /api/compatibility/batch`

***Description:*** Submit multiple compatibility reports in a single request.

***Request Body:*** An array of compatibility report objects, each following the same structure as the `POST /api/compatibility` endpoint.

***Example Request Body:***
```json
[
  {
    "packageId": "reloaded3.gamesupport.persona5royal.s56",
    "packageVersion": "1.0.1",
    "gameId": "persona5royal",
    "gameVersionId": 1
  },
  {
    "packageId": "reloaded3.utility.reloadedhooks.s56",
    "packageVersion": "2.3.0",
    "gameId": "SonicHeroes",
    "gameVersionId": 2
  }
]
```

***Response:***

- `200 OK` if all compatibility reports were successfully recorded.
- `400 Bad Request` if any of the compatibility reports in the request body are invalid.
- `404 Not Found` if any of the following is true for any of the compatibility reports:
    - The `gameId` is not recognized. Response body: `{ "error": "Unrecognized gameId" }`
    - The `gameVersionId` is not recognized. Response body: `{ "error": "Unrecognized gameVersionId" }`
    - The `packageId` is not recognized. Response body: `{ "error": "Unrecognized packageId" }`
    - The `packageVersion` is not recognized. Response body: `{ "error": "Unrecognized packageVersion" }`

## SteamGridDB API

!!! info "This is a wrapper around the SteamGridDB API to avoid log-ins."

    The central server will perform requests on behalf of my account and then cache the results,
    to help ease the load.

    Planned response cache time is ~24 hours.

For more implementation details, see [SteamGridDB][steam-grid-db].

### Search

***Description:*** Search SteamGridDB for images with suitable sizes.

***Request Body:*** An array of objects, each containing `packageId` and `version` fields.

- ***Game Icons***: `GET /api/steamgriddb/search/icon/{gameId}`:
    - Unique Parameters:
        - `includeLogos` (optional): Include results from the `logo` category. (Default: `false`).
        - `includeGrids` (optional): Include results from the `grid` category. (Default: `false`).

- ***Square Banners***: `GET /api/steamgriddb/search/banner-square/{gameId}`
    - Unique Parameters:
        - `includeLogos` (optional): Include results from the `logo` category. (Default: `false`).
        - `includeIcons` (optional): Include results from the `icon` category. (Default: `false`).

- ***Horizontal Banners***: `GET /api/steamgriddb/search/banner-horizontal/{gameId}`
- ***Vertical Banners***: `GET /api/steamgriddb/search/banner-vertical/{gameId}`

#### Common Parameters

- `nsfw` (optional): Filter by NSFW content.
    - Possible values: `true`, `false`, `any`. Default: `false`.
- `humor` (optional): Filter by humor content.
    - Possible values: `true`, `false`, `any`. Default: `false`.
- `epilepsy` (optional): Filter by epilepsy warning.
    - Possible values: `true`, `false`, `any`. Default: `false`.

#### Path Parameters

- `gameId`: The unique identifier of the game.

#### Response

- `200 OK` with an array of matching asset objects in the response body if the request was successful.
- `404 Not Found` if no matching assets were found for the specified game.

***Example Response Body:***
```json
[
  {
    "url": "https://example.com/image1.jpg",
    "score": 85,
    "nsfw": false,
    "humor": false,
    "upvotes": 120,
    "downvotes": 5,
    "authorName": "JohnDoe",
    "authorAvatar": "https://example.com/avatar1.jpg"
  },
  {
    "url": "https://example.com/image2.jpg",
    "score": 92,
    "nsfw": true,
    "humor": false,
    "upvotes": 200,
    "downvotes": 10,
    "authorName": "JaneSmith",
    "authorAvatar": "https://example.com/avatar2.jpg"
  }
]
```

The returned asset objects will have the following properties:

- `url`: The URL of the asset image.
- `score`: The score of the asset (integer).
- `nsfw`: Indicates if the asset contains NSFW content (boolean).
- `humor`: Indicates if the asset contains humor content (boolean).
- `upvotes`: The number of upvotes for the asset (integer).
- `downvotes`: The number of downvotes for the asset (integer).
- `authorName`: The name of the author who uploaded the asset.
- `authorAvatar`: The URL of the author's avatar image.

The returned objects are just a simplified response from `SteamGridDB`, with server side caching.

## Package Metadata

!!! info "The Central Server provides access to package metadata and configurations."

!!! note "Any API labelled `fromhash` accepts a `packageIdHash` as the parameter instead of `packageId`."

### Get Package Metadata

- `POST /api/packages/metadata`
- `POST /api/packages/metadata-fromhash`

***Description:*** Get the raw `Package.toml` files, `Config.toml` files, and associated language files for multiple packages in a single request.

***Request Body:*** An array of objects, each containing `packageId` (or `packageIdHash` for `/api/packages/metadata-fromhash`) and `version` fields.

***Example Request Body:***

- `POST /api/packages/metadata`:
```json
[
  {
    "packageId": "reloaded3.gamesupport.persona5royal.s56",
    "version": "1.0.1"
  },
  {
    "packageId": "reloaded3.utility.reloadedhooks.s56",
    "version": "2.3.0"
  }
]
```

- `POST /api/packages/metadata-fromhash`:
```json
[
  {
    "packageIdHash": "c88fcd6edc933d2a",
    "version": "1.0.1"
  },
  {
    "packageIdHash": "ff900b821c9f5e89",
    "version": "2.3.0"
  }
]
```

***Example Response Body:***
```json
[
  {
    "packageId": "reloaded3.gamesupport.persona5royal.s56",
    "packageIdHash": "c88fcd6edc933d2a",
    "version": "1.0.1",
    "packageToml": "Id = \"reloaded3.gamesupport.persona5royal.s56\"\nName = \"Persona 5 Royal Support\"...",
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
  {
    "packageId": "reloaded3.utility.reloadedhooks.s56",
    "packageIdHash": "ff900b821c9f5e89",
    "version": "2.3.0",
    "packageToml": "Id = \"reloaded3.utility.reloadedhooks.s56\"\nName = \"Reloaded3 Hooking Library\"...",
    "configToml": "...",
    "languageFiles": [
      {
        "path": "languages/en-GB.toml",
        "data": "..."
      }
    ]
  }
]
```

In the response, `packageToml` contains the raw contents of the [Package.toml][package-metadata]
file as a string. This can be directly saved to disk by the client.

The same goes for the config, and the language files contain all language files for the package,
which are likely referenced by `configToml`.

The `/api/packages/metadata` endpoint accepts an array of objects containing the `packageId` and
`version` fields, while the `/api/packages/metadata-fromhash` endpoint accepts an array of objects
containing the `packageIdHash` (the XXH3 hash of the package ID) and `version` fields.

***Typical Use Cases:***

- Restore metadata and configuration for all packages when syncing mods to a new PC.
- Mod Search UIs/Engines

!!! question "Why is there a `by-hash` API?"

    [Package References][package-reference-ids] use hashes in this format. This allows loadouts to stay small.

### Check for Updates

- `POST /api/packages/check-updates`
- `POST /api/packages/check-updates-fromhash`

***Description:*** Check if updates are available for the specified packages.

***Request Body:*** An array of objects, each containing `packageId` and `version` fields.

***Example Request Body:***
```json
[
  {
    "packageId": "reloaded3.gamesupport.persona5royal.s56",
    "version": "1.0.1"
  },
  {
    "packageId": "reloaded3.utility.reloadedhooks.s56",
    "version": "2.3.0"
  }
]
```

***Example Response Body:***
```json
[
  {
    "packageId": "reloaded3.gamesupport.persona5royal.s56",
    "hasUpdate": true,
    "latestVersion": "1.1.0"
  },
  {
    "packageId": "reloaded3.utility.reloadedhooks.s56",
    "hasUpdate": false,
    "latestVersion": "2.3.0"
  }
]
```

### Search Translations

- `GET /api/packages/{packageId}/translations`
- `GET /api/packages/{packageId}/translations-fromhash`

***Description:*** Find available translations for a specified package.

***Path Parameters:***

- `packageId`: The package ID.

***Example Request:***

```
GET /api/packages/reloaded3.utility.examplemod.s56/translations
```

***Example Response Body:***
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
  {
    "packageId": "reloaded3.utility.examplemod.s56.uwu",
    "languageCode": "uwu-en",
    "friendlyName": "UwU (English)"
  }
]
```

***Typical Use Cases:***

- Discover available translations for a package.
- Download and install translations for a package.

For more information on how translations are structured and added to packages, refer to the
[Adding Localisations][adding-localisations] documentation.

### Get Translation Contents

- `POST /api/packages/translations`
- `POST /api/packages/translations-fromhash`

***Description:*** Retrieve the contents of translation files for one or more translations.

***Request Body:*** An array of objects, each containing `packageId` and `version` fields.

***Example Request Body:***
```json
[
  {
    "packageId": "reloaded3.utility.examplemod.s56.de",
    "version": "1.0.0"
  },
  {
    "packageId": "reloaded3.utility.examplemod.s56.fr",
    "version": "1.0.0"
  }
]
```

***Example Response Body:***
```json
[
  {
    "packageId": "reloaded3.utility.examplemod.s56.de",
    "version": "1.0.0",
    "translations": {
      "languages/config/de-DE.toml": "...",
      "languages/dll/de-DE.toml": "..."
    }
  },
  {
    "packageId": "reloaded3.utility.examplemod.s56.fr",
    "version": "1.0.0",
    "translations": {
      "languages/config/fr-FR.toml": "..."
    }
  }
]
```

***Typical Use Cases:***

- Retrieve the contents of all translation files for a package.
- Implement a translation management system that allows editing and updating translation files.

### Download Information

- `POST /api/packages/download-info`

***Description:*** Get the download locations and file information for the specified packages.
This is used to restore packages to a new PC [after syncing a loadout][sync-loadout] and to provide update information.

***Request Body:*** An array of objects, each containing `packageId` and `version` fields. If version field
is not specified, all versions will be returned.

***Example Request Body:***
```json
[
  {
    "packageId": "reloaded3.gamesupport.persona5royal.s56",
    "version": "1.1.0"
  },
  {
    "packageId": "reloaded3.utility.reloadedhooks.s56",
    "version": "2.3.0"
  }
]
```

***Example Response Body:***
```json
[
  {
    "packageId": "reloaded3.gamesupport.persona5royal.s56",
    "version": "1.1.0",
    "updateSourceData": {
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
    ]
  },
  {
    "packageId": "reloaded3.utility.reloadedhooks.s56",
    "version": "2.3.0",
    "updateSourceData": {
      "GitHub": {
        "UserName": "Reloaded-Project",
        "RepositoryName": "reloaded3.utility.reloadedhooks"
      }
    },
    "downloadInfo": [
      {
        "type": "GitHub",
        "userName": "Reloaded-Project",
        "repositoryName": "Reloaded.Hooks",
        "assetId": 160499685,
        "fileSize": 552
      },
      {
        "type": "NexusMods",
        "uid": "7318624808114",
        "fileSize": 552
      }
    ]
  }
]
```

The response contains two main sections for each package:

1. [`updateSourceData`](#update-source-data):
    - This section contains information about the mod page or repository where the package was originally sourced from.

2. [`downloadInfo`](#download-info):
    - This section provides specific information required to download this package version.
    - Includes unique identifiers and file sizes for each platform.

#### Update Source Data

The `updateSourceData` section contains the following information for each supported platform.

##### GameBanana Update Info

| Type   | Name     | Description                                                                        |
| ------ | -------- | ---------------------------------------------------------------------------------- |
| string | ItemType | Type of item on GameBanana API, e.g. 'Mod', 'Sound', 'Wip'                         |
| int    | ItemId   | Id of the item on GameBanana, this is the last number in the URL to your mod page. |

##### GitHub Update Info

| Type   | Name           | Description                                                                    |
| ------ | -------------- | ------------------------------------------------------------------------------ |
| string | UserName       | The user/organization name associated with the repository to fetch files from. |
| string | RepositoryName | The name of the repository to fetch files from.                                |

##### Nexus Update Info

| Type   | Name       | Description                               |
| ------ | ---------- | ----------------------------------------- |
| string | GameDomain | The ID/Domain for the game. e.g. 'skyrim' |
| int    | Id         | Unique id for the mod.                    |

#### Download Info

The `downloadInfo` array contains objects with the following structure:

| Type   | Name           | Description                                                    |
| ------ | -------------- | -------------------------------------------------------------- |
| string | type           | The platform type (e.g., "GameBanana", "NexusMods", "GitHub")  |
| varies | identifier     | Platform-specific identifier (e.g., idRow, uid, assetId)       |
| int    | fileSize       | Size of the file in bytes                                      |
| string | userName       | (GitHub only) The username associated with the repository      |
| string | repositoryName | (GitHub only) The name of the repository containing the file   |

The `identifier` field varies depending on the platform:
- For GameBanana, it's `idRow`
- For NexusMods, it's `uid`
- For GitHub, it's `assetId`

This combined API provides all the necessary information for both updating and downloading packages from various sources.

## Static CDN API

!!! info "The Static CDN API provides offline access to package metadata, configurations, compatibility reports, and other essential information."

!!! info "The API is hosted on BackBlaze with CloudFlare CDN."

    Or directly on CloudFlare R2, we'll see when we get there.

The API uses a file structure designed to efficiently handle lookups for over 1 million packages, with packages split into multiple files based on the first three bytes of their XXH3 hash, calculated from the package ID.

### Lookup Process

To look up a package, translation, or other hash based data:

1. Calculate the XXH3 hash of the package ID.
2. Take the first two bytes of the hash.
3. Navigate to the corresponding directory based on the first byte and second byte.
4. Load the corresponding `.msgpack.zstd` file (or folder) within that directory.
5. Search for the package entry with the matching full hash within that file.

This file structure provides benefits such as scalability, fast lookups, and balanced distribution
of packages across files, while accommodating the potential for accessing around 16.8 million unique mods.

(In a manner where 1 file == 1 mod)

### Download Information API

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
    "packageIdHash": "XXH3(UTF8(packageId))",
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
    ]
  },
  ...
]
```

!!! note "Expect only contents for 1 package per file"

The contents of this API mirror those in the [Download Information] API, so use that API for reference.

### Package Metadata API

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
    "packageIdHash": "XXH3(UTF8(packageId))",
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

### Translations API

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

### Compatibility Reports API

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

### Search API

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

#### Banner Files

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

#### Searching Mods

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

[adding-localisations]: ../Common/Localisation/Adding-Localisations.md
[community-repository]: ./Community-Repository.md
[community-repository-versions]: ./Community-Repository.md#version
[community-repository-id]: ../Server/Storage/Games/About.md#whats-inside-an-game-configuration
[game-id]: ../Server/Storage/Games/About.md#id
[package-metadata]: ../Server/Packaging/Package-Metadata.md
[update-data]: ../Server/Packaging/Package-Metadata.md#update-source-data
[steam-grid-db]: ../Research/External-Services/SteamGridDB.md
[r2-all-deps-idx]: https://github.com/Reloaded-Project/Reloaded-II.Index/blob/main/AllDependencies.json.br
[pages-limits]: https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages#usage-limits
[package-id]: ../Server/Packaging/Package-Metadata.md#id
[sync-loadout]: ../Server/Storage/Loadouts/File-Format/Unpacked.md#restoring-actual-package-files
[package-reference-ids]: ../Server/Storage/Loadouts/File-Format/Unpacked.md#package-idsbin
[hashing]: ../Common/Hashing.md#stable-hashing-for-general-purpose-use
[mod-metadata-search-image]: ../Server/Packaging/Package-Metadata.md#icon-search
[Download Information]: #download-information