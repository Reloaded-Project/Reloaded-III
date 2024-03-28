# Linux

!!! note

    Wine is covered under [Windows](./Windows.md).

!!! question "This Topic Needs Research"

    This topic is a grey area for me; native Linux games are not often modded.
    Any feedback from an expert would be appreciated.

!!! info

    This will be implemented when the need to support a cross-platform game arises. Always open for PRs 💜.

## Bootstrapping

Covered in [Linux Preload Bootloader](../Bootloaders/Linux-Preload.md).

This is the only approach (I'm aware of) that can satisfy the constraint of executing custom code before game code.

This is not possible with `ptrace` at least.