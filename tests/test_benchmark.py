import unittest
import threading
import time
import os
import sys
import csv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.network import Receiver, Sender
from src.benchmark import BenchmarkRunner, generate_plaintext
from src.data import DataWriter
from src import protocol
from src import crypto
import config
from src.timing import Timer

class TestBenchmark(unittest.TestCase):
    def test_randomization_and_csv_output(self):
        host = '127.0.0.1'
        port = 5558
        
        receiver = Receiver(host, port)
        sender = Sender(host, port)
        
        def receiver_thread():
            receiver.start()
            receiver.handshake()
            
            while True:
                payload = receiver.receive_message()
                
                with Timer() as dec_timer:
                    nonce, ciphertext, tag = protocol.unpackage(payload)
                    try:
                        plaintext = crypto.decrypt(receiver.session_key, nonce, ciphertext, tag)
                        success = True
                    except:
                        success = False
                        plaintext = b""
                
                if len(plaintext) == 0 and success:
                    break
                    
                dec_time = dec_timer.elapsed_ns
                receiver.send_ack(protocol.pack_ack(success, dec_time))
                
            receiver.close()
            
        t = threading.Thread(target=receiver_thread)
        t.start()
        time.sleep(0.1)
        
        sender.connect()
        sender.handshake()
        
        test_csv = "test_results.csv"
        if os.path.exists(test_csv):
            os.remove(test_csv)
            
        writer = DataWriter(test_csv)
        runner = BenchmarkRunner(sender, data_writer=writer)
        
        # Capture the original sizes list
        original_sizes = list(config.MESSAGE_SIZES)
        
        # Override config sizes to make test fast
        config.MESSAGE_SIZES = [16, 64, 256]
        config.MEASURED_RUNS = 2
        config.WARMUP_RUNS = 1
        
        runner.run_experiment()
        
        t.join(timeout=2.0)
        sender.close()
        
        # Verify CSV
        self.assertTrue(os.path.exists(test_csv))
        
        rows = []
        with open(test_csv, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
                
        # 3 sizes * 2 runs = 6 rows
        self.assertEqual(len(rows), 6)
        
        sizes_in_order = []
        for row in rows:
            size = int(row['message_size_bytes'])
            if len(sizes_in_order) == 0 or sizes_in_order[-1] != size:
                sizes_in_order.append(size)
                
        self.assertEqual(len(sizes_in_order), 3)
        self.assertEqual(set(sizes_in_order), {16, 64, 256})
        
        # Reset config
        config.MESSAGE_SIZES = original_sizes
        config.MEASURED_RUNS = 30
        config.WARMUP_RUNS = 5
        
        if os.path.exists(test_csv):
            os.remove(test_csv)

if __name__ == '__main__':
    unittest.main()
