!!! info "This currently only contains information for Windows."

    Native support for other OSes will be added in the future.

The File Emulation Framework hooks several low level file APIs to intercept file operations.

The goal is to handle every API which:

- ***Opens a File***: To initiate emulated files, and keep track which are open.
- ***Closes a File***: To keep track of when emulated files are closed.
- ***Reads Files***: To return the data of emulated files. (As opposed to original file)
- ***Modifies File Information***: To handle things like file pointer position for emulated files.
- ***Queries File Information***: To handle spoof details like file size for emulated files.

Below is a list of hooked APIs.

## Windows

The strategy is to target the lowest level APIs in `ntdll.dll`.

These in turn are used by the higher level APIs in `kernel32.dll` such as `CreateFileW`, `CreateFileA`,
`CreateFile2` etc.

On both Windows, and Wine, all higher level APIs pass through these functions.

### NtCreateFile

Intercepts file creation and opening operations.
This keeps track of and creates `route`(s) for emulated files.

In addition this calls into the emulators, invoking the `try_create_file` method.

### NtClose

Intercepts closing files.

Disposes of `FileEmulator`'s internal state for the emulated file, such as current read offset.

### NtReadFile

Intercepts file read operations.

If the file is being emulated, it reads data from the emulated file instead of the original file.

### NtSetInformationFile

Intercepts handle update operations.

In particular we're interested in intercepting updating the file pointer position so we can
send that information down to the emulators.

### NtQueryInformationFile

Intercepts file information querying operations.

Here we overwrite the file size information for emulated files.

### NtQueryFullAttributesFile

Intercepts file attribute querying operations.

Here we overwrite the file size information for emulated files.