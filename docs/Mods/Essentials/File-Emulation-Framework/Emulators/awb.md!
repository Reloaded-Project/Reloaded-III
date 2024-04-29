!!! info

    AWB is a general purpose data container from CRI Middleware.  
    It's the successor to [AFS](./afs.md) and uses the header AFS2.  
    Code for this emulator lives inside main project's GitHub repository.  

## Supported Applications

This emulator should support every application out there.  

It has been tested with the following:  
- Bayonetta (PC)  
- Persona 5 Royal (PC) [Note: ADX files Require Encryption]  

## Example Usage

A. Add a dependency on this mod in your mod configuration. (via `Edit Mod` menu dependencies section, or in `ModConfig.json` directly)

```json
"ModDependencies": ["reloaded.universal.fileemulationframework.awb"]
```

B. Add a folder called `FEmulator/AWB` in your mod folder.  
C. Make folders corresponding to AWB Archive names, e.g. `BGM000.AWB`.  

Files inside AWB Archives are accessed by index, i.e. order in the archive: 0, 1, 2, 3 etc.  

Inside each folder make files, with names corresponding to the file's index.  

### Example(s)

To replace a file in an archive named `BGM000.AWB`...

Adding `FEmulator/AWB/BGM000.AWB/0.adx` to your mod would replace the 0th item in the original AWB Archive.

Adding `FEmulator/AWB/BGM000.AWB/32.aix` to your mod would replace the 32th item in the original AWB Archive.

![example](../images/afs/afs_example.png)

File names can contain other text, but must start with a number corresponding to the index.  

## ACB & BDX Patching 

!!! info

    When an AWB is accompanied by an ACB file, the header of the AWB file is usually ignored and instead read from ACB which makes life difficult.  

    When the emulator sees an ACB file, it will automatically try to match any found AWB header with previously patched AWB and patch it inside the ACB if there's a match. 

!!! warning

    In some cases, the ACB may be loaded BEFORE the AWB, in which case the emulator will try load the AWB by replacing the extension of the file from `.acb` to `.awb`.  

    If you run into a title where the ACB and AWB names don't match and require custom file linking, let me know.

## Notes (AFS)

The following notes/limitations are known to exist in AFS, and may still apply in AWB, they have been untested.

!!! info 

    For audio playback, you can usually place ADX/AHX/AIX files interchangeably. e.g. You can place a `32.adx` file even if the original AWB archive has an AIX/AHX file inside in that slot. 

!!! info 

    If dealing with AWB audio; you might need to make sure your new files have the same channel count as the originals.   