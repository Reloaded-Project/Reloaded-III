!!! info

    .ONE is a general purpose data container developed (presumably) at some branch of Sonic Team.  This emulator is for the Sonic Heroes variant. Code for thie emulator lives inside the main project's GitHub repository.  

## Supported Applications

- Sonic Heroes (PC)  
- Sonic Heroes XBOX (Emu)  

and any tools that operate on the format...  

## Example Usage 

A. Add a dependency on this mod in your mod configuration. (via `Edit Mod` menu dependencies section, or in `ModConfig.json` directly)

```json
"ModDependencies": ["reloaded.universal.fileemulationframework.heroes.one"]
```

B. Add a folder called `FEmulator/ONE` in your mod folder.  
C. Make folders corresponding to ONE Archive names, e.g. `game_disp.one`.  

Put files inside that folder to perform various actions.  

!!! info

    Refer to [Routing](../routing.md) if you want to use more specific file names.

## Adding/Replacing Files

!!! warning

    Uncompressed files will suffer from a small load time penalty upon first load of the file, since they will need to be compressed as the ONE format does not support uncompressed files.  

Simply place the file in your `.one` directory.  

![example](../images/heroes-one/heroes-one-add-file.png)

(game_disp.one/GAME_DISP.TXD)

Files placed in the directory will replace the files stored inside the ONE archive.  

!!! tip

    You should [pre-compress your files using this tool](https://github.com/Sewer56/dlang-prs/releases/latest) to avoid load time penalties. Recommend buffer size of 8191.  

    Add `.PRS` extension to compressed files. e.g. `GAME_DISP.TXD.PRS`.  

!!! danger

    Seriously, please compress your files.  Uncompressed files are backed by pagefile, overuse of those may lead to performance problems.

!!! note

    Pre-compressing files prevents them from working with other emulators. If there would hypothetically be, a TXD emulator some day; and you want to merge some textures in; don't pre-compress your TXD.  

## Deleting Files

In order to delete a file, create an empty file with the name of the file and extension `.del`.

![example](../images/heroes-one/heroes-one-delete-file.png)

e.g. This would remove the file `GAME_DISP.TXD` from the original archive.  

!!! note

    The archive builder works in the order `Delete` then `Add`. If a file is first deleted, it can be re-added by either the same or another mod.  