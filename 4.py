import base64, os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend

# AES Functions (AES-256-GCM)

def aes_gen_key() -> bytes:
    """Generate a 256-bit AES key"""
    return AESGCM.generate_key(bit_length=256)

def aes_encrypt(key: bytes, plaintext: str):
    """Encrypt text with AES-GCM"""
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)  # 96-bit nonce
    ct = aesgcm.encrypt(nonce, plaintext.encode(), None)
    ciphertext, tag = ct[:-16], ct[-16:]
    return (base64.b64encode(ciphertext).decode(),
            base64.b64encode(nonce).decode(),
            base64.b64encode(tag).decode())

def aes_decrypt(key: bytes, ciphertext_b64: str, nonce_b64: str, tag_b64: str) -> str:
    """Decrypt AES-GCM ciphertext"""
    aesgcm = AESGCM(key)
    ciphertext = base64.b64decode(ciphertext_b64)
    nonce = base64.b64decode(nonce_b64)
    tag = base64.b64decode(tag_b64)
    pt = aesgcm.decrypt(nonce, ciphertext + tag, None)
    return pt.decode()

# RSA Functions (RSA-2048 with OAEP-SHA256)

def rsa_gen_keys():
    """Generate RSA private and public key pair"""
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key

def rsa_encrypt(public_key, plaintext: str) -> str:
    """Encrypt text with RSA-OAEP"""
    ciphertext = public_key.encrypt(
        plaintext.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.b64encode(ciphertext).decode()

def rsa_decrypt(private_key, ciphertext_b64: str) -> str:
    """Decrypt RSA-OAEP ciphertext"""
    ciphertext = base64.b64decode(ciphertext_b64)
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext.decode()

# DEMO SECTION

print("--- AES Demo ---")
aes_key = aes_gen_key()
print("AES Key (base64):", base64.b64encode(aes_key).decode())

ciphertext_aes, nonce, tag = aes_encrypt(aes_key, "Hello World")
print("Ciphertext:", ciphertext_aes)
print("Nonce:", nonce)
print("Tag:", tag)

plaintext_aes = aes_decrypt(aes_key, ciphertext_aes, nonce, tag)
print("Decrypted:", plaintext_aes)

print("\n--- RSA Demo ---")
private_key, public_key = rsa_gen_keys()
ciphertext_rsa = rsa_encrypt(public_key, "Hello World ")
print("Ciphertext:", ciphertext_rsa)

plaintext_rsa = rsa_decrypt(private_key, ciphertext_rsa)
print("Decrypted:", plaintext_rsa)
