# Denuvo

Aside from obfuscating select game functions, generally Denuvo is
surprisingly the least intrusive modern DRM solution as far as loading mods is concerned.

All the pain is transferred to those making mods, be it waiting 30 hours for static analysis
to finish, or obfuscating the random game function.

That said, unlike something like SecuROM or SafeDisc, the original game isn't totally wrecked
all over the place.

## Detection

!!! info "Denuvo has an 'offline activation portal', in case your PC cannot connect to their servers."

This is a failsafe in case the game cannot connect to the Denuvo servers to verify the license.

By signature scanning for the domain `support.codefusion.technology` (usually UTF-16), you can verify
a game as Denuvo protected.

!!! note "Some extra optional steps"

    After that URL you get 4 bytes (unknown purpose) and (in all my samples) `01 00 00 00 66 66 66 2E 0F 1F 84 00 00 00 00 00`. 
    
    Following that is another null terminated string which contains the specific product ID. For example, in `Persona 5 Royal`, this is `P5R_9AG4H12`.

    Combine the two, you get `https://support.codefusion.technology/P5R_9AG4H12`. 

## Anti-Debugging Measures

!!! question "Some Denuvo titles have Anti-Debugging Measures"

    However it is unclear whether it is an optional Denuvo component or additional DRM from the publisher.

!!! info

    Some SEGA games circa 2017 featuring Denuvo also have an anti-debug measure where `ntdll.DbgUiRemoteBreakin` will
    constantly be rewritten with  `ret` (0xC3) on a background thread to prevent debugging.

    It is usually easy to patch. Known affected titles include Sonic Forces and Puyo Puyo Tetris.