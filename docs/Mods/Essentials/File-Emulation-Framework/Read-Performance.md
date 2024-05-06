# Read Performance of SOLID Files

!!! info "For other Performance Figures, see the [About Section][performance]"

    This section focuses on a *very specific edge case*.

!!! warning "Sometimes programs may read an entire file in one go from disk."

    Depending on storage medium used, this can have performance implications.

!!! example "Example: Reading a whole Texture Archive up front into memory."

	We have an emulated archive of 32 textures, and 16 textures come from external sources (are injected by an emulator).
    Normally we would read 1 large 64MB file sequentially, but now we're reading from 17 files.

For storage mediums such as Hard Drives which can only read from 1 place at one time, this will
slow down loads, as the drive now needs to seek to new locations for each file.

Other storage mediums which can read from multiple places at once, such as Solid State Drives,
this will have either no impact or slightly improve the performance.

!!! note "Amount of slowdown depends on size of chunks being read"

## Importance of These Tests

!!! tip "This page is the justification for the guideline "use [Merged File Cache][merged-file-cache] for small archives (<32M) with many small (<1M) files""

In practice you'd:

- Rarely 100% emulate files.
    - For large archives, usually less than 10% of files will be emulated.
- Use  instead.
    - To negate performance losses on HDDs seen in this very specific test.

## Test Setup

!!! note "A 32G test file size allows us to emulate a reasonable level of fragmentation."

    We will use 'Flexible IO Tester' to emulate different sorts of loads on our storage mediums.

Original Archive, Single 64MB File:

- `fio --name=test --rw=randread --bs=64M --iodepth=1 --numjobs=1 --size=32G --direct=1 --ioengine=libaio`

16 Files, each 4MB. 100% emulated file.

- `fio --name=test --rw=randread --bs=4M --iodepth=16 --numjobs=1 --size=32G --direct=1 --ioengine=libaio`

64 Files, each 1MB. 100% emulated file.

- `fio --name=test --rw=randread --bs=1M --iodepth=64 --numjobs=1 --size=32G --direct=1 --ioengine=libaio`

512 Files, each 128K. 100% emulated file.

- `fio --name=test --rw=randread --bs=128K --iodepth=512 --numjobs=1 --size=32G --direct=1 --ioengine=libaio`

## Old Hard Drive

Test performed on a 10 year old, 2014 WD Blue 1TB HDD using ntfs3 driver.

- (1.00x) `106MB/s`: Original Archive, Single 64MB File
- (0.80x) `85.2MB/s`: 16 Files, each 4MB. 100% emulated file.
- (0.71x) `75.7MB/s`: 64 Files, each 1MB. 100% emulated file.
- (0.28x) `30.2MB/s`: 512 Files, each 128K. 100% emulated file.

## Solid State Storage (SATA)

On a 10 year old `SanDisk SDSSDHP1` 128GB SSD on ntfs3 driver:

- (1.00x) `498MB/s`: Original Archive, Single 64MB File
- (1.00x) `499MB/s`: 16 Files, each 4MB. 100% emulated file.
- (1.00x) `498MB/s`: 64 Files, each 1MB. 100% emulated file.
- (0.99x) `494MB/s`: 128 Files, each 512KB. 100% emulated file.
- (0.90x) `446MB/s`: 512 Files, each 128K. 100% emulated file.

## Solid State Storage (NVME)

On an `SanDisk Samsung SSD 980 PRO 1TB` on btrfs:

- (1.00x) `3466MB/s`: Original Archive, Single 64MB File
- (1.05x) `3625MB/s`: 16 Files, each 4MB. 100% emulated file.
- (1.05x) `3618MB/s`: 64 Files, each 1MB. 100% emulated file.
- (1.05x) `3622MB/s`: 512 Files, each 128K. 100% emulated file.

Performance here improved.

!!! warning "Bottlenecked by PCI-E 3 on test system"

[merged-file-cache]: ../../Libraries/Merged-File-Cache/About.md
[performance]: ./About.md#performance-impact