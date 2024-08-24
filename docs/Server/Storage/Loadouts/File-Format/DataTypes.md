## Max Numbers

- Max number of Unique Package IDs (PackageIdIdx): `1,048,576` (20 bits)
- Max number of Unique Package Versions (PackageVerIdx): `1,048,576` (20 bits)
- Max number of Configs (ConfigIdx): `134,217,727` (27 bits)
- Max number of External Configs (ExtConfigIdx): `134,217,727` (27 bits)
- Max number of Events: `4,294,967,295` (32 bits)
- Max number of Game Versions/Revisions (GameVerIdx): `65,536` (16 bits)
- Max timestamp. (R3TimeStamp): `4,294,967,295` (32 bits).
    - This is the number of seconds since `1st January 2024`.
    - Max year 2160.

## PackageStateChange

!!! info "Represents the change in state of a package in the loadout."

    - Size: 3 bits
    - Possible values: 0-7

`PackageStateChange` is defined as:

- `0`: `Removed`. The package was removed from the loadout.
- `1`: `Hidden`. The package was hidden from the loadout.
- `2`: `Disabled` (Default State). The package was disabled in the loadout.
- `3`: `Added`. The package was added to the loadout.
- `4`: `Enabled`. The package was enabled in the loadout.
- `5`: `InstalledAsDependency`. The package was installed as a dependency.

## PackageState

!!! info "Represents the current state of a package in the loadout."

    - Size: 32 bits

`PackageState` is defined as a bit-packed flag enum:

- `0x01`: `Hidden`. The package is hidden from view in the loadout.
- `0x02`: `Enabled`. The package is disabled in the loadout.
- `0x04`: `InstalledAsDependency`. The package is installed as a dependency.

Multiple flags can be combined to represent different states.
For example:

- `0x00`: The package is visible and disabled.
- `0x01`: The package is hidden and disabled.
- `0x02`: The package is visible and enabled.
- `0x03`: The package is hidden and enabled.

!!! note "The absence of the `Enabled` flag implies that the package is disabled."

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
- `6`: `Alphabetical Ascending`. Sort alphabetically from A to Z.
- `7`: `Alphabetical Descending`. Sort alphabetically from Z to A.

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
- `2`: List
- `3`: Grid (Search)

The actual sizes of these images is stated in [mod metadata][mod-metadata].

## StoreType

!!! info "Represents the store or location from which a game has shipped from."

    - Size: 8 bits
    - Possible values: 0-255

- 0: `Unknown` (Disk)
- 1: `GOG`
- 2: `Steam`
- 3: `Epic`
- 4: `Microsoft`

This can also include game launchers.

[mod-metadata]: ../../../Packaging/Package-Metadata.md#icons