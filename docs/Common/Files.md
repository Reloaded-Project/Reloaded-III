!!! info "This contains development notes related to reading/writing files."

## Inline Data Sizes

!!! tip "Sometimes very small files can be directly embedded into the FileSystem Metadata."

    This avoids reading from an additional separate place, speeding up reads.

This table shows the approximate amount of space that can typically be inlined in common file systems.

| FileSystem | Size        |
| ---------- | ----------- |
| NTFS       | ~900 bytes  |
| ext4       | ~60 bytes   |
| btrfs      | ~2000 bytes |

As a general rule of thumb, if you have text-like data which is expected to be around 2KB,
try compressing it.

This will likely make the data fit in inline on the common use case of NTFS, improving reads.