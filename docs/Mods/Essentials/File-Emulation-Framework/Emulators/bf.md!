!!! info

    BF is a script file used by Atlus, for more information on the format check out [ShrineFox's intro to scripting](https://docs.shrinefox.com/flowscript/intro-to-scripting). 
    
    Code for this emulator lives inside main project's GitHub repository.  

## Supported Applications

A number of Atlus games such as Persona, SMT, and Catherine use BF files. Any that [Atlus Script Compiler](https://github.com/tge-was-taken/Atlus-Script-Tools) has libraries for should work, however, this has only been tested with: 

- Persona 3 Portable (PC)  
- Persona 4 Golden (PC)  
- Persona 5 Royal (PC)  

For games other than these, script compiler arguments need to be supplied as detailed in [Custom Script Compiler Args](#custom-script-compiler-args). 

## Example Usage
As this mod is primarily intended for use with the PC Persona games, it is reccomended that you use [Persona Essentials](https://github.com/Sewer56/p5rpc.modloader) which has this as a dependency. However, the steps for using it on its own are very similar to with Persona Essentials:

A. Add a dependency on this mod in your mod configuration. (via `Edit Mod` menu dependencies section, or in `ModConfig.json` directly)

```json
"ModDependencies": ["reloaded.universal.fileemulationframework.bf"]
```

B. Add a folder called `FEmulator/BF` in your mod folder.  
C. Make a `.flow` file with the same name as the bf you want to edit, e.g. `f007.flow` to edit `f007.bf` (this can be in subfolders as per  [Routing](../routing.md)).  
D. In the `.flow` file include any new procedures and hooks of existing procedures from the base `.bf` file  

!!! warning

    Only include **new** procedures and **hooked** procedures, **do not** copy and paste the entire decompiled bf into your flow.
    
    To hook a procedure add `_hook` to the end of the name of the original (e.g. to hook `init` make a procedure called `init_hook`)

### Message Hooking
If you just want to change existing messages inside of a `bf` you can do so using message hooking which works very similarly to regular flowscript merging. 

To do so:

A. Follow steps A and B from above.    
B. Make a `.msg` file with the same name as the bf you want to edit, e.g. `f007.msg` to edit messages in `f007.bf`     
C. In the `.msg` file include any messages that you want to edit from the base `.bf` file.

!!! warning

    Only include edited messages, **do not** copy and paste the entire decompiled msg file into your new msg.

    The edited messages must have exactly the same names as the originals otherwise they will not be overwritten and instead will be added.

Note that you can also hook messages in flow files by having messages with the same name as original ones in any imported `.msg` files. Normally script compiler would ignore duplicate named messages, however, the version in BF Emulator has been modified to instead overwrite them.

### Forced Procedure Indices
In some cases you will need to add new procedures to a `bf` which are at a specific index, such as when adding new interactable NPCs. In this case you can force a specific index by adding `_index_x` to the end of the procedure's name.

For example, if you have a new NPC that calls procedure `21`, in your `.flow` file should have a procedure with a name like `npc_thing_index_21` to ensure your new procedure is always at index `21` (the stuff before `_index_21` is completely arbitrary).

!!! info
    
    This is neceessary as other mods hooking functions in the same `bf` could potentially change the index of your procedures if they are not forced.

### Script Compiler Library Overrides
In some cases you will want to utilise custom flowscript functions provided either by your mod or a dependency. In these cases you can use library overrides to replace the information about existing (generally unused) functions with your custom ones. 

To do so:

A. Create a file named `Functions.json` in your `FEmulator/BF` folder.  
B. Inside of `Functions.json` copy the information of the changed functions into the file inside of a json array.

For example, to use the [P3P Movie Player mod's](https://github.com/AnimatedSwine37/p3ppc.moviePlayer) `CUSTOM_MOVIE_PLAY` function you would have the following in `Functions.json`

```json
[
  {
    "Index": "0x0004",
    "ReturnType": "void",
    "Name": "CUSTOM_MOVIE_PLAY",
    "Description": "Custom function that plays a usm based on its id. This REQUIRES the Movie Player mod to work!",
    "Parameters": [
      {
        "Type": "int",
        "Name": "CutsceneId",
        "Description": "The id of the usm to play, the usm should be in \\data\\sound\\usm and be called CutsceneId.usm (e.g. 21.usm for id 21)"
      }
    ]
  }
]
```

Where that information was copied directly from [the mod's readme](https://github.com/AnimatedSwine37/p3ppc.moviePlayer#usage-makers).

!!! warning

    Do not change the information of functions that are **not unused** (such as changing the name of undocumented functions). If any other mod hooks the same bf and uses those functions they will be unable to compile.

    If you have documented previously unknown functions you should make a pull request with these changes to the main [Atlus-Script-Tools repository](https://github.com/tge-was-taken/Atlus-Script-Tools), this can then be merged into BF Emulator at a later time. 

This can also be done with custom enums by adding an `Enums.json` file into `FEmulator/BF` and adding the information in a similar manner. For example:

```json
[
    {
        "Name": "Cutscene",
        "Description": "This enum represents different movies added by cutscenes restored",
        "Members": [
            {
                "Name": "First",
                "Value": 1,
                "Description": ""
            }
        ]
    }
]
```

This enum can then be used in your code like: `CUSTOM_MOVIE_PLAY( Cutscene.First );`

### Custom Script Compiler Args
!!! info

    If you are doing this to use BF Emulator with an unsupported game you could instead make a pull request, adding automatic support for it by adding to the constructor in [BfEmulator.cs](https://github.com/Sewer56/FileEmulationFramework/blob/main/Emulator/BF.File.Emulator/BfEmulator.cs#L53).

If you want to use BF Emulator on a game that is not automatically supported you will need to supply Atlus Script Compiler with the correct arguments to compile the bf for it.

To do so:

A. Create a file named `CompilerArgs.json` in your `FEmulator/BF` folder.   
B. Inside of `CompilerArgs.json` use the following template with the appropriate arguments (which can usually be found in the [Script Compiler GUI repo](https://github.com/ShrineFox/AtlusScriptCompiler-GUI/blob/master/AtlusScriptCompilerGUI/GUI.cs#L101))

```json
{
    "Library": "P3P",
    "Encoding": "P3",
    "OutFormat": "V1"
}
```