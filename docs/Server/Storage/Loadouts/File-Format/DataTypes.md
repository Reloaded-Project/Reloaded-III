## Max Numbers

- Max number of Package Download Data/Metadata (MetadataIdx): `268,435,456` (28 bits)
- Max number of Configs (ConfigIdx): `134,217,727` (27 bits)
- Max number of Events: `4,294,967,295` (32 bits)
- Max number of Game Versions/Revisions (GameVerIdx): `65,536` (16 bits)
- Max timestamp. R3TimeStamp: `4,294,967,295` (32 bits).
    - This is the number of seconds since `1st January 2024`.
    - Max year 2160.

## PackageState

!!! info "Represents the state of a package in the loadout."

    - Size: 3 bits
    - Possible values: 0-7

`PackageState` is defined as:

- `0`: `Removed`. The package was removed from the loadout.
- `1`: `Hidden`. The package was hidden from the loadout.
- `2`: `Disabled` (Default State). The package was disabled in the loadout.
- `3`: `Added`. The package was added to the loadout.
- `4`: `Enabled`. The package was enabled in the loadout.

## SortingMode

!!! info "Represents the sorting mode for packages in the LoadoutGrid."

    - Size: 7 bits
    - Possible values: 0-127

`SortingMode` is defined as:

- `0`: Unchanged
- `1`: `Static`. The order of mods is fixed and does not change between reboots.
- `2`: `Release Date Ascending`. Show from oldest to newest.
- `3`: `Release Date Descending`. Show from newest to oldest.
- `4`: `Install Date Ascending`. Show from oldest to newest.
- `5`: `Install Date Descending`. Show from newest to oldest.

## SortOrder

!!! info "Represents the sort order for the load order reorderer."

    - Size: 2 bits
    - Possible values: 0-3

`SortOrder` is defined as:

- `0`: Unchanged
- `1`: `BottomToTop` (Default). Mods at bottom load first, mods at top load last and 'win'.
- `2`: `TopToBottom`. Sort in ascending order.

## GridDisplayMode

!!! info "Represents the display mode for the LoadoutGrid."

    - Size: 4 bits
    - Possible values: 0-15

`GridDisplayMode` is defined as:

- `0`: Unchanged
- `1`: List (Compact)
- `2`: List (Thick)
- `3`: Grid (Search)

## StoreType

!!! info "Represents the store or location from which a game has shipped from."

    - Size: 8 bits
    - Possible values: 0-15

- 0: `Unknown` (Disk)
- 1: `GOG`
- 2: `Steam`
- 3: `Epic`
- 4: `Microsoft`

This can also include game launchers.