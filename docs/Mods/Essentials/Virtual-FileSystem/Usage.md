
# Basic Usage

## Download the Mod

First, download the `Reloaded File Redirector` mod which provides the virtual filesystem functionality.

![DownloadMod](https://raw.githubusercontent.com/Reloaded-Project/reloaded.universal.redirector/master/docs/images/DownloadMod.png)

## Add Dependency to Redirector

In the `Edit Mod` menu, add `Reloaded File Redirector` as a dependency to your mod.

![AddDependency](https://raw.githubusercontent.com/Reloaded-Project/reloaded.universal.redirector/master/docs/images/AddDependency.png)

This will ensure the `Reloaded File Redirector` mod is always loaded when your mod is loaded.

### Opening the Mod Folder

![OpenModFolder](https://raw.githubusercontent.com/Reloaded-Project/reloaded.universal.redirector/master/docs/images/OpenModFolder.png)

Go to the folder where your mod is stored by clicking the `Open Folder` button.

### Add Some Files

Make a folder called `Redirector`. Inside it, place files that you want to be replaced.

![FileRedirectorFolder](https://raw.githubusercontent.com/Reloaded-Project/reloaded.universal.redirector/master/docs/images/FileRedirectorFolder.png)

Files are mapped by their location relative to the EXE of the application.

For example, if the game is at `E:/SonicHeroes/TSonic_win.exe`, the paths are relative to: `E:/SonicHeroes/`.

To replace a music file at `E:/SonicHeroes/dvdroot/bgm/SNG_STG26.adx`, your mod should place the file at `Redirector/dvdroot/bgm/SNG_STG26.adx`.

The contents of the mod folder should now look as follows:

```
// Mod Contents
ModConfig.json
Preview.png
Redirector
└─dvdroot
  ├─advertise
  │   adv_pl_rouge.one
  └─playmodel
      ro.txd
      ro_dff.one
```

The connectors `└─` represent folders.

## Debugging

![DebugMod](https://raw.githubusercontent.com/Reloaded-Project/reloaded.universal.redirector/master/docs/images/DebugMod.png)

To debug the mod, highlight the `Reloaded File Redirector` mod in your mod manager and click `Configure Mod`.

The following settings are available:
- `Log Open Files`: Prints a message to `Console` when a new file is being opened.
- `Log Redirections`: Prints a message when a custom file is loaded from your or another mod.
- `Log Attribute Fetches`: Prints a message when game gets file properties such as file size.
