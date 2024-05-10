# Package Tiering

!!! warning "This feature is not part of the 'Minimum Viable Product'"

    This is mostly a 'post release' feature. A brief is included in the planning docs to
    ensure the final product is built in a way that won't make this feature difficult to implement.

A common setup on Desktop PCs is to have a small SSD for OS and programs and a larger HDD for large data.

In some cases, it is possible to automatically move certain mods to a slower, bigger storage medium
if you know that the data won't have an impact on performance.

The most common example of this is:

- Video Mods (Replacing Pre-Rendered Cutscenes)
- Audio Mods (Replacing Music)

As this data is often streamed, and the read speed is capped by how fast the file is played back,
putting these files on a bigger or smaller storage medium has very little impact on performance.

## Design

!!! tip "Allow the user to specify multiple package storage locations in the UI."

More specifically, allow the user to specify:

- Main Storage Location
- Secondary Storage Location(s)

In this UI this should be presented as `Primary` and `Secondary`.

The `Primary` is determined by trying to guess the fastest available Disk.
If we can't determine this, we should default to the OS disk.

If there is only one disk, don't show any dialog on first startup.

## Which Packages to Move?

!!! info "Describes how we determine which packages to put on slower storage."

!!! tip "Mods should opt-in to being placed on slower storage."

    This can be done by setting the [StoragePreference][storage-preference] field on a package.

    This way a package can decide if it should be installed on an SSD or HDD by default.

To enforce this, we will create a [diagnostic][diagnostics] that checks the mod content against
known data and suggests updating the [StoragePreference][storage-preference] flag.

Diagnostic Details:

- **Id**: `R3.S56.PKGTIER-01`
- **Summary**: "Consider moving `{ModName}` to secondary storage"
- **Severity**: Warning
- **Body**:

```markdown
Hey there! 👋

I noticed that your mod, `{ModName}`, contains some files that could be stored on a slower
drive without affecting performance much.

{FileList}

These files are pretty large (over {SizeThreshold}), but they're the kind that don't need to be on
a super-fast SSD.

If you want to save some of that precious SSD space, you can set the [StoragePreference][storage-preference]
flag in your mod's `package.toml` file. This way, if someone has a big ol' HDD and a speedy SSD,
your mod will automatically be installed on the HDD when they download it.

Neat, right? 😄

## A Note for Big Mod Creators

Hey, if you're making a big mod pack that's has a lot of music n' stuff, listen up! 📢

In the world of Reloaded, we really dig ***modularity***.
That means breaking your big mod into smaller, focused mods.

Not only does this save space on people's precious SSDs, but it also lets them pick and choose the
parts of your mod they want. It's like a modding buffet! 🍽️

Consider making separate separate mods for your individual music track, characters, or whatever
you got going on fam.

There's still ways to make your stuff appear as one mod, we've got your back 👌.

[Here's a super cool guide.][packaging-guide]
Give it a look, and if you still have questions, feel free to ask the community.
We're here to help! 💪

## Actions

Btn(Ignore Warning)
Btn(Update Storage Preference to HDD (SLOW))
```

### Substitutions

The `{FileList}` should be a bullet list of the files that triggered the diagnostic, along
with their sizes. For example:

```markdown
- `video/intro.webm` (50 MB)
- `video/ending.webm` (75 MB)
- `audio/music/bgm01.adx` (10 MB)
```

The `{SizeThreshold}` should be replaced with the actual size threshold used.
For now, this threshold is `5MB` for all file types.

### Recognised File Formats

The diagnostic emitter should check for the following file types and their corresponding size thresholds:

| File Extension | File Type                     |
| -------------- | ----------------------------- |
| `.webm`        | Video (WebM)                  |
| `.mp4`         | Video (MP4)                   |
| `.sfd`         | Video (SFD)                   |
| `.bik`         | Video (Bink)                  |
| `.ogv`         | Video (Ogg Theora/Vorbis)     |
| `.wmv`         | Video (Windows Media Video)   |
| `.avi`         | Video (AVI)                   |
| `.mov`         | Video (QuickTime)             |
| `.mkv`         | Video (Matroska)              |
| `.adx`         | Audio (ADX)                   |
| `.ogg`         | Audio (Ogg Vorbis)            |
| `.wav`         | Audio (WAV)                   |
| `.psb`         | Audio (PSB)                   |
| `.at3`         | Audio (ATRAC3)                |
| `.at9`         | Audio (ATRAC9)                |
| `.vag`         | Audio (VAG)                   |
| `.aiff`        | Audio (AIFF)                  |
| `.flac`        | Audio (FLAC)                  |
| `.m4a`         | Audio (MPEG-4 Audio)          |
| `.opus`        | Audio (Opus)                  |

If a mod contains files of these types that exceed the specified size thresholds, the diagnostic
should be emitted.

## Technical Details

[sysinfo disks][disks] can be used to determine the type of storage medium in a cross platform fashion.
Specifically the `DiskKind` enum.

In general we should use preference order of:

- `SSD`
- `HDD`
- `Unknown`

In the case of multiple SSDs, prefer the OS disk, as there may be an NVMe and non-NVMe.

!!! note "Down the road, we can eventually add improved measurement methods."

[diagnostics]: ../Diagnostics.md
[disks]: https://docs.rs/sysinfo/latest/sysinfo/struct.Disks.html
[storage-preference]: ../Packaging/Package-Metadata.md#storage-preference