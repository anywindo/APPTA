import sys
from src.network import Sender
from src.benchmark import BenchmarkRunner

def main():
    host = '127.0.0.1'
    port = 5000
    
    sender = Sender(host, port)
    print(f"Connecting to receiver on {host}:{port}...")
    try:
        sender.connect()
        print("Connected.")
        sender.handshake()
        print("ECDH Handshake complete.")
        
        runner = BenchmarkRunner(sender)
        runner.run_experiment()
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sender.close()

if __name__ == "__main__":
    main()
