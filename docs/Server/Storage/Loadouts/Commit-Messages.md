!!! info "This is a full list of [Commit Messages][commit-messages] for each event in [events.bin][events-bin]"

## 00: PackageAdded

!!! info "Source: Event [0x00: PackageStatusChanged][event-00]"

```
Added Package {} with version {}.
```

## 01: PackageRemoved

!!! info "Source: Event [0x00: PackageStatusChanged][event-00]"

```
Removed Package {}.
```

## 02: PackageHidden

!!! info "Source: Event [0x00: PackageStatusChanged][event-00]"

```
Hid Package {} from view.
```

## 03: PackageDisabled

!!! info "Source: Event [0x00: PackageStatusChanged][event-00]"

```
Disabled Package {}.
```

## 04: PackageEnabled

!!! info "Source: Event [0x00: PackageStatusChanged][event-00]"

```
Enabled Package {}.
```

## 05: GameLaunched

!!! info "Invoked by [Event 0x01: GameLaunched][game-launched]"

```
Launched game at {}.
```

## 06: ConfigUpdated

!!! info "Invoked by [Event 0x02: ConfigUpdated][event-02]"

```
Updated configuration for Package {}.
```

## 07: LoadoutGridEnabledSortModeChanged

!!! info "Invoked by [Event 0x03: LoadoutDisplaySettingChanged][event-03]"

```
Changed enabled package sort mode to {}.
```

## 08: LoadoutGridDisabledSortModeChanged

!!! info "Invoked by [Event 0x03: LoadoutDisplaySettingChanged][event-03]"

```
Changed disabled package sort mode to {}.
```

## 09: ModLoadOrderSortChanged

!!! info "Invoked by [Event 0x03: LoadoutDisplaySettingChanged][event-03]"

```
Changed mod load order sort to {}.
```

## 10: LoadoutGridStyleChanged

!!! info "Invoked by [Event 0x03: LoadoutDisplaySettingChanged][event-03]"

```
Changed loadout grid style to {}.
```

[commit-messages]: ../Loadouts/About.md#commit-msgbin
[events-bin]: ../Loadouts/About.md#eventsbin
[event-00]: ./Events.md#00-packagestatuschanged
[event-02]: ./Events.md#02-configupdated
[event-03]: ./Events.md#04-loadoutdisplaysettingchanged
[game-launched]: ./Events.md#01-gamelaunched