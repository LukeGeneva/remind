import pytest
from datetime import datetime, timedelta

from time_parser import applescript_date, parse_clock, parse_time

# Fixed "now" for deterministic tests: 2026-06-24 10:00:00
NOW = datetime(2026, 6, 24, 10, 0, 0)
TOMORROW = NOW + timedelta(days=1)


# --- parse_time: relative ---

def test_relative_minutes():
    result = parse_time(["+30m"], now=NOW)
    assert result == NOW + timedelta(minutes=30)

def test_relative_minutes_no_plus():
    result = parse_time(["30m"], now=NOW)
    assert result == NOW + timedelta(minutes=30)

def test_relative_minutes_word():
    result = parse_time(["30min"], now=NOW)
    assert result == NOW + timedelta(minutes=30)

def test_relative_hours():
    result = parse_time(["+1h"], now=NOW)
    assert result == NOW + timedelta(hours=1)

def test_relative_hours_no_plus():
    result = parse_time(["2h"], now=NOW)
    assert result == NOW + timedelta(hours=2)

def test_relative_hours_and_minutes():
    result = parse_time(["1h30m"], now=NOW)
    assert result == NOW + timedelta(hours=1, minutes=30)

def test_relative_hours_and_minutes_plus():
    result = parse_time(["+1h30m"], now=NOW)
    assert result == NOW + timedelta(hours=1, minutes=30)

def test_relative_strip_leading_in():
    result = parse_time(["in", "45m"], now=NOW)
    assert result == NOW + timedelta(minutes=45)


# --- parse_time: absolute clock (future) ---

def test_absolute_future_pm():
    # 3pm is after 10am, so should be today
    result = parse_time(["3pm"], now=NOW)
    assert result == NOW.replace(hour=15, minute=0, second=0, microsecond=0)

def test_absolute_future_24h():
    result = parse_time(["14:30"], now=NOW)
    assert result == NOW.replace(hour=14, minute=30, second=0, microsecond=0)

def test_absolute_past_rolls_to_tomorrow():
    # 9am is before 10am NOW, so rolls to tomorrow
    result = parse_time(["9am"], now=NOW)
    assert result == TOMORROW.replace(hour=9, minute=0, second=0, microsecond=0)

def test_absolute_with_minutes():
    result = parse_time(["3:45pm"], now=NOW)
    assert result == NOW.replace(hour=15, minute=45, second=0, microsecond=0)

def test_absolute_24h_past_rolls():
    result = parse_time(["09:30"], now=NOW)
    assert result == TOMORROW.replace(hour=9, minute=30, second=0, microsecond=0)


# --- parse_time: tomorrow ---

def test_tomorrow_simple():
    result = parse_time(["tomorrow", "9am"], now=NOW)
    assert result == TOMORROW.replace(hour=9, minute=0, second=0, microsecond=0)

def test_tomorrow_24h():
    result = parse_time(["tomorrow", "14:30"], now=NOW)
    assert result == TOMORROW.replace(hour=14, minute=30, second=0, microsecond=0)

def test_tomorrow_with_minutes():
    result = parse_time(["tomorrow", "9:30am"], now=NOW)
    assert result == TOMORROW.replace(hour=9, minute=30, second=0, microsecond=0)


# --- parse_clock ---

def test_parse_clock_12h_pm():
    base = datetime(2026, 6, 24, 0, 0, 0)
    result = parse_clock("3pm", base)
    assert result == base.replace(hour=15, minute=0)

def test_parse_clock_12h_am():
    base = datetime(2026, 6, 24, 0, 0, 0)
    result = parse_clock("9am", base)
    assert result == base.replace(hour=9, minute=0)

def test_parse_clock_with_colon():
    base = datetime(2026, 6, 24, 0, 0, 0)
    result = parse_clock("3:45pm", base)
    assert result == base.replace(hour=15, minute=45)

def test_parse_clock_24h():
    base = datetime(2026, 6, 24, 0, 0, 0)
    result = parse_clock("14:30", base)
    assert result == base.replace(hour=14, minute=30)

def test_parse_clock_invalid():
    with pytest.raises(ValueError, match="Can't parse time"):
        parse_clock("notaTime", datetime(2026, 6, 24))


# --- applescript_date ---

def test_applescript_date_format():
    dt = datetime(2026, 6, 24, 15, 30, 0)
    assert applescript_date(dt) == "06/24/2026 15:30:00"
