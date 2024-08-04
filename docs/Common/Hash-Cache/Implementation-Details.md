This page lists suggestions for when the hash cache is eventually implemented.

## No Embedded Hash Table

!!! info "The Hash Cache format does not include an embedded `HashTable`."

Instead, we generate one at runtime after loading.

Populating a `HashTable` with all the file name hashes is cheap because:

- The total number of items is known.
- All of the names are sequential in the file, thus we have high cache hit rate.

With a non-embedded hashtable, it's also possible to use a more efficient implementation; for example,
SwissTable works [better in `usize` groups due to high NEON latency][swisstable].

### Finding an Entry

!!! info "Implementation tip for Rust `HashBrown` [HashTable][hashtable]."

An entry could be stored as:

```rust
pub struct TableEntry
{
    pub key: XXH3, // u64
}
```

And query with:

```rust
table.find(KEY_HASH, |&val| val.key == KEY_HASH);
```

This performs a fast key only query.

## File Path Size Optimization

!!! tip "The file entries can be rearranged to optimize for compression ratios."

The entries can be sorted such that the strings in the [File Paths Section][paths-section] are
lexicographically sorted before compression. This far increases the likelihood of similar paths
being grouped together; leading to a smaller file, and thus faster load.

[hashtable]: https://docs.rs/hashbrown/latest/hashbrown/struct.HashTable.html#method.find
[swisstable]: https://faultlore.com/blah/hashbrown-tldr/
[paths-section]: File-Format.md#paths-section