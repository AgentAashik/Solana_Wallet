import base58
import os
from solders.keypair import Keypair
from solana.rpc.api import Client
from solders.transaction import Transaction
from solders.system_program import TransferParams, transfer
from solders.rpc.responses import GetLatestBlockhashResp
from solders.message import Message
from solana.rpc.commitment import Commitment
from solders.transaction import VersionedTransaction
from solders.message import MessageV0
from solders.pubkey import Pubkey  # Ensure this import is correct



# Connect to Solana Devnet
solana_client = Client("https://api.devnet.solana.com")

# ✅ Generate a new Solana wallet
def create_wallet():
    wallet = Keypair()  # Generate a new keypair
    public_key = wallet.pubkey()
    private_key = wallet.to_bytes()  # Get private key as bytes

    # Convert private key to base58 encoding for easy storage
    private_key_b58 = base58.b58encode(private_key).decode("utf-8")

    print(f"Public Key: {public_key}")
    print(f"Private Key: {private_key_b58} (Save this securely!)")
    return public_key, private_key_b58

# ✅ Fetch SOL balance
def get_balance(address):
    try:
        response = solana_client.get_balance(Pubkey.from_string(address))

        # Debugging Output
        print("Raw balance response:", response)

        # Handle the response format correctly
        if hasattr(response, 'value') and response.value is not None:
            return response.value / 1_000_000_000  # Convert lamports to SOL
        else:
            return "ERROR: Unable to fetch balance."
    except Exception as e:
        return f"ERROR: {str(e)}"


# ✅ Send SOL transaction

def send_transaction(private_key, to_address, amount):
    sender_keypair = Keypair.from_bytes(base58.b58decode(private_key))
    sender_pubkey = sender_keypair.pubkey()

    # Check sender's balance
    balance_resp = solana_client.get_balance(sender_pubkey)
    balance = balance_resp.value / 1e9  # Convert lamports to SOL

    if balance < amount:
        print(f"❌ ERROR: Insufficient funds! Your balance is {balance} SOL, but you tried to send {amount} SOL.")
        return

    # Get latest blockhash
    blockhash_resp = solana_client.get_latest_blockhash()
    recent_blockhash = blockhash_resp.value.blockhash

    # Create transfer instruction
    transfer_instruction = transfer(
        TransferParams(
            from_pubkey=sender_pubkey,
            to_pubkey=PublicKey.from_string(to_address),
            lamports=int(amount * 1e9),  # Convert SOL to lamports
        )
    )

    # Create a MessageV0 object
    message = MessageV0.try_compile(sender_pubkey, [transfer_instruction], [], recent_blockhash)

    # Create a VersionedTransaction
    txn = VersionedTransaction(message, [sender_keypair])

    # Send transaction
    txn_resp = solana_client.send_transaction(txn)

    print(f"✅ Transaction successful! Txn Hash: {txn_resp.value}")
    return txn_resp.value
