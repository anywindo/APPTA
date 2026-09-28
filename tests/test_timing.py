import unittest
import time
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.timing import Timer, calculate_throughput
from src import protocol

class TestTiming(unittest.TestCase):
    def test_timer_positive(self):
        with Timer() as t:
            time.sleep(0.01)
        self.assertGreater(t.elapsed_ns, 0)
        
    def test_throughput_calculation(self):
        # 1024 bytes in 1,000,000,000 ns (1s) = 1024 bytes/s
        throughput = calculate_throughput(1024, 1_000_000_000)
        self.assertAlmostEqual(throughput, 1024.0)
        
    def test_throughput_zero_latency(self):
        # Prevent division by zero
        throughput = calculate_throughput(1024, 0)
        self.assertEqual(throughput, 0.0)
        
    def test_ack_packing(self):
        success = True
        dec_time = 123456789
        
        payload = protocol.pack_ack(success, dec_time)
        r_success, r_dec_time = protocol.unpack_ack(payload)
        
        self.assertEqual(success, r_success)
        self.assertEqual(dec_time, r_dec_time)
        
    def test_ack_packing_invalid(self):
        with self.assertRaises(ValueError):
            protocol.unpack_ack(b"short")

    def test_timing_boundaries_sanity(self):
        import threading
        from src.network import Receiver, Sender
        from src import crypto
        
        host = '127.0.0.1'
        port = 5557
        
        receiver = Receiver(host, port)
        sender = Sender(host, port)
        
        dec_time_ns_receiver = 0
        
        def receiver_thread():
            nonlocal dec_time_ns_receiver
            receiver.start()
            receiver.handshake()
            payload = receiver.receive_message()
            
            with Timer() as dec_timer:
                nonce, ciphertext, tag = protocol.unpackage(payload)
                crypto.decrypt(receiver.session_key, nonce, ciphertext, tag)
            
            dec_time_ns_receiver = dec_timer.elapsed_ns
            ack_payload = protocol.pack_ack(True, dec_time_ns_receiver)
            
            # Simulate a slow network send to prove it doesn't inflate decryption time
            time.sleep(0.05)
            receiver.send_ack(ack_payload)
            receiver.close()
            
        t = threading.Thread(target=receiver_thread)
        t.start()
        time.sleep(0.1)
        
        sender.connect()
        sender.handshake()
        
        test_msg = b"timing boundary test"
        
        with Timer() as total_timer:
            with Timer() as enc_timer:
                nonce, ciphertext, tag = crypto.encrypt(sender.session_key, test_msg)
                packaged_data = protocol.package(nonce, ciphertext, tag)
            
            # Simulate a slow network send to prove it doesn't inflate encryption time
            time.sleep(0.05)
            sender.send_message(packaged_data)
            ack = sender.receive_ack()
            
        latency_ns = total_timer.elapsed_ns
        encryption_time_ns = enc_timer.elapsed_ns
        
        success, decryption_time_ns = protocol.unpack_ack(ack)
        
        t.join(timeout=2.0)
        sender.close()
        
        # 1. Latency >= encryption + decryption
        self.assertGreaterEqual(latency_ns, encryption_time_ns + decryption_time_ns)
        
        # 2. Network delays (0.05s * 2 = 100ms) are NOT included in enc/dec time,
        # but ARE included in latency.
        # So encryption and decryption should be much less than 50ms (50,000,000 ns).
        self.assertLess(encryption_time_ns, 50_000_000)
        self.assertLess(decryption_time_ns, 50_000_000)
        
        # Latency should be at least 100ms (100,000,000 ns) due to the sleeps
        self.assertGreaterEqual(latency_ns, 100_000_000)
        
if __name__ == '__main__':
    unittest.main()
