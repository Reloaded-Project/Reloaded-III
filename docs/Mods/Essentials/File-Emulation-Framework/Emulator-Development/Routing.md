# Routing

!!! info "This contains additional information on routing for developers."

## Route.Matches

!!! note "`route.Matches` checks if the route ends with `input`."

    So if the full path is `<PATH_TO_GAME_FOLDER>/dvdroot/BGM/EVENT_ADX_E.AFS`,
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