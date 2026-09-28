import platform
import os
import json
import sys
import cryptography

def record_environment(output_path):
    env_info = {
        "python_version": sys.version,
        "cryptography_version": cryptography.__version__,
        "os": platform.system(),
        "os_release": platform.release(),
        "os_version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "architecture": platform.architecture()[0],
        "cpu_count": os.cpu_count()
    }
    
    with open(output_path, "w") as f:
        json.dump(env_info, f, indent=4)
        
    print(f"Environment documentation saved to {output_path}")

if __name__ == "__main__":
    out_path = sys.argv[1] if len(sys.argv) > 1 else "results/environment.json"
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    record_environment(out_path)
