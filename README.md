# remind

Create Apple Reminders from the command line.

## Usage

```
remind "Title"                 # no due time
remind "Title" 3pm             # today at 3pm (tomorrow if already past)
remind "Title" 14:30           # 24-hour format
remind "Title" +30m            # 30 minutes from now
remind "Title" +1h             # 1 hour from now
remind "Title" +1h30m          # 1 hour 30 minutes from now
remind "Title" in 45m          # same as +45m
remind "Title" tomorrow 9am    # tomorrow at 9am
```

Reminders are added to your default **Reminders** list. Absolute clock times roll to the next day if the time has already passed.

## Install

```sh
curl -fsSL https://raw.githubusercontent.com/LukeGeneva/remind/main/install.sh | bash
```

This downloads the latest binary from GitHub Releases and installs it to `/usr/local/bin/remind`.

**Build from source:**

```sh
make install
```

**Publish a new release:**

```sh
make release VERSION=1.0.0
```

## Development

Run tests:

```sh
pytest
```

Clean build artifacts:

```sh
make clean
```
