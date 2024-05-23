# GOG Games

!!! warning "TODO: This document is a work in progress."

This document provides an overview of the process for verifying and downloading with GOG.

## Local Files

!!! info "Below is a listing of useful files that may already be locally stored on the user machine."

### goggame-{gameid}.info

!!! info "This contains general information on the current game download."

```json
{
    "buildId": "56010259761743716",
    "clientId": "48480352668663651",
    "gameId": "1444826419",
    "language": "English",
    "languages": [
        "en-US"
    ],
    "name": "The Legend of Heroes: Trails in the Sky SC",
    "playTasks": [
        {
            "category": "game",
            "isPrimary": true,
            "languages": [
                "en-US"
            ],
            "name": "The Legend of Heroes: Trails in the Sky SC",
            "path": "ed6_win2_DX9.exe",
            "type": "FileTask"
        },
        {
            "category": "launcher",
            "languages": [
                "en-US"
            ],
            "name": "Configuration Tool",
            "path": "Config2_DX9.exe",
            "type": "FileTask"
        },
        {
            "category": "game",
            "isHidden": true,
            "languages": [
                "en-US"
            ],
            "name": "Configuration Tool - launcher process ed6_win2_DX9_exe",
            "path": "ed6_win2_DX9.exe",
            "type": "FileTask"
        },
        {
            "category": "game",
            "languages": [
                "en-US"
            ],
            "name": "DirectX 8 Version",
            "path": "ed6_win2.exe",
            "type": "FileTask"
        },
        {
            "category": "launcher",
            "languages": [
                "en-US"
            ],
            "name": "Configuration Tool (DX8)",
            "path": "Config2.exe",
            "type": "FileTask"
        },
        {
            "category": "game",
            "isHidden": true,
            "languages": [
                "en-US"
            ],
            "name": "Configuration Tool (DX8) - launcher process ed6_win2_exe",
            "path": "ed6_win2.exe",
            "type": "FileTask"
        }
    ],
    "rootGameId": "1444826419",
    "version": 1
}
```

Useful information for us includes:

- `buildId`: The current game version!
- `gameId`: The game ID. Used for API requests.
- `playTasks`: The actions the user may run to launch the game.
    - Useful as this identifies the launchers, etc.

### goggame-{gameid}.hashdb

!!! info "This is a zip file which contains a binary file that has MD5 hashes for all files."

The file inside the zip file has the same name as the parent.

When unzipped, the top of the file should look something like

```
0:0000  0C 00 00 00 01 00 00 00 9E 01 00 00 62 69 6E 6B  ........ž...bink
0:0010  77 33 32 2E 64 6C 6C 00 00 00 00 00 00 00 00 00  w32.dll.........
```

This file has the following format (Little Endian):

| Type | Name         | Description                                                    |
| ---- | ------------ | -------------------------------------------------------------- |
| u32  | HeaderLength | Believed to be header length. Always 0C in all tested samples. |
| u32  | Unknown.     | Constant 01. Maybe Version.                                    |
| u32  | FileCount    | Number of files.                                               |

After that follows an array of `FileCount` file entries, where each entry is

| Type     | Name     | Description                           |
| -------- | -------- | ------------------------------------- |
| u8[1024] | FileName | Name of file. Probably UTF-8 Encoded. |
| u8[32]   | MD5Hash  | MD5 Hash.                             |

File then ends.

!!! tip "For convenience, here's a C-like template."

```c
//------------------------------------------------
//--- 010 Editor v14.0.1 Binary Template
//
//      File: GOG .hashdb
//    Author: Sewer56
//   Version: 23rd May 2024
//------------------------------------------------

LittleEndian();
struct Header
{
    uint32 HeaderLength;
    uint32 MaybeVersion;
    uint32 FileCount;
} header;

struct FileEntry
{
    char FileName[1024];
    char MD5[32];
} fileEntry[header.FileCount];
```

!!! warning "One of the games I tested (Worms Forts) the name was `goggame-{gameid}.hashdb.temporary`."

    The inclusion of `.temporary` may have been a result of a bug in the publishing tools,
    the file had a discrepancy in the hash count, it may have been incomplete.

## Interacting with the GOG API

!!! info "Some API responses are compressed using default `zlib` compression."

    Header: 0x789C

    You can decompress the responses in the CLI using `pigz -d -z response.zz`.

Some 3rd party launchers on Linux also use these endpoints.
This info is a simplified version of the [Game Launcher Research][game-launcher-research] wiki.

### Retrieving Available Game Versions

Send a GET request to `https://content-system.gog.com/products/{GAME_ID}/os/{PLATFORM}/builds?generation=2`

Inputs:

- The `GAME_ID` you can derive from the `gameId` in `goggame-{gameid}.info`.
- The `PLATFORM` can be `windows` or `osx`. (Linux doesn't exist 🥹)

Example Output:

`https://content-system.gog.com/products/1444826419/os/windows/builds?generation=2`

```
{
    "total_count": 26,
    "count": 5,
    "items": [
        {
            "build_id": "56010259761743716",
            "product_id": "1444826419",
            "os": "windows",
            "branch": null,
            "version_name": "2022-09-22",
            "tags": [
                "editor_v_1_5_0",
                "csb_10_6_3_w_7"
            ],
            "public": true,
            "date_published": "2022-11-23T20:38:32+0000",
            "generation": 2,
            "link": "https://gog-cdn-fastly.gog.com/content-system/v2/meta/12/b5/12b585b6125b73d4160e669d4a3b618e"
        },
        {
            "build_id": "55221323621340745",
            "product_id": "1444826419",
            "os": "windows",
            "branch": null,
            "version_name": "2022-02-24a",
            "tags": [
                "editor_v_1_4_0",
                "csb_10_6_1_w_157"
            ],
            "public": true,
            "date_published": "2022-02-24T17:28:45+0000",
            "generation": 2,
            "link": "https://gog-cdn-fastly.gog.com/content-system/v2/meta/63/c6/63c6b9c7a5365eca4092068b9ad63060"
        },
        {
            "build_id": "55221223280436939",
            "product_id": "1444826419",
            "os": "windows",
            "branch": null,
            "version_name": "2022-02-24",
            "tags": [
                "editor_v_1_4_0",
                "csb_10_6_1_w_157"
            ],
            "public": true,
            "date_published": "2022-02-24T16:39:59+0000",
            "generation": 2,
            "link": "https://gog-cdn-fastly.gog.com/content-system/v2/meta/2a/f1/2af1f21839f62d5dc15693ad03c8001f"
        },
        {
            "build_id": "53682761534698442",
            "product_id": "1444826419",
            "os": "windows",
            "branch": null,
            "version_name": "2020-09-10",
            "tags": [
                "csb_10_6_1_w_141"
            ],
            "public": true,
            "date_published": "2020-09-12T00:40:19+0000",
            "generation": 2,
            "link": "https://gog-cdn-fastly.gog.com/content-system/v2/meta/3d/82/3d82adebeb6a3d287930d3bf06fb9b3c"
        },
        {
            "build_id": "52876522987831941",
            "product_id": "1444826419",
            "os": "windows",
            "branch": null,
            "version_name": "2019-12-08",
            "tags": [
                "csb_10_6_1_w_130"
            ],
            "public": true,
            "date_published": "2019-12-08T22:17:44+0000",
            "generation": 2,
            "link": "https://gog-cdn-fastly.gog.com/content-system/v2/meta/ce/57/ce57a10d28e44ec0bdd57594c2f82957"
        }
    ],
    "has_private_branches": true
}
```

Useful Info:

- The `build_id` (uint64) is equivalent to the manifest you'd get from Steam and identifies the current game version.
- The `version_name` is the user-friendly name that can be displayed in the UI.
- The `link` provides a URL to the metadata, which contains links to depots with file hashes.

!!! warning "To get some (legacy) update versions, you have to use the older V1 API"

    That is, changing `?generation=2` to `?generation=1`.

### Getting Information about a Release

Send a GET request to the `link` URL obtained in the previous step, for example
`https://gog-cdn-fastly.gog.com/content-system/v2/meta/12/b5/12b585b6125b73d4160e669d4a3b618e`.

This returns a zlib compressed response with info of downloadbable depots.

```
{
    "baseProductId": "1444826419",
    "buildId": "56010259761743716",
    "clientId": "48480352668663651",
    "clientSecret": "91bd881cd6610d0541566db56e904b4a6dfef984a83d33d1d88af89c228efd89",
    "dependencies": [
        "DirectX",
        "MSVC2017"
    ],
    "depots": [
        {
            "compressedSize": 4100105637,
            "languages": [
                "en-US"
            ],
            "manifest": "e9161c8b414317dbf1dbb93ecfd39588",
            "productId": "1444826419",
            "size": 4565755053
        },
        {
            "compressedSize": 4839,
            "isGogDepot": true,
            "languages": [
                "en-US"
            ],
            "manifest": "bdd1aba965852d65ed5859bc5f57f673",
            "productId": "1444826419",
            "size": 5121
        },
        {
            "compressedSize": 390,
            "isGogDepot": true,
            "languages": [
                "en-US"
            ],
            "manifest": "acde017057791e1ba6da4c768e72e38c",
            "productId": "1444826419",
            "size": 1885
        }
    ],
    "installDirectory": "Trails in the Sky SC",
    "offlineDepot": {
        "compressedSize": 665,
        "languages": [
            "*"
        ],
        "manifest": "cdf282dce3e6604e77ceda8dc94b62eb",
        "productId": "1444826419",
        "size": 3600
    },
    "platform": "windows",
    "products": [
        {
            "name": "The Legend of Heroes: Trails in the Sky SC",
            "productId": "1444826419",
            "temp_arguments": "",
            "temp_executable": ""
        }
    ],
    "scriptInterpreter": true,
    "tags": [
        "editor_v_1_5_0",
        "csb_10_6_3_w_7",
        "galaxy"
    ],
    "version": 2
}
```

The actual `depots` provide a listing of files that are available to download, and their corresponding,
MD5 hashes, so we will take a look at that.

For this, we will take the `manifest` field from here.

### Getting Information about a Depot

To do this, use the link:

```
https://cdn.gog.com/content-system/v2/meta/GALAXY_PATH
```

The `GALAXY_PATH` should be substituted with a `manifest`,
in this example we will use `e9161c8b414317dbf1dbb93ecfd39588`.

The link will be
```
https://cdn.gog.com/content-system/v2/meta/e9/16/e9161c8b414317dbf1dbb93ecfd39588
```

Note we added the prefix `e9/16` after `meta`. This is derived from the start of the manifest.
Likely an optimization on GOG's part.

This response is also zlib compressed, after decompression you get something like:

```json
{
    "version": 2
    "depot": {
        "items": [
            {
                "chunks": [
                    {
                        "compressedMd5": "63b11ee937b521972d10f00d07081679",
                        "compressedSize": 562066,
                        "md5": "9c78a13d67a5fbaa5c29d991c86a377f",
                        "size": 859136
                    }
                ],
                "flags": [
                    "executable"
                ],
                "path": "Config2.exe",
                "sha256": "610a9b9e5a72e52f5031d5f8a66dd45a65c28ab24360d4aebef5e48ca069310d",
                "type": "DepotFile"
            },
            {
                "chunks": [
                    {
                        "compressedMd5": "c2d3176e63d0cf589881e2b484ad0a96",
                        "compressedSize": 785968,
                        "md5": "f26d65661b0474622b16922f46386375",
                        "size": 1099264
                    }
                ],
                "flags": [
                    "executable"
                ],
                "path": "Config2_DX9.exe",
                "sha256": "5ccb3af3adf3c5fe5c180128e0596fbb23b67f4a4c4ea2227edb2334539ca09b",
                "type": "DepotFile"
            },
            ...
```

Note that files can sometimes have multiple chunks

```json
{
    "chunks": [
        {
            "compressedMd5": "98406c607c2a36286951e38c9745ba40",
            "compressedSize": 10147685,
            "md5": "b880a81628e5894183b536fd583f29ae",
            "size": 10485760
        },
        {
            "compressedMd5": "132bad7f9b22480373ccce40d8fed0c0",
            "compressedSize": 10318037,
            "md5": "e49c513990e4f72508e14d617256a7f1",
            "size": 10485760
        },
        {
            "compressedMd5": "0b04d60906db4a60f1193bd4fd96de41",
            "compressedSize": 10425727,
            "md5": "86e79fa113ab6ff67a9d11a91790bc59",
            "size": 10485760
        },
        {
            "compressedMd5": "a096f0cd00cea0d759c6765792d305b1",
            "compressedSize": 10206289,
            "md5": "f0526bf27c81b0105509e1dea5c1e0ff",
            "size": 10485760
        },
        {
            "compressedMd5": "1c31832ee37c672f56dd5467f12ceb41",
            "compressedSize": 10195354,
            "md5": "9aa67c55ca91846eb22a0a3e4a2f764d",
            "size": 10485760
        },
        {
            "compressedMd5": "b5c7249bc94a1fe54fc5ae29d814c441",
            "compressedSize": 10291149,
            "md5": "e50ccb0e0b55663a522da0d6967e40f2",
            "size": 10485760
        },
        {
            "compressedMd5": "9741c3be1825b6df780759cf6c215286",
            "compressedSize": 10360747,
            "md5": "adb9925476e06aa67ae71c841f2c8b55",
            "size": 10485760
        },
        {
            "compressedMd5": "53fad8c31946deccc5ab52835d0a6565",
            "compressedSize": 10332534,
            "md5": "b7e03697174b7d68eec149f3a38930ab",
            "size": 10485760
        },
        {
            "compressedMd5": "309db429420081e42a99cc27a5f85174",
            "compressedSize": 10359744,
            "md5": "4040bd5bc077b8bc69358a835fb2d068",
            "size": 10485760
        },
        {
            "compressedMd5": "05241370d352f6e745e50d187ccc31f8",
            "compressedSize": 10427653,
            "md5": "cb92ebf8e136b4d83d9d99c8e1fab6b8",
            "size": 10485760
        },
        {
            "compressedMd5": "579430e1e99a7bb3e9842fcbf872227d",
            "compressedSize": 10400344,
            "md5": "3a358bd796bf512254c746055a5fe51a",
            "size": 10485760
        },
        {
            "compressedMd5": "8ab5917d4c94b23abe62c0de4d7e22da",
            "compressedSize": 10040449,
            "md5": "6e5687a7731911b08e47877c344b0a83",
            "size": 10485760
        },
        {
            "compressedMd5": "350727d359b80d7c975ebdc2b1ede60d",
            "compressedSize": 10218914,
            "md5": "7e1426b4231e1df890dccc144a0f74ad",
            "size": 10485760
        },
        {
            "compressedMd5": "a792030e1e77037ea514ca1c6a58dc21",
            "compressedSize": 10439010,
            "md5": "985c107f4349bfd36285ef70d721585b",
            "size": 10485760
        },
        {
            "compressedMd5": "533d9aab2ca4d07a5e8a38e22c0324b6",
            "compressedSize": 10472191,
            "md5": "55a303a5044580e3fac165b2a11659af",
            "size": 10485760
        },
        {
            "compressedMd5": "aff71fe137ec0c41afb70ed065b53468",
            "compressedSize": 10436894,
            "md5": "9f162b2f1ad288d3b57562237fa5bd12",
            "size": 10485760
        },
        {
            "compressedMd5": "c10c22b8627879bfc22d0abbbae9e8a5",
            "compressedSize": 10314153,
            "md5": "529c8816829417cc7e06d03bb6bee544",
            "size": 10485760
        },
        {
            "compressedMd5": "051244c4c24980b2ce0b0de71510dfc0",
            "compressedSize": 10055400,
            "md5": "70ee042e5aa0905da77459bec50691f3",
            "size": 10485760
        },
        {
            "compressedMd5": "3503fc3d1238bc8ac1f53a9ac5f75f4b",
            "compressedSize": 10166454,
            "md5": "ee07424265bc0e70eae6842c9c0e3b65",
            "size": 10485760
        },
        {
            "compressedMd5": "6314bfd461073725dc05b04cbd98f137",
            "compressedSize": 10413701,
            "md5": "a524bb4a983595fabf025812af18c2a5",
            "size": 10485760
        },
        {
            "compressedMd5": "3b4a45beb6529bcd710a8654aebd7385",
            "compressedSize": 10207625,
            "md5": "34980066a5aea38c82a6d2c3432ccb7e",
            "size": 10485760
        },
        {
            "compressedMd5": "98c3f13fd94093edd8d66c844768e8df",
            "compressedSize": 10329518,
            "md5": "dd827f8e801e86887601c496d353f9db",
            "size": 10485760
        },
        {
            "compressedMd5": "566771f723f9c8a21d3916f5daeca97d",
            "compressedSize": 10359292,
            "md5": "ec93b6aa3a4d0f307415f6f5ddf917d8",
            "size": 10485760
        },
        {
            "compressedMd5": "3ea64ea2687ddd4486b6ff6c13bd9f09",
            "compressedSize": 10720550,
            "md5": "b29b644d7a25a6b40d65d5872ca3b289",
            "size": 13167442
        }
    ],
    "md5": "a3e9d297cb3c696e54e7881058cfea23",
    "path": "ed6_2_op.avi",
    "type": "DepotFile"
},
```

The most useful thing for us here are:

- `md5`: This contains the MD5 hash, same as found in the `goggame-{gameid}.hashdb`.
- `path`: The path of the file.

If a file has only 1 chunk, the `md5` of the first chunk is the `md5` of the file.

If the file has multiple chunks, there is a separate `md5` field beside the path,
and that is the hash of the file.

### Downloading Files

!!! warning "TODO: We'll figure this out later."

You need to perform OAuth authentication using the steps described in the
[Game Launcher Research][game-launcher-research] wiki.

## Unsolved Questions

- Can games have relative file paths that are over 1024 characters?
    - Is there a special version of `goggame-{gameid}.hashdb` to handle that?
- Are there cases where you don't want to download all the depots (e.g., games with language-specific depots)?

[game-launcher-research]: https://github.com/Lariaa/GameLauncherResearch/wiki/GoG-:-Installing-games