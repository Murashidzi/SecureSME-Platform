import random
from datetime import datetime, timedelta

# Configuration
FILENAME = "heavy_attack.log"
NUM_LINES = 1500
IPS = ["192.168.1.50", "10.0.0.5", "172.16.0.99", "45.33.22.11", "185.22.1.4"]
USERS = ["root", "admin", "test", "deploy", "ubuntu"]

print(f"Generating {NUM_LINES} fake attack logs...")

with open(FILENAME, "w") as f:
    start_time = datetime.now().replace(hour=0, minute=0, second=0)

    for i in range(NUM_LINES):
        # 1. Random Time (spread across 24 hours)
        current_time = start_time + timedelta(minutes=random.randint(0, 1400))
        ts = current_time.strftime("%b %d %H:%M:%S")

        # 2. Random Attack Details
        ip = random.choice(IPS)
        user = random.choice(USERS)

        # 3. Create the Log Line (Matches our Regex)
        # "Feb  5 07:16:42 ip-172-31-18-59 sshd[2538]: Failed password for invalid user admin from 192.168.1.5 port 55555 ssh2"
        line = f"{ts} ip-172-31-18-59 sshd[{random.randint(1000,9999)}]: Failed password for invalid user {user} from {ip} port {random.randint(20000,60000)} ssh2\n"

        f.write(line)

print(f"✅ Created {FILENAME}. Upload this to your dashboard!")
