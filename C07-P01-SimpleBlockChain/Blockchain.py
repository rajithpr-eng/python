import json
import hashlib
import base64

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.exceptions import InvalidSignature

from Block import Block


class Blockchain:
    # Basic blockchain init
    # Includes the chain as a list of blocks in order, pending transactions, and known accounts
    # Includes the current value of the hash target. It can be changed at any point to vary the difficulty
    # Also initiates a genesis block
    def __init__(self, hash_target):
        self._chain = []
        self._pending_transactions = []
        self._chain.append(self.__create_genesis_block())
        self._hash_target = hash_target
        self._accounts = {}

    def __str__(self):
        return f"Chain:\n{self._chain}\n\nPending Transactions: {self._pending_transactions}\n"

    @property
    def hash_target(self):
        return self._hash_target

    @hash_target.setter
    def hash_target(self, hash_target):
        self._hash_target = hash_target

    # Creating the genesis block, taking arbitrary previous block hash since there is no previous block
    # Using the famous bitcoin genesis block string here :)  
    def __create_genesis_block(self):
        genesis_block = Block(0, [], 'The Times 03/Jan/2009 Chancellor on brink of second bailout for banks', 
            None, 'Genesis block using same string as bitcoin!')
        return genesis_block

    def __validate_transaction(self, transaction):
        # Serialize transaction data with keys ordered, and then convert to bytes format
        hash_string = json.dumps(transaction['message'], sort_keys=True)
        encoded_hash_string = hash_string.encode('utf-8')
        
        # Take sha256 hash of the serialized message, and then convert to bytes format
        message_hash = hashlib.sha256(encoded_hash_string).hexdigest()
        encoded_message_hash = message_hash.encode('utf-8')

        # Signature - Encode to bytes and then Base64 Decode to get the original signature format back 
        signature = base64.b64decode(transaction['signature'].encode('utf-8'))

        try:
            # Load the public_key object and verify the signature against the calculated hash
            sender_public_pem = self._accounts.get(transaction['message']['sender']).public_key
            sender_public_key = serialization.load_pem_public_key(sender_public_pem)
            sender_public_key.verify(
                                        signature,
                                        encoded_message_hash,
                                        padding.PSS(
                                            mgf=padding.MGF1(hashes.SHA256()),
                                            salt_length=padding.PSS.MAX_LENGTH
                                        ),
                                        hashes.SHA256()
                                    )
        except InvalidSignature:
            return False

        return True

    def __process_transaction_sucess(self, transaction):
        # Appropriately transfer value from the sender to the receiver
        sender = self._accounts[transaction['message']['sender']]
        receiver = self._accounts[transaction['message']['receiver']]
        value = transaction['message']['value']
        sender.decrease_balance(value)
        receiver.increase_balance(value)

    def __process_transaction_fail(self, transaction):
        # Appropriately rollback value from the sender to the receiver
        sender = self._accounts[transaction['message']['sender']]
        receiver = self._accounts[transaction['message']['receiver']]
        value = transaction['message']['value']
        receiver.decrease_balance(value)
        sender.increase_balance(value)

    def __process_transactions(self, transactions):
        count = 0
        for transaction in transactions:
            count = count + 1
            sender = self._accounts[transaction['message']['sender']]
            value = transaction['message']['value']
            # For all transactions, first check that the sender has enough
            # balance. 
            if (value > sender.balance):
                #Rollback all the transactions processed so far
                for i in range(0,count - 1) :
                    self.__process_transaction_fail(transactions[i])
                return False
            self.__process_transaction_sucess(transaction)
        return True

    def __mock_process_transactions(self, transactions):
        for transaction in transactions:
            sender = self._accounts[transaction['message']['sender']]
            value = transaction['message']['value']
            if (value > sender._mock_balance):
                return False
            receiver = self._accounts[transaction['message']['receiver']]
            sender.decrease_mock_balance(value)
            receiver.increase_mock_balance(value)
        return True

    # Creates a new block and appends to the chain
    # Also clears the pending transactions as they are part of the new block now
    def create_new_block(self):
        new_block = Block(len(self._chain), self._pending_transactions, self._chain[-1].block_hash, self._hash_target)
        if self.__process_transactions(self._pending_transactions):
            self._chain.append(new_block)
            self._pending_transactions = []
            print(f'Block {new_block} created successfully')
            return new_block
        else:
            print(f'Block creation failed due to insufficient balance in transaction')
            return False

    # Simple transaction with just one sender, one receiver, and one value
    # Created by the account and sent to the blockchain instance
    def add_transaction(self, transaction):
        if self.__validate_transaction(transaction):
            self._pending_transactions.append(transaction)
            return True
        else:
            print(f'ERROR: Transaction: {transaction} failed signature validation')
            return False


    # Run through the whole blockchain and ensure that previous hash is actually the hash of the previous block
    # Return False otherwise
    def __validate_chain_hash_integrity(self):
        for index in range(1, len(self._chain)):
            if (self._chain[index].previous_block_hash != self._chain[index - 1].hash_block()):
                print(f'Previous block hash mismatch in block index: {index}')
                return False
        return True

    # Run through the whole blockchain and ensure that block hash meets hash target criteria, and is the actual hash of the block
    # Return False otherwise
    def __validate_block_hash_target(self):
        for index in range(1, len(self._chain)):
            if (int(self._chain[index].hash_block(), 16) >= int(self._chain[index].hash_target, 16)):
                print(f'Hash target not achieved in block index: {index}')
                return False
        return True

    # Run through the whole blockchain and ensure that balances never become negative from any transaction
    # Return False otherwise
    def __validate_complete_account_balances(self):
        # Note the initial balance on the working/mock copy
        for account in self._accounts:
            self._accounts[account]._mock_balance =self._accounts[account]._initial_balance

        # Run through all the transactions and mock the transaction processing
        for index in range(1, len(self._chain)):
            if False == self.__mock_process_transactions(self._chain[index]._transactions):
                return False
        return True

    # Blockchain validation function
    # Runs through the whole blockchain and applies appropriate validations
    def validate_blockchain(self):
        if False == self.__validate_chain_hash_integrity():
            return False
        if False == self.__validate_block_hash_target():
            return False
        if False == self.__validate_complete_account_balances():
            return False

        #All validation passe, return True
        return True

    def add_account(self, account):
        self._accounts[account.id] = account

    def get_account_balances(self):
        return [{'id': account.id, 'balance': account.balance} for account in self._accounts.values()]


