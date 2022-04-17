# World In Conflict FPM tweaks

The initial state of the `ModKit` directory is a copy of all the *text* files
from the [World In Conflict ModKit][], as autodetected by the following command:

```
grep --recursive --files-with-matches --binary-files=without-match . .
```

This approach makes it possible to track modified files through Git.

[World In Conflict modkit]: https://www.massgate.org/downloads.php#modkit
