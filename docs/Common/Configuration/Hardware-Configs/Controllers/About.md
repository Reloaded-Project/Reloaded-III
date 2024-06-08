# Gamepad Bindings and Settings

!!! info "This allows you to configure gamepad bindings and settings on a per-controller basis."

    This functionality is based on SDL2 and the GameController API.

    Users should expect controllers to therefore work out of the box.

You can add gamepad binding settings under the `[[hardware.gamepads.bindings]]` section and
per-controller settings under the `[[hardware.gamepads.settings]]` section.

!!! note "Gamepads are serialized into a separate binary file"

    This can be used outside of Reloaded3.

    Therefore in settings, a single index is used to refer to a gamepad.

## Requirements

!!! info "In addition to those in [Hardware Settings][hw-requirements]"

### Per Controller Settings

!!! info "Some 'global' settings should be scoped per-controller."

For example, a user may want to swap out a controller for another, but keep the same bindings.

Therefore they should be able to configure things like 'global stick radius' separately of
each set of bindings.

### Must be Usable outside of [config.toml][config-toml]

!!! info "In case an external program wants to use the code."

## Sections

!!! tip "In reading order."

| Section                              | Description                                         |
| ------------------------------------ | --------------------------------------------------- |
| [Config-Schema.md](Config-Schema.md) | The available settings in controller config.        |
| [Binary-Format.md](Binary-Format.md) | How the controller settings are serialized to file. |

[hw-requirements]: ../About.md#requirements
[config-toml]: ../../Config-Schema.md