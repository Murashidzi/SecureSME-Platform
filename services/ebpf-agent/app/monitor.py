#!/usr/bin/python3
from bcc import BPF
import time
import requests
import joblib
import pandas as pd
import warnings

# Suppress scikit-learn warnings about feature names
warnings.filterwarnings("ignore", category=UserWarning)

# ---------------------------------------------------------
# 1. Load the Machine Learning Model (The Brain)
# ---------------------------------------------------------
print(" Loading AI Anomaly Detection Engine...")
try:
    # Load the Isolation Forest we trained earlier
    model = joblib.load("isolation_forest.pkl")
    print(" AI Engine loaded successfully.")
except Exception as e:
    print(f" CRITICAL ERROR: Could not load ML model: {e}")
    exit(1)

# ---------------------------------------------------------
# 2. Kernel Code (C Language)
# ---------------------------------------------------------
bpf_text = """
#include <uapi/linux/ptrace.h>
#include <linux/sched.h>

struct data_t {
    u32 pid;
    char comm[TASK_COMM_LEN];
    char fname[256];
};

BPF_PERF_OUTPUT(events);

int syscall__execve(struct pt_regs *ctx,
                    const char __user *filename,
                    const char __user *const __user *argv,
                    const char __user *const __user *envp)
{
    struct data_t data = {};
    data.pid = bpf_get_current_pid_tgid() >> 32;
    bpf_get_current_comm(&data.comm, sizeof(data.comm));
    bpf_probe_read_user_str(&data.fname, sizeof(data.fname), filename);
    events.perf_submit(ctx, &data, sizeof(data));
    return 0;
}
"""

# ---------------------------------------------------------
# 3. User Space Processing & AI Inference
# ---------------------------------------------------------
b = BPF(text=bpf_text)
execve_fn = b.get_syscall_fnname("execve")
b.attach_kprobe(event=execve_fn, fn_name="syscall__execve")

print(f" Hooked into {execve_fn.decode()}! AI is actively scoring syscalls...")
print("-" * 60)

API_ENDPOINT = "http://securesme_api:5000/api/ebpf-alert"

def print_event(cpu, data, size):
    event = b["events"].event(data)
    try:
        comm = event.comm.decode('utf-8', 'replace')
        fname = event.fname.decode('utf-8', 'replace')

        # Ignore obvious system noise to save CPU cycles
        if comm in ["systemd", "sa1", "cron"] or fname == "":
            return

        # --- FEATURE ENGINEERING (Live Extraction) ---
        cmd_length = len(fname)
        special_chars = sum(fname.count(c) for c in ['|', '>', '&', '/', ';', '$'])
        in_suspicious_dir = 1 if '/tmp' in fname or '/dev' in fname else 0  # nosec B108
        has_network_keyword = 1 if any(k in fname for k in ['tcp', 'http', 'wget', 'curl', 'nc ']) else 0

        # Create a DataFrame identical to what the model was trained on
        features = pd.DataFrame(
            [[cmd_length, special_chars, in_suspicious_dir, has_network_keyword]],
            columns=['cmd_length', 'num_special_chars', 'in_suspicious_dir', 'has_network_keyword']
        )

        # --- AI INFERENCE ---
        # Predict: 1 means Normal, -1 means Anomaly
        prediction = model.predict(features)[0]

        if prediction == -1:
            print(f" [AI ANOMALY] PID: {event.pid} | Parent: {comm} | Cmd: {fname}")

            payload = {
                "pid": event.pid,
                "parent_comm": comm,
                "executed_cmd": fname,
                "mitre_tactic": "T1059 (ML Detected Anomaly)"
            }
            try:
                requests.post(API_ENDPOINT, json=payload, timeout=2)
            except Exception as e:
                pass # Fail silently if API is unreachable to prevent agent crash

    except Exception as e:
        pass

b["events"].open_perf_buffer(print_event)

while True:
    try:
        b.perf_buffer_poll()
    except KeyboardInterrupt:
        exit()
