import secrets


def generate_secret_key():
    return secrets.token_hex(32)  # Generates a 64-character random key


print(generate_secret_key())
