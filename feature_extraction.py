import json
import csv
import os
from datetime import datetime

# Folder containing session JSON files
sessions_folder = "sessions"

# Final dataset storage
final_data = []

# Loop through all session files
for filename in os.listdir(sessions_folder):

    # Only process JSON files
    if not filename.endswith(".json"):
        continue

    filepath = os.path.join(sessions_folder, filename)

    events = []
    command_count = 0

    # Open session file
    with open(filepath, "r") as file:

        for line in file:

            try:
                event = json.loads(line)

                event_type = event.get("eventid")

                # Count commands
                if event_type == "cowrie.command.input":
                    command_count += 1

                # Keep login + command events
                if event_type not in [
                    "cowrie.login.failed",
                    "cowrie.login.success",
                    "cowrie.command.input"
                ]:
                    continue

                timestamp = event.get("timestamp")

                if not timestamp:
                    continue

                username = event.get("username", "")

                # Convert timestamp
                time_obj = datetime.fromisoformat(
                    timestamp.replace("Z", "")
                )

                events.append({
                    "username": username,
                    "event_type": event_type,
                    "time": time_obj
                })

            except:
                pass

    # Skip empty sessions
    if len(events) == 0:
        continue

    #Feature Extraction

    total_attempts = sum(
        1
        for e in events
        if e["event_type"] in [
            "cowrie.login.failed",
            "cowrie.login.success"
        ]
    )

    usernames = set(
        e["username"]
        for e in events
        if e["username"]
    )

    unique_usernames = len(usernames)

    failed_attempts = sum(
        1
        for e in events
        if e["event_type"] == "cowrie.login.failed"
    )

    success_attempts = sum(
        1
        for e in events
        if e["event_type"] == "cowrie.login.success"
    )

    # Sort timestamps
    times = sorted(
        e["time"]
        for e in events
    )

    # Session duration
    session_duration = (
        (times[-1] - times[0]).total_seconds()
        if len(times) > 1 else 0
    )

    # Time gaps
    gaps = [
        (times[i + 1] - times[i]).total_seconds()
        for i in range(len(times) - 1)
    ]

    avg_time_gap = (
        sum(gaps) / len(gaps)
        if gaps else 0
    )

   
    # LABELING

    filename_lower = filename.lower()

    if "bruteforce" in filename_lower:
        attack_label = "brute_force"

    elif "medusa" in filename_lower:
        attack_label = "brute_force"

    elif "scan" in filename_lower:
        attack_label = "scanning"

    elif "interactive" in filename_lower:
        attack_label = "interactive"

    elif "attack_chain" in filename_lower:
        attack_label = "interactive"

    else:
        attack_label = "interactive"

    # ADD TO DATASET
    
    final_data.append([
        filename,
        total_attempts,
        unique_usernames,
        failed_attempts,
        success_attempts,
        round(avg_time_gap, 2),
        command_count,
        round(session_duration, 2),
        attack_label
    ])


# SAVE CSV
with open("honeypot_features.csv", "w", newline="") as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow([
        "session",
        "total_attempts",
        "unique_usernames",
        "failed_attempts",
        "success_attempts",
        "avg_time_gap",
        "command_count",
        "session_duration",
        "attack_label"
    ])

    writer.writerows(final_data)

print("\nDataset created successfully!")
print("Total sessions processed:", len(final_data))
