# APPTA - Thesis Experimental Instrument

This repository contains the Python implementation of an experimental end-to-end encrypted (E2EE) one-to-one text messaging system. It serves as a measurement instrument to analyze the effect of message size on E2EE performance, using ECDH for key exchange and AES-GCM for message encryption.

## Requirements

- Python 3.9+
- Dependencies listed in `requirements.txt`

## Setup

It is recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```

## Running the Experiment

The experiment requires two components running, ideally on two separate machines on a local area network (LAN) for realistic measurements.

1.  **Start the receiver:**
    ```bash
    python receiver.py
    ```

2.  **Start the sender:**
    ```bash
    python sender.py
    ```

The sender will connect to the receiver, perform the ECDH key exchange, and automatically run the benchmark across predefined message sizes. Results will be saved to a CSV file.
