import platform
import os
import json
import sys
import cryptography
import psutil
import socket

def get_size(bytes, suffix="B"):
    """Scale bytes to its proper format."""
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor
    return f"{bytes:.2f}Y{suffix}"

def record_environment(output_path):
    # Basic system info
    uname = platform.uname()
    
    # CPU frequencies
    try:
        cpufreq = psutil.cpu_freq()
        cpu_freq_current = f"{cpufreq.current:.2f}Mhz" if cpufreq else "Unknown"
        cpu_freq_max = f"{cpufreq.max:.2f}Mhz" if cpufreq else "Unknown"
    except Exception:
        cpu_freq_current = "Unknown"
        cpu_freq_max = "Unknown"
        
    # Memory Info
    try:
        svmem = psutil.virtual_memory()
        total_ram = get_size(svmem.total)
    except Exception:
        total_ram = "Unknown"

    env_info = {
        "python_version": sys.version,
        "cryptography_version": cryptography.__version__,
        "os_system": uname.system,
        "os_node_name": uname.node,
        "os_release": uname.release,
        "os_version": uname.version,
        "machine": uname.machine,
        "processor": uname.processor,
        "architecture": platform.architecture()[0],
        "cpu_count_physical": psutil.cpu_count(logical=False),
        "cpu_count_logical": psutil.cpu_count(logical=True),
        "cpu_freq_current": cpu_freq_current,
        "cpu_freq_max": cpu_freq_max,
        "total_ram": total_ram,
        "hostname": socket.gethostname()
    }
    
    with open(output_path, "w") as f:
        json.dump(env_info, f, indent=4)
        
    print(f"Environment documentation saved to {output_path}")

if __name__ == "__main__":
    out_path = sys.argv[1] if len(sys.argv) > 1 else "results/environment.json"
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    record_environment(out_path)
