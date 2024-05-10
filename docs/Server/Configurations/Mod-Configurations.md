
## Inline Data Sizes

!!! info "This is how much data can be stored 'inline' alongside the file properties."

| FileSystem | Size        |
| ---------- | ----------- |
| NTFS       | ~900 bytes  |
| ext4       | ~60 bytes   |
| btrfs      | ~2000 bytes |

When configurations are under this size, reads are greatly accelerated.