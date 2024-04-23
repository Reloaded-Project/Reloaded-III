# Implementation Details

This section dives deeper into some of the implementation details of the Reloaded VFS.

## Used Hooks

The VFS hooks several Win32 and NT File APIs to intercept file operations. The goal is to handle every API which:

- Accepts a File Path: In this case we set a new path to our redirected file.

- Returns Files at Given Path: In this case we inject new files into the result.

Here is a flowchart of the hooked APIs:

```mermaid
flowchart LR
    subgraph Win32

    %% Definitions
    FindFirstFileA
    FindFirstFileExA
    FindFirstFileW
    FindFirstFileExW
    FindFirstFileExFromAppW
    FindNextFileA
    FindNextFileW

    CreateDirectoryA
    CreateDirectoryW
    CreateFileA
    CreateFileW
    CreateFile2
    CreateFile2FromAppW
    CreateFileFromAppW
    CreateDirectoryExW
    CreateDirectoryFromAppW
    DeleteFileA
    DeleteFileW
    DeleteFileFromAppW
    GetCompressedFileSizeA
    GetCompressedFileSizeW
    CloseHandle

    GetFileAttributesA
    GetFileAttributesExA
    GetFileAttributesExFromAppW
    GetFileAttributesExW
    GetFileAttributesW
    SetFileAttributesA
    SetFileAttributesFromAppW
    SetFileAttributesW

    RemoveDirectoryA
    RemoveDirectoryFromAppW
    RemoveDirectoryW

    %%% Win32 Internal Redirects
    FindFirstFileA --> FindFirstFileExW
    FindFirstFileExA --> FindFirstFileExW
    FindFirstFileExFromAppW --> FindFirstFileExW
    FindNextFileA --> FindNextFileW
    CreateDirectoryA --> CreateDirectoryW
    CreateFile2FromAppW --> CreateFile2
    CreateDirectoryFromAppW --> CreateDirectoryExW
    CreateFileFromAppW --> CreateFile2FromAppW
    DeleteFileFromAppW --> DeleteFileW
    DeleteFileA --> DeleteFileW
    GetCompressedFileSizeA --> GetCompressedFileSizeW
    GetFileAttributesA --> GetFileAttributesW
    GetFileAttributesExA --> GetFileAttributesExW
    GetFileAttributesExFromAppW --> GetFileAttributesExW
    RemoveDirectoryA --> RemoveDirectoryW
    RemoveDirectoryFromAppW --> RemoveDirectoryW
    SetFileAttributesFromAppW --> SetFileAttributesW
    SetFileAttributesA --> SetFileAttributesW
    end

    subgraph NT API
    %% Definitions
    NtCreateFile
    NtOpenFile
    NtQueryDirectoryFile
    NtQueryDirectoryFileEx
    NtDeleteFile
    NtQueryAttributesFile
    NtQueryFullAttributesFile
    NtClose

    %%% Win32 -> NT API
    FindFirstFileExW --> NtOpenFile
    FindFirstFileExW --> NtQueryDirectoryFileEx
    FindFirstFileW --> NtOpenFile
    FindFirstFileW --> NtQueryDirectoryFileEx
    FindNextFileW --> NtQueryDirectoryFileEx
    CreateFileA --> NtCreateFile
    CreateFileW --> NtCreateFile
    CreateFile2 --> NtCreateFile
    CreateDirectoryW --> NtCreateFile
    CreateDirectoryExW --> NtOpenFile
    CreateDirectoryExW --> NtCreateFile
    DeleteFileW --> NtOpenFile
    RemoveDirectoryW --> NtOpenFile
    GetCompressedFileSizeW --> NtOpenFile
    CloseHandle --> NtClose
    GetFileAttributesExW --> NtQueryFullAttributesFile
    GetFileAttributesW --> NtQueryAttributesFile
    SetFileAttributesW --> NtOpenFile
    end

    %%% Hooks
    subgraph Hooks
    NtCreateFile_Hook
    NtOpenFile_Hook
    NtQueryDirectoryFileEx_Hook
    NtDeleteFile_Hook
    NtQueryAttributesFile_Hook
    NtQueryFullAttributesFile_Hook
    NtClose_Hook

    %% NT API -> Hooks
    NtCreateFile --> NtCreateFile_Hook
    NtOpenFile --> NtOpenFile_Hook
    NtQueryDirectoryFileEx --> NtQueryDirectoryFileEx_Hook
    NtQueryDirectoryFile --> NtQueryDirectoryFile_Hook

    NtDeleteFile --> NtDeleteFile_Hook
    NtQueryAttributesFile --> NtQueryAttributesFile_Hook
    NtQueryFullAttributesFile --> NtQueryFullAttributesFile_Hook
    NtClose --> NtClose_Hook
    end
```

On Windows 10+, `NtQueryDirectoryFileEx` API becomes available and `NtQueryDirectoryFile` acts as a wrapper around it. On Wine and earlier Windows, only `NtQueryDirectoryFile` exists.

In this VFS we hook both, and detect if one recurses to the other using a semaphore. If we're recursing from `NtQueryDirectoryFile` to `NtQueryDirectoryFileEx`, we skip the hook code.

## Lookup Tree

The `LookupTree` is a visualization of the data structure used to map paths of old files to new files ***after*** all mods are loaded during startup.
When all mods are loaded, this structure is generated from the `RedirectionTree`.

It uses a strategy of:

1. Check common prefix.
2. Check remaining path in dictionary.
3. Check file name in dictionary.

The prefix is based on the idea that a game will have all of its files stored under a common folder path.
We use this to save memory in potentially huge games.

```mermaid
flowchart LR
    subgraph LookupTree
        subgraph Common Prefix
            C[C:/SteamLibrary/steamapps/common/Game]
        end
        subgraph Dictionary
            D[.]
            M[music]
        end
        C --> D
        D --> data_1.pak
        D --> data_2.pak
        D --> data_3.pak
        M --> jingle.wav
        M --> ocean.wav
    end
    data_2.pak --> f[FULL_PATH_TO_NEW_FILE 'isDirectory: false']
```

### In Code

```csharp
/// <summary>
/// A version of <see cref="RedirectionTree"/> optimised for faster lookups in the scenario of use with game folders.
/// </summary>
public struct LookupTree<TTarget>
{
    /// <summary>
    /// Prefix of all paths.
    /// Stored in upper case for faster performance.
    /// </summary>
    public string Prefix { get; private set; }

    /// <summary>
    /// Dictionary that maps individual subfolders to map of files.
    /// </summary>
    public SpanOfCharDict<SpanOfCharDict<TTarget>> SubfolderToFiles { get; private set; }
}
```

## Redirection Tree

The `RedirectionTree` is a visualization of the data structure used to map paths of old files to new files as the mods are loading during startup.

It uses an O(N) lookup time (where N is the number of components separated by '/') that make up the final file path. The resolution steps are:

1. Start at tree root.
2. Split the input path on '/' character.
3. Traverse the tree one level at a time, using each split component to move down next level.
4. At each level check if there's a child node corresponding to current path component.
    - If there is no child node, lookup has failed and path is not in the tree.
5. When all components have been consumed, check the `Items` dictionary of the final node reached to see if the path is present.
6. If it is, the lookup succeeds and the corresponding value is returned. If it is not, the lookup fails and the path is not found in the tree.

When all mods are loaded, this trie-like structure is converted to a `LookupTree`.

```mermaid
flowchart LR
    subgraph RedirectionTree
        C: --> SteamLibrary --> steamapps --> common --> Game
        Game --> data_1.pak
        Game --> data_2.pak
        Game --> data_3.pak
    end
    data_2.pak --> f[FULL_PATH_TO_NEW_FILE 'isDirectory: false']
```

### In Code

```csharp
/// <summary>
/// Represents that will be used for performing redirections.
/// </summary>
public struct RedirectionTree<TTarget>
{
    /// <summary>
    /// Root nodes, e.g. would store drive: C:/D:/E: etc.
    /// In most cases there is only one.
    /// </summary>
    public RedirectionTreeNode<TTarget> RootNode { get; private set; }
}
```

```csharp
/// <summary>
/// Individual node in the redirection tree.
/// </summary>
public struct RedirectionTreeNode<TTarget>
{
    /// <summary>
    /// Child nodes of this nodes.
    /// i.e. Maps 'folder' to next child.
    /// </summary>
    public SpanOfCharDict<RedirectionTreeNode<TTarget>> Children;

    /// <summary>
    /// Files present at this level of the tree.
    /// </summary>
    public SpanOfCharDict<TTarget> Items;
}
```

```csharp
/// <summary>
/// Target for a file covered by the redirection tree.
/// </summary>
public struct RedirectionTreeTarget
{
    /// <summary>
    /// Path to the directory storing the file.
    /// </summary>
    public string Directory; // (This is deduplicated, saving memory)

    /// <summary>
    /// Name of the file in the directory.
    /// </summary>
    public string FileName;

    /// <summary>
    /// True if this is a directory, else false.
    /// </summary>
    public bool IsDirectory;
}
```