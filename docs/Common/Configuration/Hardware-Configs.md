!!! info "Hardware settings are settings that are tied to your user."

    These are not carried as part of loadouts, but rather as part of the user/profile configuration.

!!! tip "To define hardware-specific settings, add an `[hardware]` section to the [config.toml][config-schema] file."

!!! warning "In some cases, hardware settings may not be available depending on OS."

    In those cases, you will be able to set settings for a 'generic' device, as fallback.
    Which settings this applies to will be specified with `HasFallback`.

## How are Hardware Settings Stored?

!!! info "Hardware Settings are tied to your user profile."

    These settings apply between all [Loadouts][loadouts].

To give an example of this, suppose you have a mod that gives you widescreen with a custom resolution
for a 2004 game (that was originally locked to 1024x768 and 4:3).

If you switch a Loadout, you would not want to reconfigure those settings all over again.

!!! warning "TODO: Document in [Game][games] section how this is stored."

## Monitor Settings

!!! info "This allows you to configure settings on a per-monitor basis."

!!! warning "Not all displays may support this."

    Over 95% will, but availability of these settings may depend on the OS and display connector used.

    - HasFallback: `yes`

You can add `monitor` specific settings under the `[[hardware.monitors]]` section.

Example:

```toml
[[hardware.monitors]]

[[hardware.monitors.settings]]
index = 32
type = "resolution_dropdown"
name = "RESOLUTION"
description = "Game resolution on this monitor"

[[hardware.monitors.settings]]
index = 33
type = "resolution_refresh_rate_dropdown"
name = "RESOLUTION_REFRESH_RATE"
description = "Resolution and refresh rate on this monitor"

[[hardware.monitors.settings]]
index = 34
type = "bool"
name = "ENABLE_BORDERLESS"
description = "Enable borderless mode on this monitor"
default = false
```

To uniquely identify a monitor, Reloaded3 settings use the `unique_id` field, which is bytes
8-15 of the monitor's EDID. That's manufacturer ID, product ID, and serial number.

!!! warning "Ensure that each setting has a unique `index` value."

    The settings defined under the monitor section are an extension of the regular settings.
    Therefore, they should have a unique `index` value.

### `resolution_dropdown` Setting

!!! info "A dropdown to select a specified resolution for the monitor."

Additional Fields:

| Field         | Type       | Description                                                                |
| ------------- | ---------- | -------------------------------------------------------------------------- |
| `resolutions` | Resolution | [Optional] Array of available resolutions, auto-populated from the monitor |

If `resolutions` is not provided, the available resolutions will be automatically queried from the monitor.

!!! tip "Use this for old games with a fixed delta time."

    i.e. Games that only run at 60fps and have physics tied to the frame rate.

### `resolution_refresh_rate_dropdown` Setting

!!! info "A dropdown to select a resolution and refresh rate combo for the monitor."

Additional Fields:

| Field                      | Type                  | Description                                                                                       |
| -------------------------- | --------------------- | ------------------------------------------------------------------------------------------------- |
| `resolution_refresh_rates` | ResolutionRefreshRate | [Optional] Array of available resolution and refresh rate combos, auto-populated from the monitor |

If `resolution_refresh_rates` is not provided, the available resolution and refresh rate combos
will be automatically queried from the monitor.

Users can also manually enter an arbitrary resolution or refresh rate value.

[config-schema]: ./Config-Schema.md
[loadouts]: ../../Server/Storage/Loadouts/About.md
[games]: ../../Server/Storage/Games/About.md