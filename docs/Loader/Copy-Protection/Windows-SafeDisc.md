# SafeDisc

!!! error "These games cannot be played on Wine or Windows 7+"

SafeDisc is not supported on Windows 7 and later, or on Wine.

This is due to the fact that SafeDisc requires a driver. Wine won't run kernel drivers,
and Windows 7 (with updates) and later have blacklisted the driver.

## Detection

### SafeDisc V1

Unknown.

### SafeDisc V2, V3, V4

Search for string `BoG_ *90.0&!!  Yy>`.
Should usually be after Section Headers in PE header.

After this magic string, you can also extract version (if you feel like it).
It comes as set of `u32` integers right before section end.

Verified this to work with following games:

- SafeDisc V3 Confirmed with `Sims 2`
- SafeDisc V4 Confirmed with `Assasin's Creed` & `Sonic Heroes`

!!! tip "If you feel adventurous, you can also check for section named `stxt371`."

## Mitigation Strategies

Tell the user to get a DRM free version of the game.<br/>
This may either be a DRM-free release from the publisher (if possible), or a cracked version.

That's all.

!!! warning

    Please do not distribute or post linked to cracked EXE files.

    Binary diffs (e.g. xdelta, VCDiff) patches that convert legal installs to community preferred
    game version(s) are ok, but not redistribution of unmodified game files.
