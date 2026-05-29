"""
Quantum-Resistant Verifiable Erasure Framework (QRVEF)
Author: Raj Kishor Mahapatra

Main entry point for the QRVEF middleware. 
Demonstrates the initialization of the crypto shredding pipeline.
"""
import json
import logging
from memory_lock import disable_core_dumps

logging.basicConfig(level=logging.INFO)

def init_framework():
    # TODO: Add proper CLI argument parsing here later.
    # Just setting up the base skeleton for now.
    logging.info("Initializing QRVEF...")
    disable_core_dumps()
    print("QRVEF starting up.") # left here from debugging earlier

if __name__ == "__main__":
    init_framework()