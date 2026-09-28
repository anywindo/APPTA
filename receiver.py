import sys
import socket
from src.network import Receiver
from src import crypto
from src import protocol
from src.timing import Timer

def main():
    host = '127.0.0.1'
    port = 5000
    
    receiver = Receiver(host, port)
    print(f"Starting receiver on {host}:{port}...")
    try:
        receiver.start()
        print("Sender connected.")
        receiver.handshake()
        print("ECDH Handshake complete. Waiting for messages...")
        
        messages_received = 0
        
        while True:
            payload = receiver.receive_message()
            
            with Timer() as dec_timer:
                nonce, ciphertext, tag = protocol.unpackage(payload)
                try:
                    plaintext = crypto.decrypt(receiver.session_key, nonce, ciphertext, tag)
                    success = True
                except Exception as e:
                    success = False
                    plaintext = b""
            
            if len(plaintext) == 0 and success:
                # 0-byte plaintext is the STOP signal
                print(f"Received STOP signal. Total messages processed: {messages_received}")
                break
                
            decryption_time_ns = dec_timer.elapsed_ns
            
            ack_payload = protocol.pack_ack(success, decryption_time_ns)
            receiver.send_ack(ack_payload)
            messages_received += 1
            
    except socket.timeout:
        print("Receiver timeout reached. Graceful shutdown.")
    except ConnectionError:
        print(f"Connection lost mid-experiment. Graceful shutdown, partial results valid. Processed: {messages_received}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        receiver.close()

if __name__ == "__main__":
    main()
