import random
import hashlib

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

q_hex = """
B10B8F96 A080E01D AE5D54EC 52C99FBC FB06A3C6
9A6A9DCA 52D23B61 6073E286 75A23D18 9838EF1E 2EE652C0
13ECB4AE A9061123 24975C3C D49B83BF ACCBDD7D 90C4BD70
98488E9C 219A7372 4EFFD6FA E5644738 FAA31A4F F55BCCC0
A151AF5F 0DC8B4BD 45BF37DF 365C1A65 E68CFDA7 6D4DA708
DF1FB2BC 2E4A4371
"""
 
g_hex = """
A4D1CBD5 C3FD3412 6765A442 EFB99905 F8104DD2 58AC507F
D6406CFF 14266D31 266FEA1E 5C41564B 777E690F 5504F213
160217B4 B01B886A 5E91547F 9E2749F4 D7FBD7D3 B9A92EE1
909D0D22 63F80A76 A6A24C08 7A091F53 1DBF0A01 69B6A28A
D662A4D1 8E73AFA3 2D779D59 18D08BC8 858F4DCE F97C2A24
855E6EEB 22B3B2E5
"""
 
q = int("".join(q_hex.split()), 16)
g = int("".join(g_hex.split()), 16)

def generate_keypair():
    private_key = random.SystemRandom().randint(2, q - 2)
    public_key = pow(g, private_key, q)
    return private_key, public_key

def shared_secret(private_key, public_key):
    return pow(public_key, private_key, q)

def derive_key(shared_secret):
    shared_secret_bytes = str(shared_secret).encode()
    key = hashlib.sha256(shared_secret_bytes).digest()[:16]
    return key

def encrypt(message, iv, key) -> bytes:
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
    return ciphertext

def decrypt(ciphertext, iv, key) -> str:
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode()

def main():
    

    # Generate key pairs for Alice and Bob
    alice_private, alice_public = generate_keypair()
    bob_private, bob_public = generate_keypair()

    print(f"Alice's private key: {alice_private}")
    print(f"Alice's public key: {alice_public}")
    print(f"Bob's private key: {bob_private}")
    print(f"Bob's public key: {bob_public}")

    # Compute shared secrets
    alice_shared_secret = shared_secret(alice_private, bob_public)
    bob_shared_secret = shared_secret(bob_private, alice_public)

    print(f"Alice's computed shared secret: {alice_shared_secret}")
    print(f"Bob's computed shared secret: {bob_shared_secret}")

    # Derive symmetric keys from shared secrets
    alice_key = derive_key(alice_shared_secret)
    bob_key = derive_key(bob_shared_secret)

    print(f"Alice's derived key:  {alice_key.hex()}")
    print(f"Bob's derived key: {bob_key.hex()}")
    print(f"Alice and Bob have the same key: {alice_key == bob_key}")
    print()

    # Encrypt a message from Alice to Bob
    m0 = "Hi Bob!"
    iv_alice = random.randbytes(16)
    c0 = encrypt(m0, iv_alice, alice_key)
 
    print(f"Alice's message: {m0}")
    print(f"Alice's IV: {iv_alice.hex()}")
    print(f"Alice's ciphertext: {c0.hex()}")
 
    bob_decrypted = decrypt(c0, iv_alice, bob_key)
    print(f"Bob's decrypted message: {bob_decrypted}")
    print()
 
    # --- Bob -> Alice ---
    m1 = "Hi Alice!"
    iv_bob = random.randbytes(16)
    c1 = encrypt(m1, iv_bob, bob_key)
 
    print(f"Bob's message: {m1}")
    print(f"Bob's IV: {iv_bob.hex()}")
    print(f"Bob's ciphertext: {c1.hex()}")
 
    alice_decrypted = decrypt(c1, iv_bob, alice_key)
    print(f"Alice's decrypted message: {alice_decrypted}")

if (__name__ == "__main__"):
    main()