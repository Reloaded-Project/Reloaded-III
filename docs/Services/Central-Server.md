# Central Server

!!! info "The Central Server is a web API that provides various services to support the Reloaded3 ecosystem."

It is responsible for the tasks listed below.

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
  "packageId": "reloaded3.gamesupport.p5rpc.s56",
  "packageVersion": "1.0.1",
  "gameId": "P5R",
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
  "packageId": "reloaded3.gamesupport.p5rpc.s56",
  "packageVersion": "1.0.1",
  "gameId": "P5R",
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
    "packageId": "reloaded3.gamesupport.p5rpc.s56",
    "packageVersion": "1.0.1",
    "gameId": "P5R",
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

### Get Package Metadata

- `POST /api/packages/metadata`

***Description:*** Get the raw `Package.toml` files for multiple packages in a single request.

***Request Body:*** An array of objects, each containing `packageId` and `version` fields.

***Example Request Body:***
```json
[
  {
    "packageId": "reloaded3.gamesupport.p5rpc.s56",
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
    "packageId": "reloaded3.gamesupport.p5rpc.s56",
    "version": "1.0.1",
    "packageToml": "Id = \"reloaded3.gamesupport.p5rpc.s56\"\nName = \"Persona 5 Royal Support\"..."
  },
  {
    "packageId": "reloaded3.utility.reloadedhooks.s56",
    "version": "2.3.0",
    "packageToml": "Id = \"reloaded3.utility.reloadedhooks.s56\"\nName = \"Reloaded3 Hooking Library\"..."
  }
]
```

In the response, `packageToml` contains the raw contents of the [Package.toml][package-metadata] file as a string.
This can be directly saved to disk by the client.

***Typical Use Cases:***

- Restore metadata for all packages when syncing mods to a new PC.
- Mod Search UIs/Engines

### Get Package Configuration

- `POST /api/packages/config`

***Description:*** Get the raw `Configuration.toml` files for multiple packages in a single request.

***Request Body:*** An array of objects, each containing `packageId` and `version` fields.

***Example Request Body:***
```json
[
  {
    "packageId": "reloaded3.gamesupport.p5rpc.s56",
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
    "packageId": "reloaded3.gamesupport.p5rpc.s56",
    "version": "1.0.1",
    "configToml": "..."
  },
  {
    "packageId": "reloaded3.utility.reloadedhooks.s56",
    "version": "2.3.0",
    "configToml": "..."
  }
]
```

In the response, `configToml` contains the raw contents of the `Configuration.toml` file as a string.
This can be directly saved to disk by the client.

***Typical Use Cases:***

- Restore config files after restoring all metadata files.
    - Very few mods have config files, so returning them separately is more efficient.

### Check for Updates

- `POST /api/packages/check-updates`

***Description:*** Check if updates are available for the specified packages.

***Request Body:*** An array of objects, each containing `packageId` and `version` fields.

***Example Request Body:***
```json
[
  {
    "packageId": "reloaded3.gamesupport.p5rpc.s56",
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
    "packageId": "reloaded3.gamesupport.p5rpc.s56",
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

### Download Locations

- `POST /api/packages/download-locations`

***Description:*** Get the latest download locations for the specified packages.

***Request Body:*** An array of objects, each containing `packageId` and `version` fields.

***Example Request Body:***
```json
[
  {
    "packageId": "reloaded3.gamesupport.p5rpc.s56",
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
    "packageId": "reloaded3.gamesupport.p5rpc.s56",
    "version": "1.1.0",
    "updateData": {
      "GameBanana": {
        "ItemType": "Mod",
        "ItemId": 408376
      },
      "GitHub": {
        "UserName": "Sewer56",
        "RepositoryName": "reloaded3.gamesupport.p5rpc"
      },
      "Nexus": {
        "GameDomain": "persona5",
        "Id": 789012
      },
      "NuGet": {
        "DefaultRepositoryUrls": [
          "http://packages.sewer56.moe:5000/v3/index.json"
        ],
        "AllowUpdateFromAnyRepository": false
      }
    }
  },
  {
    "packageId": "reloaded3.utility.reloadedhooks.s56",
    "version": "2.3.0",
    "updateData": {
      "GitHub": {
        "UserName": "Reloaded-Project",
        "RepositoryName": "reloaded3.utility.reloadedhooks"
      }
    }
  }
]
```

The response contains the contents of the [`UpdateData`][update-data] struct from [Package.toml][package-metadata] for each package.

!!! tip "To get the full package, including documentation, the entire package must be downloaded."

## GitHub Fallback

!!! info "In case of downtime, critical functionality is handled by GitHub"

[community-repository]: ./Community-Repository.md
[community-repository-versions]: ./Community-Repository.md#version
[community-repository-id]: ../Server/Storage/Games/About.md#whats-inside-an-game-configuration
[package-metadata]: ../Server/Packaging/Package-Metadata.md
[update-data]: ../Server/Packaging/Package-Metadata.md#update-data
[steam-grid-db]: ../Research/External-Services/SteamGridDB.md