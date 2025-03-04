from ecdsa import SigningKey, SECP256k1
from hashlib import sha256
from ecdsa import VerifyingKey, BadSignatureError, SECP256k1


# Generate a private key
private_key = SigningKey.generate(curve=SECP256k1)
public_key = private_key.verifying_key

# Serialize keys
private_key_hex = private_key.to_string().hex()
public_key_hex = public_key.to_string().hex()

# Sign the payload
payload = "my_secure_data"
hashed_payload = sha256(payload.encode()).digest()
signature = private_key.sign(hashed_payload)

# Display the results
print(f"Payload: {payload}")
print(f"Signature: {signature.hex()}")
print(f"Public Key: {public_key_hex}")
print(f"Private Key: {private_key_hex} {private_key}")

# Send payload, signature (hex), and public_key (hex) to the server



#  Validation
signature_str = signature.hex()
signature_bytes = bytes.fromhex(signature_str)
public_key_bytes = bytes.fromhex(public_key_hex)

# Hash the payload
hashed_payload = sha256(payload.encode()).digest()

# Load the public key
verifying_key = VerifyingKey.from_string(public_key_bytes, curve=SECP256k1)

# Verify the signature
verifying_key.verify(signature_bytes, hashed_payload)
