!!! info "This page contains some benchmarks for different key-value storage systems."

Testing was done using a fork of [`redb`][redb-fork], with
a rough quick implementation of filesystem storage.

Each 'item' is a blob of random 150 bytes; which makes it small enough to embed into the MFT on NTFS
and inode metadata in BTRFS.

## Linux (BTRFS)

```
filesystem: Bulk loaded 100000 items in 1130ms
filesystem: Wrote 100 individual items in 1ms
filesystem: Wrote 100 x 1000 items in 1199ms
filesystem: len() in 24ms
filesystem: Random read 100000 items in 318ms
filesystem: Random read 100000 items in 320ms
filesystem: Random read (4 threads) 100000 items in 119ms
filesystem: Random read (8 threads) 100000 items in 70ms
filesystem: Random read (16 threads) 100000 items in 56ms
filesystem: Random read (32 threads) 100000 items in 53ms
filesystem: Removed 50000 items in 537ms
lmdb-rkv: Bulk loaded 100000 items in 72ms
lmdb-rkv: Wrote 100 individual items in 1246ms
lmdb-rkv: Wrote 100 x 1000 items in 2620ms
lmdb-rkv: len() in 0ms
lmdb-rkv: Random read 100000 items in 46ms
lmdb-rkv: Random read 100000 items in 36ms
lmdb-rkv: Random read (4 threads) 100000 items in 11ms
lmdb-rkv: Random read (8 threads) 100000 items in 6ms
lmdb-rkv: Random read (16 threads) 100000 items in 4ms
lmdb-rkv: Random read (32 threads) 100000 items in 3ms
lmdb-rkv: Removed 50000 items in 106ms
rocksdb: Bulk loaded 100000 items in 345ms
rocksdb: Wrote 100 individual items in 609ms
rocksdb: Wrote 100 x 1000 items in 944ms
rocksdb: len() in 38ms
rocksdb: Random read 100000 items in 91ms
rocksdb: Random read 100000 items in 98ms
rocksdb: Random read (4 threads) 100000 items in 25ms
rocksdb: Random read (8 threads) 100000 items in 13ms
rocksdb: Random read (16 threads) 100000 items in 8ms
rocksdb: Random read (32 threads) 100000 items in 8ms
rocksdb: Removed 50000 items in 211ms
```

### Extra Benches

```
redb: Bulk loaded 100000 items in 175ms
redb: Wrote 100 individual items in 702ms
redb: Wrote 100 x 1000 items in 2365ms
redb: len() in 0ms
redb: Random read 100000 items in 61ms
redb: Random read 100000 items in 48ms
redb: Random read (4 threads) 100000 items in 27ms
redb: Random read (8 threads) 100000 items in 14ms
redb: Random read (16 threads) 100000 items in 9ms
redb: Random read (32 threads) 100000 items in 7ms
redb: Removed 50000 items in 189ms
rocksdb: Removed 50000 items in 209ms
sled: Bulk loaded 100000 items in 359ms
sled: Wrote 100 individual items in 681ms
sled: Wrote 100 x 1000 items in 1199ms
sled: len() in 70ms
sled: Random read 100000 items in 96ms
sled: Random read 100000 items in 94ms
sled: Random read (4 threads) 100000 items in 35ms
sled: Random read (8 threads) 100000 items in 18ms
sled: Random read (16 threads) 100000 items in 12ms
sled: Random read (32 threads) 100000 items in 10ms
sled: Removed 50000 items in 152ms
sanakirja: Bulk loaded 100000 items in 80ms
sanakirja: Wrote 100 individual items in 1284ms
sanakirja: Wrote 100 x 1000 items in 3010ms
sanakirja: len() in 11ms
sanakirja: Random read 100000 items in 60ms
sanakirja: Random read 100000 items in 51ms
sanakirja: Random read (4 threads) 100000 items in 28ms
sanakirja: Random read (8 threads) 100000 items in 96ms
sanakirja: Random read (16 threads) 100000 items in 387ms
sanakirja: Random read (32 threads) 100000 items in 487ms
sanakirja: Removed 50000 items in 134ms
```

## Win11 NTFS (No Defender)

```
filesystem: Bulk loaded 100000 items in 32085ms
filesystem: Wrote 100 individual items in 27ms
filesystem: Wrote 100 x 1000 items in 34359ms
filesystem: len() in 223ms
filesystem: Random read 100000 items in 5372ms
filesystem: Random read 100000 items in 4893ms
filesystem: Random read (4 threads) 100000 items in 1567ms
filesystem: Random read (8 threads) 100000 items in 1242ms
filesystem: Random read (16 threads) 100000 items in 852ms
filesystem: Random read (32 threads) 100000 items in 1019ms
filesystem: Removed 50000 items in 5785ms
lmdb-rkv: Bulk loaded 100000 items in 99ms
lmdb-rkv: Wrote 100 individual items in 202ms
lmdb-rkv: Wrote 100 x 1000 items in 3271ms
lmdb-rkv: len() in 0ms
lmdb-rkv: Random read 100000 items in 59ms
lmdb-rkv: Random read 100000 items in 52ms
lmdb-rkv: Random read (4 threads) 100000 items in 11ms
lmdb-rkv: Random read (8 threads) 100000 items in 8ms
lmdb-rkv: Random read (16 threads) 100000 items in 4ms
lmdb-rkv: Random read (32 threads) 100000 items in 4ms
lmdb-rkv: Removed 50000 items in 175ms
rocksdb: Bulk loaded 100000 items in 491ms
rocksdb: Wrote 100 individual items in 194ms
rocksdb: Wrote 100 x 1000 items in 614ms
rocksdb: len() in 49ms
rocksdb: Random read 100000 items in 129ms
rocksdb: Random read 100000 items in 118ms
rocksdb: Random read (4 threads) 100000 items in 26ms
rocksdb: Random read (8 threads) 100000 items in 17ms
rocksdb: Random read (16 threads) 100000 items in 11ms
rocksdb: Random read (32 threads) 100000 items in 9ms
rocksdb: Removed 50000 items in 284ms
```

## Win11 NTFS (with Defender)

```
filesystem: Bulk loaded 100000 items in 42114ms
filesystem: Wrote 100 individual items in 42ms
filesystem: Wrote 100 x 1000 items in 45605ms
filesystem: len() in 197ms
filesystem: Random read 100000 items in 5647ms
filesystem: Random read 100000 items in 4988ms
filesystem: Random read (4 threads) 100000 items in 1767ms
filesystem: Random read (8 threads) 100000 items in 1360ms
filesystem: Random read (16 threads) 100000 items in 883ms
filesystem: Random read (32 threads) 100000 items in 898ms
filesystem: Removed 50000 items in 6012ms
lmdb-rkv: Bulk loaded 100000 items in 97ms
lmdb-rkv: Wrote 100 individual items in 202ms
lmdb-rkv: Wrote 100 x 1000 items in 3278ms
lmdb-rkv: len() in 0ms
lmdb-rkv: Random read 100000 items in 54ms
lmdb-rkv: Random read 100000 items in 49ms
lmdb-rkv: Random read (4 threads) 100000 items in 11ms
lmdb-rkv: Random read (8 threads) 100000 items in 8ms
lmdb-rkv: Random read (16 threads) 100000 items in 4ms
lmdb-rkv: Random read (32 threads) 100000 items in 4ms
lmdb-rkv: Removed 50000 items in 169ms
rocksdb: Bulk loaded 100000 items in 488ms
rocksdb: Wrote 100 individual items in 236ms
rocksdb: Wrote 100 x 1000 items in 622ms
rocksdb: len() in 46ms
rocksdb: Random read 100000 items in 152ms
rocksdb: Random read 100000 items in 119ms
rocksdb: Random read (4 threads) 100000 items in 27ms
rocksdb: Random read (8 threads) 100000 items in 18ms
rocksdb: Random read (16 threads) 100000 items in 11ms
rocksdb: Random read (32 threads) 100000 items in 10ms
rocksdb: Removed 50000 items in 294ms
```

## Conclusion

For Reloaded3's use case, which sometimes requires fast access to very small files, `lmdb` is preferable; as it achieves the best read performance with very good write performance.

As for code size, using [heed][heed] wrapper for Rust, with the minimal example:

```
RUSTFLAGS="-C panic=abort -C lto=fat -C embed-bitcode=yes" cargo +nightly bloat -Z build-std=std,panic_abort -Z build-std-features=panic_immediate_abort --target x86_64-unknown-linux-gnu --profile profile --filter mdb
```

We get around 65KiB of code size, with the following breakdown:

```
File .text    Size           Crate Name
0.4%  5.7%  5.9KiB       [Unknown] _mdb_cursor_put
0.4%  5.6%  5.8KiB       [Unknown] mdb_page_split
0.4%  5.5%  5.7KiB       [Unknown] _mdb_txn_commit
0.3%  5.0%  5.2KiB       [Unknown] mdb_rebalance
0.3%  4.1%  4.3KiB       lmdb_test lmdb_test::main
0.1%  2.0%  2.0KiB       [Unknown] mdb_page_merge
0.1%  1.9%  2.0KiB       [Unknown] _mdb_cursor_del.part.0
0.1%  1.9%  1.9KiB       [Unknown] mdb_page_search
0.1%  1.7%  1.7KiB       [Unknown] mdb_page_alloc.isra.0
0.1%  1.6%  1.7KiB lmdb_master_sys mdb_dbi_open
0.1%  1.5%  1.5KiB       [Unknown] mdb_cursor_set
0.1%  1.4%  1.4KiB       [Unknown] mdb_txn_renew0
0.1%  1.2%  1.3KiB       [Unknown] mdb_cursor_get.localalias
0.1%  1.2%  1.2KiB       [Unknown] mdb_drop0
0.1%  1.1%  1.2KiB       [Unknown] mdb_page_flush
0.1%  1.0%  1.1KiB       [Unknown] mdb_node_add
0.1%  1.0%  1.0KiB       [Unknown] mdb_page_touch
0.1%  0.9%    993B lmdb_master_sys mdb_txn_begin
0.1%  0.9%    972B       [Unknown] mdb_env_open2
0.1%  0.9%    913B lmdb_master_sys mdb_env_open
1.1% 16.9% 17.5KiB                 And 81 smaller methods. Use -n N to show more.
4.2% 62.9% 65.2KiB                 filtered data size, the file size is 1.5MiB
```

Cargo.toml:

```toml
# Profile Build
[profile.profile]
inherits = "release"
debug = true
codegen-units = 1
lto = true
strip = false  # No stripping!!

# Optimized Release Build
[profile.release]
codegen-units = 1
lto = true
strip = true  # Automatically strip symbols from the binary.
panic = "abort"
```

main.rs:

```rust
use heed::{byteorder, Database, EnvOpenOptions};
use heed::types::*;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let env = unsafe { EnvOpenOptions::new().open("my-first-db")? };

    // We open the default unnamed database
    let mut wtxn = env.write_txn()?;
    let db: Database<Str, U32<byteorder::NativeEndian>> = env.create_database(&mut wtxn, None)?;

    // We open a write transaction
    db.put(&mut wtxn, "seven", &7)?;
    db.put(&mut wtxn, "zero", &0)?;
    db.put(&mut wtxn, "five", &5)?;
    db.put(&mut wtxn, "three", &3)?;
    wtxn.commit()?;

    // We open a read transaction to check if those values are now available
    let mut rtxn = env.read_txn()?;

    let ret = db.get(&rtxn, "zero")?;
    assert_eq!(ret, Some(0));

    let ret = db.get(&rtxn, "five")?;
    assert_eq!(ret, Some(5));

    Ok(())
}
```

[redb-fork]: https://github.com/Sewer56/redb/tree/test-filesystem
[heed]: https://github.com/meilisearch/heed