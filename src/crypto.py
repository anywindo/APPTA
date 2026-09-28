import os
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import config
from src.logger import get_logger

logger = get_logger("crypto")

def generate_keypair():
    """Generates an ECDH keypair using the curve specified in config."""
    # Assuming config.ECDH_CURVE == "SECP256R1" based on Priority 2 Decision 9
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()
    logger.debug("Generated new SECP256R1 ECDH keypair.")
    return private_key, public_key

def derive_shared_key(private_key, peer_public_key):
    """Performs ECDH and HKDF-SHA256 to derive a 256-bit AES key."""
    shared_secret = private_key.exchange(ec.ECDH(), peer_public_key)
    
    # KDF: HKDF-SHA256 (Decision 10)
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=config.AES_KEY_SIZE // 8,
        salt=None,
        info=b'handshake data',
    ).derive(shared_secret)
    
    logger.debug(f"Derived {config.AES_KEY_SIZE}-bit AES key via HKDF-SHA256 from shared secret.")
    return derived_key

def encrypt(key, plaintext_bytes):
    """
    Encrypts plaintext using AES-256-GCM.
    Returns (nonce, ciphertext, tag).
    """
    aesgcm = AESGCM(key)
    nonce = os.urandom(config.NONCE_SIZE)
    # AESGCM.encrypt appends the tag to the ciphertext
    ct_with_tag = aesgcm.encrypt(nonce, plaintext_bytes, None)
    
    tag_size_bytes = config.TAG_SIZE
    ciphertext = ct_with_tag[:-tag_size_bytes]
    tag = ct_with_tag[-tag_size_bytes:]
    
    logger.debug(f"AES-256-GCM Encryption: {len(plaintext_bytes)}B plaintext -> {len(ciphertext)}B ciphertext + {len(tag)}B tag (nonce: {nonce.hex()}).")
    return nonce, ciphertext, tag

def decrypt(key, nonce, ciphertext, tag):
    """
    Decrypts ciphertext using AES-256-GCM.
    Raises an exception (InvalidTag) on authentication failure.
    """
    aesgcm = AESGCM(key)
    # Reassemble ciphertext + tag for AESGCM.decrypt
    ct_with_tag = ciphertext + tag
    try:
        plaintext = aesgcm.decrypt(nonce, ct_with_tag, None)
        logger.debug(f"AES-256-GCM Decryption SUCCESS: {len(ciphertext)}B ciphertext -> {len(plaintext)}B plaintext.")
        return plaintext
    except Exception as e:
        logger.error(f"AES-256-GCM Decryption FAILED: {str(e)}")
        raise
