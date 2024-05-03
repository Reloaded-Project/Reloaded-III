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
| parent.bin/child.bin                 | parent.bin/child.dds      | true                       | Matches `parent.bin/child.dds` at end.                                  |
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

| route             | group.Route                    | route.Matches(group.Route) | Description                                                        |
| ----------------- | ------------------------------ | -------------------------- | ------------------------------------------------------------------ |
| parent.bin        | parent.bin/child               | true                       | Matched via `parent.bin` in front.                                 |
| parent.bin        | parent.bin/child/child2        | true                       | Matched via `parent.bin` in front.                                 |
| folder/parent.bin | parent.bin/child               | true                       | Matched via `parent.bin` in front.                                 |
| folder/parent.bin | parent.bin/child/child2        | true                       | Matched via `parent.bin` in front.                                 |
| folder/parent.bin | folder/parent.bin/child        | true                       | Matched via `folder/parent.bin` in front.                          |
| folder/parent.bin | folder/parent.bin/child/child2 | true                       | Matched via `folder/parent.bin` in front.                          |
| folder/parent.bin | folder/other/parent.bin/child  | false                      | `folder/parent.bin` != `folder/other`                              |
| parent.bin        | parent.bin_suffix/child        | false                      | `parent.bin` is not a prefix of `parent.bin_suffix`.               |
| folder/parent.bin | folder/parent.bin_suffix/child | false                      | `folder/parent.bin` is not a prefix of `folder/parent.bin_suffix`. |

