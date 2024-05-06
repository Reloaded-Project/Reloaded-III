!!! tip "Additional information for programmers is contained at [Emulator-Development/Routing.md][routing]"

!!! info "This section explains how files on disk are used to create virtual/emulated files."

When creating virtual/emulated files, the library keeps track of a `Route`. This `Route` is a
combination of the base file path and the names of any recursive internal files.

!!! example "An example"

    When you open the file `00000.adx` located in folder `<GameFolder>/English/Sound.afs`,
    the `Route` will be `<GameFolder>/English/Sound.afs/00000.adx`.

This `Route` is then passed to individual `emulators` (mods) for further processing.

## File Resolution

!!! info "This section describes how files in user mods are matched to the file to be modified."

Each emulator mod has its own folder under the `FileEmulationFramework` folder.

For example, the emulator for CRIWARE's `.AFS` files would use the `FileEmulationFramework/AFS` folder.

Folder names are used to determine which files should be modified by each emulator.
The folder name corresponds to the file to be modified, and the contents of the folder serve
as the input to the emulator.

Emulators are most often used to modify archives. In this case, of `AFS` emulator, placing files
inside the folder can be used to override existing files from the original archive.

- A folder named `Sound.afs/00000.adx` in `FileEmulationFramework/AFS` will override files named
  `00000.adx` in all files named `Sound.afs`.

Additional folders can be used to specify the file to be overwritten more precisely, which is useful
when multiple files with the same name exist.

For example, `English/Sound.afs/00000.adx` in `FileEmulationFramework/AFS`:

- Will match `<GameFolder>/English/Sound.afs`
- Will not match `<GameFolder>/Japanese/Sound.afs`

Comparisons are case-insensitive (unless specified otherwise by emulator), and partial matches
like `nglish/Sound.afs` are allowed but discouraged.

## Recursive Resolution

!!! info "Emulators work recursively, meaning you can emulate a file inside an emulated file."

For example, if you have `textures.one` and inside that `textures.txd`, you can inject into `textures.txd` by doing the following:

- Add `FileEmulationFramework/ONE/textures.one/textures.txd` to inject an unmodified `textures.txd` into `textures.one`.
- Add `FileEmulationFramework/TXD/textures.txd/texture_001.dds` to inject `texture_001` into `textures.txd`.

## File Usage

!!! note "The contents of the folder corresponding to the emulated file are open to the emulator's interpretation."

For example, for an ADX (sound file) emulator, `Musictrack.adx/settings.json` could be a valid file,
and the emulator could use `settings.json` to perform post-processing on the file, such as sound
normalization or concatenating music tracks.

Similarly, for archives that use compression for internal files, having pre-compressed files is also valid.

[routing]: ./Emulator-Development/Routing.md