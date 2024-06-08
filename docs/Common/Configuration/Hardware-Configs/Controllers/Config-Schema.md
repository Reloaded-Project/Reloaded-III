An Example:

```toml
[[hardware.gamepads]]
# This is the index for config.toml
index = 40

[[hardware.gamepads.bindings]]
# Bindings have their own 'scope' so the index should reset to 0.
index = 0
type = "gamepad_action_button"
name = "GAMEPAD_ACTION_JUMP"
description = "GAMEPAD_ACTION_JUMP_DESC"
default_bindings = [
    { controller_index = 0, type = "button", value = "SDL_GAMEPAD_BUTTON_A" },
    { controller_index = 1, type = "button", value = "SDL_GAMEPAD_BUTTON_A" },
    { controller_index = 0, type = "axis", value = "SDL_GAMEPAD_AXIS_RIGHT_TRIGGER", threshold = 0.5, comparison = "greater_than_or_equal" },
    { controller_index = 1, type = "hat", value = "SDL_HAT_UP" }
]

[[hardware.gamepads.bindings]]
index = 1
type = "gamepad_action_button"
name = "GAMEPAD_ACTION_FIRE"
description = "GAMEPAD_ACTION_FIRE_DESC"
default_bindings = [
    { controller_index = 0, type = "button", value = "SDL_GAMEPAD_BUTTON_RIGHT_SHOULDER" },
    { controller_index = 1, type = "button", value = "SDL_GAMEPAD_BUTTON_B" }
]

[[hardware.gamepads.bindings]]
index = 2
type = "gamepad_action_axis"
name = "GAMEPAD_ACTION_MOVE_X"
description = "GAMEPAD_ACTION_MOVE_X_DESC"
default_bindings = [
    { controller_index = 0, type = "axis", value = "SDL_GAMEPAD_AXIS_LEFTX", deadzone = 0.2, radius = 1.0 },
    { controller_index = 1, type = "button", value = "SDL_GAMEPAD_BUTTON_DPAD_RIGHT", scale = 0.5 },
    { controller_index = 1, type = "button", value = "SDL_GAMEPAD_BUTTON_DPAD_LEFT", scale = -0.5 }
]

[[hardware.gamepads.bindings]]
index = 3
type = "gamepad_action_button"
name = "GAMEPAD_ACTION_BOOST"
description = "GAMEPAD_ACTION_BOOST_DESC"
default_bindings = [
    { controller_index = 0, type = "axis", value = "SDL_GAMEPAD_AXIS_LEFTX", threshold = -0.5, comparison = "less_than_or_equal" }
]

# Settings using `config.toml` schema
# These settings are saved `per-controller`.

[[hardware.gamepads.settings]]
# These have their own 'scope', so the index should reset to 0.
index = 0
type = "float_range"
name = "GAMEPAD_VIBRATION_STRENGTH"
description = "GAMEPAD_VIBRATION_STRENGTH_DESC"
min = 0.0
max = 1.0
step = 0.1
default = 0.7
labels = ["LABEL_NONE", "LABEL_MAX"]

[[hardware.gamepads.settings]]
index = 1
type = "float_range"
name = "GAMEPAD_TRIGGER_SENSITIVITY"
description = "GAMEPAD_TRIGGER_SENSITIVITY_DESC"
min = 0.1
max = 0.9
step = 0.05
default = 0.5
labels = ["LABEL_LOW", "LABEL_HIGH"]

[[hardware.gamepads.settings]]
index = 2
type = "float_range"
name = "GAMEPAD_STICK_SENSITIVITY"
description = "GAMEPAD_STICK_SENSITIVITY_DESC"
min = 0.5
max = 2.0
step = 0.1
default = 1.0

[[hardware.gamepads.settings]]
index = 3
type = "bool"
name = "GAMEPAD_INVERT_Y_AXIS"
description = "GAMEPAD_INVERT_Y_AXIS_DESC"
default = false

[[hardware.gamepads.settings]]
index = 4
type = "bool"
name = "GAMEPAD_SWAP_STICKS"
description = "GAMEPAD_SWAP_STICKS_DESC"
default = false
```

!!! note "When using outside of [config.toml][config-schema], drop the `hardware` prefix."

    For example, `[[hardware.gamepads]]` becomes `[[gamepads]]`.

Gamepads are uniquely identified by their `controller_index`, which is specific to SDL.

!!! note "The index of `[[hardware.gamepads]]` corresponds to the index in [config.toml][config-schema]."

    This allows for easy reference to the gamepad settings.

    The `index` inside each binding under `[[hardware.gamepads.bindings]]` is unique to the gamepad
    bindings and is used to identify the binding within the binary schema.

    The `index` inside each setting under `[[hardware.gamepads.settings]]` follows the
    regular config schema defined in `config-schema.md` (config.toml).

    It is separately scoped however, so should reset to 0.

!!! warning "Ensure that each binding and setting has a unique `index` value within their respective sections."

    The bindings defined under the `[[hardware.gamepads.bindings]]` section have their own unique
    `index` values, separate from the regular config settings.

    The settings defined under the `[[hardware.gamepads.settings]]` section follow the regular
    config schema and should have unique `index` values within the context of all config settings.

## `gamepad_action_button` Setting

!!! info "A setting to bind a game action button to one or more gamepad inputs (buttons, axes, or hats) across multiple controllers."

Fields:

| Field              | Type  | Description                                         |
| ------------------ | ----- | --------------------------------------------------- |
| `default_bindings` | array | An array of default bindings for the action button. |

Each binding in the `default_bindings` array has the following fields:

| Field              | Type   | Description                                                                                                                                     |
| ------------------ | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `controller_index` | int    | The index of the gamepad to which the binding applies.                                                                                          |
| `type`             | string | The type of the binding: `"button"`, `"axis"`, or `"hat"`.                                                                                      |
| `value`            | string | The value of the binding (e.g., `"SDL_GAMEPAD_BUTTON_A"`, `"SDL_GAMEPAD_AXIS_LEFTX"`).                                                          |
| `threshold`        | float  | [Optional] The threshold value for axis bindings to trigger the action (default: 0.0, range: -1.0 to 1.0).                                      |
| `comparison`       | string | [Optional] The comparison operator for axis bindings: `"greater_than_or_equal"` or `"less_than_or_equal"` (default: `"greater_than_or_equal"`). |

## `gamepad_action_axis` Setting

!!! info "A setting to bind a game action axis to one or more gamepad inputs (buttons or axes) across multiple controllers."

Fields:

| Field              | Type  | Description                                       |
| ------------------ | ----- | ------------------------------------------------- |
| `default_bindings` | array | An array of default bindings for the action axis. |

Each binding in the `default_bindings` array has the following fields:

| Field              | Type   | Description                                                                            |
| ------------------ | ------ | -------------------------------------------------------------------------------------- |
| `controller_index` | int    | The index of the gamepad to which the binding applies.                                 |
| `type`             | string | The type of the binding: `"button"` or `"axis"`.                                       |
| `value`            | string | The value of the binding (e.g., `"SDL_GAMEPAD_BUTTON_A"`, `"SDL_GAMEPAD_AXIS_LEFTX"`). |
| `deadzone`         | float  | [Optional] The deadzone value for axis bindings (default: 0.2, range: 0.0 to 1.0).     |
| `radius`           | float  | [Optional] The radius value for axis bindings (default: 1.0, range: 0.0 to 1.0).       |
| `scale`            | float  | [Optional] The scale value for button bindings to emulate an axis (default: 1.0).      |

Users can customize the bindings for each action button and action axis and assign them to multiple
controllers using the Reloaded3 configuration interface.

This allows for flexibility in input mapping, such as jumping with either the first or second controller.

## Controller-Specific Settings

!!! info "You can define per-controller settings, using the [config.toml][config-schema] format."

    Do note that this acts as a 'nested file', and is scoped to this controller.

    So the index should be reset to 0.

### Vibration Strength

```toml
[[hardware.gamepads.settings]]
index = 0
type = "float_range"
name = "GAMEPAD_VIBRATION_STRENGTH"
description = "GAMEPAD_VIBRATION_STRENGTH_DESC"
min = 0.0
max = 1.0
step = 0.1
default = 0.7
labels = ["LABEL_NONE", "LABEL_MAX"]
```

This setting allows users to adjust the vibration strength of the controller. The value ranges from 0.0 (no vibration) to 1.0 (maximum vibration).

### Trigger Sensitivity

```toml
[[hardware.gamepads.settings]]
index = 1
type = "float_range"
name = "GAMEPAD_TRIGGER_SENSITIVITY"
description = "GAMEPAD_TRIGGER_SENSITIVITY_DESC"
min = 0.1
max = 0.9
step = 0.05
default = 0.5
labels = ["LABEL_LOW", "LABEL_HIGH"]
```

This setting adjusts the sensitivity of the trigger buttons. A lower value makes the triggers more sensitive, while a higher value requires more pressure to activate the triggers.

### Stick Sensitivity

```toml
[[hardware.gamepads.settings]]
index = 2
type = "float_range"
name = "GAMEPAD_STICK_SENSITIVITY"
description = "GAMEPAD_STICK_SENSITIVITY_DESC"
min = 0.5
max = 2.0
step = 0.1
default = 1.0
```

This setting adjusts the sensitivity of the analog sticks. A lower value makes the sticks less sensitive, while a higher value makes them more responsive.

### Invert Y-Axis

```toml
[[hardware.gamepads.settings]]
index = 3
type = "bool"
name = "GAMEPAD_INVERT_Y_AXIS"
description = "GAMEPAD_INVERT_Y_AXIS_DESC"
default = false
```

This boolean setting allows users to invert the Y-axis of the analog sticks. When enabled, pushing the stick up will result in downward movement, and vice versa.

### Swap Sticks

```toml
[[hardware.gamepads.settings]]
index = 4
type = "bool"
name = "GAMEPAD_SWAP_STICKS"
description = "GAMEPAD_SWAP_STICKS_DESC"
default = false
```

This boolean setting allows users to swap the functionality of the left and right analog sticks. When enabled, the left stick will control camera movement, and the right stick will control character movement.

## Available Gamepad Bindings

!!! info "The following gamepad bindings are available"

| Binding                             | Description                               | Value |
| ----------------------------------- | ----------------------------------------- | ----- |
| `SDL_GAMEPAD_BUTTON_A`              | The A button on the gamepad.              | 0     |
| `SDL_GAMEPAD_BUTTON_B`              | The B button on the gamepad.              | 1     |
| `SDL_GAMEPAD_BUTTON_X`              | The X button on the gamepad.              | 2     |
| `SDL_GAMEPAD_BUTTON_Y`              | The Y button on the gamepad.              | 3     |
| `SDL_GAMEPAD_BUTTON_BACK`           | The Back button on the gamepad.           | 4     |
| `SDL_GAMEPAD_BUTTON_GUIDE`          | The Guide button on the gamepad.          | 5     |
| `SDL_GAMEPAD_BUTTON_START`          | The Start button on the gamepad.          | 6     |
| `SDL_GAMEPAD_BUTTON_LEFT_STICK`     | The Left Stick button on the gamepad.     | 7     |
| `SDL_GAMEPAD_BUTTON_RIGHT_STICK`    | The Right Stick button on the gamepad.    | 8     |
| `SDL_GAMEPAD_BUTTON_LEFT_SHOULDER`  | The Left Shoulder button on the gamepad.  | 9     |
| `SDL_GAMEPAD_BUTTON_RIGHT_SHOULDER` | The Right Shoulder button on the gamepad. | 10    |
| `SDL_GAMEPAD_BUTTON_DPAD_UP`        | The D-Pad Up button on the gamepad.       | 11    |
| `SDL_GAMEPAD_BUTTON_DPAD_DOWN`      | The D-Pad Down button on the gamepad.     | 12    |
| `SDL_GAMEPAD_BUTTON_DPAD_LEFT`      | The D-Pad Left button on the gamepad.     | 13    |
| `SDL_GAMEPAD_BUTTON_DPAD_RIGHT`     | The D-Pad Right button on the gamepad.    | 14    |

| Binding                          | Description                            | Value |
| -------------------------------- | -------------------------------------- | ----- |
| `SDL_GAMEPAD_AXIS_LEFTX`         | The Left Stick X-axis on the gamepad.  | 0     |
| `SDL_GAMEPAD_AXIS_LEFTY`         | The Left Stick Y-axis on the gamepad.  | 1     |
| `SDL_GAMEPAD_AXIS_RIGHTX`        | The Right Stick X-axis on the gamepad. | 2     |
| `SDL_GAMEPAD_AXIS_RIGHTY`        | The Right Stick Y-axis on the gamepad. | 3     |
| `SDL_GAMEPAD_AXIS_LEFT_TRIGGER`  | The Left Trigger axis on the gamepad.  | 4     |
| `SDL_GAMEPAD_AXIS_RIGHT_TRIGGER` | The Right Trigger axis on the gamepad. | 5     |

| Binding         | Description                       | Value |
| --------------- | --------------------------------- | ----- |
| `SDL_HAT_UP`    | The Up direction on the D-Pad.    | 0     |
| `SDL_HAT_DOWN`  | The Down direction on the D-Pad.  | 1     |
| `SDL_HAT_LEFT`  | The Left direction on the D-Pad.  | 2     |
| `SDL_HAT_RIGHT` | The Right direction on the D-Pad. | 3     |

## Examples

Here are a few examples to illustrate the usage of the gamepad bindings:

### Jumping with a button, trigger, or D-Pad up

```toml
[[hardware.gamepads.settings]]
index = 40
type = "gamepad_action_button"
name = "GAMEPAD_ACTION_JUMP"
description = "GAMEPAD_ACTION_JUMP_DESC"
default_bindings = [
    { controller_index = 0, type = "button", value = "SDL_GAMEPAD_BUTTON_A" },
    { controller_index = 1, type = "button", value = "SDL_GAMEPAD_BUTTON_A" },
    { controller_index = 0, type = "axis", value = "SDL_GAMEPAD_AXIS_RIGHT_TRIGGER", threshold = 0.5, comparison = "greater_than_or_equal" },
    { controller_index = 1, type = "hat", value = "SDL_HAT_UP" }
]
```

The jump action can be triggered by:
- Pressing the A button on either the first or second controller
- Pulling the right trigger past the 50% threshold on the first controller
- Pressing up on the D-Pad on the second controller.

### Moving character along the X-axis (left-right)

```toml
[[hardware.gamepads.bindings]]
index = 2
type = "gamepad_action_axis"
name = "GAMEPAD_ACTION_MOVE_X"
description = "GAMEPAD_ACTION_MOVE_X_DESC"
default_bindings = [
    { controller_index = 0, type = "axis", value = "SDL_GAMEPAD_AXIS_LEFTX", deadzone = 0.2, radius = 1.0 },
    { controller_index = 1, type = "button", value = "SDL_GAMEPAD_BUTTON_DPAD_RIGHT", scale = 0.5 },
    { controller_index = 1, type = "button", value = "SDL_GAMEPAD_BUTTON_DPAD_LEFT", scale = -0.5 }
]
```

- Pressing Left on the D-Pad on the second controller will simulate a Left stick tilt of 50%.
- Pressing Right on the D-Pad on the second controller will simulate a Right stick tilt of 50%.
- The left stick on the first controller will behave as a regular left stick.

### Triggering a boost action by tilting the left stick to the left

```toml
[[hardware.gamepads.bindings]]
index = 3
type = "gamepad_action_button"
name = "GAMEPAD_ACTION_BOOST"
description = "GAMEPAD_ACTION_BOOST_DESC"
default_bindings = [
    { controller_index = 0, type = "axis", value = "SDL_GAMEPAD_AXIS_LEFTX", threshold = -0.5, comparison = "less_than_or_equal" }
]
```

This example shows how to trigger an action button by tilting the left stick to the left past the
-0.5 threshold on the first controller.

## Dealing with Disconnecting Controllers

!!! info "Usually at runtime it's not possible to know if a re-connected controller is the same as the disconnected one."

According to questions [such as this one][sdl-discourse-guid], it's not possible to know if a
re-connected controller is the same as a disconnected one.

Therefore we will take the following approach if a controller disconnects:

- First new `connected` controller that is currently not in use will be assigned to the `disconnected` player slot.

This allows someone to, for example, switch between 2 controllers (e.g. XBOX to PS) without having
to re-assign the controller.

### If a GUI is available

!!! info "If we're able to render a user interface, pause the game."

    For example, via `Dear ImGui`.

And tell the player explicitly the controller has been disconnected.

They can then press a button on the screen to re-assign the controller.

Re-assigning works by pressing any button on controller once the button to start the process has begun.

[config-schema]: ../../Config-Schema.md
[sdl-discourse-guid]: https://discourse.libsdl.org/t/basic-design-using-sdl-with-joysticks-that-come-and-go-during-runtime-fwd/22803