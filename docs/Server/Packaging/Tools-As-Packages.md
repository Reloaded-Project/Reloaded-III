!!! info "This page details the caveats involved in shipping 3rd party tools are packages."

Think of it as an ADR.

## Configurations

!!! info "External tools don't know about Reloaded's Loadout system."

We must be able to observe changes to configurations and *integrate* them into the loadout data.

Doing so is relatively tricky:

- The user may want to run the tool outside of Reloaded3.
- The tool may write its configuration files to arbitrary locations.
- The user may want to have global configurations for tools.
    - And also possibly per-version configurations.
- Some configurations, e.g. file paths are not portable across PCs.

### Configuration Location

!!! info "Where are the software configurations stored?"

There are multiple ways to work here:

- **Reloaded 3 Manages the Tool's Configuration**: Reloaded3 monitors where the tool writes its configurations and automatically syncs them.
    - 🛈 Requires regex filters & extra fields to monitor config locations.

- **Request Specific Config Location**: Reloaded3 requests a specific location to write config via commandline parameter.
    - ❌ Cannot ingest changes made by running tool outside of Reloaded3.

These are somewhat opposites of each other.

For example, R3 managing the tool's configuration would mean that any tool can be shipped as a package
without any source changes. However as a consequence, that means it's more likely to sync unnecessary
(machine specific) data, and thus increase my cloud storage costs. etc.

There's also the question of whether you want the configurations to 'leak' outside of Reloaded3
as a user. I think for most users, that may be 'yes' as most users would only install a tool once,
without separate per-loadout configurations.

### Synchronization Times

!!! info "When do we check for configuration changes?"

- **Process Sync**: The tool is run within Reloaded3 and its configurations are automatically synced.
    - ✅ Fairly efficient.
    - ❌ This means users running the tool outside of Reloaded3 will have suboptimal experience.
    - ❌ Fails if tool launches sub-process.

- **File System Watcher Sync**: The FileSystem is periodically checked for changes
    - ✅ Always works.
    - ❌ May produce multiple config change event over a single run of application.

- **Sync on Run**: Let the user choose between local and loadout config if they don't match at startup.
    - ✅ Works in and out of process.
    - ✅ Does not unnecessarily ingest.
    - ❌ Increases startup latency.

### Handling Multiple Configuration Files

!!! info "How do we handle multiple configuration files?"

The [Loadout][loadout] format is written primarily under the assumption that 1 mod == 1 config,
because that is the expected standard for mods.

However for `Tools`, it's necessary to support multiple configuration files, as we're not in control
of how they are built.

That proposes 2 approaches:

- **Merge Configurations**: Merge all configurations into a single file.
    - ✅ Simple to implement.
    - ❌ Inefficient on disk space (uncompressed).

- **Ingest Individual Files**: Store each file separately.
    - ✅ Efficient on disk space (uncompressed).
    - ⚠ Requires extensions to event format.

### Chosen Approach

The following approaches have been chosen:

- **Configuration Location**: Reloaded3 manages the tool's configuration.
- **Synchronization Times**: Process Sync ***AND*** Sync on Run.
    - The user is prompted to choose between local and loadout config if they mismatch.
- **Handling Multiple Configuration Files**: Ingest Individual Files.

The `Ingest` operation will happen upon loading of a tool.

[loadout]: ../Storage/Loadouts/About.md