# Windows Inject into Suspended

!!! info

    You create a process in suspended state, then inject a DLL into it and unsuspend; relatively trivial.

!!! note

    Although preferred, this approach is not enforced by the spec.

To create a process in suspended state, use `CreateProcessW` with `CREATE_SUSPENDED` flag; then resume the primary
thread after injecting Reloaded.

Pseudocode:
```csharp
// Create a suspended process
if (CreateProcessW(NULL, commandLine, NULL, NULL, FALSE, CREATE_SUSPENDED, NULL, NULL, &si, &pi))
{
    // DLL Inject in Here
    DllInjectReloaded();

    // Resume the process
    ResumeThread(pi.hThread);
}
```

## Technical Issues

!!! info

    DLL Injection into a 32-bit process from a 64-bit process can be tricky.

Basically, some approaches to DLL Injection cannot be used with a suspended process.

This comes down to, `EnumProcessModulesEx` (and its friends). On Windows, you can't enumerate the modules of a process
that was started suspended because they haven't been loaded in yet. This in turn means you can't get the address of
`kernel32.dll` in an x86 process from a x64 process; and `kernel32` is necessary for `LoadLibraryW` to in turn inject your DLLs.

The good news? [Reloaded.Injector][reloaded-injector] will support this use case in >= 2.X.

<!-- Links -->
[reloaded-injector]: https://github.com/Reloaded-Project/Reloaded.Injector