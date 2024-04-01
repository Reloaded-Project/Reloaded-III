# Linux Library Preload

This technique is effectively equivalent to [Windows: Inject Into Suspended Process][inject-into-suspended] but officially supported at the OS level.
Run the target process with `LD_PRELOAD=path/to/your/library.so command args...`

Summary:
This is the only approach (I'm aware of) that can satisfy the constraint of executing custom code before game code.
This is not possible with `ptrace` at least.

## Issue: Spaces in Paths

!!! info

    The `LD_PRELOAD` variable uses space as a directory delimiter to

If the path to the mod loader contains a space, the mod manager must create a Symlink for the file with a location where a space isn't present.

## General Approach

- Read the current value of `LD_PRELOAD`.
- Create temporary symlink if path to mod loader contains space.
- Add mod loader library to value of `LD_PRELOAD`.
- Start the process.
- Restore original `LD_PRELOAD` value.

<!-- Links -->
[inject-into-suspended]: ./Windows-InjectIntoSuspended.md