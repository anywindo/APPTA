"""
Experiment configuration constants for APPTA thesis project.
"""

# Message sizes in bytes
MESSAGE_SIZES = [16, 64, 256, 1024, 4096, 16384, 65536, 262144, 1048576]

# Repetitions
MEASURED_RUNS = 30
WARMUP_RUNS = 5

# Cryptographic parameters
ECDH_CURVE = "SECP256R1"
AES_KEY_SIZE = 256  # bits
NONCE_SIZE = 12     # bytes
TAG_SIZE = 16       # bytes

# Protocol parameters
LENGTH_PREFIX_SIZE = 4  # bytes

# CSV Dataset configuration
CSV_COLUMNS = [
    "run_id",
    "message_size_bytes",
    "encryption_time_ns",
    "decryption_time_ns",
    "latency_ns",
    "throughput_bytes_per_s",
    "success",
    "timestamp_utc"
]

def validate_config():
    if not all(isinstance(x, int) and x > 0 for x in MESSAGE_SIZES):
        raise ValueError("Invalid configuration: All MESSAGE_SIZES must be positive integers")
    if not isinstance(MEASURED_RUNS, int) or MEASURED_RUNS <= 0:
        raise ValueError("Invalid configuration: MEASURED_RUNS must be a positive integer")

validate_config()
