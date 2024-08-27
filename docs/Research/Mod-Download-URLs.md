!!! info "This section provides examples of how to retrieve download information from various sources using their respective APIs."

The examples below already have URL segments filled in, they are placeholders for easier understanding.

## Reasoning

!!! info "In some locations, we need to uniquely identify an externally hosted file."

In order for the `rollback` feature to work properly, we must be able to uniquely identify the location
from which the mod was downloaded.

Likewise the [Central Server] needs a way to know which version of a package is tied to which file.

In order to achieve this, we must look at the external site APIs and see if they provide a way to
uniquely identify a file.

## API Request Examples

!!! info "These are some relevant API requests and responses."

### GameBanana

#### Obtain a Mod Page

**Example URL:**
```
https://gamebanana.com/apiv11/Mod/302016?_csvProperties=_aFiles
```

**Response Data (simplified):**
```json
{
  "_aFiles": [
    {
      "_idRow": 610939,
      "_sFile": "example_mod.zip",
      "_nFilesize": 1048576,
      "_sDownloadUrl": "https:\/\/gamebanana.com\/dl\/610939",
    }
  ]
}
```

**Data Explanation:**

- `_idRow`: Unique identifier for the download (use this as `downloadId`)
- `_sFile`: Filename of the download
- `_nFilesize`: File size in bytes
- `_sDownloadUrl`: URL of the file

#### Obtain an Individual File

!!! info "The last part of the url is the obtained `_idRow` from the previous request."

**Example URL:**

```
https://gamebanana.com/apiv11/File/610939
```

```json
{
    "_idRow": 610939,
    "_sFile": "screenshot-commandmenu-02.zip",
    "_nFilesize": 552,
    "_sDownloadUrl": "https://gamebanana.com/dl/610939",
}
```

### NexusMods

#### Obtain a Mod Page

**Example GraphQL Query:**

```
query Mods {
    mods {
        totalCount
        nodes {
            modId
            gameId
        }
    }
}
```

**Response Data (simplified, truncated):**
```json
{
    "data": {
        "mods": {
            "totalCount": 607400,
            "nodes": [
                {
                    "modId": 27329,
                    "gameId": 1303
                },
                {
                    "modId": 127700,
                    "gameId": 1704
                }
            ]
        }
    }
}
```

!!! tip "Use `pageInfo` for pagination"

    ```json
    pageInfo {
        hasNextPage
        endCursor
    }
    ```

#### Obtain Mod Files

!!! info "Use `modId` and `gameId` from the previous query."

**Example GraphQL Query:**

```graphql
query ModFiles($modId: ID!, $gameId: ID!) {
  modFiles(modId: $modId, gameId: $gameId) {
    uid
    size
    name
    uri
  }
}
```

**Variables:**
```json
{
  "modId": 127772,
  "gameId": 1704
}
```

**Response Data (simplified):**
```json
{
  "data": {
    "modFiles": [
      {
        "uid": "7318624808113",
        "size": 1048576,
        "name": "Interesting NPCs SE - Loose Files",
        "uri": "Interesting NPCs SE - Alternative Locations-29194-3-42Beta-1569342731.7z",
      }
    ]
  }
}
```

**Data Explanation:**

- `uid`: Unique identifier for the file (use this as unique identifier)
- `size`: File size in bytes
- `name`: User friendly name of the file
- `uri`: URL to download the file (reportedly).
    - Maybe not yet fully functional.

**Alternative Query for Specific UIDs:**

```graphql
query ModFilesByUid($uids: [String!]!) {
  modFilesByUid(uids: $uids) {
    uid
    size
    name
    uri
  }
}
```

This fetches us the mod files by specific UID.

### GitHub

**Example URL:**
```
https://api.github.com/repos/Sewer56/nanokit-rs/releases?per_page=1&page=1
```

**Response Data (simplified):**
```json
[
  {
    "tag_name": "0.1.0",
    "name": "0.1.0",
    "published_at": "2024-04-05T14:45:15Z",
    "assets": [
      {
        "url": "https://api.github.com/repos/Sewer56/nanokit-rs/releases/assets/160499684",
        "id": 160499684,
        "name": "Changelog.md",
        "size": 495,
        "browser_download_url": "https://github.com/Sewer56/nanokit-rs/releases/download/0.1.0/Changelog.md",
        "created_at": "2024-04-05T14:45:15Z"
      }
    ]
  }
]
```

**Data Explanation:**

- `tag_name`: The tag name of the release (often corresponds to the version)
- `name`: The name of the release
- `published_at`: Timestamp of when the release was published
- `assets`: Array of assets (downloadable files) associated with the release
    - `url`: Stable URL for this file.
    - `id`: Unique identifier for the asset (use this as `assetId`)
    - `name`: Filename of the asset
    - `size`: File size in bytes
    - `browser_download_url`: Direct download URL for the asset (don't use this one!!)
    - `created_at`: Timestamp of when the asset was created

!!! danger "Do not use `browser_download_url`, it changes with file name."

    Instead use the `url` field, it is stable as it is tied to the asset id.

!!! note "Max 100 items per page per file."

    GitHub doesn't return error, just caps it to 100 silently.

## Unique Identifiers

### GameBanana


[Central Server]: ../Services/Central-Server.md