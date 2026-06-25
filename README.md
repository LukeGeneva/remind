# remind

Create Apple Reminders from the command line.

## Requirements

- macOS (uses AppleScript)
- Python 3.8+

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

**Quick (script, no binary):**

```sh
chmod +x remind.py
sudo cp remind.py /usr/local/bin/remind
```

**Signed binary via PyInstaller** (required for Gatekeeper on other machines):

```sh
make install \
  APPLE_ID=you@example.com \
  APPLE_TEAM_ID=XXXXXXXXXX \
  APPLE_SIGNING_IDENTITY="Developer ID Application: Your Name (XXXXXXXXXX)"
```

This runs `build → sign → notarize → install` in sequence. The notarization password is pulled from Keychain under the service name `notarytool`.

To build without installing:

```sh
make build   # outputs dist/remind
make sign    # codesigns the binary
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
