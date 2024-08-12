# Guidelines

!!! info "These are guidelines for structuring workflows from a UX perspective, as opposed to hard rules."

## Workflows should be 'Objective' (Goal Based)

Instead of being 'technical'. This is to aid first time users.

✅ Prefer naming workflows such as:

- Change a Character
- Change an Object
- Change a Music Track
- Change a Sound Effect
- Change a Stage

❌ Instead of:

- Replace a Model
- Replace an Audio File

## Nesting

!!! info "Use nesting to group similar items within workflows together."

For example in the `Change an Object` workflow, you'd do the following:

- 🌊 Seaside Hill
    - 🌲 Tree
    - 🪨 Rock
- 🏙 Grand Metropolis
    - 🚗 Flying Car
    - 🪧 Sign

Where `Seaside Hill` and `Grand Metropolis` are the levels, and `Tree`, `Rock`, `Flying Car`, and `Sign` are the objects within those levels. You would first select the object, then the level.

As the last layer of nesting, consider making options for whether you want to `Replace` or `Add` the object.

- ➕ Add as New Object
- 🔄 Replace the Original Object

!!! tip "Maximize the use of images."

## Automate as Much as Possible

!!! info "Prefer reducing the number of steps required to perform a task on the user's end."

This not only makes the process faster for the user, but it also reduces how much
you have to document for the `post creation` phase.

To give an example; here's a common list of possible tasks to automate:

- Place original unmodified files where the new files should be.
    - This helps users understand the structure of how to place the files.
- Auto convert music files to the correct format.
    - Help user find loops in music tracks.
- Allow user to fill in extra template specific details.
    - For example, the name of the stage being added if the workflow is `Add a Stage`.

## Generic Workflows

!!! info "Some workflows can be non-game specific."

For example, multiple games that use the same engine or middleware, may share workflows.

In this case, we can use [Signature Scans][signature-scans] to detect potential workflows
for 'new' games.

## Provide Wiki Page with Additional Information

!!! info "Some workflows may require additional action/guidance for the user."

Wiki pages can be shipped in one of the two following ways:

- URL to wiki page.
- As template with the workflow, and then exported to user's mod folder.

The first is preferred, as it can be updated without updating the workflow.
However, one must be careful not to make breaking changes. If things change significantly,
a new page should be created alongside the old one.

[signature-scans]: ../../Mods/Libraries/Signature-Scanner/About.md