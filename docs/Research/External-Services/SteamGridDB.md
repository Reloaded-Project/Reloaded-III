# SteamGridDB

!!! note "To avoid having end users register on SteamGridDB, we will expose a 1st party server that wraps the API"

    With a local cache of ~24 hours, depending on the API kind. After discussion with Zennn (SteamGridDB maintainer),
    this should be fine to avoid overloading the SteamGridDB servers.

To see where this is used, see [Central Server][central-server]

## Using the API (Example)

API Docs:

- `https://www.steamgriddb.com/api/v2`

If you run a query like:

- `https://www.steamgriddb.com/api/v2/icons/game/5247913`

You'll get multiple results in the form:

```json
"success": true,
"data": [
    {
        "id": 21699,
        "score": 0,
        "style": "official",
        "width": 0,
        "height": 0,
        "nsfw": false,
        "humor": false,
        "notes": "Pulled from the game executable.",
        "mime": "image/vnd.microsoft.icon",
        "language": "en",
        "url": "https://cdn2.steamgriddb.com/icon/61d647c1a3d7b66b408e4a21c3167fe2.ico",
        "thumb": "https://cdn2.steamgriddb.com/icon/61d647c1a3d7b66b408e4a21c3167fe2/32/256x256.png",
        "lock": false,
        "epilepsy": false,
        "upvotes": 0,
        "downvotes": 0,
        "author": {
            "name": "cynojien",
            "steam64": "76561197971169044",
            "avatar": "https://avatars.steamstatic.com/a5dda94a5752ec305ff430dda89b034b41f42cff_medium.jpg"
        }
    },
```

We can convert the `thumb` URL to a `jxl` image and store it in the game configuration.

## Undocumented Endpoints

!!! warning "TODO: We will not use these endpoints."

    After speaking with the SteamGridDB maintainer, it has been decided
    to create a unique endpoint for fetching a unique asset.

    In the future, this endpoint will be noted here.

!!! tip "These are used by the website, but not documented."

- Get a specific grid: `https://www.steamgriddb.com/api/public/asset/grid/{gridID}`
- Get a specific hero: `https://www.steamgriddb.com/api/public/asset/hero/{heroID}`
- Get a specific logo: `https://www.steamgriddb.com/api/public/asset/logo/{logoID}`
- Get a specific icon: `https://www.steamgriddb.com/api/public/asset/icon/{iconID}`

The individual IDs are the same as the ones you obtain from search.

No API key is required for these endpoints.

[central-server]: ../../Services/Central-Server/Online-API.md