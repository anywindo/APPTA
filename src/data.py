import csv
import os
import datetime
import config

class DataWriter:
    def __init__(self, filename=None):
        if filename is None:
            if "E2E_RUN_FOLDER" in os.environ:
                filename = os.path.join(os.environ["E2E_RUN_FOLDER"], "results.csv")
            else:
                tz_utc_7 = datetime.timezone(datetime.timedelta(hours=7))
                now = datetime.datetime.now(tz_utc_7).strftime('%Y%m%d_%H%M%S')
                os.makedirs("results", exist_ok=True)
                filename = f"results/results_{now}.csv"
            
        self.filename = filename
        self.file = open(self.filename, mode='w', newline='')
        self.writer = csv.DictWriter(self.file, fieldnames=config.CSV_COLUMNS)
        self.writer.writeheader()
        self.file.flush()
        
    def write_row(self, run_id, message_size_bytes, encryption_time_ns, decryption_time_ns, latency_ns, throughput_bytes_per_s, success, timestamp_utc=None):
        if timestamp_utc is None:
            timestamp_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
            
        row = {
            "run_id": run_id,
            "message_size_bytes": message_size_bytes,
            "encryption_time_ns": encryption_time_ns,
            "decryption_time_ns": decryption_time_ns,
            "latency_ns": latency_ns,
            "throughput_bytes_per_s": throughput_bytes_per_s,
            "success": success,
            "timestamp_utc": timestamp_utc
        }
        self.writer.writerow(row)
        self.file.flush()
        
    def close(self):
        self.file.close()
