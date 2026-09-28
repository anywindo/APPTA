import csv
import os
import datetime
import config

class DataWriter:
    def __init__(self, filename=None):
        if filename is None:
            now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d_%H%M%S')
            filename = f"results_{now}.csv"
            
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
