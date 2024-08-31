!!! info "The Central Server is a web API that provides various services to support the Reloaded3 ecosystem."

It is responsible for the tasks listed below.

!!! note "API returns ***Zstandard compressed MessagePack by default***."

    But we will use JSON in the examples for readability.

    This is to reduce bandwidth usage and improve performance.

    Gotta remember that Reloaded is funded out of pocket, at a loss, so we need to keep costs low.

## Compatibility Reports (Batch)

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

## Package Metadata (Batch)

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

### Check for Updates (Batch)

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

### Search Translations (Batch)

- `POST /api/packages/translations`

***Description:*** Find available translations for multiple specified packages.
Use this API when searching for translations for one or more packages.
For single package lookups, prefer the [CDN based Static API][translations-api].

***Request Body:*** An array of package IDs for which to find translations.

***Example Request Body:***
```json
[
  "reloaded3.utility.examplemod.s56",
  "reloaded3.gamesupport.persona5royal.s56"
]
```

***Example Response Body:***
```json
{
  "reloaded3.utility.examplemod.s56": [
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
  ],
  "reloaded3.gamesupport.persona5royal.s56": [
    {
      "packageId": "reloaded3.gamesupport.persona5royal.s56.jp",
      "languageCode": "ja-JP",
      "friendlyName": "日本語 (日本)"
    },
    {
      "packageId": "reloaded3.gamesupport.persona5royal.s56.es",
      "languageCode": "es-ES",
      "friendlyName": "Español (España)"
    }
  ]
}
```

***Response:***

- `200 OK` with an object containing translation information for each requested package ID.
- `400 Bad Request` if the request body is invalid or empty.

***Notes:***

1. This API is optimized for batch queries of multiple packages.
2. For single package translation lookups, it's recommended to use the CDN-based Static API for better performance and reduced server load.
3. If a package has no available translations, an empty array will be returned for that package ID.

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
        "GameId": 1000,
        "Id": 789012
      }
    },
    "downloadInfo": [
      {
        "type": "GameBanana",
        "idRow": 610939,
        "fileSize": 1048576,
        "xxhash3": 1311768467294899695,
        "wasDeleted": false
      },
      {
        "type": "NexusMods",
        "uid": "7318624808113",
        "fileSize": 1048576,
        "xxhash3": 1311768467294899695,
        "wasDeleted": false
      },
      {
        "type": "GitHub",
        "userName": "Sewer56",
        "repositoryName": "persona5royal-modloader",
        "assetId": 160499684,
        "fileSize": 495,
        "xxhash3": 1311768467294899695,
        "wasDeleted": false
      }
    ],
    "deltaUpdates": [
      {
        "fromVersion": "1.0.0",
        "downloadInfo": [
          {
            "type": "GameBanana",
            "idRow": 610940,
            "fileSize": 102400,
            "xxhash3": 18364758544493064721,
            "wasDeleted": false
          },
          {
            "type": "NexusMods",
            "uid": "7318624808114",
            "fileSize": 102400,
            "xxhash3": 18364758544493064721,
            "wasDeleted": false
          },
          {
            "type": "GitHub",
            "userName": "Sewer56",
            "repositoryName": "persona5royal-modloader",
            "assetId": 160499685,
            "fileSize": 102400,
            "xxhash3": 18364758544493064721,
            "wasDeleted": false
          }
        ]
      },
      {
        "fromVersion": "1.0.1",
        "downloadInfo": [
          {
            "type": "GameBanana",
            "idRow": 610941,
            "fileSize": 51200,
            "xxhash3": 18364758544493064721,
            "wasDeleted": false
          },
          {
            "type": "NexusMods",
            "uid": "7318624808115",
            "fileSize": 51200,
            "xxhash3": 18364758544493064721,
            "wasDeleted": false
          },
          {
            "type": "GitHub",
            "userName": "Sewer56",
            "repositoryName": "persona5royal-modloader",
            "assetId": 160499686,
            "fileSize": 51200,
            "xxhash3": 18364758544493064721,
            "wasDeleted": false
          }
        ]
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
        "fileSize": 552,
        "xxhash3": 1311768467294899695,
        "wasDeleted": false
      },
      {
        "type": "NexusMods",
        "uid": "7318624808114",
        "fileSize": 552,
        "xxhash3": 1311768467294899695,
        "wasDeleted": false
      }
    ],
    "deltaUpdates": [
      {
        "fromVersion": "2.2.0",
        "downloadInfo": [
          {
            "type": "GitHub",
            "userName": "Reloaded-Project",
            "repositoryName": "Reloaded.Hooks",
            "assetId": 160499686,
            "fileSize": 102,
            "xxhash3": 18364758544493064721,
            "wasDeleted": false
          },
          {
            "type": "NexusMods",
            "uid": "7318624808116",
            "fileSize": 102,
            "xxhash3": 18364758544493064721,
            "wasDeleted": false
          }
        ]
      }
    ]
  }
]
```

The response contains the following main sections for each package:

1. [`updateSourceData`](../../Server/Packaging/Package-Metadata.md#update-source-data):
    - This section contains information about the mod page or repository where the package was originally sourced from.

2. [`downloadInfo`](#download-info):
    - This section provides specific information required to download this package version.
    - Includes unique identifiers and file sizes for each platform.

3. [`deltaUpdates`][delta-update-header]:
    - This section provides information about delta updates available for the package.
    - You can obtain the delta info using the (TODO: API).

#### Download Info

The `downloadInfo` array contains objects with the following structure:

| Type   | Name           | Description                                                    |
| ------ | -------------- | -------------------------------------------------------------- |
| string | type           | The platform type (e.g., "GameBanana", "GitHub", "NexusMods")  |
| varies | identifier     | Platform-specific identifier (e.g., idRow, uid, assetId)       |
| int    | fileSize       | Size of the file in bytes                                      |
| u64    | xxhash3        | The `xxhash3` sum of the data (in little endian)               |
| string | userName       | (GitHub only) The username associated with the repository      |
| string | repositoryName | (GitHub only) The name of the repository containing the file   |
| bool   | wasDeleted     | True if this package has been deleted from the original source |

The `identifier` field varies depending on the platform:

- For GameBanana, it's `idRow`
- For NexusMods, it's `uid`
- For GitHub, it's `assetId`

This combined API provides all the necessary information for both updating and downloading packages from various sources.

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
[Download Information]: #download-information
[delta-update-header]: ../../Server/Packaging/File-Format/Archive-User-Data-Format.md#header-delta-update
[XXH3]: ../../Common/Hashing.md#stable-hashing-for-general-purpose-use
[translations-api]: ./Static-API.md#translations-api