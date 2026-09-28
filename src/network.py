import socket
import struct
from src import crypto
from src import protocol

def read_exactly(sock, num_bytes):
    data = b''
    while len(data) < num_bytes:
        chunk = sock.recv(num_bytes - len(data))
        if not chunk:
            raise ConnectionError("Socket closed prematurely")
        data += chunk
    return data

class Receiver:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.conn = None
        self.session_key = None
        
    def start(self, timeout=30.0):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        self.server_socket.settimeout(timeout)
        self.conn, addr = self.server_socket.accept()
        self.conn.settimeout(timeout)
        
    def handshake(self):
        # Generate own keypair
        priv_key, pub_key = crypto.generate_keypair()
        pub_bytes = protocol.serialize_public_key(pub_key)
        
        # Receive peer's public key
        len_prefix = read_exactly(self.conn, 4)
        peer_pub_len = struct.unpack(">I", len_prefix)[0]
        peer_pub_bytes = read_exactly(self.conn, peer_pub_len)
        peer_pub_key = protocol.deserialize_public_key(peer_pub_bytes)
        
        # Send own public key
        self.conn.sendall(struct.pack(">I", len(pub_bytes)) + pub_bytes)
        
        # Derive shared key
        self.session_key = crypto.derive_shared_key(priv_key, peer_pub_key)
        
    def receive_message(self):
        """Reads a length-prefixed frame from the socket and returns raw payload."""
        len_prefix = read_exactly(self.conn, 4)
        msg_len = struct.unpack(">I", len_prefix)[0]
        payload = read_exactly(self.conn, msg_len)
        return payload
        
    def send_ack(self, payload=b"ACK"):
        """Sends a lightweight ACK response (length prefixed)."""
        data = struct.pack(">I", len(payload)) + payload
        self.conn.sendall(data)
        
    def close(self):
        if self.conn:
            self.conn.close()
        self.server_socket.close()

class Sender:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.session_key = None
        
    def connect(self):
        self.sock.connect((self.host, self.port))
        
    def handshake(self):
        # Generate own keypair
        priv_key, pub_key = crypto.generate_keypair()
        pub_bytes = protocol.serialize_public_key(pub_key)
        
        # Send own public key
        self.sock.sendall(struct.pack(">I", len(pub_bytes)) + pub_bytes)
        
        # Receive peer's public key
        len_prefix = read_exactly(self.sock, 4)
        peer_pub_len = struct.unpack(">I", len_prefix)[0]
        peer_pub_bytes = read_exactly(self.sock, peer_pub_len)
        peer_pub_key = protocol.deserialize_public_key(peer_pub_bytes)
        
        # Derive shared key
        self.session_key = crypto.derive_shared_key(priv_key, peer_pub_key)
        
    def send_message(self, data):
        """Sends pre-packaged (length-prefixed) data over the socket."""
        self.sock.sendall(data)
        
    def receive_ack(self):
        len_prefix = read_exactly(self.sock, 4)
        ack_len = struct.unpack(">I", len_prefix)[0]
        payload = read_exactly(self.sock, ack_len)
        return payload
        
    def close(self):
        self.sock.close()
