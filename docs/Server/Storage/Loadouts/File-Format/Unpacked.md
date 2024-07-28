!!! info "This lists the format of the binary data used by an unpacked loadout."

    For the location of folder containing unpacked loadout, see the [Locations][locations] page.

| Item                                                     | Path                                                                                                   | Description                                                           |
| -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------- |
| [Header](#headerbin)                                     | `header.bin`                                                                                           | Header with current loadout pointers. Facilitates 'transactions'.     |
| [Events](#eventsbin)                                     | `events.bin`                                                                                           | List of all emitted events in the loadout.                            |
| [Timestamps](#timestampsbin)                             | `timestamps.bin`                                                                                       | Timestamps for each commit.                                           |
| [Commit Parameters](#commit-parameters)                  | `commit-parameter-types.bin`<br/>+`commit-parameter-lengths-{x}.bin`<br/>+ `commit-parameters-{x}.bin` | List of commit message parameters for each event.                     |
| [Configs](#configbin)                                    | `config.bin`<br/>+ `config-data.bin`                                                                   | Package Configurations.                                               |
| [Package Reference (IDs)](#package-references)           | `package-reference-ids.bin`                                                                            | Hashes of package IDs in this loadout.                                |
| [Package Reference (Versions)](#package-references)      | `package-reference-versions-len.bin`<br/>+ `package-reference-versions.bin`                            | String versions of package IDs in this loadout.                       |
| [Store Manifests](#storesbin)                            | `stores.bin`<br/>+ `store-data.bin`                                                                    | Game store specific info to restore game to last version if possible. |
| [Commandline Parameters](#commandline-parameter-databin) | `commandline-parameter-data.bin`                                                                       | Raw data for commandline parameters. Length specified in event.       |

These files are deliberately set up in such a way that making a change in a loadout means appending
to the existing files. No data is overwritten. Rolling back in turn means truncating the files to the desired length.

In some cases, data is grouped to improve compression ratios by bundling similar data
together when sharing.

And in other cases, we put cold data that is infrequently accessed, e.g. `commit message` params in
a separate file as that information is rarely accessed.

!!! note "All values are in little endian unless specified otherwise."

    They are shown in lowest to highest bit order.<br/>
    So an order like `u8`, and `u24` means 0:8 bits, then 8:32 bits.

## header.bin

!!! info "This is a master file which tracks the state of other files in the loadout."

This stores the version of the loadout and structure counts for remainder of the loadout files.

In the event of an unexpected crash, this file is used to determine the last state of the Loadout before
performing a cleanup of unused data (by truncating remaining files).

Format:

| Data Type | Name            | Description                                                  |
| --------- | --------------- | ------------------------------------------------------------ |
| `u16`     | Version         | Version of the loadout format.                               |
| `u16`     | Reserved        |                                                              |
| `u32`     | NumEvents       | Total number of events and timestamps in this loadout.       |
| `u32`     | NumMetadata     | Total number of package metadata files in this loadout.      |
| `u32`     | NumConfigs      | Total number of package configuration files in this loadout. |
| `u32`     | NumGameVersions | Total number of game versions.                               |

!!! warning "Backwards compatibility is supported but not forwards."

    If you're loading a `Version` that is newer than what you support, you should reject the file
    to avoid errors.

## events.bin

!!! info "This file contains all of the events that occurred in this loadout."

Each event has a 1:1 mapping to a timestamp in [timestamps.bin](#timestampsbin).
The number of events stored here is stored in [header.bin](#headerbin).

!!! info "The event format is documented in the [Event List Page][events]."

As a summary. Each event is composed of an `u8` EventType and 0, 8, 24 or 56 bits of InlineData
(depending on `EventType`). Events are laid out such that they [align with 8 byte boundaries][events].

Any data that doesn't fit in the `InlineData` field is stored in another file and loaded by index.
Details of that can be seen on each individual event entry.

### Optimizing Events

!!! tip "Sometimes events can be optimized."

For example, if a package is added and then immediately enabled, we can cancel out the events.

As the nature of the events is such that they are always appended, we don't do this during normal operation.
However, when we pack the loadout we will run certain clever optimizations like this to reduce clutter
and save space.

Situations where optimizations are applied at pack stage will be noted in the event's description.

## timestamps.bin

!!! info "This contains the timestamp for each event."

!!! tip "Each timestamp here corresponds to an event in [events.bin](#eventsbin)."

This is an array of 32-bit timestamps ([`R3TimeStamp[]`][max-numbers]). The number of items is defined in
[header.bin](#headerbin).

## config.bin

!!! info "This stores all historical mod configurations for any point in time."

This is the array of file sizes, each being:

| Data Type | Name     | Description                     |
| --------- | -------- | ------------------------------- |
| `u16`     | FileSize | Size of the configuration file. |

Every new config is appended to [config-data.bin](#config-databin) as it is added.

Each unique config has an index, a.k.a. [ConfigIdx][max-numbers], which is an incrementing value from 0
every time a config is added. Emitted events refer to this index.

!!! question "How do you use this data?"

    When loading a loadout, calculate the offsets of each config in memory, by iterating through the
    `FileSize` field(s).

    - First config is at 0
    - Second is at 0 + `FileSize(first)`
    - Third is at `second` + `FileSize(second)`.

    etc. As you do this also, hash the configs. ([AHash][hashing] recommended)

    When a new config is created, hash it and check if it's a duplicate, if it isn't, add it to the
    config list.

### config-data.bin

!!! info "This is a buffer of raw, unmodified configuration files."

You can get the file size and offsets from the [config.bin](#configbin) file.

## Package References

!!! info "A 'package reference' consists of a [XXH3(PackageID)][hashing] and Version."

    From [Package.toml][package-toml].

    This is the minimum amount of data required to uniquely identify a package.

Packages are referred to by an index known as [MetadataIdx][max-numbers] in the events.

So a `MetadataIdx == 1` means `fetch the entry at index 1` of [package-reference-ids.bin](#package-reference-idsbin)
and [package-reference-versions.bin](#package-reference-idsbin).

As for how to use the data, it is similar to [config.bin](#configbin), essentially we deduplicate
entries by in-memory hash. So an event can always refer to a [MetadataIdx][max-numbers] created
in an earlier event to save space.

!!! danger "Launcher MUST ensure each published mod has valid update/download data."

    Otherwise this system could fail, as a hash of packageID is not useful.

### package-reference-ids.bin

!!! info "This is a buffer of [XXH3(PackageID)][hashing]"

    Each entry is 8 bytes long.

Using a 64-bit hash, we need around 5 billion hashes until we reach a 50% chance of collision,
that's quite plenty!

System can still always fail, we just pray it won't.

!!! note "Some Numbers"

    Nexus Mods alone hosts 815999 mods as of 30th of May 2024 (obtained via GraphQL API).

    The probability of a hash collision on whole mod set is roughly the following:

    ```python
    >>> r=815999
    >>> N=2**64
    >>> ratio = 2*N / r**2
    >>> ratio
    55407743.67551148
    >>> 1-math.exp(-1/ratio)
    1.8048018635141716e-08
    ```

    That ends up being ~0.0000018%
    I'll be damned if R3 comes anywhere close to that.

Anyway, assuming a more modest '100000' mods will be made in R3's lifetime, we can expect
a probability of 0.0000000027%, or more than 1 in 3.7 trillion.

If I'm ever *that* successful, I'd probably be funded enough that I could extend this to 128-bit hash,
and at that point a meteor is more likely to land on your house (no joke).

### package-reference-versions-len.bin

Contains the lengths of entries in [package-reference-versions.bin](#package-reference-idsbin).

| Data Type | Name          | Description                 |
| --------- | ------------- | --------------------------- |
| `u8`      | VersionLength | Size of the Version string. |

!!! tip "This data compresses extremely well."

    Most versions are of form `X.Y.Z` so there is a lot of repetition of `05`.

### package-reference-versions.bin

!!! info "This is a buffer consisting of package versions, whose length is defined in [package-reference.bin](#package-references)"

These versions are stored as UTF-8 strings. No null terminator.

!!! tip "This data compresses extremely well."

    Because the randomness (entropy) of values is low, the version components
    are super commonly 1s and 0s, and almost always all first two numbers `0-1` and dot `.`

### Restoring Actual Package Files

!!! info "We follow a multi step process in order to reliably try restore Reloaded3 packages."

First we attempt to obtain full package metadata from [Central Server][central-server].

!!! failure "But what if [Central Server][central-server] is down?"

We will query the [Static CDN API][static-cdn-api].
That contains a dump of the latest package update info.

## stores.bin

!!! info "This stores all game store specific info."

!!! info "Why do we store this info?"

    This info can be used to identify the game when you share the loadout with a friend,
    and the game isn't known by the [Community Repository][community-repository].

    Or in the event that you cloud sync a game (between your machines) that's not known
    by the [Community Repository][community-repository].

    It can also be used to identify when game updates have taken place when auditing the log.

| Data Type                      | Name      | Description                              |
| ------------------------------ | --------- | ---------------------------------------- |
| `u8` [(StoreType)][store-type] | StoreType | The store from which the game came from. |
| `u16`                          | FileSize  | Size of the configuration file.          |
| `u8`                           |           | Currently Unused                         |

The offsets can be derived from file sizes.

Basically this contains data specific to game stores such as `GOG`, `Steam`, `Epic` etc. that can
be used to revert the game to an older version.

!!! warning "Reverting to earlier versions is not possible in all game stores."

### store-data.bin

When values, e.g. strings are not available, they are encoded as 0 length strings, i.e. constant 00.

- `String8` is assumed to be a 1 byte length prefixed UTF-8 string.
- `String16` is assumed to be a 2 byte length prefixed UTF-8 string.

#### CommmonData Struct

!!! info "This struct is shared between all store entries."

i.e. This game was manually added.

| Data Type  | Name    | Description                                               |
| ---------- | ------- | --------------------------------------------------------- |
| `u64`      | ExeHash | The hash of the game executable (using [(XXH3)][hashing]) |
| `String16` | ExePath | The path to the game executable                           |
| `String8`  | AppId   | The application ID of the game                            |

We store this for every game, regardless of store.

#### Unknown

| Data Type    | Name       | Description                  |
| ------------ | ---------- | ---------------------------- |
| `u8`         | Version    | The version of the structure |
| `CommonData` | CommonData | The common data structure    |

#### Steam

| Data Type    | Name           | Description                                               |
| ------------ | -------------- | --------------------------------------------------------- |
| `u8`         | Version        | The version of the structure                              |
| `CommonData` | CommonData     | The common data structure                                 |
| `u64`        | AppId          | The Steam application ID                                  |
| `u64`        | DepotId        | The Steam depot ID                                        |
| `u64`        | ManifestId     | The Steam manifest ID                                     |
| `String8`    | Branch         | The Steam branch name                                     |
| `String8`    | BranchPassword | The password for the Steam branch (if password-protected) |

To perform rollback, will maintain basic minimal change fork of `DepotDownloader`,
no need to reinvent wheel. Manifest contains SHA checksums and
all file paths, we might be able to only do partial downloads.

To determine current version, check the App's `.acf` file in
`steamapps`. The `InstalledDepots` will give you the current
`Depot` and `Manifest` ID. Steam does not unfortunately have
user friendly version names.

To determine downloadable manifests, we'll probably have to use
`SteamKit2`. Use [DepotDownloader code][depot-downloader] for inspiration.

#### GOG

Extended details in [Stores: GOG][gog].

We can get the info from the registry at
`HKEY_LOCAL_MACHINE\Software\GOG.com\Games\{GameId}`

| Data Type    | Name        | Description                                         |
| ------------ | ----------- | --------------------------------------------------- |
| `u8`         | Version     | The version of the structure                        |
| `CommonData` | CommonData  | The common data structure                           |
| `u64`        | GameId      | The unique identifier for the game on GOG           |
| `u64`        | BuildId     | The [unique identifier for the build][gog-buildid]  |
| `String8`    | VersionName | The user-friendly version name for display purposes |

The `VersionName` is also copied into the commit message on each update.

To identify the version reliably, it seems we will need to compare the hashes against the ones in the different depots.

This will also allow us to support e.g. Heroic on Linux.

##### Heroic & Playnite

!!! note "These are 3rd party launchers that support GOG"

    They need to be supported, because there's no official Linux launcher.

!!! info "TODO: To be determined."

#### Epic

!!! warning "Version downgrade with Epic isn't possible."

    We will store the minimal amount of data required to identify the game in the hopes it is one day.

With Epic we can nip this data from `C:\Program Data\Epic\EpicGamesLauncher\Data\Manifests`.
We want the following:

| Data Type    | Name             | Description                                  |
| ------------ | ---------------- | -------------------------------------------- |
| `u8`         | Version          | The version of the structure                 |
| `CommonData` | CommonData       | The common data structure                    |
| `u128`       | CatalogItemId    | The MD5 hash identifier for the game on Epic |
| `String8`    | AppVersionString | The version string of the game on Epic       |

These values are directly extracted from the manifest file.

#### Microsoft

!!! warning "Version downgrade with Microsoft isn't possible."

    We will store the minimal amount of data required to identify the game in the hopes it is one day.

We're interested in `AppXManifest.xml` in this case.

| Data Type    | Name              | Description                                                                                                           |
| ------------ | ----------------- | --------------------------------------------------------------------------------------------------------------------- |
| `u8`         | Version           | The version of the structure                                                                                          |
| `CommonData` | CommonData        | The common data structure                                                                                             |
| `String8`    | PackageFamilyName | The unique identifier for the game on the Microsoft Store. [{Identity.Name}_{hash(Identity.Publisher)}][ms-store-pfm] |
| `String8`    | PackageVersion    | The version of the game package on the Microsoft Store, from `Identity` field.                                        |

The `PackageVersion` is actually a four part version, but is stored as string, so just in case an invalid
version exists in some manifest, we will string it.

### commandline-parameter-data.bin

This file contains the raw strings for commandline parameters.
The lengths of the parameters are specified in the [UpdateCommandline event][update-command-line].

## Commit Parameters

!!! tip "These files contain the parameters for any event that requires additional info in its commit message."

    The [Commit Message][commit-messages] file lists when messages appear in this file for each message.

    When the message is not a [contextual-parameter][commit-messages-contextual], it is stored in this file.

!!! note "A timestamp is shown beside each event, it does not need to be embedded into description."

### An Example

You emit the [PackageStatusChanged event][event-packagestatuschanged] with the message
[commit-messages-packageadded][commit-messages-packageadded]:

```
Added '**{Name}**' with ID '**{ID}**' and version '**{Version}**'.
```

Which could be marked as:

```
Added '**Super Cool Mod**' with ID '**reloaded3.utility.scmexample**' and version '**1.0.0**'
```

#### Encoding

!!! note "Parameters are encoded in the order in which they appear in the template!!"

This would be encoded as:

1. [commit-parameter-types.bin](#commit-parameters-typesbin): [0, 0, 0]

    Explanation:

    - 0: UTF-8 Char Array for "Super Cool Mod"
    - 0: UTF-8 Char Array for "reloaded3.utility.scmexample"
    - 0: UTF-8 Char Array for "1.0.0"

2. [commit-parameters-lengths.bin][commitparam8len]: [14, 28, 5]

    Explanation:

    - 14: Length of "Super Cool Mod"
    - 28: Length of "reloaded3.utility.scmexample"
    - 5: Length of "1.0.0"

3. [commit-parameters-text.bin](#parametertype):

    - `Super Cool Mod`
    - `reloaded3.utility.scmexample`
    - `1.0.0`

    These strings are written directly to the `commit-parameters-text.bin` file, without any null
    terminator or padding.

4. [commit-parameters-versions.bin](#commit-parameters-versionsbin): [0]

    Explanation:

    - 0: Version of the commit message.

    It's 0 because this is the initial version of the message format.

#### With [Back References](#back-references)

!!! info "Suppose you wanted to repeat the earlier parameter, we would use [back references](#back-references)."

1. [commit-parameter-types.bin](#commit-parameters-typesbin): [7, 7, 7]

    Explanation:

    - 5: BackReference8 for `"Super Cool Mod"`
    - 5: BackReference8 for `"reloaded3.utility.scmexample"`
    - 5: BackReference8 for `"1.0.0"`

2. [commit-parameters-backrefs-8.bin](#back-references): [0, 1, 2]

    Explanation:

    - 0: Index of `"Super Cool Mod"`
    - 1: Index of `"reloaded3.utility.scmexample"`
    - 2: Index of `"1.0.0"`

3. [commit-parameters-versions.bin](#commit-parameters-versionsbin): [0]

    Explanation:

    - 0: Version of the commit message.

    It's still 0 because we're using the same message format, just with back references.

#### With [Back References](#back-references) (Optimized)

!!! info "Suppose you have multiple parameters to backreference, there are optimized variants."

Let's say we want to reference all three parameters from the previous example in a new event:

1. [commit-parameter-types.bin](#commit-parameters-typesbin): [11]

    Explanation:

    - 11: BackReference3_8 for all three parameters

2. [commit-parameters-backrefs-8.bin](#back-references): [0, 1, 2]

    Explanation:

    - 0: Index of `"Super Cool Mod"`
    - 1: Index of `"reloaded3.utility.scmexample"`
    - 2: Index of `"1.0.0"`

3. [commit-parameters-versions.bin](#commit-parameters-versionsbin): [0]

    Explanation:

    - 0: Version of the commit message.

This optimized approach uses a single [ParameterType](#parametertype) (`11: BackReference3_8`) to
reference all three parameters at once, reducing the overall size of the encoded data.

It's particularly efficient when you need to reference multiple consecutive parameters from a
previous event.

#### Decoding

!!! info "To construct commit messages from the unpacked loadout data, follow these steps."

1. **Read Events Sequentially**:<br/>
   Process the events in [events.bin][events-bin] in the order they appear.

2. **Determine Commit Message Type**:<br/>
   Based on the event type, identify the corresponding commit message template from [Commit-Messages.md][commit-messages].<br/><br/>
   These are listed in the [Event List][events] page for each event under the `Messages` section ([Example][events-messages])

3. **Check Message Version**:<br/>
   Read the version of the commit message from [commit-parameters-versions.bin][commit-param-versions].<br/>
   This ensures you're using the correct message format for that event type.

4. **Read and Process Parameters**:<br/>

    1. Fetch the pre-parsed message template. (and number of parameters)
    2. Read the parameter types from [commit-parameter-types.bin][commit-param-types].
    3. Based on the parameter types, retrieve the actual parameter data from the appropriate locations:
        - Contextual parameters like `EventTime` can be inferred from the event context.
        - Text data from [commit-parameters-text.bin](#parametertype)
        - Timestamps from [commit-parameters-timestamps.bin](#parametertype)
        - Back references from the appropriate [commit-parameters-backrefs-*.bin][commit-param-backrefs] file
        - Lists from [commit-parameters-lists.bin][commit-param-lists]

5. **Construct the Message**:
   Use the template from step 2 and fill in the parameters obtained in steps 4 and 5.

### commit-parameters-types.bin

This is an array of:

| Data Type | Name                            | Description            |
| --------- | ------------------------------- | ---------------------- |
| `u8`      | [ParameterType](#parametertype) | Type of the parameter. |

### commit-parameters-versions.bin

!!! info "This enables versioning, ensuring that different variations of the same commit message can coexist."

!!! warning "There should be 1 entry for each event!! Regardless of whether it has a message or not!!"

This is an array of:

| Data Type | Name    | Description                    |
| --------- | ------- | ------------------------------ |
| `u8`      | Version | Version of the commit message. |

This is an array of `u8` values which correspond to the version of the commit message last issued.

For example, if the message for an event like [PackageStatusChanged][message-packagestatuschanged]
is encoded in its current version, it would be written as `0`:

```
Added '**{Name}**' with ID '**{ID}**' and version '**{Version}**'.
```

However if the ***meaning***, **order of parameters** or ***number of parameters changes***, for example:

```
Added '**{Name}**' with ID '**{ID}**' and version '**{Version}**' at '**{Timestamp}**'.
```

Then the number will be `1`.

In practice expect to see only `0`, the text for most commit messages is unlikely to ever change.

!!! note "Compressing 1M zeroes with zstd yields file size of ~50 bytes."

### commit-parameters-lengths-8.bin

This is an array of:

| Data Type | Name            | Description                       |
| --------- | --------------- | --------------------------------- |
| `u8`      | ParameterLength | Length of the parameter in bytes. |

### commit-parameters-lengths-16.bin

This is an array of:

| Data Type | Name            | Description                       |
| --------- | --------------- | --------------------------------- |
| `u16`     | ParameterLength | Length of the parameter in bytes. |

### commit-parameters-lengths-32.bin

This is an array of:

| Data Type | Name            | Description                       |
| --------- | --------------- | --------------------------------- |
| `u32`     | ParameterLength | Length of the parameter in bytes. |

### ParameterType

`ParameterType` is defined as:

| Type | Data Type                                               | Example                                 | Description                                                                             |
| ---- | ------------------------------------------------------- | --------------------------------------- | --------------------------------------------------------------------------------------- |
| `0`  | `UTF-8 Char Array (u8 length)`                          | `Hello, World!`                         | UTF-8 characters, length stored in [commit-parameters-lengths-8.bin][commitparam8len]   |
| `1`  | `UTF-8 Char Array (u16 length)`                         | `A longer string...`                    | UTF-8 characters, length stored in [commit-parameters-lengths-16.bin][commitparam16len] |
| `2`  | `UTF-8 Char Array (u32 length)`                         | `An even longer string...`              | UTF-8 characters, length stored in [commit-parameters-lengths-32.bin][commitparam32len] |
| `3`  | `u32` ([R3TimeStamp][max-numbers])                      | `1st of January 2024`                   | Renders as human readable time.                                                         |
| `4`  | `u32` ([R3TimeStamp][max-numbers])                      | `5 minutes ago`                         | Renders as relative time.                                                               |
| `5`  | `u8` [(BackReference8)](#back-references)               | Entry 1                                 | Reference to a single previous item.                                                    |
| `6`  | `u16` [(BackReference16)](#back-references)             | Entry 2                                 | Reference to a single previous item.                                                    |
| `7`  | `u24` [(BackReference24)](#back-references)             | Entry 3                                 | Reference to a single previous item.                                                    |
| `8`  | `u32` [(BackReference32)](#back-references)             | Entry 4                                 | Reference to a single previous item.                                                    |
| `9`  | `variable` [List](#parameter-lists)                     | See [Parameter Lists](#parameter-lists) | Defines the start of a list.                                                            |
| `10` | `u8, u8` [(BackReference2_8)](#back-references)         | Entries 1, 2                            | Reference to two previous items, each index stored as u8.                               |
| `11` | `u8, u8, u8` [(BackReference3_8)](#back-references)     | Entries 1, 2, 3                         | Reference to three previous items, each index stored as u8.                             |
| `12` | `u16, u16` [(BackReference2_16)](#back-references)      | Entries 1, 2                            | Reference to two previous items, each index stored as u16.                              |
| `13` | `u16, u16, u16` [(BackReference3_16)](#back-references) | Entries 1, 2, 3                         | Reference to three previous items, each index stored as u16.                            |
| `14` | `u24, u24` [(BackReference2_24)](#back-references)      | Entries 1, 2                            | Reference to two previous items, each index stored as u24.                              |
| `15` | `u24, u24, u24` [(BackReference3_24)](#back-references) | Entries 1, 2, 3                         | Reference to three previous items, each index stored as u24.                            |
| `16` | `u32, u32` [(BackReference2_32)](#back-references)      | Entries 1, 2                            | Reference to two previous items, each index stored as u32.                              |
| `17` | `u32, u32, u32` [(BackReference3_32)](#back-references) | Entries 1, 2, 3                         | Reference to three previous items, each index stored as u32.                            |

The parameter data is split into multiple files to aid compression:

- Text is expected to be mostly (English) ASCII and thus be mostly limited to a certain character set.
- Timestamps are expected to mostly be increasing.
- Other/Misc integers go in a separate file.
- Other/Misc floats go in a separate file.

Here is a listing of which parameter types go where:

| Type | Data Type                                               | File                                |
| ---- | ------------------------------------------------------- | ----------------------------------- |
| `0`  | `UTF-8 Char Array (u8 length)`                          | `commit-parameters-text.bin`        |
| `1`  | `UTF-8 Char Array (u16 length)`                         | `commit-parameters-text.bin`        |
| `2`  | `UTF-8 Char Array (u32 length)`                         | `commit-parameters-text.bin`        |
| `3`  | `u32` ([R3TimeStamp][max-numbers])                      | `commit-parameters-timestamps.bin`  |
| `4`  | `u32` ([R3TimeStamp][max-numbers])                      | `commit-parameters-timestamps.bin`  |
| `5`  | `u8` [(BackReference8)](#back-references)               | `commit-parameters-backrefs-8.bin`  |
| `6`  | `u16` [(BackReference16)](#back-references)             | `commit-parameters-backrefs-16.bin` |
| `7`  | `u24` [(BackReference24)](#back-references)             | `commit-parameters-backrefs-24.bin` |
| `8`  | `u32` [(BackReference32)](#back-references)             | `commit-parameters-backrefs-32.bin` |
| `9`  | `variable` [List](#parameter-lists)                     | `commit-parameters-lists.bin`       |
| `10` | `u8, u8` [(BackReference2_8)](#back-references)         | `commit-parameters-backrefs-8.bin`  |
| `11` | `u8, u8, u8` [(BackReference3_8)](#back-references)     | `commit-parameters-backrefs-8.bin`  |
| `12` | `u16, u16` [(BackReference2_16)](#back-references)      | `commit-parameters-backrefs-16.bin` |
| `13` | `u16, u16, u16` [(BackReference3_16)](#back-references) | `commit-parameters-backrefs-16.bin` |
| `14` | `u24, u24` [(BackReference2_24)](#back-references)      | `commit-parameters-backrefs-24.bin` |
| `15` | `u24, u24, u24` [(BackReference3_24)](#back-references) | `commit-parameters-backrefs-24.bin` |
| `16` | `u32, u32` [(BackReference2_32)](#back-references)      | `commit-parameters-backrefs-32.bin` |
| `17` | `u32, u32, u32` [(BackReference3_32)](#back-references) | `commit-parameters-backrefs-32.bin` |

### Back References

!!! info "Back References are a Special Type of Parameter that references a previous item."

!!! note "Back References are used to deduplicate parameters."

    The writer maintains a hash of all parameters so far and reuses the same
    parameter index if the parameter ends up being a duplicate.

This improves loadout sizes by reducing existing previous data.

Back References are defined as 1 or more `ParameterIndex` fields, whose location and data type
depends on [ParameterType](#parametertype).

A `ParameterIndex` of `0` means 'the first commit parameter' in file.
`1` means 'the second commit parameter' etc.

These are essentially indices into the [commit-parameters-types.bin](#commit-parameters-typesbin) file.

!!! tip "In order to quickly handle back-references, the `reader` should keep offsets of all parameters."

    That is offsets in their perspective files, e.g. offsets into `commit-parameters-text.bin` etc.

### Parameter Lists

!!! info "This primitive is used when you have an unknown number of items."

Imagine you have a message which says:

```
Changes were made, here they are:

{ChangeList}
```

And you want `ChangeList` to have multiple items, so it could be something like:

```
Changes were made, here they are:

- Value **ResolutionX** changed to **1920**
- Value **ResolutionY** changed to **1080**
```

Where each localizable `Change` item could be:

```
- Value **{Name}** changed to **{NewValue}**
```

This is where `Parameter Lists` come in.

A `Parameter List` is defined as:

| Data Type | Name                            | Description                           |
| --------- | ------------------------------- | ------------------------------------- |
| `u8`      | [ParameterType](#parametertype) | Type of the parameter.                |
| `u4`      | Version                         | [Event Specific] version of the list. |
| `u20`     | NumParameters                   | Number of parameters.                 |

For the example above, we can treat each `Change` as 2 parameters.
In which case, if we had 2 changes, we would set `NumParameters` to `4`.

The individual parameters for `Name` and `NewValue` would then follow
as regular parameters in [Commit Parameters](#commit-parameters).

!!! question "Why is there a `Version` field?"

    Sometimes it may be desireable to change the structure.
    Suppose you wanted to change `Change` item to also have the previous value:

    ```
    - Value **{Name}** changed from **{OldValue}** to **{NewValue}**
    ```

    In order to perform this change, you would set the `Version` field to `1`.
    So when you read loadouts you can interpret both the old and new format side by side.

### Message Template List

!!! info "Find the full list of templates on the [Commit Messages Page][commit-messages]."

[locations]: ../About.md#location
[update-command-line]: ./Events.md#updatecommandline
[events]: ./Events.md
[events-messages]: ./Events.md#messages
[max-numbers]: ./DataTypes.md#max-numbers
[commit-messages]: ./Commit-Messages.md
[hashing]: ../../../../Common/Hashing.md
[package-toml]: ../../../Packaging/Package-Metadata.md
[central-server]: ../../../../Services/Central-Server.md
[static-cdn-api]: ../../../../Services/Central-Server.md#static-cdn-api
[store-type]: ./DataTypes.md#storetype
[depot-downloader]: https://github.com/SteamRE/DepotDownloader/blob/b96125f9cbbb0f63d47e14784929f255f6c21ce1/DepotDownloader/ContentDownloader.cs#L185
[gog]: ../Stores/GOG.md
[gog-buildid]: ../Stores/GOG.md#retrieving-available-game-versions
[ms-store-pfm]: ../../../../Loader/Copy-Protection/Windows-MSStore.md
[commit-messages-contextual]: ./Commit-Messages.md#contextual-parameters
[event-packagestatuschanged]: ./Events.md#packagestatuschanged
[message-packagestatuschanged]: ./Commit-Messages.md#package-status-changed-v0
[commit-messages-packageadded]: ./Commit-Messages.md#package_added_v0
[commitparam8len]: #commit-parameters-lengths-8bin
[commitparam16len]: #commit-parameters-lengths-16bin
[commitparam32len]: #commit-parameters-lengths-32bin
[events-bin]: ./Unpacked.md#eventsbin
[commit-messages]: ./Commit-Messages.md
[commit-param-versions]: ./Unpacked.md#commit-parameters-versionsbin
[commit-param-types]: ./Unpacked.md#commit-parameters-typesbin
[commit-param-backrefs]: ./Unpacked.md#back-references
[commit-param-lists]: ./Unpacked.md#parameter-lists
[event-packagestatuschanged]: ./Events.md#packagestatuschanged
[package-added]: ./Commit-Messages.md#package_added_v0
