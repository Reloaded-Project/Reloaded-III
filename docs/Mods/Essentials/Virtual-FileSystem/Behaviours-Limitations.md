# Behaviours & Limitations

!!! info "The Reloaded VFS is only intended to be used for '*well defined*' functionality."

For now, this means the VFS is 'read only'. Write operations, such as creating a file are unaffected.

If a game wants to write a new file (such as a savefile), no action will be taken and the file will
be written to the game folder. If a native DLL plugin wants to write a config file, it will write it
to the game folder, as normal.

## Warnings

!!! warning "Proceed with care if any of the following applies"

- If your game's modding tools operate on a modified game directory (e.g. Skyrim xEdit),
  using VFS is not recommended as new files might be written to the game folder.

- Do not use VFS to redirect files deleted and then recreated by games; ***you will lose the files from inside your mod***.

## Error Cases

!!! error "Using this VFS is not appropriate for your game if any of the following is true"

- This VFS does not handle child processes. Do not use VFS for games that can run
  external tools with virtualized files.
    - Will be implemented in the future if mods ever will end up opening external tools.
    - However that workflow is not recommended... (e.g. might be problematic for Linux users)

## Additional Limitations

!!! note "The following limitations also exist but should not cause concern."

- Reloaded VFS does not support Reparse Point Tags.
    - However, this shouldn't cause issues with mods stored on cloud/OneDrive/etc.
- Reloaded VFS does not return 8.3 DOS file names for virtualized files.

## File Write Behaviours

!!! warning "What happens when you try editing files in a 'read-only' VFS?"

| Description                        | Action Performed                                                                                              |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| File Deletion                      | Delete the mod file instead of the original file                                                              |
| New File Creation                  | Create new files in the original game folder                                                                  |
| File Editing (in Place)            | Edits the redirected file                                                                                     |
| File Delete & Recreate (New)       | Delete the overwritten file and place the new file in game folder                                             |
| Renaming Folders to Other Location | Either move the original folder or files in original folder and overlaid folders (depends on how API is used) |