# Routing

!!! info "This contains additional information on routing for developers."

    It may also provide insight on how a function should be implemented.

## Route.Matches

!!! note "`route.Matches` checks if the route ends with `input`."

    While also accounting for subfolders.

    So if the route is `<PATH_TO_GAME_FOLDER>/dvdroot/BGM/EVENT_ADX_E.AFS`,
    `route.Matches` will return `true` for `EVENT_ADX_E.AFS` because it ends with
    `EVENT_ADX_E.AFS`.

!!! info "A Truth table for `route.Matches(group.Route)`."

Standard routes:

| route        | group.Route | route.Matches(group.Route) | Description                          |
| ------------ | ----------- | -------------------------- | ------------------------------------ |
| a.bin        | b.bin       | false                      | `b.bin` not at end of `a.bin`        |
| b.bin        | b.bin       | true                       | Direct match.                        |
| folder/a.bin | a.bin       | true                       | Matches `a.bin` at end.              |
| folder/a.bin | b.bin       | false                      | `b.bin` not at end of `folder/a.bin` |

Nested files of same type:

| route                                | group.Route               | route.Matches(group.Route) | Description                                                             |
| ------------------------------------ | ------------------------- | -------------------------- | ----------------------------------------------------------------------- |
| parent.bin/child.bin                 | child.bin                 | true                       | Matches `child.bin` at end.                                             |
| parent.bin/child.bin                 | parent.bin/child.bin      | true                       | Matches `parent.bin/child.bin` at end.                                  |
| parent.bin/parentSubfolder/child.bin | parent.bin/child.bin      | false                      | Not direct descendant of `parent.bin`.                                  |
| parent.bin/parentSubfolder/child.bin | parentSubfolder/child.bin | true                       | Matches `child.bin` at end. May match multiple parent folders/archives. |

Nested files of different type:

| route                                | group.Route               | route.Matches(group.Route) | Description                                                             |
| ------------------------------------ | ------------------------- | -------------------------- | ----------------------------------------------------------------------- |
| parent.bin/child.dds                 | child.dds                 | true                       | Matches `child.dds` at end.                                             |
| parent.bin/child.dds                 | parent.bin/child.dds      | true                       | Matches `parent.bin/child.dds` at end.                                  |
| parent.bin/parentSubfolder/child.dds | parent.bin/child.dds      | false                      | Not direct descendant of `parent.bin`.                                  |
| parent.bin/parentSubfolder/child.dds | parentSubfolder/child.dds | true                       | Matches `child.dds` at end. May match multiple parent folders/archives. |

Unintended Actions / Collateral Damage:

| route                        | group.Route | route.Matches(group.Route) | Description                                                               |
| ---------------------------- | ----------- | -------------------------- | ------------------------------------------------------------------------- |
| ModBFolder/child.bin         | child.bin   | true                       | Overrides file `child.bin` in another folder. ❌ Potentially Undesireable. |
| child.bin/.../ModBFolder/... | child.bin   | false                      | ModBFolder doesn't end with `child.bin`.                                  |

In practice, the `route` is a full path to a file, with any recursive children tacked on if doing
recursive emulation.

e.g. `route` is

- `C:/Full/Path/To/file.afs`

If you are accessing file with path `SomeFolder/file.afs/00000.adx` while you are already building
`file.afs`, the `route` will be:

- `C:/Full/Path/To/file.afs/00000.adx`

This allows for recursive emulation of files.

!!! warning "Consider writing a diagnostic for undesireable overrides."

    We should avoid overriding files outside of game folders when that is not desireable.
    To avoid this, we should write a diagnostic to ensure people specify top level archives
    as `GameFolderName/file.afs` or `GameFolderName/data/file.afs` rather than just `file.afs`.

### Handling Subfolders

!!! info "This is a special case."

Sometimes an emulated file may have a hierarchy of internal files.
For example, an archive may have multiple nested folders.

For example, a mod may have the path `parent.bin/child/child.dds`, which should add `child/child.dds`
to `parent.bin`.

| route             | group.Route                             | route.Matches(group.Route) | Description                                                        |
| ----------------- | --------------------------------------- | -------------------------- | ------------------------------------------------------------------ |
| parent.bin        | parent.bin/child                        | true                       | Matched via `parent.bin` in front.                                 |
| parent.bin        | parent.bin/child/child2                 | true                       | Matched via `parent.bin` in front.                                 |
| folder/parent.bin | parent.bin/child                        | true                       | Matched via `parent.bin` in front.                                 |
| folder/parent.bin | parent.bin/child/child2                 | true                       | Matched via `parent.bin` in front.                                 |
| folder/parent.bin | folder/parent.bin/child                 | true                       | Matched via `folder/parent.bin` in front.                          |
| folder/parent.bin | der/parent.bin/child                    | true                       | Matched via `der/parent.bin` in front.                             |
| folder/parent.bin | folder/parent.bin/child/child2          | true                       | Matched via `folder/parent.bin` in front.                          |
| folder/parent.bin | folder/other/parent.bin/child           | false                      | `folder/parent.bin` != `folder/other`                              |
| parent.bin        | parent.bin_suffix/child                 | false                      | `parent.bin` is not a prefix of `parent.bin_suffix`.               |
| folder/parent.bin | folder/parent.bin_suffix/child          | false                      | `folder/parent.bin` is not a prefix of `folder/parent.bin_suffix`. |
| parent.bin        | parent.bin/otherFolder/parent.bin/child | true                       | Recursive `parent.bin` folders should not throw the logic off.     |

### Code

The algorithm for this is nontrivial, so here is a reference implementation.

```rust
use std::path::MAIN_SEPARATOR;
use memchr::memchr_iter;

pub fn route_matches(route: &str, group: &str) -> bool {
    // Neither should be empty, this should be disabled in release builds.
    #[cfg(debug_assertions)]
    {
        if route.is_empty() {
            panic!("Route cannot be empty");
        }
        if group.is_empty() {
            panic!("Group cannot be empty");
        }
        if group.starts_with(MAIN_SEPARATOR) {
            panic!("Group cannot start with forwrard slash");
        }
    }

    // We don't care about semantics of encoding, this is a pure byte match.
    route_matches_impl(route.as_bytes(), group.as_bytes())
}

pub fn route_matches_impl(route: &[u8], group: &[u8]) -> bool {
    let mut forward_slash_iter = memchr_iter(MAIN_SEPARATOR as u8, group);

    while let Some(group_index) = forward_slash_iter.next(){
        let current_group_slice = &group[..group_index];
        if route.ends_with(current_group_slice) {
            return true;
        }
    }

    // This may be a hot path depending on use case.
    return route.ends_with(group);
}

#[cfg(test)]
mod tests {
    use super::*;
    use rstest::rstest;

    #[rstest]
    #[case("a.bin", "b.bin", false, "`b.bin` not at end of `a.bin`")]
    #[case("b.bin", "b.bin", true, "Direct match")]
    #[case("folder/a.bin", "a.bin", true, "Matches `a.bin` at end")]
    #[case("folder/a.bin", "b.bin", false, "`b.bin` not at end of `folder/a.bin`")]
    fn test_standard_routes(
        #[case] route: &str,
        #[case] pattern: &str,
        #[case] expected: bool,
        #[case] description: &str,
    ) {
        assert_eq!(
            route_matches(route, pattern),
            expected,
            "Failed assertion for case: {}\nReason: {}",
            format!("{} , {}", route, pattern),
            description
        );
    }

    #[rstest]
    #[case(
        "/full/path/to/a.bin",
        "b.bin",
        false,
        "`b.bin` not at end of `/full/path/to/a.bin`"
    )]
    #[case("/full/path/to/b.bin", "b.bin", true, "Direct match")]
    #[case("/full/path/to/folder/a.bin", "a.bin", true, "Matches `a.bin` at end")]
    #[case(
        "/full/path/to/folder/a.bin",
        "b.bin",
        false,
        "`b.bin` not at end of `/full/path/to/folder/a.bin`"
    )]
    fn test_standard_routes_with_full_path_routes(
        #[case] route: &str,
        #[case] pattern: &str,
        #[case] expected: bool,
        #[case] description: &str,
    ) {
        assert_eq!(
            route_matches(route, pattern),
            expected,
            "Failed assertion for case: {}\nReason: {}",
            format!("{} , {}", route, pattern),
            description
        );
    }

    #[rstest]
    #[case(
        "parent.bin/child.bin",
        "child.bin",
        true,
        "Matches `child.bin` at end"
    )]
    #[case(
        "parent.bin/child.bin",
        "parent.bin/child.bin",
        true,
        "Matches `parent.bin/child.bin` at end"
    )]
    #[case(
        "parent.bin/parentSubfolder/child.bin",
        "parent.bin/child.bin",
        false,
        "Not direct descendant of `parent.bin`"
    )]
    #[case(
        "parent.bin/parentSubfolder/child.bin",
        "parentSubfolder/child.bin",
        true,
        "Matches `child.bin` at end. May match multiple parent folders/archives"
    )]
    fn test_nested_files_same_type(
        #[case] route: &str,
        #[case] pattern: &str,
        #[case] expected: bool,
        #[case] description: &str,
    ) {
        assert_eq!(
            route_matches(route, pattern),
            expected,
            "Failed assertion for case: {}\nReason: {}",
            format!("{} , {}", route, pattern),
            description
        );
    }

    #[rstest]
    #[case(
        "/full/path/to/parent.bin/child.bin",
        "child.bin",
        true,
        "Matches `child.bin` at end"
    )]
    #[case(
        "/full/path/to/parent.bin/child.bin",
        "parent.bin/child.bin",
        true,
        "Matches `parent.bin/child.bin` at end"
    )]
    #[case(
        "/full/path/to/parent.bin/parentSubfolder/child.bin",
        "parent.bin/child.bin",
        false,
        "Not direct descendant of `parent.bin`"
    )]
    #[case(
        "/full/path/to/parent.bin/parentSubfolder/child.bin",
        "parentSubfolder/child.bin",
        true,
        "Matches `child.bin` at end. May match multiple parent folders/archives"
    )]
    fn test_nested_files_same_type_with_full_path_routes(
        #[case] route: &str,
        #[case] pattern: &str,
        #[case] expected: bool,
        #[case] description: &str,
    ) {
        assert_eq!(
            route_matches(route, pattern),
            expected,
            "Failed assertion for case: {}\nReason: {}",
            format!("{} , {}", route, pattern),
            description
        );
    }

    #[rstest]
    #[case(
        "parent.bin/child.dds",
        "child.dds",
        true,
        "Matches `child.dds` at end"
    )]
    #[case(
        "parent.bin/child.dds",
        "parent.bin/child.dds",
        true,
        "Matches `parent.bin/child.dds` at end"
    )]
    #[case(
        "parent.bin/parentSubfolder/child.dds",
        "parent.bin/child.dds",
        false,
        "Not direct descendant of `parent.bin`"
    )]
    #[case(
        "parent.bin/parentSubfolder/child.dds",
        "parentSubfolder/child.dds",
        true,
        "Matches `child.dds` at end. May match multiple parent folders/archives"
    )]
    fn test_nested_files_different_type(
        #[case] route: &str,
        #[case] pattern: &str,
        #[case] expected: bool,
        #[case] description: &str,
    ) {
        assert_eq!(
            route_matches(route, pattern),
            expected,
            "Failed assertion for case: {}\nReason: {}",
            format!("{} , {}", route, pattern),
            description
        );
    }

    #[rstest]
    #[case(
        "/full/path/to/parent.bin/child.dds",
        "child.dds",
        true,
        "Matches `child.dds` at end"
    )]
    #[case(
        "/full/path/to/parent.bin/child.dds",
        "parent.bin/child.dds",
        true,
        "Matches `parent.bin/child.dds` at end"
    )]
    #[case(
        "/full/path/to/parent.bin/parentSubfolder/child.dds",
        "parent.bin/child.dds",
        false,
        "Not direct descendant of `parent.bin`"
    )]
    #[case(
        "/full/path/to/parent.bin/parentSubfolder/child.dds",
        "parentSubfolder/child.dds",
        true,
        "Matches `child.dds` at end. May match multiple parent folders/archives"
    )]
    fn test_nested_files_different_type_with_full_path_routes(
        #[case] route: &str,
        #[case] pattern: &str,
        #[case] expected: bool,
        #[case] description: &str,
    ) {
        assert_eq!(
            route_matches(route, pattern),
            expected,
            "Failed assertion for case: {}\nReason: {}",
            format!("{} , {}", route, pattern),
            description
        );
    }

    #[rstest]
    #[case(
        "ModBFolder/child.bin",
        "child.bin",
        true,
        "Overrides file `child.bin` in another folder. ❌ Potentially Undesireable"
    )]
    #[case(
        "child.bin/.../ModBFolder/...",
        "child.bin",
        false,
        "ModBFolder doesn't end with `child.bin`"
    )]
    fn test_unintended_actions(
        #[case] route: &str,
        #[case] pattern: &str,
        #[case] expected: bool,
        #[case] description: &str,
    ) {
        assert_eq!(
            route_matches(route, pattern),
            expected,
            "Failed assertion for case: {}\nReason: {}",
            format!("{} , {}", route, pattern),
            description
        );
    }

    #[rstest]
    #[case(
        "/full/path/to/ModBFolder/child.bin",
        "child.bin",
        true,
        "Overrides file `child.bin` in another folder. ❌ Potentially Undesireable"
    )]
    #[case(
        "/full/path/to/child.bin/.../ModBFolder/...",
        "child.bin",
        false,
        "ModBFolder doesn't end with `child.bin`"
    )]
    fn test_unintended_actions_with_full_path_routes(
        #[case] route: &str,
        #[case] pattern: &str,
        #[case] expected: bool,
        #[case] description: &str,
    ) {
        assert_eq!(
            route_matches(route, pattern),
            expected,
            "Failed assertion for case: {}\nReason: {}",
            format!("{} , {}", route, pattern),
            description
        );
    }

    #[rstest]
    #[case(
        "parent.bin",
        "parent.bin/child",
        true,
        "Matched via `parent.bin` in front"
    )]
    #[case(
        "parent.bin",
        "parent.bin/child/child2",
        true,
        "Matched via `parent.bin` in front"
    )]
    #[case(
        "folder/parent.bin",
        "parent.bin/child",
        true,
        "Matched via `parent.bin` in front"
    )]
    #[case(
        "folder/parent.bin",
        "parent.bin/child/child2",
        true,
        "Matched via `parent.bin` in front"
    )]
    #[case(
        "folder/parent.bin",
        "folder/parent.bin/child",
        true,
        "Matched via `folder/parent.bin` in front"
    )]
    #[case(
        "folder/parent.bin",
        "der/parent.bin/child",
        true,
        "Matched via `der/parent.bin` in front"
    )]
    #[case(
        "folder/parent.bin",
        "folder/parent.bin/child/child2",
        true,
        "Matched via `folder/parent.bin` in front"
    )]
    #[case(
        "folder/parent.bin",
        "folder/other/parent.bin/child",
        false,
        "`folder/parent.bin` != `folder/other`"
    )]
    #[case(
        "parent.bin",
        "parent.bin_suffix/child",
        false,
        "`parent.bin` is not a prefix of `parent.bin_suffix`"
    )]
    #[case(
        "folder/parent.bin",
        "folder/parent.bin_suffix/child",
        false,
        "`folder/parent.bin` is not a prefix of `folder/parent.bin_suffix`"
    )]
    #[case(
        "parent.bin",
        "parent.bin/otherFolder/parent.bin/child",
        true,
        "Recursive `parent.bin` folders should not throw the logic off"
    )]
    fn test_handling_subfolders(
        #[case] route: &str,
        #[case] pattern: &str,
        #[case] expected: bool,
        #[case] description: &str,
    ) {
        assert_eq!(
            route_matches(route, pattern),
            expected,
            "Failed assertion for case: {}\nReason: {}",
            format!("{} , {}", route, pattern),
            description
        );
    }

    #[rstest]
    #[case(
        "/full/path/to/parent.bin",
        "parent.bin/child",
        true,
        "Matched via `parent.bin` in front"
    )]
    #[case(
        "/full/path/to/parent.bin",
        "parent.bin/child/child2",
        true,
        "Matched via `parent.bin` in front"
    )]
    #[case(
        "/full/path/to/folder/parent.bin",
        "parent.bin/child",
        true,
        "Matched via `parent.bin` in front"
    )]
    #[case(
        "/full/path/to/folder/parent.bin",
        "parent.bin/child/child2",
        true,
        "Matched via `parent.bin` in front"
    )]
    #[case(
        "/full/path/to/folder/parent.bin",
        "full/path/to/folder/parent.bin/child",
        true,
        "Matched via `/full/path/to/folder/parent.bin` in front"
    )]
    #[case(
        "/full/path/to/folder/parent.bin",
        "other/full/path/to/folder/parent.bin/child",
        false,
        "Does not match because of 'other' folder at front."
    )]
    #[case(
        "/full/path/to/parent.bin",
        "parent.bin_suffix/child",
        false,
        "`parent.bin` is not a prefix of `parent.bin_suffix`"
    )]
    #[case(
        "/full/path/to/folder/parent.bin",
        "folder/parent.bin_suffix/child",
        false,
        "`/full/path/to/folder/parent.bin` is not a prefix of `folder/parent.bin_suffix`"
    )]
    #[case(
        "/full/path/to/parent.bin",
        "parent.bin/otherFolder/parent.bin/child",
        true,
        "Recursive `parent.bin` folders should not throw the logic off"
    )]
    fn test_handling_subfolders_with_full_path_routes(
        #[case] route: &str,
        #[case] pattern: &str,
        #[case] expected: bool,
        #[case] description: &str,
    ) {
        assert_eq!(
            route_matches(route, pattern),
            expected,
            "Failed assertion for case: {}\nReason: {}",
            format!("{} , {}", route, pattern),
            description
        );
    }
}
```

The algorithm below is technically O(n^2), however in practice it's O(n) because the number of directory
separarators which we test against is 1, or very close to 1.

When ported over to the actual emulator implementation, this should be benched, because with short
strings used for directory names (likely <8 chars), doing a byte by byte check may be faster latency
wise. (`memchr` is more optimised for throughput)