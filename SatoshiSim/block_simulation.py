
import hashlib
import time
import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

def calculate_hash(data):
    """Calculates the SHA-256 hash of the given data."""
    sha256 = hashlib.sha256()
    sha256.update(str(data).encode('utf-8'))
    return sha256.hexdigest()

class Block:
    def __init__(self, index, timestamp, data, previous_hash='', nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}{self.nonce}"
        return calculate_hash(block_string)

DIFFICULTY = 4 # Target: Hash must start with '0000'

def mine_block(block, difficulty):
    """
    Simulates the Proof-of-Work mining process.
    Finds a nonce that results in a hash meeting the difficulty target.
    """
    target_prefix = '0' * difficulty
    print(f"Starting mining process for Block {block.index}...")
    
    while block.hash[0:difficulty] != target_prefix:
        block.nonce += 1
        block.hash = block.calculate_hash()

    print(f"Mining SUCCESS for Block {block.index}!")
    print(f"  Nonce Found: {block.nonce}")
    print(f"  Final Hash: {block.hash}\n")
    return block

def generate_key_pair_and_address():
    """
    Generates an ECDSA private/public key pair and a corresponding public address.
    """
    # 1. Generate a new private key using the SECP256k1 curve (same as Bitcoin)
    private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())
    
    # 2. Derive the public key
    public_key = private_key.public_key()
    
    # 3. Serialize the public key to the standard uncompressed format
    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint
    )
    
    # 4. Create the address: SHA-256 hash of the public key
    sha256 = hashlib.sha256()
    sha256.update(public_key_bytes)
    address = sha256.hexdigest()
    
    return private_key, public_key, address


class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis = Block(
            index=0, 
            timestamp=time.time(),
            data="The Genesis Block: Bitcoin Activated", 
            previous_hash="0",
            nonce=0
        )
        self.chain.append(mine_block(genesis, DIFFICULTY))

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_data):
        latest_block = self.get_latest_block()
        new_index = latest_block.index + 1
        
        new_block = Block(
            index=new_index,
            timestamp=time.time(),
            data=new_data,
            previous_hash=latest_block.hash
        )
        
        mined_block = mine_block(new_block, DIFFICULTY)
        
        self.chain.append(mined_block)
        print(f"Block {new_index} successfully added to the chain.")

# --- Test Key Generation ---
my_private_key, my_public_key, my_address = generate_key_pair_and_address()

print("\n--- Key Pair and Address Generation ---")
print(f"My Address: {my_address}")

# Note: Don't print the private key in a real application!
# For this simulation, we can serialize it to see what it looks like.
private_key_pem = my_private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
).decode('utf-8')
# print(f"\nMy Private Key (PEM Format):\n{private_key_pem}")



