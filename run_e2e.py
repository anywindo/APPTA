import subprocess
import time
import os
import sys

def main():
    print("Starting E2E Validation Test...")
    os.makedirs("results", exist_ok=True)
    
    # 1. Record Environment
    print("Recording Environment...")
    subprocess.run([sys.executable, "src/environment.py", "results/environment.json"], check=True)
    
    # 2. Start Receiver
    print("Starting Receiver...")
    receiver = subprocess.Popen([sys.executable, "receiver.py"])
    time.sleep(1)
    
    # 3. Start Sender
    print("Starting Sender (running benchmark)...")
    sender = subprocess.run([sys.executable, "sender.py"])
    
    if sender.returncode != 0:
        print("Sender failed.")
        receiver.terminate()
        sys.exit(1)
        
    receiver.wait()
    
    # Find generated CSV
    csv_files = [f for f in os.listdir(".") if f.startswith("results_") and f.endswith(".csv")]
    if not csv_files:
        print("No CSV found.")
        sys.exit(1)
        
    # Sort to get the latest
    csv_files.sort()
    latest_csv = csv_files[-1]
    
    print(f"Running Analysis on {latest_csv}...")
    subprocess.run([sys.executable, "src/analysis.py", latest_csv, "--outdir", "results"], check=True)
    
    # Check outputs
    assert os.path.exists("results/plot_latency.png"), "Latency plot missing"
    assert os.path.exists("results/summary_" + latest_csv[8:]), "Summary CSV missing"
    
    print("E2E Test completed successfully!")

if __name__ == "__main__":
    main()
