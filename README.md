# World In Conflict FPM tweaks

The initial state of the `ModKit` directory is a copy of all the *text* files
from the [World In Conflict ModKit][], as autodetected by the following command:

```
grep --recursive --files-with-matches --binary-files=without-match . .
```

This approach makes it possible to track modified files through Git.

[World In Conflict modkit]: https://www.massgate.org/downloads.php#modkitss

## Random notes and observations

### Unit type `RoleCost`

The `RoleCost` `myPriceType` doesn't just affect how the unit type icon is shown
in the buy menu - it also determines which buy menu tab it ends up in. If a
non-`FPM_ROLE` `RoleCost` has a `myPriceType` of `REBATE_REBATED` or
`REBATE_UNIQUE`, the unit will appear in the buy menu tab that corresponds to
`myRole`.
