import hashlib
import json
import base64

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_private_key


class Account:
    # Default balance is 100 if not sent during account creation
    # nonce is incremented once every transaction to ensure tx can't be replayed and can be ordered (similar to Ethereum)
    # private and public pem strings should be set inside __generate_key_pair
    def __init__(self, sender_id, balance=100):
        self._id = sender_id
        self._balance = balance
        self._nonce = 0
        self._private_pem = None
        self._public_pem = None
        self.__generate_key_pair()
        self._initial_balance = balance
        self._mock_balance = balance

    @property
    def id(self):
        return self._id

    @property
    def public_key(self):
        return self._public_pem

    @property
    def balance(self):
        return self._balance

    def increase_balance(self, value):
        self._balance += value

    def decrease_balance(self, value):
        self._balance -= value

    def increase_mock_balance(self, value):
        self._mock_balance += value

    def decrease_mock_balance(self, value):
        self._mock_balance -= value


    def __generate_key_pair(self):
        # Generating the private/public key pair
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
		# Assigning the public key from the pair
        public_key = private_key.public_key()

        # Convert them to pem format strings and store in the class attributes already defined
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        self._private_pem = private_pem
        self._public_pem = public_pem

    def create_transaction(self, receiver_id, value, tx_metadata=''):
        nonce = self._nonce + 1
        transaction_message = {'sender': self._id, 'receiver': receiver_id, 'value': value, 'tx_metadata': tx_metadata, 'nonce': nonce}

        # Derive the private key object from private PEM
        private_key = load_pem_private_key(self._private_pem, None, default_backend())

        # Generate hash of the transaction
        tmsg_string = json.dumps(transaction_message, sort_keys=True)
        encoded_tmsg_string = tmsg_string.encode('utf-8')
        hashv = hashlib.sha256(encoded_tmsg_string).hexdigest()
        hashb = bytes((hashv), 'utf-8')

        # Encrypting the hash of transaction using the private key
        encrypted_message = private_key.sign(
            hashb,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        signature = str(base64.b64encode(encrypted_message), 'utf-8')

        self._nonce = nonce
        return {'message': transaction_message, 'signature': signature}

