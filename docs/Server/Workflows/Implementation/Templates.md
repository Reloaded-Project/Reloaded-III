!!! info "After Rhai scripts have executed, MiniJinja is used for the final template substitution step."

 All variables set during the workflow chain and modified by Rhai scripts are available for use in templates.

## Template Files

Template files are specified in the `workflow.toml` file under the `[metadata]` section:

```toml
[metadata]
# ... other metadata ...
files = [
    "templates/package.toml",
    "templates/stage_config.txt"
]
```

These files will have their contents processed by MiniJinja, with the resulting output being
written to the final mod package.

## Template Syntax

MiniJinja uses a syntax similar to Jinja2. Here are some basic examples:

```jinja
// Variable substitution
Stage Name: {{ stage_name }}

// Conditionals
{% if difficulty == "Hard" %}
This is a challenging stage!
{% endif %}

// Loops
Available zones:
{% for zone in zones %}
- {{ zone }}
{% endfor %}

// Filters
Lowercase stage name: {{ stage_name | lower }}
```