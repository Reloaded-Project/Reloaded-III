# About Copy Protection (DRM)

!!! info

    This section notes things we should be mindful of when dealing with various pieces of
    Digital Rights Management (Copy Protection), and similar mechanisms.

The purpose of copy protection is to prevent 3rd party tampering with games.

And unfortunately, naturally, that means sometimes copy protection gets in the way of modding.

## Sub-Sections

- [Windows: Denuvo][windows-denuvo]
- [Windows: Microsoft Store][windows-msstore]
- [Windows: Steam][windows-steam]
- [Windows: SafeDisc][windows-safedisc]

!!! info "There's more protection schemes out there"

    If you know of any other possible challenges ahead, please contribute!

## Suggestions & Actions

### Prefer DRM-Free Versions

!!! info "Mods should always target DRM-Free version(s) of games if available."

In some rare scenarios a game may be officially distributed in both 
DRM-Free and ***Defective by Design*** versions.

Example: `Yakuza: Like a Dragon`

- [DRM Free Goodness][yakuza-gog] on GOG
- [Denuvo Infested Garbage][yakuza-steam] on Steam

The Steam version is harder to mod, may have more performance issues and will one day...

***STOP. WORKING. FOREVER.***

With the GOG version, you can at least have peace of mind and one day show your kids or grandkids
the joy of your childhood games.

!!! note "An 'encouragement' to buy DRM-Free version(s) in the future is suggested for launcher."

    This helps with future preservation of games, and spreads awareness.

### Provide Delta Patches

!!! tip "For some very old games which have releases in multiple regions, providing delta patches may be acceptable."

Likewise, many modders for old games usually make mods that target a specific region's release.

To make things easier for end users, under ***very exceptional circumstances*** we may provide delta 
patches which transform regional releases of games to the preferred region.

An example of 'exceptional circumstances' are SafeDisc games, which cannot be played ***AT ALL*** 
on Windows 7+ in their original form. (Modded or not modded)

!!! failure "Redistribution of unmodified game files is prohibited."

    By 'delta patches' we refer to binary diffs (e.g. xdelta, VCDiff)
    that convert ***only legal installs*** to community preferred game version(s).

<!-- Links -->
[yakuza-gog]: https://www.gog.com/en/game/yakuza_like_a_dragon
[yakuza-steam]: https://store.steampowered.com/app/1235140/Yakuza_Like_a_Dragon/
[windows-denuvo]: ./Windows-Denuvo.md
[windows-msstore]: ./Windows-MSStore.md
[windows-steam]: ./Windows-Steam.md
[windows-safedisc]: ./Windows-SafeDisc.md