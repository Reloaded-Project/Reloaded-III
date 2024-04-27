# About the Reloaded Virtual FileSystem

The Reloaded Virtual File System (VFS) is an invisible helper that sits between your games and the
files they use. It allows your games to 'see' and open files that aren't really 'there', keeping
your game folder unmodified.

```mermaid
flowchart LR

    p[Game] -- Open File --> vfs[Reloaded VFS]
    vfs -- Open Different File --> of[Operating System]
```

The VFS sits in the middle and does some magic 😇.

```mermaid
classDiagram

    class `Mod Folder`
    `Mod Folder` : data3.pak

    class `Mod 2 Folder`
    `Mod 2 Folder` : data4.pak

    class `Real Game Folder`
    `Real Game Folder` : data1.pak
    `Real Game Folder` : data2.pak
    `Real Game Folder` : game.exe

    class `Virtual Game Folder [What Game Sees]`
    `Virtual Game Folder [What Game Sees]` : data1.pak
    `Virtual Game Folder [What Game Sees]` : data2.pak
    `Virtual Game Folder [What Game Sees]` : data3.pak
    `Virtual Game Folder [What Game Sees]` : data4.pak
    `Virtual Game Folder [What Game Sees]` : game.exe

    `Mod Folder` --|> `Virtual Game Folder [What Game Sees]`
    `Mod 2 Folder` --|> `Virtual Game Folder [What Game Sees]`
    `Real Game Folder` --|> `Virtual Game Folder [What Game Sees]`
```

## Characteristics

Compared to Windows symlinks/hardlinks:

- Links are only visible to the current application.
- Write access to game folder is not needed. Can even link new content into read-only folders.
- Administrator rights are not needed.
- Can overlay multiple directories on top of the destination.

And with the following benefits:

- Easy to use API for programmers.
- Practically zero overhead.
- Can add/remove and remap files on the fly (without making changes on disk).
- Supports Wine on Linux.
