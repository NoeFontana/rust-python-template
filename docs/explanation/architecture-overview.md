# Architecture overview

<!-- TODO: Why the project is split into three layers rather than one — what
`-core` buys by forbidding unsafe and refusing to link libpython, why `-ffi`
is conversion-only and `publish = false`, and why the Python wrapper exists at
all rather than exposing `._core` directly. Also: why abi3, and what that
commits the project to. Understanding-oriented: no steps, no API listings.
Link to the records in `docs/adr/` rather than restating their reasoning. -->
