import struct
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
import config

def package(nonce, ciphertext, tag):
    """
    Packages nonce, ciphertext, and tag with a 4-byte length prefix.
    Length prefix covers the entire payload length.
    """
    payload = nonce + ciphertext + tag
    # 4-byte big-endian payload length
    length_prefix = struct.pack(">I", len(payload))
    return length_prefix + payload

def unpackage(data):
    """
    Unpackages data into nonce, ciphertext, and tag.
    Note: 'data' is the payload *without* the length prefix.
    """
    nonce_size = config.NONCE_SIZE
    tag_size = config.TAG_SIZE
    
    if len(data) < nonce_size + tag_size:
        raise ValueError("Data too short")
        
    nonce = data[:nonce_size]
    tag = data[-tag_size:]
    ciphertext = data[nonce_size:-tag_size]
    
    return nonce, ciphertext, tag

def serialize_public_key(public_key):
    """Serializes a public key to bytes for transmission."""
    return public_key.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint
    )

def deserialize_public_key(data):
    """Deserializes a public key from bytes."""
    return ec.EllipticCurvePublicKey.from_encoded_point(
        ec.SECP256R1(), data
    )

def pack_ack(success: bool, decryption_time_ns: int) -> bytes:
    """Packs success flag (1 byte) and decryption time (8 bytes) into an ACK payload."""
    flag = 1 if success else 0
    return struct.pack(">B Q", flag, decryption_time_ns)

def unpack_ack(payload: bytes):
    """Unpacks ACK payload into (success_flag, decryption_time_ns)."""
    if len(payload) != 9:
        raise ValueError("Invalid ACK payload length")
    flag, dec_time = struct.unpack(">B Q", payload)
    return bool(flag), dec_time

