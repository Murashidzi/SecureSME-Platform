import re
from collections import Counter, defaultdict
from datetime import datetime

def parse_auth_log(filepath):
    """
    Robust Log Parser. Skips malformed lines instead of crashing.
    """

    # Pattern: "Failed password for (invalid user) <user> from <ip>"
    failed_password_pattern = re.compile(r'Failed password for (invalid user )?(\w+) from (\d+\.\d+\.\d+\.\d+)')

    # Pattern: "Feb  5 07:16:42" (Syslog standard)
    timestamp_pattern = re.compile(r'^(\w{3}\s+\d+\s\d{2}:\d{2}:\d{2})')

    stats = {
        "total_threats": 0,
        "hourly_counts": defaultdict(int),
        "attack_types": Counter(),
        "top_ips": Counter()
    }

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                try:
                    # 1. Hunt for the Attack
                    match = failed_password_pattern.search(line)
                    if match:
                        stats["total_threats"] += 1

                        user = match.group(2)
                        ip = match.group(3)

                        # categorize
                        if user == 'root':
                            stats["attack_types"]["Root Access"] += 1
                        elif match.group(1):
                            stats["attack_types"]["Invalid User"] += 1
                        else:
                            stats["attack_types"]["Brute Force"] += 1

                        stats["top_ips"][ip] += 1

                        # 2. Extract Time (Safe Mode)
                        time_match = timestamp_pattern.search(line)
                        if time_match:
                            ts_str = time_match.group(1)
                            try:
                                # Try parsing "Feb  5 07:16:42"
                                # Note: Python requires the month to match the locale (English)
                                dt = datetime.strptime(ts_str, "%b %d %H:%M:%S")
                                hour_key = dt.strftime("%H:00")
                                stats["hourly_counts"][hour_key] += 1
                            except ValueError:
                                # If date fails, just count it as "Unknown Time" or skip
                                pass
                except Exception:
                    # If a single line causes an error, skip it and continue!
                    continue

        return format_results(stats)

    except Exception as e:
        print(f"CRITICAL PARSER ERROR: {e}")
        # Return an empty valid structure so the frontend doesn't break
        return {
            "summary": {"total_incidents": 0, "top_attacker": "Parser Error"},
            "chart_data": [],
            "pie_data": []
        }

def format_results(stats):
    chart_data = []
    # Sort hours safely
    sorted_hours = sorted(stats["hourly_counts"].keys())
    for hour in sorted_hours:
        chart_data.append({
            "name": hour,
            "threats": stats["hourly_counts"][hour]
        })

    pie_data = [
        {"name": "Brute Force", "value": stats["attack_types"]["Brute Force"], "color": "#EF4444"},
        {"name": "Root Access", "value": stats["attack_types"]["Root Access"], "color": "#F59E0B"},
        {"name": "Invalid User", "value": stats["attack_types"]["Invalid User"], "color": "#6366F1"},
    ]

    # Handle case where top_ips is empty
    top_attacker = "N/A"
    if stats["top_ips"]:
        top_attacker = stats["top_ips"].most_common(1)[0][0]

    return {
        "summary": {
            "total_incidents": stats["total_threats"],
            "top_attacker": top_attacker
        },
        "chart_data": chart_data,
        "pie_data": pie_data
    }
