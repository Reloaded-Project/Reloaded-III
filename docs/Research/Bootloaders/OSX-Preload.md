# OSX Library Preload

This technique is effectively equivalent to [Windows: Inject Into Suspended Process][inject-into-suspended] but officially supported at the OS level.

Run the target process with `DYLD_INSERT_LIBRARIES=path/to/your/library.so command args...`

For more details see: [Linux Preload][linux-preload].

## Issue: Disabled by Default?

!!! error

    Reportedly you may need to disable [System Integrity Protection][system-integrity-protection] 
    (SIP) in order to use it in some cases (I believe only for binaries signed by Apple though).

Unfortunately, I do not have an Apple machine.

<!-- Links -->
[inject-into-suspended]: ./Windows-InjectIntoSuspended.md
[linux-preload]: ./Linux-Preload.md
[system-integrity-protection]: https://developer.apple.com/documentation/security/disabling_and_enabling_system_integrity_protection