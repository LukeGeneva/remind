from datetime import datetime, timedelta
import re


def parse_time(args, now=None):
    """Parse one or two time arguments into a datetime."""
    if now is None:
        now = datetime.now()
    time_str = " ".join(args).strip().lower()

    # Strip leading "in "
    time_str = re.sub(r"^in\s+", "", time_str)

    # --- Relative: +30m, 30m, +1h, 1h, 1h30m ---
    m = re.match(r"^\+?(\d+)\s*h(?:ours?)?\s*(\d+)?\s*m?(?:in(?:utes?)?)?$", time_str)
    if m:
        hours = int(m.group(1))
        minutes = int(m.group(2)) if m.group(2) else 0
        return now + timedelta(hours=hours, minutes=minutes)

    m = re.match(r"^\+?(\d+)\s*h(?:ours?)?$", time_str)
    if m:
        return now + timedelta(hours=int(m.group(1)))

    m = re.match(r"^\+?(\d+)\s*m(?:in(?:utes?)?)?$", time_str)
    if m:
        return now + timedelta(minutes=int(m.group(1)))

    # --- "tomorrow HH:MMam/pm" or "tomorrow Hpm" ---
    m = re.match(r"^tomorrow\s+(.+)$", time_str)
    if m:
        base = (now + timedelta(days=1)).replace(second=0, microsecond=0)
        return parse_clock(m.group(1).strip(), base)

    # --- Absolute clock time (roll to tomorrow if already past) ---
    result = parse_clock(time_str, now)
    if result <= now:
        result += timedelta(days=1)
    return result


def parse_clock(s, base):
    """Parse a clock string like 3pm, 3:45pm, 14:30 relative to base date."""
    for fmt in ["%I:%M%p", "%I:%M %p", "%I%p", "%I %p", "%H:%M"]:
        try:
            t = datetime.strptime(s.upper(), fmt)
            return base.replace(hour=t.hour, minute=t.minute, second=0, microsecond=0)
        except ValueError:
            continue
    raise ValueError(f"Can't parse time: '{s}'")


def applescript_date(dt):
    """Format datetime for AppleScript: MM/DD/YYYY HH:MM:SS"""
    return dt.strftime("%m/%d/%Y %H:%M:%S")
