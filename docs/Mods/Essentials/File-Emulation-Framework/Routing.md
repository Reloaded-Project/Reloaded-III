!!! tip "Additional information for programmers is contained at [Emulator-Development/Routing.md][routing]"

!!! info "This section explains how files on your computer are used to create custom game files."

When creating custom game files, FileEmulationFramework keeps track of a `Route`.
This `Route` is a combination of the original game file's path and the names of any files inside it.

!!! example "An example"

    When you open the file `00000.adx` located in the folder `<GameFolder>/English/Sound.afs`,
    the `Route` will be `<GameFolder>/English/Sound.afs/00000.adx`.

This `Route` is then passed to individual `emulators` (mods) for further processing.

## File Matching

!!! info "This section describes how files in your mods are matched to the game files you want to change."

Each emulator mod has its own folder under the `FileEmulationFramework` folder.

For example, the emulator for CRIWARE's `.AFS` files would use the `FileEmulationFramework/AFS` folder.

Folder names are used to determine which game files should be modified by each emulator.
The folder name should match the game file you want to change, and the contents of the folder
will be used by the emulator to make those changes.

!!! tip "Emulators are most often used to modify game archives."

In the case of the `AFS` emulator, placing files inside the folder can replace existing files
from the original archive.

- A folder named `Sound.afs/00000.adx` in `FileEmulationFramework/AFS` will replace files
  named `00000.adx` in all files named `Sound.afs`.

You can use additional folders to be more specific about which file you want to replace.
This is useful when there are multiple files with the same name.

For example, `English/Sound.afs/00000.adx` in `FileEmulationFramework/AFS`:

- Will match `<GameFolder>/English/Sound.afs`
- Will not match `<GameFolder>/Japanese/Sound.afs`

File name comparisons are not case sensitive (unless specified otherwise by the emulator),
and partial matches like `nglish/Sound.afs` are allowed but not recommended.

## Modifying Files Inside Other Files

!!! info "Emulators can work with files inside other emulated files, meaning you can modify a file that's inside another modified file."

For example, if you have `textures.one` and inside that `textures.txd`, you can modify `textures.txd` by doing the following:

- Add `FileEmulationFramework/ONE/textures.one/textures.txd` to inject an unmodified `textures.txd` into `textures.one`.
- Add `FileEmulationFramework/TXD/textures.txd/texture_001.dds` to inject `texture_001` into `textures.txd`.

## File Usage

!!! note "The contents of the folder matching the game file are used by the emulator to make changes."

For example, for an ADX (sound file) emulator, `Musictrack.adx/settings.json` could be a valid file,
and the emulator could use `settings.json` to make changes to the sound file, like adjusting the
volume or combining multiple tracks.

Similarly, for archives that use compression for files inside them, you can also use pre-compressed
files.

[routing]: ./Emulator-Development/Routing.md