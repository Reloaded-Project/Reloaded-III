# Hash Cache API

!!! info "This document outlines the API for the Reloaded3 Hash Cache system."

It is composed of a `writer` for creating hash cache data and a `reader` for accessing the
data from existing sources.


!!! note "Some of the code here was made by an LLM and not yet tested."

    And as per the [R3 code guidelines][code-guidelines], it uses `no_std` with `alloc` as a starting point.


## Common Types

```rust
use alloc::string::String;

pub type FILETIME = u64;

#[derive(Clone)]
pub struct FileInfo {
    pub partial_hash: u64,
    pub full_hash: u64,
    pub path_hash: u64,
    pub last_modified: FILETIME,
    pub path: Option<String>,
}

// A wrapper around a valid index in the HashCacheReader
#[derive(Copy, Clone, Debug, Eq, PartialEq)]
pub struct EntryIndex(usize);
```

## Writer API

!!! info "The `HashCacheWriter` is responsible for creating new hash cache data with optional [path storage][paths-section]."

It is thread-safe and allows adding file information. The `finalize` method uses a destination factory to create a properly sized destination.

```rust
pub trait WriteDestinationFactory: Send + Sync {
    type Error;
    type Destination: WriteDestination;

    /// Creates a destination with the specified capacity
    fn create_destination(&self, capacity: usize) -> Result<Self::Destination, Self::Error>;
}

pub trait WriteDestination: Send + Sync {
    type Error;
    type Reader: Source;

    fn write(&mut self, data: &[u8]) -> Result<(), Self::Error>;
    fn finish(self) -> Result<Self::Reader, Self::Error>;
}

pub struct HashCacheWriter {
    // Internal fields
}

impl HashCacheWriter {
    /// Creates a new HashCacheWriter instance
    pub fn new() -> Self;

    /// Adds file information to the hash cache
    pub fn add_file(&mut self, file_info: FileInfo);

    /// Finalizes the writing process and returns a reader
    ///
    /// This method computes the required capacity for the destination,
    /// creates the destination using the factory, writes the data,
    /// and returns a reader for the written data.
    pub fn finalize<F: WriteDestinationFactory>(
        self,
        factory: F,
        include_paths: bool
    ) -> Result<HashCacheReader<F::Destination::Reader>, F::Error>;
}
```

## Reader API

!!! info "The `HashCacheReader` is used to read and query data from [existing hash cache data][file-format]."

It's designed to be thread-safe and can work with various data sources efficiently.

```rust
pub trait Source: Send + Sync {
    fn as_slice(&self) -> &[u8];
}

pub struct HashCacheReader<S: Source> {
    // Internal fields
}

impl<S: Source> HashCacheReader<S> {
    /// Creates a new HashCacheReader instance from a source
    pub fn new(source: S) -> Self;

    /// Returns the number of entries in the hash cache
    pub fn entry_count(&self) -> usize;

    /// Checks if paths are included in this hash cache
    pub fn has_paths(&self) -> bool;

    /// Finds an entry by path hash and returns a wrapper around its index
    pub fn find_by_path_hash(&self, path_hash: u64) -> Option<EntryIndex>;

    /// Gets the partial hash for a file using an EntryIndex
    pub fn partial_hash(&self, entry: EntryIndex) -> u64;

    /// Gets the full hash for a file using an EntryIndex
    pub fn full_hash(&self, entry: EntryIndex) -> u64;

    /// Gets the path hash for a file using an EntryIndex
    pub fn path_hash(&self, entry: EntryIndex) -> u64;

    /// Gets the last modified time for a file using an EntryIndex
    pub fn last_modified(&self, entry: EntryIndex) -> FILETIME;

    /// Gets the path for a file using an EntryIndex (if paths are included)
    pub fn path(&self, entry: EntryIndex) -> Option<&str>;

    /// Iterates over all entries in the hash cache
    pub fn iter(&self) -> impl Iterator<Item = FileInfo>;
}
```

## Write Destinations

!!! info "This section describes some example write destination factories for the `HashCacheWriter`."

### Memory-Mapped File Destination Factory

```rust
pub struct MmapFileDestinationFactory {
    path: String,
}

impl WriteDestinationFactory for MmapFileDestinationFactory {
    type Error = IoError;
    type Destination = MmapFileDestination;

    fn create_destination(&self, capacity: usize) -> Result<Self::Destination, Self::Error>;
}

pub struct MmapFileDestination {
    // Internal fields
}

impl WriteDestination for MmapFileDestination {
    type Error = IoError;
    type Reader = MmapFileSource;

    // Method implementations
}
```

### In-Memory Destination Factory

```rust
pub struct InMemoryDestinationFactory;

impl WriteDestinationFactory for InMemoryDestinationFactory {
    type Error = Never; // This implementation cannot fail
    type Destination = InMemoryDestination;

    fn create_destination(&self, capacity: usize) -> Result<Self::Destination, Self::Error>;
}

pub struct InMemoryDestination {
    // Internal fields
}

impl WriteDestination for InMemoryDestination {
    type Error = Never; // This implementation cannot fail
    type Reader = InMemorySource;

    // Method implementations
}
```

## Read Sources

!!! info "This section describes the available/reference read sources for the `HashCacheReader`."

### Memory-Mapped File Source

```rust
pub struct MmapFileSource(/* Internal fields */);

impl Source for MmapFileSource {
    // Method implementation
}
```

### In-Memory Source

```rust
pub struct InMemorySource(/* Internal fields */);

impl Source for InMemorySource {
    // Method implementation
}
```

## Usage Examples

!!! info "This section provides examples of how to use the Hash Cache API."

    Disclaimer: This is pseudocode generated by a large language model.

### Writing to a Hash Cache

```rust
use alloc::string::String;

// Creating a new HashCacheWriter
let mut writer = HashCacheWriter::new();

// Adding file information to the hash cache
let file_info = FileInfo {
    partial_hash: 0x1234567890ABCDEF,
    full_hash: 0xFEDCBA0987654321,
    path_hash: 0xABCDEF0123456789,
    last_modified: 132514620000000000, // Windows FILETIME (100-nanosecond intervals since January 1, 1601)
    path: Some(String::from("file1.txt")),
};

writer.add_file(file_info);
// Add more files...

// Creating a memory-mapped file destination factory
let factory = MmapFileDestinationFactory::new(String::from("hash_cache.bin"));

// Finalizing the writing process and obtaining a reader
let reader = writer.finalize(factory, true).expect("Failed to finalize");

// Now you can use the reader to access the hash cache data
println!("Number of entries: {}", reader.entry_count());
```

### Reading from a Hash Cache

```rust
// Creating a memory-mapped file source
let source = MmapFileSource::new("hash_cache.bin").expect("Failed to open file");

// Creating a new HashCacheReader
let reader = HashCacheReader::new(source);

// Using the reader to access hash cache data
if let Some(entry) = reader.find_by_path_hash(compute_path_hash("file1.txt")) {
    println!("Partial Hash: {:x}", reader.partial_hash(entry));
    println!("Full Hash: {:x}", reader.full_hash(entry));
    println!("Last Modified: {:x}", reader.last_modified(entry));
    if let Some(path) = reader.path(entry) {
        println!("Path: {}", path);
    }
}

// Iterating over all entries in the hash cache
for entry in reader.iter() {
    println!("Partial Hash: {:x}, Full Hash: {:x}", entry.partial_hash, entry.full_hash);
}
```

## Implementation Notes

!!! info "Notes for those using the API."

- The `HashCacheWriter` internally computes the required capacity during finalization.
- The destination factory creates a destination with the exact required capacity, avoiding unnecessary re-allocations.
- Path compression is performed as first step of `finalization`.
- The `HashCacheReader` uses a generic `Source` trait, allowing it to work efficiently with different
  data sources without runtime overhead.
- The `EntryIndex` wrapper allows for efficient, unchecked access to entry data after the initial safety check.

## Thread Safety

- Both the `HashCacheReader` and `HashCacheWriter` are designed to be thread-safe and can be safely
  shared between threads without additional synchronization.

[paths-section]: ./File-Format.md#paths-section
[file-format]: ./File-Format.md
[code-guidelines]: ../../Code-Guidelines/Code-Guidelines.md