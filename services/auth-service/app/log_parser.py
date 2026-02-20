import re

def parse_log_file(filepath):
    """
    Parses a Linux auth.log file and extracts attack patterns.
    Returns a list of dictionaries.
    """
    data = []

    # Regex patterns for common attacks
    patterns = {
        'ssh_fail': r"Failed password for (?:invalid user )?(\w+) from (\d+\.\d+\.\d+\.\d+)",
        'root_attempt': r"Failed password for root from (\d+\.\d+\.\d+\.\d+)",
        'invalid_user': r"Invalid user (\w+) from (\d+\.\d+\.\d+\.\d+)"
    }

    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                # Default timestamp extraction (simple approach for demo)
                # In production, use regex to extract "Feb 10 09:00:01"
                timestamp = line[:15]

                # Check for Root Attempts (High Severity)
                if "root" in line and "Failed" in line:
                    match = re.search(patterns['root_attempt'], line)
                    if match:
                        data.append({
                            'ip': match.group(1),
                            'user': 'root',
                            'attack_type': 'Root Access Attempt',
                            'timestamp': timestamp,
                            'raw': line
                        })
                        continue

                # Check for Invalid Users
                if "Invalid user" in line:
                    match = re.search(patterns['invalid_user'], line)
                    if match:
                        data.append({
                            'ip': match.group(2),
                            'user': match.group(1),
                            'attack_type': 'Invalid User',
                            'timestamp': timestamp,
                            'raw': line
                        })
                        continue

                # Check for Standard Brute Force
                if "Failed password" in line:
                    match = re.search(patterns['ssh_fail'], line)
                    if match:
                        data.append({
                            'ip': match.group(2),
                            'user': match.group(1),
                            'attack_type': 'Brute Force',
                            'timestamp': timestamp,
                            'raw': line
                        })

    except Exception as e:
        print(f"Error parsing file: {e}")
        return []

    return data
