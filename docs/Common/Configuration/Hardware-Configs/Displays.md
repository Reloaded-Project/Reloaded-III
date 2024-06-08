# Monitor Settings

!!! info "This allows you to configure settings on a per-monitor basis."

!!! warning "Not all displays may support this."

    Over 95% will, but availability of these settings may depend on the OS and display connector used.

    - HasFallback: `yes`

!!! info "We will use SDL for this"

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

If the EDID is not available, we will try [monitor_name][monitor-name], and lastly
[monitor_index][sdl-num-displays].

## `resolution_dropdown` Setting

!!! info "A dropdown to select a specified resolution for the monitor."

Additional Fields:

| Field         | Type       | Description                                                                |
| ------------- | ---------- | -------------------------------------------------------------------------- |
| `resolutions` | Resolution | [Optional] Array of available resolutions, auto-populated from the monitor |

If `resolutions` is not provided, the available resolutions will be automatically queried from the monitor.

!!! tip "Use this for old games with a fixed delta time."

    i.e. Games that only run at 60fps and have physics tied to the frame rate.

## `resolution_refresh_rate_dropdown` Setting

!!! info "A dropdown to select a resolution and refresh rate combo for the monitor."

Additional Fields:

| Field                      | Type                  | Description                                                                                       |
| -------------------------- | --------------------- | ------------------------------------------------------------------------------------------------- |
| `resolution_refresh_rates` | ResolutionRefreshRate | [Optional] Array of available resolution and refresh rate combos, auto-populated from the monitor |

If `resolution_refresh_rates` is not provided, the available resolution and refresh rate combos
will be automatically queried from the monitor.

Users can also manually enter an arbitrary resolution or refresh rate value.

[monitor-name]: https://wiki.libsdl.org/SDL2/SDL_GetDisplayName
[sdl-num-displays]: https://wiki.libsdl.org/SDL2/SDL_GetNumVideoDisplays