# Loading Localisations

!!! info "How things should look from an library consumer's point of view."

Psuedocode:

```rust
// Get the localiser utility.
let localiser = load_localisation("languages/dll/en-GB.toml")
```

This should load the language `en-GB.toml` as the default, base language.

Once this is done, the user's preferred languages should then automatically be loaded ontop of this,
replacing all known text.

## Language Load Order

!!! note "The user may set multiple languages as their 'preferred' languages."

    In this scenario, the languages 'stack' like layers, same way mods do.

If the user's preference is the following:

1. `uwu-en.toml` (`UwU`, English)
2. `fr-FR.toml` (French, France)

Then when you call `load_localisation`, languages will be loaded in the following order:

1. `en-GB.toml` (Default Language)
2. `fr-FR.toml` (Second Preference)
3. `uwu-en.toml` (First Preference)

Keys from next file replace last file.

So what will happen, is if `UwU` does not have a translation for a given key, it will fall back to
`French`, and then `English`.

## Language Specific Notes

### C\#

!!! info "If you are doing front-end work, consider also changing the locale of the current thread."

```csharp
// Forces British Date, Time, Number etc. formatting.
Thread.CurrentThread.CurrentUICulture = new CultureInfo("en-GB");
```

i.e. if you're loading `en-GB.toml`, you should also set the locale to `en-GB`.