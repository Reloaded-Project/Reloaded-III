!!! info

    This page describes the basics of how files on disk are used to modify existing files through the use of 'emulators'.

When virtual/emulated files are being built, the library keeps track of a `Route`.  

This 'route' is a combination of the base file, and the name of each recursive internal file(s):  
- Base file uses full path, e.g. `<GameFolder>/English/Sound.afs`.  
- Internal files are delimited by `/` character.  

e.g. File `00000.adx` in `<GameFolder>/English/Sound.afs` would make the full path `<GameFolder>/English/Sound.afs/00000.adx`.  

This route is passed onto the individual `emulators` to work with.  

## File Resolution

!!! info

    Describes how files in user mods are matched to the file to be modified.  

Each emulator will have its own folder under the `FEmulator` folder inside user made mods, so the emulator for CRIWARE `.AFS` would use `FEmulator/AFS`.  

Folder names are used for resolving what files should be modified by each 'emulator'; with the folder name corresponding to the file to modify and the contents of the folder being the input to the 'emulator'.  

In the case of 'archive emulators' like the AFS ones, placing files inside can be used to override existing files inside the source `.afs` file.

- Folder `Sound.afs/00000.adx` in `FEmulator/AFS` will override files named `00000.adx` in all `Sound.afs` loaded.  

Additional folders can be used to specify the file to be overwritten more precisely.  
This can be useful when multiple files of the same name exist.  

For example, `English/Sound.afs/00000.adx` in `FEmulator/AFS`:  
- Will match `<GameFolder>/English/Sound.afs`  
- Will not match `<GameFolder>/Japanese/Sound.afs`  

Comparisons performed are case insensitive. Partial matches e.g. `nglish/Sound.afs` are allowed, but are discouraged from use.

## Recursive Resolution

!!! info

    Emulators work recursively.  Meaning you can emulate a file inside an emulated file.

In the case of archives, suppose you have `textures.one` and inside that `textures.txd`.  

You can inject into `textures.txd` by doing the following:  
- Add `FEmulator/ONE/textures.one/textures.txd`.  [inject unmodified `textures.txd` into `textures.one`].  
- Add `FEmulator/TXD/textures.txd/texture_001.dds`. [inject texture_001 into `textures.txd`]  

## File Usage

The [File Resolution](#file-resolution) section used the 'AFS Redirector' as an example of inserting/replacing files into an archive by using existing files.  

The contents of the folder corresponding to the emulated file are open to the emulator's interpretation.  

For example, for an ADX (sound file) emulator, `Musictrack.adx/settings.json` could be a valid file; and the emulator use `settings.json` to perform post processing the file such as sound normalization or concatenating music tracks.  

Equally well, for archives which use compression for internal files, having pre-compressed files is also valid.