!!! info

    BMD is a script file used by Atlus, for more information on the format check out [ShrineFox's intro to scripting](https://docs.shrinefox.com/flowscript/intro-to-scripting). 
    
    Code for this emulator lives inside main project's GitHub repository.  

## Supported Applications

A number of Atlus games such as Persona, SMT, and Catherine use BMD files. Any that [Atlus Script Compiler](https://github.com/tge-was-taken/Atlus-Script-Tools) has libraries for should work, however, this has only been tested with: 

- Persona 3 Portable (PC)  
- Persona 4 Golden (PC)  
- Persona 5 Royal (PC)  

For games other than these, script compiler arguments need to be supplied as detailed in [Custom Script Compiler Args](#custom-script-compiler-args). 

## Example Usage
As this mod is primarily intended for use with the PC Persona games, it is recommended that you use [Persona Essentials](https://github.com/Sewer56/p5rpc.modloader) which has this as a dependency. However, the steps for using it on its own are very similar to with Persona Essentials:

A. Add a dependency on this mod in your mod configuration. (via `Edit Mod` menu dependencies section, or in `ModConfig.json` directly)

```json
"ModDependencies": ["reloaded.universal.fileemulationframework.bmd"]
```

B. Add a folder called `FEmulator/BMD` in your mod folder.  
C. Make a `.msg` file with the same name as the bmd you want to edit, e.g. `e722_103.msg` to edit messages in `e722_103.bmd`     
D. In the `.msg` file include any messages that you want to edit from the base `.bmd` file.

!!! warning

    Only include edited messages, **do not** copy and paste the entire decompiled msg file into your new msg.

    The edited messages must have exactly the same names as the originals otherwise they will not be overwritten and instead will be added.

Normally script compiler would ignore duplicate named messages, however, the version in BMD Emulator has been modified to instead overwrite them.

### Custom Script Compiler Args
!!! todo

    The link in the below is copypasted from bf.md and is not correct.

!!! info

    If you are doing this to use BMD Emulator with an unsupported game you could instead make a pull request, adding automatic support for it by adding to the constructor in [BfEmulator.cs](https://github.com/Sewer56/FileEmulationFramework/blob/main/Emulator/BF.File.Emulator/BfEmulator.cs#L53).

If you want to use BMD Emulator on a game that is not automatically supported you will need to supply Atlus Script Compiler with the correct arguments to compile the bmd for it.

To do so:

A. Create a file named `CompilerArgs.json` in your `FEmulator/BMD` folder.   
B. Inside of `CompilerArgs.json` use the following template with the appropriate arguments (which can usually be found in the [Script Compiler GUI repo](https://github.com/ShrineFox/AtlusScriptCompiler-GUI/blob/master/AtlusScriptCompilerGUI/GUI.cs#L101))

```json
{
    "Library": "P3P",
    "Encoding": "P3",
    "OutFormat": "V1"
}
```