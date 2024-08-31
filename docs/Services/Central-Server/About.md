# About the Reloaded3 Central Server

!!! info "The `Reloaded3` Maintainer Operates a Central Server providing a Package Index and Download Services"

The Central Server is a crucial component of the Reloaded3 ecosystem,
serving as a centralized source for information related to packages.

## Purpose and Features

The Central Server fulfills several key roles:

1. **Package Indexing**: Monitors mod sites for new mods and packages, keeping an up-to-date index of available reloaded3 content.
    - This is used for *Dependency Resolution* and *Mod Search*.
    - Provides info for all sources where a package can be downloaded from.
2. **Compatibility Tracking**: Collects and provides user-submitted compatibility reports for mods and game versions.
    - A possible way to detect when mods break due to game updates.
3. **Update Management**: Checks for and provides information about available updates for packages.
    - Accelerates the checking of updates for individual users.
4. **Translation Services**: Manages and provides access to available translations for packages.
    - Makes it easier for users to find translations for mods.
    - Makes it easier for authors to keep track of translation progress.

## API Availability

The Central Server offers two types of APIs to access its services:

1. **Online API**: Hosted directly by the Reloaded3's Maintainer.
2. **Static API**: A serverless, authentication-free API hosted on Cloudflare, offering a subset of features with potentially higher availability and lower latency.

!!! info "This is a table of all APIs and where they are available."

| Purpose                    | Online API                    | Static API                                    |
| -------------------------- | ----------------------------- | --------------------------------------------- |
| Search Banners             | [SteamGridDB Wrapper]         | ❌                                             |
| Mod Compatibility Tracking | [Compatibility API (Batch)]   | [Compatibility Reports] (Read Only)           |
| Package Metadata           | [Package Metadata (Batch)]    | [Static Package Metadata]                     |
| Check for Updates          | [Check for Updates (Batch)]   | ⚠ Possible with [Static Package Metadata] API |
| Search Translations        | [Search Translations (Batch)] | [Static Translations]                         |
| Get Translation Contents   |                               | [Translation Data]                            |
| Download Information       | [Download Info]               | [Static Download Info]                        |
| Search Packages            | ❌                             | [Search API]                                  |
| Delta Update Verification  | ❌                             | [Delta Verification]                          |

The inclusion of both an Online API and a Static API ensures maximized availability,
such that basic Reloaded3 functionality can continue to function even when the server is being
restarted or is down.

## Security and Reliability

!!! info "The Central Server implements several measures to ensure security and reliability"

1. **Package Verification**: Implements cross-referencing to prevent unauthorized package updates.
2. **Moderation**: Relies on third-party websites as moderators for package entries.
3. **Automatic Backups**: Regularly backs up all packages to HDD/Cloud Storage to prevent data loss.

[SteamGridDB Wrapper]: ./Online-API.md#steamgriddb-api
[Compatibility API (Batch)]: ./Online-API.md#compatibility-reports-batch
[Package Metadata (Batch)]: ./Online-API.md#package-metadata-batch
[Check for Updates (Batch)]: ./Online-API.md#check-for-updates-batch
[Search Translations (Batch)]: ./Online-API.md#search-translations-batch
[Download Info]: ./Online-API.md#download-information
[Compatibility Reports]: ./Static-API.md#compatibility-reports-api
[Static Package Metadata]: ./Static-API.md#package-metadata-api
[Static Translations]: ./Static-API.md#translations-api
[Translation Data]: ./Static-API.md#translation-packages-api
[Static Download Info]: ./Static-API.md#download-information-api
[Search API]: ./Static-API.md#search-api
[Delta Verification]: ./Static-API.md#delta-verification-api