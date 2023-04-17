# OSX Library Preload

This technique is effectively equivalent to [Windows: Inject Into Suspended Process](./Windows-InjectIntoSuspended.md) but officially supported at the OS level.

Run the target process with `DYLD_INSERT_LIBRARIES=path/to/your/library.so command args...`

For more details see: [Linux Preload](./Linux-Preload.md).

## Issue: Disabled by Default?

!!! error

    Reportedly you may need to disable [System Integrity Protection](https://developer.apple.com/documentation/security/disabling_and_enabling_system_integrity_protection) (SIP) in order to use it in some cases (I believe only for binaries signed by Apple though).

Unfortunately, I do not have an Apple machine.