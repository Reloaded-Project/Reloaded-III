!!! info "`Package Indexing` is the monitoring of Mod Sites for new Mods and Packages."

This process is crucial for maintaining an up-to-date database of available mods and packages within the Reloaded3 ecosystem.

It provides essential information such as [Package Metadata] needed to resolve missing dependencies in [Loadouts].

## Indexing Overview

1. **Monitoring Mod Sites**: The indexing system regularly scans supported mod sites (e.g., `GameBanana`, `NexusMods`, `GitHub`) for new or updated Reloaded3 packages.
    - We do this by subscribing (GraphQL) or polling (REST API) to the mod site's API.
    - Sorting by 'last modified' and stopping when we reach an entry already indexed.

2. **Metadata Extraction**: When a new package is detected, the system extracts relevant metadata, including:
    - [Package Metadata]
    - [Package Header Information]

3. **Validation**: The extracted metadata is validated to ensure it complies with Reloaded3 standards.
    - Updates to packages are cross-referenced with existing entries to prevent unauthorized updates (see [Indexing Rules][Indexing Rules] below).

4. **Database Update**: Once validated and cross-referenced, the package information is added to the central database.
    - The server running the [Online API] updates self and does write through to the [Static API].
    - Some elements of [Static API] e.g. `Compatibility Reports` may sync at later date.

5. **Backup**: The package is backed up to `HDD/Cloud Storage` for long-term preservation.
    - If a mod is ever 'lost', it is uploaded to [archive.org] for safekeeping.

6. **Deletion Tracking**: If a package is no longer found on a mod site during indexing, it's marked as deleted in the database.

7. **Reinstatement Checking**: During indexing, the system also checks for reappearance of previously deleted packages.

## Indexing Rules

!!! info "Things to keep in mind while indexing."

### Putting Packages `on Hold` Until Cross Referenced

!!! info "If a new version of a package (higher version number) is detected ***from a new mod site***, it is placed `on hold`."

!!! warning "This is an important security feature"

    Without this feature, it's possible to construct an attack where you upload a higher version
    of an existing package to an alternate site and users (incorrectly) receive an update.

An example:

1. User uploads package `reloaded3.utility.examplemod.s56 1.0.0` to `NexusMods`.
2. Package is indexed and added to the database.

A malicious attacker then tries to upload a bad version of `reloaded3.utility.examplemod.s56`

1. They upload `reloaded3.utility.examplemod.s56 2.0.0` to `GameBanana`.
2. They hope users' clients will update to the new version.

#### How Server Should Resolve This

!!! info "This is how the server resolves the `'trust issue'`"

1. The upload of `reloaded3.utility.examplemod.s56 2.0.0` is placed `on hold` (delayed).
2. System waits for `reloaded3.utility.examplemod.s56 2.0.0` to be uploaded to original source (NexusMods), considered 'trusted'.
3. When `reloaded3.utility.examplemod.s56 2.0.0` at NexusMods is detected, we download the [Package Metadata] and check for [Update Source Data].

If the [Update Source Data] allows for updating from the same mod page as listed in the `on hold` package,
the `on hold` package is added to the index.

If the `on hold` package remains `on hold` after 24 hours, a message to notify the maintainer (me) is sent.
In that case, I will backup the package to my local drive, then to [archive.org] for safekeeping if
the original uploader doesn't respond after some time.

!!! warning "Not all packages which remain `on hold` are malicious"

    It is technically possible for a mod author to upload a new version to a different site
    and not upload to the original site out of choice. In this case, the original mod author must be
    notified.

#### Reinstating Accidentally Deleted Packages

When a package that was previously marked as deleted is detected during indexing:

1. The system calculates the XXH3 hash of the newly found package archive file.
2. This hash is compared with the stored hash (`XXH3(archiveFile)`) for the corresponding mod site and download type (full package or delta update).
3. If the hashes match, the package is reinstated (marked as not deleted).
4. If the hashes don't match, the package remains marked as deleted and a warning is logged.
   - Mod author is notified via the mod site's comments section.
   - Otherwise, maintainer is notified (manual intervention required).

!!! info "Packages have a `wasDeleted` flag and site-specific XXH3 hashes in their metadata"

    This allows for tracking deletion status and verifying package integrity during reinstatement.

!!! warning "Packages available on multiple sites are tracked separately for each site"

    A package is only considered fully reinstated when it's available again on all previously known sources.

!!! note "XXH3 hashes are stored per download and update type"

    The `XXH3(archiveFile)` hash is stored for each download in both full package downloads and delta updates.
    This allows for distinguishing between full package and delta update hashes.

### External Sites are the Moderators

!!! info "No manual moderation of packages is done by the Reloaded Maintainer."

!!! warning "Third party websites act as moderators for entries"

What this means is that the Reloaded Maintainer does not manually remove/alter packages on the index.

If a package is infringing, please report the package to the respective mod site.

Any deleted packages [will be backed up](#automatic-backup) to [archive.org] for safekeeping, in case
of accidental deletion by the original mod site.

### Automatic Backup

!!! info "Automatically backup all packages to [archive.org]"

    This is to ensure that packages are not lost.

This needs to be done indiscriminately, regardless of whether the package has been removed or not.

Current plan is to use own HDD and store on 'lifetime cloud' I have.
If sizes get out of hide, then [local drive + backblaze backup][backblaze-cloud].

#### Reference File Sizes

!!! info "These are reference file sizes for all mod downloads with certain data sets."

##### Latest Reloaded-II Packages

!!! info "Total size of ***latest version*** of all searchable Reloaded-II packages as of `31st of August 2024`"

```
Total number of packages: 1495
Total size: 43430.13 MB
Average size per package: 29.05 MB
```

##### Sewer's GameBanana Mod Stats

!!! info "Stats for various games on `GameBanana` from `10th of September 2022`"

These are some numbers I gathered many years ago, while testing metadata sizes for a JSON
based mod search index.

***CS 1.6***:

```
Total Mod Count: 30643
Total Size of All Mods: 89.78GiB
Avg Mod Size: 3MiB
```

***Smash Ultimate***:

(Music heavy game)

```
Total Mod Count: 6773
Total Size of All Mods: 137.808 GiB
Avg Mod Size: 20MiB
```

***Guilty Gear Strive***:

```
Total Mod Count: 2742
Total Size of All Mods: 47.81GiB
Avg Mod Size: 17.85MiB
```

***Team Fortress 2***:

```
Total Mod Count: 22783
Total Size of All Mods: 163.45GiB
Avg Mod Size: 7.35MiB
```

***Miku Megamix+***:
(Many music packs)

```
Total Mod Count: 240
Total Size of All Mods: 26.83GiB
Avg Mod Size: 114.47MiB
```

***Mario Kart 8 Deluxe***:

```
Total Mod Count: 1117
Total Size of All Mods: 13.64GiB
Avg Mod Size: 12.51MiB
```

***Smash 4 WiiU***:

```
Total Mod Count: 7422
Total Size of All Mods: 98GiB
Avg Mod Size: 13.52MiB
```

***TOTAL***:

```
Mod Count: 71720
Size of All Mods: 577 GiB
```

<!-- TODO: More Details -->

[Loadouts]: ../../Server/Storage/Loadouts/About.md
[Package Metadata]: ./Online-API.md#package-metadata-batch
[archive.org]: https://archive.org
[Package Header Information]: ../../Server/Packaging/File-Format/Archive-User-Data-Format.md
[Indexing Rules]: #putting-packages-on-hold-until-cross-referenced
[Online API]: ./Online-API.md
[Static API]: ./Static-API.md
[Update Source Data]: ../../Server/Packaging/Package-Metadata.md#update-source-data
[backblaze-cloud]: https://www.backblaze.com/cloud-backup/pricing