# SHA-256 implementation will go here.
import hashlib
import time
import json  # We will use this later to serialize block data consistently

def calculate_hash(data_string):
    """
    Calculates the SHA-256 hash of a given string.
    """
    # Hash functions require bytes, so we encode the string first
    return hashlib.sha256(data_string.encode('utf-8')).hexdigest()

# --- Simple Test ---
test_data = "Hello, Satoshi!"
test_hash = calculate_hash(test_data)
print(f"Test Data: {test_data}")
print(f"SHA-256 Hash: {test_hash}")