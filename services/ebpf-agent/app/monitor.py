#!/usr/bin/python3
from bcc import BPF
import time
import requests

# 1. Kernel Code (C Language)
# This code runs Inside the Linux Kernel (Ring 0).
# We hook 'sys-execve' to capture every command execution.

bpf_text = """
#include <uapi/linux/ptrace.h>
#include <linux/sched.h>

// Define the data structure we want to send back to User Space
struct data_t {
    u32 pid;
    char comm[TASK_COMM_LEN];
    char fname[256];
};

// Create a perf buffer to pass messages to Python
BPF_PERF_OUTPUT(events);

// The Hook Function
int syscall__execve(struct pt_regs *ctx,
                    const char __user *filename,
                    const char __user *const __user *argv,
                    const char __user *const __user *envp)
{
    struct data_t data = {};

    // 1. Get Process ID (PID)
    data.pid = bpf_get_current_pid_tgid() >> 32;

    // 2. Get the Command Name (e.g., "sudo", "python")
    bpf_get_current_comm(&data.comm, sizeof(data.comm));

    // 3. Read the 'filename' argument from USer Space memory
    // (We must use a safe helper function because it's user memory)
    bpf_probe_read_user_str(&data.fname, sizeof(data.fname), filename);

    // 4. Submit to the Perf Buffer
    events.perf_submit(ctx, &data, sizeof(data));

    return 0;
}
"""

# 2. Threat Intelligence Configuration
# Atteckers use these to download payloads or reverse shell
SUSPICIOUS_BINARIES = [
    "nc", "netcat", "curl", "wget", "nmap",
    "strace", "tcdump", "chmod", "chown"
]



# 3. The User Space Code (Python)
# This code runs in User Land (Ring 3).
# It compiles C code, loads it, and reads the output.

# Load the BPF program
print("Compiling and Loading eBPF Probe...")
b = BPF(text=bpf_text)

# Attach the Kprobe to the execve system call
# get_syscall_fname automagically finds the right kernel function name (e.g., __x64_sys_execve)
execve_fn = b.get_syscall_fnname("execve")
b.attach_kprobe(event=execve_fn, fn_name="syscall__execve")

print(f"Hooked into {execve_fn.decode()}! Monitoring for LotL attacks...  (Ctrl+C to stop)")
print("-" * 60)

API_ENDPOINT = "http://securesme_api:5000/api/ebpf-alert"

# Callback function to handle events from the kernel
def print_event(cpu, data, size):
    event = b["events"].event(data)
    # Decode bytes to string for printing
    try:
        comm = event.comm.decode('utf-8', 'replace')
        fname = event.fname.decode('utf-8', 'replace')

        # Threat Detection Logic: Is the executed binary suspicious?
        is_suspicious = any(suspicious in fname for suspicious in SUSPICIOUS_BINARIES)

        if is_suspicious:
            print(f" [THREAT DETECTED] PID: {event.pid} | Executed: {fname}")

            payload = {
                "pid": event.pid,
                "parent_comm": comm,
                "executed_cmd": fname,
                "mitre_tactic": "T1059/T1090"
            }
            try:
                # We use a short timeout so the agent doesn't block if the API is slow
                requests.post(API_ENDPOINT, json=payload, timeout=2)
            except Exception as e:
                print(f" Failed to send alert to API: {e}")

    except Exception as e:
        pass


# Open the Perf Buffer and loop forever
b["events"].open_perf_buffer(print_event)

while True:
    try:
        b.perf_buffer_poll()
    except KeyboardInterrupt:
        exit()
