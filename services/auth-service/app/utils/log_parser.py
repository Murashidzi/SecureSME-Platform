import re # 're' (for advanced test search")

def analyze_log(file_path):
    """
    Reads a log file line-by-line and looks for suspicious patterns.
    """
    findings = []
    # Define the 'Bad Words' (Threat Signatures)

    # We use a list of dictionaries to map patterns to severity levels.
    signatures = [
        # High priority threats
        {"pattern": r"Failed password", "severity": "HIGH", "description": "Brute Force Attempt detected"},
        {"pattern": r"anauthorized", "severity": "MEDIUM", "description": "Unauthorized access attempt"},

        # Low Priority/Info
        {"pattern": r"error", "severity": "LOW", "description": "General System Error"},
        {"pattern": r"warning", "severity": "LOW", "description": "System Warning"}
    ]

    try:
        # Open the file in 'Read' mode ('r')
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            # 3. Read line by line (Memory efficient)
            for line_num, line in enumerate(f, 1):
                #. 4 Check each signature against the current line
                for sig in signatures:
                    #re.search checks if the pattern exists in the line.
                    # re.IGNORE measn "Error" and "error" are treated the same
                    if re.search(sig["pattern"], line, re.IGNORECASE):
                        findings.append({
                            "line": line_num,
                            "content": line.strip(), # .strip removes whitespace
                            "severity": sig["severity"],
                            "description": sig["description"]
                        })
                        # We don't break here because one line might have multiple issues
    except Exception as e:
        return {"error": str(e)}

    # 5. Return the report
    return findings
