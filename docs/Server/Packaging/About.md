# Packaging

!!! info "This page contains all information related to how mods are packaged and distributed."


## Package Structure

Each mod package contains the following approximate structure.

```
reloaded3.utility.examplemod.s56
├── package
│   ├── changelog
│   │   ├── 1.0.0.md
│   │   ├── 1.1.0.md
│   │   ├── 1.2.0.md
│   │   ├── 1.2.1.md
│   │   └── 2.0.0.md
│   ├── docs
│   │   └── index.html
│   ├── images
│   │   ├── skill-1.jxl
│   │   ├── skill-2.jxl
│   │   └── skill-3.jxl
│   ├── description.md
│   ├── files.meta
│   └── license.md
├── redirector
│   └── skill-game-asset.bin
├── config.toml
└── package.toml
```

### Changelog

!!! info "Located in `package/changelog`."

!!! info "This contains the changelog for each version of the mod up until the current version."

Each version is contained in its own `Markdown` file, e.g. `1.0.0.md`.

### Config

!!! info "Located at `package/config.toml`."

!!! info "This contains the configuration for the mod."

This file may not exist in some packages.

This file stores the configuration schema used for the package when the user hits
`Configure Mod` (or equivalent) button inside the `Mod Manager` frontend.

### Description

!!! info "Located at `package/description.md`."

This contains the full description of the package, written in markdown.

For a mod, this should match what you would normally put on a modding site (e.g. GameBanana, Nexus,
ThunderStore) etc.

### Docs

!!! info "Located in `package/docs`."

!!! info "Entry point for this package documentation."

This is the file that will be opened when the user wishes to click the `documentation` button
in `Mod Manager`.

This should be a file in a format the user can be reasonably expected to open on a `Windows` or `Linux` machine.

Currently accepted formats include:

- `HTML` (`.htm`, `.html`)
- `Markdown` (`.md`)
- `PDF` (`.pdf`)
- `Text` (`.txt`)

The entry point for the documentation is specified in the [DocsFile][docs-file] field in the `package.toml`.

### Images

!!! info "Located in `package/images`."

!!! info "Images use [JPEG XL (`.jxl`)][images]"

This contains any supplementary images that are used in the package.
These images can be referenced from the main `package.toml` file, for example in
[gallery items][gallery-items].

### License

!!! info "Located at `package/license.md`."

License defaults to [CC BY-NC-SA 4.0][cc-by-nc-sa-4.0].

## Design Philosophy

### Packages Should be Self Contained

For historical preservation, we should strive to make packages as 'self contained' as possible.

That means including the following in each package:

- A full description for each mod, as you'd find in a mod page.
- Documentation on how to use the mod, e.g. `mkdocs` website.
- Complete changelog for the mod (down to first version).

!!! note "A package does not need to contain assets for previous versions, only changelogs."

[cc-by-nc-sa-4.0]: https://creativecommons.org/licenses/by-nc-sa/4.0/
[docs-file]: ./Package-Metadata.md#docsfile
[gallery-items]: ./Configurations/Mod-Metadata.md#gallery
[images]: ../../Common/Images.md