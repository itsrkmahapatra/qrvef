"""
Quantum-Resistant Verifiable Erasure Framework (QRVEF)
Author: Raj Kishor Mahapatra

Main entry point for the QRVEF middleware. 
Demonstrates the initialization of the crypto shredding pipeline.
"""
import json
import logging
import os
from memory_lock import disable_core_dumps
from crypto_core import CryptoShredderAPI
from anti_tamper import enforce_security_profile

logging.basicConfig(level=logging.INFO)

def init_framework():
    # Enforce anti-tampering FIM on our own script before proceeding
    enforce_security_profile(os.path.abspath(__file__))

    # TODO: Add proper CLI argument parsing here later.
    # Just setting up the base skeleton for now.
    logging.info("Initializing QRVEF...")
    disable_core_dumps()
    
    shredder = CryptoShredderAPI()
    
    # Simulate an event containing PII
    sample_pii = {"user": "jane.doe", "ssn": "000-00-0000", "action": "trade_execution"}
    print(f"Ingesting payload: {sample_pii}")
    
    encrypted_event = shredder.encrypt_and_log_event(sample_pii)
    print(f"Encrypted event logged. Root hash: {shredder.merkle_tree.get_root()}")
    
    # Simulate a GDPR Article 17 Erasure Request
    print("Received GDPR erasure request. Initiating crypto-shredding...")
    shredder.verify_and_shred(encrypted_event)
    
    print("PII is now unrecoverable. Merkle tree hash chain remains intact.")

if __name__ == "__main__":
    init_framework()