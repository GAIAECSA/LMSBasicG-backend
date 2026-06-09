import base64

import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()
KID = "gaia-lti-key-1"


def get_jwks() -> dict:
    numbers = public_key.public_numbers()

    def int_to_base64(n: int) -> str:
        b = n.to_bytes((n.bit_length() + 7) // 8, byteorder="big")
        return base64.urlsafe_b64encode(b).decode("utf-8").rstrip("=")

    jwk = {
        "kty": "RSA",
        "alg": "RS256",
        "use": "sig",
        "kid": KID,
        "n": int_to_base64(numbers.n),
        "e": int_to_base64(numbers.e),
    }
    return {"keys": [jwk]}


def sign_jwt(payload: dict) -> str:
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )
    headers = {"kid": KID}
    return jwt.encode(payload, private_pem, algorithm="RS256", headers=headers)
