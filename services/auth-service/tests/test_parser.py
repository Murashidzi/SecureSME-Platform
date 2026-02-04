import os
import pytest
from app.utils.log_parser import analyze_log

# A simple log line simulating an SSH Brute Force attack
BRUTE_FORCE_LOG = "Aug 15 12:00:00 server sshd[1234]: Failed password for invalid user hacker from 192.168.1.5 port 22 ssh2"
SAFE_LOG = "Aug 15 12:01:00 server systemd[1]: Started Session 1 of user root."

def test_detect_brute_force(tmp_path):
    """
    Test if the parser correctly identifies a 'Failed password' event as HIGH severity.
    """
    # 1. Create a temporary log file
    d = tmp_path / "logs"
    d.mkdir()
    p = d / "auth.log"
    p.write_text(BRUTE_FORCE_LOG)

    # 2. Run the analyzer on this file
    results = analyze_log(str(p))

    # 3. Assertions (The proof)
    assert len(results) > 0, "Parser missed the threat!"
    assert results[0]['severity'] == 'HIGH'
    assert results[0]['description'] == 'Brute Force Attempt detected'

def test_ignore_safe_logs(tmp_path):
    """
    Test if the parser correctly ignores normal system logs.
    """
    # 1. Create a temporary log file
    d = tmp_path / "logs"
    d.mkdir()
    p = d / "syslog"
    p.write_text(SAFE_LOG)

    # 2. Run the analyzer
    results = analyze_log(str(p))

    # Assertions
    assert len(results) == 0, "Parser flagged a safe log as a threat!"
