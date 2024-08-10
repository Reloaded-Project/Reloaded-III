# Workflow Schema

!!! info "This file specifies the individual layout of a Reloaded3 workflow, including schema and supporting files."

## A Typical Workflow Package

!!! info "A typical package with workflows looks something like this."

```
reloaded3.workflow.sonicheroes.addacharacter.s56
├── languages
│   └── create-a-stage
│       ├── en-GB.toml
│       └── uwu-en.toml
├── package
│   └── images
│       ├── bingo_highway.jxl
│       ├── casino_icon.jxl
│       ├── casino_park.jxl
│       ├── city_icon.jxl
│       ├── egg_hawk.jxl
│       ├── grand_metrpolis.jxl
│       ├── ocean_palace.jxl
│       ├── power_plant.jxl
│       ├── robot_carnival.jxl
│       ├── seaside_hill.jxl
│       ├── seaside_icon.jxl
│       └── team_battle_1.jxl
├── workflows
│   └── create-a-stage
│       ├── files
│       │   └── package.toml
│       └── workflow.toml
└── package.toml
```

- Each workflow is stored in a subfolder of the `workflows` folder.
    - The `files` subfolder contains templates on which we perform [`substitution`][substitution] on.
    - After `substitution`, the files are copied to the user's mod folder.
- The `languages` folder contains the localization files for each workflow.
- The `package/images` folder contains the images for each workflow (see [Packaging: Images][packaging-images] for more info).
- The [workflow.toml][workflow-toml] file defines the steps and metadata of the workflow.

## Workflow Execution Steps

!!! info "The following steps are used to execute a workflow."

1. [Run Workflow][schema]
2. [Run Workflow Script: `Post User`][scripting]
3. [Perform Substitution in Templates][substitution]
4. [Run Workflow Script: `Post`][scripting]

[workflow-toml]: ./Schema.md
[packaging-images]: ../../Packaging/About.md#images
[substitution]: ./Templates.md#substitution
[scripting]: ./Scripting.md
[schema]: ./Schema.md