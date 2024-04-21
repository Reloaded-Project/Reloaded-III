# Adding Localisations

!!! info "This page describes how localisations are added to a Reloaded3 component."

Such as a mod, utility, etc.

## Where to Add Localisations

!!! info "Within a given package, localisations are usually expected to be found in the `languages` folder."

```
reloaded3.utility.examplemod.s56
├── languages
│   ├── en-GB.toml
│   └── uwu.toml
├── config.toml
└── package.toml
```

Here the languages are:

- `en-GB.toml` (English, British)
- `uwu-en.toml` (`UwU`, English)

### Multiple Package Components

!!! tip "Some packages may have multiple localizable components."

For example, a localisable config and `DLL` code loaded at runtime.

```
reloaded3.utility.examplemod.s56
├── languages
│   ├── config
│   │   ├── en-GB.toml
│   │   └── uwu.toml
│   └── dll
│       ├── en-GB.toml
│       └── uwu.toml
├── config.toml
├── mod.dll
└── package.toml
```

In this case, translations may be split into separate folders:

- `mod.dll` will reference the languages from `languages/dll`
- `config.toml` will reference the languages from `languages/config`

## Language Naming Convention

!!! info "Describes the format in which common languages are named."

We name the files with `.toml` for purposes of syntax highlighting.

### Shorthand

Localisations can use one of the following file name convention:

```
{iso639}.toml
```

Where `{iso639}` is the [two letter ISO 639 language code][iso-lang-code].

Example: `en.toml` (English).

### Longhand

Alternatively, you can use more specific culture names

```
{iso639}-{iso3166alpha2}.toml
```

Where `{iso3166alpha2}` is the [two letter ISO 3166 alpha-2 country code][iso3166-alpha2].

Example:

- `en-GB.toml` (English, British)
- `en-US.toml` (English, American)

### Language Inheritance

!!! info "For languages using the 'standard' naming convention, the country code will inherit from the language code."

If the user sets `en-GB.toml` as their preferred language, and a mod only has `en.toml`, available,
then `en.toml` will still be loaded, as the language is still 'English'.

### Other Languages

For languages that are 'stylistic', or simply 'for fun', you can use the following format:

```
{style}-{iso639}.toml
```

Example: `uwu-en.toml` (`UwU`, English).

## Sideloading Translations

!!! tip "Reloaded3 packages can provide translations for elements in other packages."

It's possible to create 3rd party `translation` packages that add additional translations
to existing packages.

```
reloaded3.utility.examplemod.s56.de
├── language-overrides
│   └── reloaded3.utility.examplemod.s56
│       └── de-DE.toml
└── package.toml
```

The following steps are required:

- Specify the `PackageType` as `Translation` in the [`package.toml` file][package-type].
- Then Add a `language-overrides/{id-of-translated-packages}` folder to the package.
- Add individual `.toml` translation files for each language.

In this case, the language `de-DE.toml` will be added to the `reloaded3.utility.examplemod.s56`
package.

!!! note "If multiple mods override or add the same language, the last one wins."

!!! warning "For consistency, package versions of `Translations` should be equal to the original mod version(s) translated."

### Overriding Specific Components

!!! tip "The `language-overrides` folder directly overlays the original `languages` folder."

If the package has [multiple components](#multiple-package-components), the folders work in an
'overlay' fashion.

```
reloaded3.utility.examplemod.s56.de
├── languages
│   └── reloaded3.utility.examplemod.s56
│       ├── config
│       │   └── de-DE.toml
│       └── dll
│           └── de-DE.toml
└── package.toml
```

This would add a German translation to both the config and the DLL.

[iso-lang-code]: https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes
[iso3166-alpha2]: https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2
[package-type]: ../../Server/Packaging/Package-Metadata.md#packagetype