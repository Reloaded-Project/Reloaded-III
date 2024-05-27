# Central Server

!!! info "The Central Server is a web API that provides various services to support the Reloaded3 ecosystem."

It is responsible for the tasks listed below.

## Mod Compatibility Tracking

!!! info "The Central Server keeps a database of user submitted mod compatibility reports."

Users can anonymously report whether a specific mod version worked with a specific game version.

!!! note "Game versions are sourced from the [Community Repository][community-repository-versions]."

This information can be used to provide compatibility insights to other users.

### API Endpoints

- `POST /api/compatibility`: Submit a compatibility report.

- `GET /api/compatibility`: Query compatibility reports.
    - Parameters:
        - `modId`: The ID of the mod. [(Mod Metadata)][mod-metadata].
        - `modVersion`: The version of the mod. [(Mod Metadata)][mod-metadata].
        - `gameId`: The ID of the game. ([Community Repository][community-repository]) [(Documented Here)][community-repository-id].
        - `gameVersionId`: The ID of the game version. [(`ID` field in Community Repository `Version`)][community-repository-versions].

#### Request Body (`POST /api/compatibility`)

```json
{
  "modId": "reloaded3.gamesupport.p5rpc.s56",
  "modVersion": "1.0.1",
  "gameId": "P5R",
  "gameVersionId": 1
}
```

#### Response

- `200 OK` if the compatibility information was successfully recorded.
- `400 Bad Request` if the request body is invalid.

## SteamGridDB API Wrapper

!!! info "The Central Server wraps the SteamGridDB API to provide game assets."

It uses a registered API key to make requests to the SteamGridDB API and returns the results to the client.
This allows Reloaded3 clients to access game assets without needing their own API key.

### API Endpoints

- `GET /api/steamgriddb/assets/{gameId}`: Get all assets for a game.

- `GET /api/steamgriddb/assets/{gameId}/{category}/{id}`: Get a specific asset for a game.
    - `category` can be one of `grid`, `hero`, `logo`, or `icon`.
    - `id` is the ID of the asset within the category.

#### Path Parameters

- `gameId`: The unique identifier of the game.

#### Response

- `200 OK` with the game assets in the response body if the request was successful.
- `404 Not Found` if the specified game was not found.

## Package Metadata

!!! info "The Central Server provides access to package metadata and configurations."

It hosts the metadata-only packages, which contain information about mods, tools, and other packages
without the actual package contents. This includes the [Configuration Schema][mod-configurations], [Documentation][package-docs], [Images][package-images], and other miscellaneous metadata.

These metadata packages are regular Reloaded3 packages, as described in the [Package Structure][package-structure] section.

### API Endpoints

- `GET /api/packages/{packageId}/{version}/metadata`: Get the metadata package for the specified package ID and version.

#### Path Parameters

- `packageId`: The unique identifier of the package.
- `version`: The version of the package.

#### Response

- `200 OK` with the metadata package in the response body if the request was successful.
- `404 Not Found` if the specified package or version was not found.

[community-repository]: ./Community-Repository.md
[community-repository-versions]: ./Community-Repository.md#version
[community-repository-id]: ../Server/Storage/Games/About.md#whats-inside-an-game-configuration
[mod-metadata]: ../Server/Packaging/Configurations/Mod-Metadata.md
[mod-configurations]: ../Server/Packaging/Configurations/Mod-Configurations.md
[package-docs]: ../Server/Packaging/About.md#docs
[package-images]: ../Server/Packaging/About.md#images
[package-structure]: ../Server/Packaging/About.md#package-structure