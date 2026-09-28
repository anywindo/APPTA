import os
import random
import uuid
import datetime
import config
from src import crypto
from src import protocol
from src.timing import Timer, calculate_throughput
from src.data import DataWriter

def generate_plaintext(size_bytes):
    # Using random bytes for plaintext payload
    return os.urandom(size_bytes)

class BenchmarkRunner:
    def __init__(self, sender, data_writer=None):
        self.sender = sender
        self.data_writer = data_writer if data_writer else DataWriter()
        
    def run_experiment(self):
        # Create execution plan: randomize the order of message sizes
        plan = list(config.MESSAGE_SIZES)
        random.shuffle(plan)
        
        total_runs = len(plan) * config.MEASURED_RUNS
        current_run = 0
        
        experiment_start = datetime.datetime.now()
        
        print(f"Starting experiment: {len(plan)} sizes, {config.MEASURED_RUNS} runs per size (+ {config.WARMUP_RUNS} warm-ups)")
        print(f"Execution order: {plan}")
        
        for size in plan:
            print(f"\nMessage Size: {size} bytes")
            # Generate random plaintext for this size run
            plaintext = generate_plaintext(size)
            
            # Warm-up runs
            for w in range(config.WARMUP_RUNS):
                # We don't record these in CSV
                self._execute_single_run(plaintext, record=False)
                
            # Measured runs
            for m in range(config.MEASURED_RUNS):
                current_run += 1
                success = self._execute_single_run(plaintext, record=True)
                
                # Progress
                if m % 10 == 0 or m == config.MEASURED_RUNS - 1:
                    print(f"  [{current_run}/{total_runs}] Run {m+1}/{config.MEASURED_RUNS} " + ("OK" if success else "FAIL"))
                    
        experiment_end = datetime.datetime.now()
        duration = experiment_end - experiment_start
        
        # Signal receiver to stop (sending a 0-byte message)
        empty_nonce, empty_ciphertext, empty_tag = crypto.encrypt(self.sender.session_key, b"")
        self.sender.send_message(protocol.package(empty_nonce, empty_ciphertext, empty_tag))
        
        print("\nExperiment complete!")
        print(f"Total time: {duration}")
        if self.data_writer:
            print(f"Results saved to: {self.data_writer.filename}")
            self.data_writer.close()
            
    def _execute_single_run(self, plaintext, record=True):
        run_id = str(uuid.uuid4())
        
        try:
            with Timer() as total_timer:
                with Timer() as enc_timer:
                    nonce, ciphertext, tag = crypto.encrypt(self.sender.session_key, plaintext)
                    packaged_data = protocol.package(nonce, ciphertext, tag)
                
                self.sender.send_message(packaged_data)
                ack = self.sender.receive_ack()
                
            latency_ns = total_timer.elapsed_ns
            encryption_time_ns = enc_timer.elapsed_ns
            
            success, decryption_time_ns = protocol.unpack_ack(ack)
            throughput = calculate_throughput(len(plaintext), latency_ns)
            
            if record and self.data_writer:
                self.data_writer.write_row(
                    run_id=run_id,
                    message_size_bytes=len(plaintext),
                    encryption_time_ns=encryption_time_ns,
                    decryption_time_ns=decryption_time_ns,
                    latency_ns=latency_ns,
                    throughput_bytes_per_s=throughput,
                    success=success
                )
            return success
        except Exception as e:
            print(f"Error during run: {e}")
            if record and self.data_writer:
                self.data_writer.write_row(
                    run_id=run_id,
                    message_size_bytes=len(plaintext),
                    encryption_time_ns=0,
                    decryption_time_ns=0,
                    latency_ns=0,
                    throughput_bytes_per_s=0.0,
                    success=False
                )
            return False
