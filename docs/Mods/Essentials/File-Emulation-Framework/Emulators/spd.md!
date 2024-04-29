!!! info

    SPD/SPR files are sprite containers used by Atlus.
    Code for this emulator lives inside main project's GitHub repository.  

## File Types

This emulator should work with any `.SPD` or `.SPR` file. 

## Supported Applications

- Persona 3 Portable (PC)  
- Persona 4 Golden (PC)  
- Persona 5 Royal (PC)  

## Usage

As currently this mod is for the PC releases of Persona games, you will need to use the extension of Persona Essentials to use with those games. The steps for using on its own are very similar to with that extension.

Add a dependency on this mod in your mod configuration. (via `Edit Mod` menu dependencies section, or in `ModConfig.json` directly)

```json
"ModDependencies": ["reloaded.universal.fileemulationframework.spd"]
```

## Legend

- `.SPD` or `.SPR` -- sprite container files.
- `.spdspr` or `.sprt` -- sprite entry coordinate files.
- `.dds` or `.tmx` -- texture files.
<!-- -->
- `.SPD` will be used to refer to both `.SPD` and `.SPR` files unless stated otherwise.
- `.spdspr` will be used to refer to both `.spdspr` and `.sprt` files unless stated otherwise.
<!-- -->
- Entries from the texture dictionary will be referred to as "Texture Entries" or "Textures".
- Entries from the sprite coordinate dictionary will be referred to as "Sprite Entries" or "Sprites".

## Where to put files

Add a folder called `FEmulator/SPD` in your mod folder.  
Make folders corresponding to SPD Container paths, e.g. `font/chat/chat.spd/`. All files used for SPD Emulation should be placed in this folder.

### Sprites in PAK Files

Recreate the directory to the SPD inside the PAK, and create a dummy file with the name of the sprite file in that directory. A dummy file can be made my making an empty .txt file and giving it the name of the sprite file.
<!-- -->
Example: `FEmulator/PAK/init_free.bin/smap/i_mini_map01.spr`

## Tools

There are 3 tools you're going to want to make use of when preparing files for the SPD Emulator:
<!-- -->
- [Amicitia](https://github.com/tge-was-taken/Amicitia/releases)
- [PersonaEditor](https://github.com/Secre-C/PersonaEditor/releases)
- [PersonaSpriteTools](https://github.com/Secre-C/PersonaSpriteTools) (optional)

## Extracting textures and sprites

- Amicitia can extract both textures and sprite entries.
- PersonaEditor can only extract textures.
- PersonaSpriteTools can extract both textures and sprite entries using `ExtractSprite.py`

## Finding Sprite Information

- Amicitia will display the texture id above the texture window when a texture is selected, same with sprite entry ids.
- PersonaEditor will display the texture id and sprite id next to each sprite entry in the spd edit window.
- PersonaSpriteTools' `ExtractSprite.py` will have each sprite id in the sprite entry's file name, and the sprite entry files will be put in a folder with the id of the texture they belong to.

## Editing Sprite Files

`.SPD` files are made up of 3 parts. The header, the textures, and the sprite coordinates. The header will be built automatically by the emulator, and allows mod creators to patch the last two.
<!-- -->
The emulator provides 3 ways to edit `.SPD` files:
<!-- -->
- [Sprite patching](#patching-sprites)
- [Texture replacement](#replacing-textures)
- [Adding new sprites](#adding-new-sprites) (advanced)

!!! warning

    Custom texture dimensions must conform to 2^n or (2^n + 2^n-1) to prevent crashes. (ex: 384x192, 1024x512, 768x1536)

## Patching Sprites

Sprite patching in this context refers to the technique of appending a provided texture to the `.SPD`s texture dictionary, and patching a sprite entry to point to the new texture.

After editing the texture containing the sprite you want to change, change the texture's filename to reflect the appropriate sprite id(s), which can be found using PersonaEditor. 

The filename should be `spr_x.dds` where `x` is the sprite ids, using [Id Notation](#id-notation).

Textures should be the same size as the originals, and the sprites should be in the same place, unless you're supplying an edited `.spdspr` file.

If you are supplying an edited `.spdspr` file, the filename should be `spr_x.spdspr` (or `.sprt`) with `x` being the sprites id.

!!! warning
    
    Moving around sprite positions may occasionally break sprite positioning. This has only been observed with P5R so far, and affects sprites that appear next to button prompts as well as a lot of the pause menu animation sprites. These sprites must be put into an image with the same size as the original with the sprites in the correct positions in order to be displayed correctly.

### Examples

- To edit sprite id 15, name the texture `spr_15.dds`.
- To edit sprites 15 and 20, name the texture `spr_15_20.dds`
- To edit sprites 15, 20, 25-30, and 45-55, name the texture `spr_15_20_25-30_45-55.dds`

## Replacing Textures

Under the hood, texture replacement is really just sprite patching, but affects every sprite that pointed to the original texture.
<!-- -->
To replace a texture, simply name your edited texture `tex_x.dds` where `x` is the id of the texture.

You may also want to exclude some sprites from being affected by this method. You can do this by adding a tilda `~` at the end of the texture name, followed by the sprite ids in [Id Notation](#id-notation).

### Example

- To replace all sprites in texture id 4, name the texture `tex_4.dds`
- To replace all sprites in texture id 4 except for sprite id 15-20, and 24, name the texture `tex_4~15-20_24.dds` 

## Adding New Sprites

Adding a new sprite works similarly to patching sprites, but requires that an accompanying sprite entry file be present.

### Example

To add a previously non-existent sprite id 420, create a sprite entry file named `spr_420.spdspr`, and name the texture `spr_420.dds`.
You can add multiple new sprites by putting multiple sprite entry files, and naming the texture using [Id Notation](#id-notation).

## Id Notation

Both sprite patching and texture replacement allow for multiple sprites to be patched/excluded. sprite ranges are denoted by dashes `-`, and sprite ids and ranges are separated by underscores `_`.

### Examples

- 1 = 1
- 1_5 = 1 and 5
- 1-5 = 1 through 5
- 1-5_10 1 through 5, and 10
