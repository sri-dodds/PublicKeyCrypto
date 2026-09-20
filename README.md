Task 1
• Implement Diffie-Hellman protocol with q=37 and g=5
• Generate random private keys XA and XB
• Compute public keys YA and YB
• Calculate shared secret ‘s’ for both parties
• Apply SHA256 to ‘s’ and truncate to 16 bytes to get key ‘k’
• Implement AES-CBC encryption with the derived key
• Verify Alice and Bob compute identical symmetric keys
• Exchange encrypted messages "Hi Bob!" and "Hi Alice!"
• Modify implementation to use IETF-suggested 1024-bit parameters
• Handle the large values of ‘q’ and ‘g’ provided in the assignment
• Verify both parties can derive the same symmetric key
• Successfully exchange encrypted messages


Task 2: Implement MITM Key Fixing & Negotiated Groups
 Requirements
• Modify the original implementation to simulate a MITM attack
• Implement Mallory as the attacker who replaces ‘YA’ and ‘YB’ with ‘q’
• Demonstrate how Mallory can determine the shared secret s
• Show Mallory can decrypt messages ‘c0’ and ‘c1’
• Implement another MITM attack where Mallory tampers with generator ‘g’
• Test setting ‘g’ to ‘1’, ‘q’, and ‘q-1’
• Demonstrate how Mallory can recover ‘m0’ and ‘m1’ from ciphertexts Diagram:


Task 3: Implement "Textbook" RSA & MITM Key Fixing via Malleability Task 3
• Implement RSA key generation supporting variable-length primes up to 2048 bits
• Use ‘e=65537’ as the public exponent
• Implement the calculation of the multiplicative inverse (for private key)
• Convert messages to integers in Z*n (less than n)
• Test encryption and decryption of messages
• Alice encrypts a symmetric key s as c = s^e mod n
• Mallory modifies c → c′ = c * (r^e mod n) (e.g., r = 2)
• Bob decrypts c′, gets s′ = s * r
• Mallory recovers s = s′ * r⁻¹ mod n
• Use k = SHA256(s), decrypt AES-CBC encrypted m
1. Implement RSA key generation:
o Generate two large primes p and q o Compute modulus n = p * q o
Compute Euler’s totient φ(n) = (p-1)*(q-1) o Use public exponent e =
65537
o Compute private key d = e⁻¹ mod φ(n) using the Extended Euclidean Algorithm
2. Implement RSA signing function:
o Input: message m (as integer), private key (n, d) o Output: signature s = m^d
mod n
3. Implement RSA verification function:
o Input: message m, signature s, public key (n, e) o Output: Boolean indicating
whether s^e mod n == m
4. Sign two messages:
o Choose two distinct integer messages m1 and m2 such that both are in ℤₙ* o
Compute their signatures: s1 = m1^d mod n, s2 = m2^d mod n
5. Mallory creates a forged signature: o Compute m3 = m1 * m2 mod n o
Compute s3 = s1 * s2 mod n o This works because: (s1 * s2)^e mod n ==
(m1 * m2) mod n
6. Verify the forged signature:
o Confirm that verify(m3, s3, public_key) returns True
7. Explain why this demonstrates RSA signature malleability:
o Show that a valid signature for m3 = m1 * m2 can be created without signing m3
directly
o Conclude that textbook RSA signatures are multiplicatively malleable