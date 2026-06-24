#!/usr/bin/env python3
"""
remind - Create an Apple Reminder from the command line

Usage:
  remind "Title"              # reminder with no time
  remind "Title" 3pm          # absolute time today (or tomorrow if past)
  remind "Title" 14:30        # 24-hour format
  remind "Title" +30m         # 30 minutes from now
  remind "Title" +1h          # 1 hour from now
  remind "Title" +1h30m       # 1 hour 30 minutes from now
  remind "Title" tomorrow 9am # tomorrow at 9am

Install (run once):
  chmod +x remind.py
  sudo cp remind.py /usr/local/bin/remind
"""

import sys
import subprocess
from datetime import datetime, timedelta

from time_parser import applescript_date, parse_time


def create_reminder(title, due_date=None, list_name="Reminders"):
    # Escape double quotes in title
    safe_title = title.replace('"', '\\"')

    if due_date:
        date_str = applescript_date(due_date)
        script = f"""
tell application "Reminders"
    set dueDate to date "{date_str}"
    make new reminder in list "{list_name}" with properties {{name:"{safe_title}", due date:dueDate, remind me date:dueDate}}
end tell
"""
    else:
        script = f"""
tell application "Reminders"
    make new reminder in list "{list_name}" with properties {{name:"{safe_title}"}}
end tell
"""

    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr.strip()}", file=sys.stderr)
        sys.exit(1)


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    title = sys.argv[1]
    time_args = sys.argv[2:]
    due_date = None

    if time_args:
        try:
            due_date = parse_time(time_args)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    create_reminder(title, due_date)

    if due_date:
        friendly = due_date.strftime("%I:%M %p").lstrip("0")
        # Show "today" or "tomorrow"
        today = datetime.now().date()
        if due_date.date() == today:
            day = "today"
        elif due_date.date() == today + timedelta(days=1):
            day = "tomorrow"
        else:
            day = due_date.strftime("%A %b %-d")
        print(f'✓ Reminder: "{title}" — {day} at {friendly}')
    else:
        print(f'✓ Reminder created: "{title}"')


if __name__ == "__main__":
    main()
