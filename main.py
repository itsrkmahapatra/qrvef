"""
Quantum-Resistant Verifiable Erasure Framework (QRVEF)
Author: Raj Kishor Mahapatra

Main entry point for the QRVEF middleware. 
Demonstrates the initialization of the Hybrid PQC pipeline and ZKP auditing.
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

    logging.info("Initializing QRVEF 2.0 (Hybrid PQC + ZKP Auditing)...")
    disable_core_dumps()
    
    shredder = CryptoShredderAPI()
    
    # Simulate an event containing PII (e.g., from an Algorithmic Trading Adapter)
    sample_trade = {
        "user": "raj.mahapatra", 
        "trade_id": "TXN-99012", 
        "symbol": "BTCUSD", 
        "action": "BUY",
        "volume": 0.5,
        "price": 68500.00
    }
    print(f"\n[Ingestion] Processing trade log: {sample_trade}")
    
    # Derives Hybrid DEK (X25519 + ML-KEM-768)
    encrypted_event = shredder.encrypt_and_log_event(sample_trade)
    print(f"[Ledger] Event Hash: {encrypted_event['event_hash']}")
    print(f"[Ledger] Merkle Root: {shredder.merkle_tree.get_root()}")
    
    # Simulate a GDPR Article 17 Erasure Request
    print("\n[Compliance] Received GDPR erasure request for user 'raj.mahapatra'...")
    
    # Destroys key and generates ZKP Erasure Certificate
    certificate = shredder.verify_and_shred(encrypted_event)
    
    print("\n[Compliance] PII is now unrecoverable (NIST SP 800-88 Purge).")
    print("[Compliance] Generated ZKP Erasure Certificate:")
    print(json.dumps(certificate, indent=2))
    
    print("\nQRVEF: Paradox Resolved (GDPR vs MiFID II). Audit trail remains intact.")

if __name__ == "__main__":
    init_framework()