## Implementing Redirection

The virtual file system uses two main data structures:

1. The `RedirectionTree` which maps old file paths to new paths as mods are loading. It uses an O(N) trie-like structure.

2. The `LookupTree` which is an optimized version of the RedirectionTree used after all mods are loaded. It uses an O(3) structure for fast lookups.

Here is how you could implement these structures in Rust using the `hashbrown` crate:

```rust
use hashbrown::HashMap;

pub struct RedirectionTree {
    pub root: RedirectionNode
}

pub struct RedirectionNode {
    pub children: HashMap<String, RedirectionNode>,
    pub items: HashMap<String, String>,
}

impl RedirectionNode {
    pub fn new() -> Self {
        RedirectionNode {
            children: HashMap::new(),
            items: HashMap::new(),
        }
    }
}

impl RedirectionTree {
    pub fn add_path(&mut self, old_path: &str, new_path: &str) {
        let mut current = &mut self.root;
        for part in old_path.split('/') {
            current = current.children.entry(part.to_string()).or_insert(RedirectionNode::new());
        }
        current.items.insert(old_path.to_string(), new_path.to_string());
    }
}
```

```rust
use hashbrown::HashMap;

pub struct LookupTree {
    pub prefix: String,
    pub subdir_to_files: HashMap<String, HashMap<String, String>>,
}

impl LookupTree {
    pub fn from_redirection_tree(tree: &RedirectionTree) -> Self {
        let mut lookup = LookupTree {
            prefix: String::new(),
            subdir_to_files: HashMap::new(),
        };

        lookup.build_prefix(tree);
        lookup.build_subdir_to_files(&tree.root, "");

        lookup
    }

    fn build_prefix(&mut self, tree: &RedirectionTree) {
        // Find common prefix of all paths
        // ...
    }

    fn build_subdir_to_files(&mut self, node: &RedirectionNode, path: &str) {
        if !node.items.is_empty() {
            self.subdir_to_files.insert(path.to_string(), node.items.clone());
        }

        for (name, child) in &node.children {
            let sub_path = format!("{}/{}", path, name);
            self.build_subdir_to_files(child, &sub_path);
        }
    }
}
```

The `LookupTree` is built from the `RedirectionTree` when all mods are done loading. It extracts a common prefix from all paths to save memory, and builds a flat map of subdirectories to files.

To detect file changes efficiently, you can use the `notify` crate to watch the redirect folders for changes and rebuild the trees as needed. Here's a sketch:

```rust
use notify::{RecommendedWatcher, Watcher, RecursiveMode};
use std::sync::mpsc::channel;
use std::time::Duration;

fn main() {
    let (tx, rx) = channel();
    let mut watcher: RecommendedWatcher = Watcher::new(tx, Duration::from_secs(1)).unwrap();

    watcher.watch("path/to/redirector", RecursiveMode::Recursive).unwrap();

    loop {
        match rx.recv() {
            // Rebuild trees on file change events
            Ok(event) => println!("event: {:?}", event),
            Err(e) => println!("watch error: {:?}", e),
        }
    }
}
```

This sets up a watcher on the Redirector folder that will receive events when files change. You can then trigger a rebuild of the `RedirectionTree` and `LookupTree` to pick up those changes.