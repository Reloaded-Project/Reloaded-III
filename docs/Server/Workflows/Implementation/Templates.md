---
# YAML header
render_macros: false
---

!!! info "After Rhai scripts have executed, MiniJinja is used for the final template substitution step."

 All variables set during the workflow chain and modified by Rhai scripts are available for use in templates.

## Why MiniJinja?

!!! info "When looking for a suitable templating engine, I considered the following factors"

- **Familiar / Ease of use**:
    - [MiniJinja] has a syntax similar to Jinja2, which is widely used.
    - And [very strong documentation][minijinja-docs] for developers ([examples][minijinja-examples]).
    - And countless [cheat sheets]

- **Sandboxing**:
    - Each file generation must be isolated from the others.
    - Avoid arbitrary code execution if possible.

!!! warning "[MiniJinja] is not guaranteed to run on [esoteric platforms][esoteric-platforms]"

    It is not an `no_std` package, however it is modular and usage of `std` is limited, with the
    main library mostly uses types from `alloc` and `core`.

    Templating engines with `no_std` support are rare (unfortunately), however `MiniJinja` is
    known to run with WASM, which is a good sign, especially given `WASM` can't use filesystem
    and is thus limited.

## Template Files

!!! info "Template files are specified in the [workflow.toml] file under the [`[metadata]`][metadata] section"


```toml
[metadata]
# ... other metadata ...
files = [
    "templates/package.toml"
]
```

These files will have their contents processed by MiniJinja, with the resulting output being
written to the final mod package.

## Localization in Templates

!!! info "Localization keys defined in the language files are available as variables for rendering in templates."

    This is also true for `variables` created in [`metadata`][schema] and [`rhai scripts`][rhai-scripts]!

This feature allows for complete translation of template outputs, making it possible to generate
fully localized mod configurations and documentation.

### Accessing Localization Keys

Localization keys can be accessed directly as variables in your templates.
This is based on the [`localization keys`][metadata-localization] used in the workflow.

=== "MiniJinja"
    ```jinja2
    {{ WORKFLOW_NAME }}
    {{ SETTING_STAGE_NAME }}
    ```

=== "Rendered Output (English)"
    ```
    Create or Replace a Stage
    Stage Name
    ```

=== "Rendered Output (Japanese)"
    ```
    ステージの作成または置換
    ステージ名
    ```

### Example: Fully Localized Template

Here's an example of how you might use localization keys to create a fully localizable mod description:

=== "MiniJinja"
    ```jinja2
    # {{ MOD_NAME }}

    {{ MOD_DESCRIPTION }}

    ## {{ FEATURES_HEADER }}

    {% for feature in features %}
    - {{ feature }}
    {% endfor %}

    ## {{ INSTALLATION_HEADER }}

    {{ INSTALLATION_INSTRUCTIONS }}

    ## {{ COMPATIBILITY_HEADER }}

    {{ COMPATIBILITY_INFO }}
    ```

=== "Rendered Output (English)"
    ```markdown
    # Super Speed Mod

    This mod enhances your character's speed, allowing for faster gameplay and
    new speedrunning strategies.

    ## Features

    - Increased running speed
    - Improved acceleration
    - Adjustable speed multiplier

    ## Installation

    1. Download the mod file.
    2. Place it in your game's mod folder.
    3. Activate the mod in the Reloaded3 launcher.

    ## Compatibility

    This mod is compatible with Sonic Heroes version 1.0 and above.
    It may conflict with other mods that alter character speed.
    ```

=== "Rendered Output (Japanese)"
    ```markdown
    # スーパースピードMod

    このModはキャラクターの速度を向上させ、より速いゲームプレイと新しいス
    ピードラン戦略を可能にします。

    ## 特徴

    - 走る速度の増加
    - 加速度の改善
    - 調整可能な速度倍率

    ## インストール方法

    1. Modファイルをダウンロードします。
    2. ゲームのModフォルダに配置します。
    3. Reloaded3ランチャーでModを有効にします。

    ## 互換性

    このModはソニックヒーローズバージョン1.0以上と互換性があります。キャラ
    クターの速度を変更する他のModと競合する可能性があります。
    ```

!!! tip "Use localization keys if you have further instructions after a template finishes rendering"

    This way you can ensure that any further manual instructions that a user needs to perform are
    also localized. For example, links to further guidance how to work with the data.

## Cheat Sheet

!!! info "This cheat sheet provides a quick reference for Jinja syntax"

    Along with Reloaded3-themed examples and their rendered output.

!!! tip "The MiniJinja templates can access all `variables` created in [`metadata`][schema], [`localization`][metadata-localization] and [`rhai scripts`][rhai-scripts]."

### Basic Syntax

#### Variable

=== "MiniJinja"
    ```jinja2
    {{ mod_name }}
    ```

=== "Rendered Output"
    ```
    Super Speed Mod
    ```
    Assuming `mod_name = "Super Speed Mod"`

#### Comment

=== "MiniJinja"
    ```jinja2
    {# This mod increases the player's speed #}
    ```

=== "Rendered Output"
    ```

    ```
    (Comments are not rendered in the output)

### Control Structures

#### For Loop

=== "MiniJinja"
    ```jinja2
    {% for stage in stages %}
        {{ stage.name }}: {{ stage.difficulty }}
    {% endfor %}
    ```

=== "Rendered Output"
    ```
    Green Hill: Easy
    Chemical Plant: Medium
    ```
    Assuming `stages = [{"name": "Green Hill", "difficulty": "Easy"}, {"name": "Chemical Plant", "difficulty": "Medium"}]`

#### If Statement

=== "MiniJinja"
    ```jinja2
    {% if mod_type == "gameplay" %}
        This mod affects gameplay mechanics.
    {% elif mod_type == "visual" %}
        This mod changes visual elements.
    {% else %}
        This mod type is undefined.
    {% endif %}
    ```

=== "Rendered Output (gameplay)"
    ```
    This mod affects gameplay mechanics.
    ```
    Assuming `mod_type = "gameplay"`

=== "Rendered Output (visual)"
    ```
    This mod changes visual elements.
    ```
    Assuming `mod_type = "visual"`

=== "Rendered Output (other)"
    ```
    This mod type is undefined.
    ```
    Assuming `mod_type` is neither "gameplay" nor "visual"

#### Block

=== "MiniJinja"
    ```jinja2
    {% block mod_description %}
        This mod enhances the game experience.
    {% endblock %}
    ```

=== "Rendered Output"
    ```
    This mod enhances the game experience.
    ```

#### Include

=== "MiniJinja"
    ```jinja2
    {% include "mod_header.txt" %}
    ```

=== "Rendered Output"
    ```
    (The content of mod_header.txt would be inserted here)
    ```

#### Set

=== "MiniJinja"
    ```jinja2
    {% set mod_version = "1.2.0" %}
    Mod Version: {{ mod_version }}
    ```

=== "Rendered Output"
    ```
    Mod Version: 1.2.0
    ```

#### Filter

=== "MiniJinja"
    ```jinja2
    {% filter upper %}
        This mod is compatible with Sonic Heroes.
    {% endfilter %}
    ```

=== "Rendered Output"
    ```
    THIS MOD IS COMPATIBLE WITH SONIC HEROES.
    ```

### Expressions

#### Math

=== "MiniJinja"
    ```jinja2
    Speed Multiplier: {{ 1.5 * 2 }}
    ```

=== "Rendered Output"
    ```
    Speed Multiplier: 3.0
    ```

#### String concatenation

!!! info "Adding two pieces of text together."

=== "MiniJinja"
    ```jinja2
    {{ "Mod by: " ~ author_name }}
    ```

=== "Rendered Output"
    ```
    Mod by: JohnDoe
    ```
    Assuming `author_name = "JohnDoe"`

#### Comparisons

=== "MiniJinja"
    ```jinja2
    Is Advanced Mod: {{ mod_complexity > 5 }}
    ```

=== "Rendered Output"
    ```
    Is Advanced Mod: true
    ```
    Assuming `mod_complexity = 7`

#### Logic

=== "MiniJinja"
    ```jinja2
    {{ is_gameplay_mod and is_reloaded_compatible or is_standalone }}
    ```

=== "Rendered Output"
    ```
    true
    ```
    Assuming `is_gameplay_mod = true`, `is_reloaded_compatible = true`, `is_standalone = false`

### Filters

#### Uppercase

=== "MiniJinja"
    ```jinja2
    {{ mod_name|upper }}
    ```

=== "Rendered Output"
    ```
    SUPER SPEED MOD
    ```
    Assuming `mod_name = "super speed mod"`

#### Length

=== "MiniJinja"
    ```jinja2
    Number of supported games: {{ supported_games|length }}
    ```

=== "Rendered Output"
    ```
    Number of supported games: 3
    ```
    Assuming `supported_games = ["Sonic Heroes", "Sonic Adventure 2", "Sonic Generations"]`

#### Default value

=== "MiniJinja"
    ```jinja2
    Mod Category: {{ mod_category|default('Uncategorized') }}
    ```

=== "Rendered Output (with default)"
    ```
    Mod Category: Uncategorized
    ```
    Assuming `mod_category` is not defined

=== "Rendered Output (with value)"
    ```
    Mod Category: Gameplay
    ```
    Assuming `mod_category = "Gameplay"`

#### Join

=== "MiniJinja"
    ```jinja2
    Required Mods: {{ required_mods|join(', ') }}
    ```

=== "Rendered Output"
    ```
    Required Mods: Base Mod, Config Library, Input Hook
    ```
    Assuming `required_mods = ["Base Mod", "Config Library", "Input Hook"]`

### Notes

- MiniJinja doesn't support line statements or custom delimiters by default.
- Python-specific methods (like `.items()`) are not supported. Use `|items` filter instead.
- Tuples are treated as lists.
- Keyword arguments in filters are passed as a dictionary.
- `*args` and `**kwargs` syntax is not supported.
- The `{% continue %}` and `{% break %}` statements are not supported in loops.

[esoteric-platforms]: ../../../Code-Guidelines/Hardware-Requirements.md#about-esoteric-and-experimental-platforms
[MiniJinja]: https://lib.rs/crates/minijinja
[minijinja-docs]: https://docs.rs/minijinja/latest/minijinja/
[minijinja-usage]: https://docs.rs/minijinja/latest/minijinja/
[minijinja-examples]: https://github.com/mitsuhiko/minijinja/tree/main/examples
[workflow.toml]: ./Schema.md
[metadata]: ./Schema.md#metadata-section
[metadata-localization]: ./Schema.md#localization
[rhai-scripts]: ./Scripting.md
[schema]: ./Schema.md