# Auto_Screenshot

**Auto Screenshot Monitor with GUI**

This Python application captures screenshots from one or more monitors on a scheduled interval. It's designed to automatically record screen activity during specified time windows with a user-friendly GUI interface.

## Key Features:

- **Multi-Monitor Support**: Captures screenshots from all connected monitors simultaneously
- **Scheduled Capture**: Define start and end times (with AM/PM) for when capturing should occur
- **Configurable Interval**: Set the capture frequency in seconds (default: 5 seconds)
- **Black Screen Detection**: Optionally skip saving black/turned-off screens to save storage
- **Organized Storage**: Automatically creates a folder structure with today's date, organizing screenshots by screen number
- **Real-time Status**: GUI displays live capture status, cycle count, and current timestamp
- **Non-blocking Operation**: Runs capture loop in a background thread while keeping the GUI responsive

## How It Works:

1. User sets start/end times and capture interval via dropdown menus
2. Application waits until the scheduled time window
3. When active, captures screenshots from each monitor and saves them as JPEG files
4. Skips black screens unless the "Save black screen images" option is enabled
5. Displays real-time feedback on capture progress and system status

## Default Behavior:

- Saves to: `~/Pictures/[YYYY-MM-DD]/`
- Starts at: 09:00 AM
- Ends at: 03:30 PM
- Interval: 5 seconds
- Black screens: Skipped by default
