import unittest
import threading
import time
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.network import Receiver, Sender
from src import crypto
from src import protocol

class TestNetwork(unittest.TestCase):
    def test_network_exchange(self):
        host = '127.0.0.1'
        port = 5555
        
        receiver = Receiver(host, port)
        sender = Sender(host, port)
        
        received_plaintext = None
        received_ack = None
        error = None
        
        def receiver_thread():
            nonlocal received_plaintext, error
            try:
                receiver.start()
                receiver.handshake()
                payload = receiver.receive_message()
                nonce, ciphertext, tag = protocol.unpackage(payload)
                received_plaintext = crypto.decrypt(receiver.session_key, nonce, ciphertext, tag)
                receiver.send_ack(b"ACK")
            except Exception as e:
                error = e
            finally:
                receiver.close()
                
        t = threading.Thread(target=receiver_thread)
        t.start()
        
        # Give server a moment to bind and listen
        time.sleep(0.1)
        
        try:
            sender.connect()
            sender.handshake()
            
            test_msg = b"network test message"
            nonce, ciphertext, tag = crypto.encrypt(sender.session_key, test_msg)
            data = protocol.package(nonce, ciphertext, tag)
            sender.send_message(data)
            
            received_ack = sender.receive_ack()
        finally:
            sender.close()
            
        t.join(timeout=2.0)
        
        self.assertIsNone(error)
        self.assertEqual(received_plaintext, b"network test message")
        self.assertEqual(received_ack, b"ACK")
        self.assertEqual(sender.session_key, receiver.session_key)

    def test_multiple_messages(self):
        host = '127.0.0.1'
        port = 5556
        
        receiver = Receiver(host, port)
        sender = Sender(host, port)
        
        received_messages = []
        error = None
        
        messages_to_send = [b"msg1", b"msg2", b"msg3"]
        
        def receiver_thread():
            nonlocal error
            try:
                receiver.start()
                receiver.handshake()
                for _ in range(len(messages_to_send)):
                    payload = receiver.receive_message()
                    nonce, ciphertext, tag = protocol.unpackage(payload)
                    pt = crypto.decrypt(receiver.session_key, nonce, ciphertext, tag)
                    received_messages.append(pt)
                    receiver.send_ack(b"ACK")
            except Exception as e:
                error = e
            finally:
                receiver.close()
                
        t = threading.Thread(target=receiver_thread)
        t.start()
        time.sleep(0.1)
        
        try:
            sender.connect()
            sender.handshake()
            
            for msg in messages_to_send:
                nonce, ciphertext, tag = crypto.encrypt(sender.session_key, msg)
                data = protocol.package(nonce, ciphertext, tag)
                sender.send_message(data)
                sender.receive_ack()
                
        finally:
            sender.close()
            
        t.join(timeout=2.0)
        
        self.assertIsNone(error)
        self.assertEqual(received_messages, messages_to_send)

if __name__ == '__main__':
    unittest.main()
