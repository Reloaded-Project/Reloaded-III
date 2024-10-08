# Storage Locations

!!! note "Note: Location of The Server Itself is Not Discussed Here."

    The `Server` binary should be distributed alongside or as part of the Front-End [(Launcher)][launcher].<br/>
    An outdated `Server` binary will simply self-update, no worries.

!!! example "Example Problem."

    You are at a LAN party or an Office Space. You want to quickly start playing modded online
    with your friends but the machine you're at is not the machine you used the last time.

    Another person last using the machine has previously downloaded the mods.<br/>
    You shouldn't need to download and store them on disk again.

Achieving these advanced use cases requires some careful planning.

For example `Mod`(s) themselves could be stored in a location that's shared between all users on a machine,
provided they don't store any user specific data, for example ***mod settings***.

## Scoped Storage System

!!! info "Data stored by Reloaded3 is categorised into the following categories."

- **Machine (Persistent)**: Machine specific data that cannot be regenerated.
    - Should not be deleted by user manually.
    - For example, Game Backups.
- **Machine (Non-Persistent)**: Machine specific data that can be regenerated.
    - These items can be safely deleted when not used.
    - For example, Downloaded packages (Mods, Tools etc.)
    - Items that can always be restored with [Package Metadata][package-metadata].
- **User**: User specific data.
    - Settings, loadouts, configurations etc.

## Where are the Files Stored?

- **Machine (Persistent)**:
    - Windows: `C:\ProgramData\Reloaded3\Main` (a.k.a. `$CommonApplicationData`+`Main`)
    - macOS: `/Library/Application Support/Reloaded3`
    - Linux: `/var/lib/Reloaded3` ([Filesystem Hierarchy Standard Info][var-lib])

- **Machine (Non-Persistent)**:
    - Windows: `C:\ProgramData\Reloaded3\Cache` (a.k.a. `$CommonApplicationData`+`Cache`)
    - macOS: `/Library/Caches/Reloaded3`
    - Linux: `/var/cache/Reloaded3` ([Filesystem Hierarchy Standard Info][var-cache])

- **User**:
    - Windows: `C:\Users\{User}\AppData\Roaming\Reloaded3` (a.k.a. `ApplicationData`)
    - macOS: `~/Library/Application Support/Reloaded3`
    - Linux: `~/.local/share/Reloaded3` (a.k.a. `XDG_DATA_HOME`)

Also see: [Portable Installs](#portable-install).

## Items to Store

!!! info "What do we want to store and where do we store it?"

### Machine (Non-Persistent)

| Item                                                 | Subfolder                   | Description                                                                |
| ---------------------------------------------------- | --------------------------- | -------------------------------------------------------------------------- |
| [Packages][package-metadata]                         | `Packages`                  | Pretty much anything you can download (Mods, Tools, etc.).                 |
| Temporary Files (Mods)                               | `Temp/{processId}`[1]       | Runtime-generated temporary files. Not persisted across runs.              |
| [Server Cache Files](#server-cache-files)            | `Cache/Server`              | Cache files tied to the Reloaded3 server.                                  |
| [Package Cache Files](#cache-files-machine-specific) | `Cache/Package/{packageId}` | Cache files that consist of inputs that do not contain [User](#user) data. |
| [Hash Cache Files](#hash-cache-files)                | `Hashes`                    | File hash caches.                                                          |

[1] Temporary Files should be tied to `ProcessID`, if a process with that ID is dead, they should be
auto deleted by the server. To avoid files in use accidentally being deleted, temporary files are stored
in persistent storage. We will auto clean them ourselves.

### User

| Item                                              | Subfolder                    | Description                                                           |
| ------------------------------------------------- | ---------------------------- | --------------------------------------------------------------------- |
| [Loadouts](#loadouts)                             | `Loadouts`                   | Loadouts that are private to the current user.                        |
| [Added Games][game-metadata]                      | `Games/{gameId}`             | And all of user's global preferences for that game.                   |
| Package Configs                                   | Inside [Loadouts](#loadouts) | Extra details in [Package Config Handling](#package-config-handling). |
| [Package Cache Files](#cache-files-user-specific) | `Cache/Package/{packageId}`  | Cache files that have inputs ***with user data***.                    |

## Extra Details on Stored Items

### Cache Files

!!! note "Cache format is specific to the package/implementation."

Each package gets its own cache folder. The package itself is responsible it can handle errors
with the cache, such as a version/format upgrade.

!!! note "There are 2 `Cache` folders, *machine* and *user* specific."

#### Cache Files (Machine Specific)

!!! info "These are cache files that are not specific to a loadout or any user data."

This category covers >90% (most) of cache files, including:

- [Merged Files][merged-files].
- Pre-parsed metadata for game files.

#### Cache Files (User Specific)

!!! info "These are cache files that are specific to a user."

Basically stuff that doesn't make sense to share between users.

Examples include:

- User's replays of last *X* games.
- Cookies, tokens, etc.

### Server Cache Files

!!! note "These are cache files tied to the Reloaded3 server."

It has the following structure:

```
CommunityRepository
```

#### Community Repository

!!! info "This contains a local cache of the [Community Repository][community-repository]"

This folder consists of a file named `etag.txt` and a copy of the `Nx` packed
[CommunityRepository.nx][community-repository-hosting].

The ETag will be used to determine if the local cached archive is outdated.

If it is, we will download the new [CommunityRepository.nx][community-repository-hosting], else
we'll use the local cache.

### Loadouts

!!! info "The file format of the actual loadouts is defined in the [Loadouts][loadouts] page."

Loadouts are stored in the `Loadouts` folder.

=== "LMDB Implementation"

    Packed loadouts and snapshots are stored inside `database.mdb`.

    ```
    .
    ├── 7f2cc8b7d9f1e3a5
    │   └── ... unpacked files
    └── database.mdb
        ├── 7f2cc8b7d9f1e3a5.nx
        └── 7f2cc8b7d9f1e3a5.snapshot.bin
    ```

=== "FileSystem Reference Implementation"

    This is a reference implementation for testing and for use in
    [esoteric platforms] where LMDB may be hard to compile.

    ```
    Loadouts
    ├── 7f2cc8b7d9f1e3a5
    │   └── ... unpacked files
    ├── 7f2cc8b7d9f1e3a5.nx
    └── 7f2cc8b7d9f1e3a5.snapshot.bin
    ```

For the exact details, see the [Loadouts][loadouts-location] page.

### Hash Cache Files

!!! info "This folder stores the unmodified last states of files in packages and games."

    [Documentation can be found here][hashcache-docs].

This folder has the following layout:

```
Hashes
└── hashes.mdb
    ├── 24c69d40-090e-406b-9a1b-2487571a568c.hashcache
    └── reloaded3.utility.examplemod.s56+1.2.3.hashcache
```

Details on how the hash cache files are is in the [Usage in Server][hash-cache-usage] page.

The hash cache files are stored inside a [lmdb][fs-performance] database, named `hashes.mdb`.

### Package Config Handling

!!! info "Package configs are stored inside [Loadouts](#loadouts)."

However, that may raise some questions, so here they are.

1. **Why are package configs stored in Loadouts?**
    - Performance. Random file access is slow on Windows; so we want to avoid that.
    - See [Loader Binary Format](https://github.com/Reloaded-Project/Reloaded-III/issues/34) for more info. <!-- (TODO: Replace Link to format page) -->

2. **How can I modify configs in real time?**
    - Configs can be adjusted in real time in two ways, **with saving** and **without saving**.
    - Without saving can be done entirely in-process when inside a game.
    - With saving will spawn a server process (if one does not already exist), and commit a save via server API. <!-- (TODO: Link to server API) -->

3. **How are tool configs stored?**
    - Tools can specify locations of config files inside [Package Metadata][package-metadata].
    - When a loadout is loaded or tool stops running, updated configs are `ingested` (integrated) into the loadout.
    - If local files are newer than remote files, the user is prompted if they wish to `integrate`.

## Extra

### Multi-User Networked Systems

- On Windows, files in `AppData/Roaming` are usually downloaded upon login in multi-user setup
  configurations, and this download typically happens on every login.

- On Linux systems, it's much more likely that the Home Directory is accessed over the network in
  real-time, resulting in no wait time at the expense of high latency. Likely with some sort of
  caching mechanism in place.

- To optimize performance, keep user data as small as possible, and ensure we don't unnecessarily
  access too many small files. Parallelize file access if possible to reduce the impact of high latency.

### Portable Install

!!! warning "Portable Use is Discouraged"

    Unless the game you're modding is itself portable, i.e. on a USB stick,
    use of portable mode should be discouraged.

The Server & Loader will recognise the following condition as 'portable':

> *A folder named `.Reloaded3` exists in the same folder as the game and Server binary.*

In this case the following locations should be used.

- **Machine (Persistent)**: `.Reloaded3/Main`
- **Machine (Non-Persistent)**: `.Reloaded3/Cache`
- **User**: `.Reloaded3/User`

For `Tools` downloaded via the R3 package manager, they should assume portable mode if `.Reloaded3`
is part of the path to the main binary.

!!! note "About Portable Installs"

    Some users will (very strongly) insist that they want to run Reloaded3 in a 'portable' way.

    Sometimes it's personal preference, sometimes it's a more niche use case like running a modded
    game on a USB stick.

## Future Considerations

Loadouts and package configs may be shared in the future on a machine level.

| Item                     | Subfolder                    | Description                                 |
| ------------------------ | ---------------------------- | ------------------------------------------- |
| Loadouts (Shared)        | `Loadouts`                   | Loadouts that are shared between all users. |
| Package Configs (Shared) | `PackageConfigs/{packageId}` | Config/Save files for packages.             |

[game-metadata]: ../Storage/Games/About.md
[loadouts]: ./Loadouts/About.md
[loadouts-location]: ./Loadouts/About.md#location
[loadout-file-format]: ./Loadouts/About.md#loadout-file-format
[package-metadata]: ../Packaging/Package-Metadata.md
[community-repository]: ../../Services/Community-Repository.md
[community-repository-hosting]: ../../Services/Community-Repository.md#hosting
[loadout-snapshot]: ./Loadouts/About.md#snapshots
[var-lib]: https://refspecs.linuxfoundation.org/FHS_3.0/fhs/ch05s08.html
[var-cache]: https://refspecs.linuxfoundation.org/FHS_3.0/fhs/ch05s05.html
[merged-files]: ../../Mods/Libraries/Merged-File-Cache/About.md
[hashcache-docs]: ../../Common/Hash-Cache/About.md
[hash-cache-usage]: ../../Common/Hash-Cache/Usage-In-Server.md
[fs-performance]: ../../Research/FileSystem-Performance.md
[esoteric platforms]: ../../Code-Guidelines/Code-Guidelines.md#esoteric-and-embedded-platforms
[tools-as-packages-approach]: ../Packaging/Tools-As-Packages.md#chosen-approach