"""
Quantum-Resistant Verifiable Erasure Framework (QRVEF)
Author: Raj Kishor Mahapatra

Implements AES-256-GCM crypto-shredding, Merkle tree event logging,
Hybrid Post-Quantum Key Encapsulation (FIPS 203), and ZKP-based compliance auditing.
"""
import os
import hashlib
import json
import logging
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import ed25519, x25519
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from memory_lock import SecureMemoryBuffer

# PQC Imports
try:
    from mlkem.ml_kem import ML_KEM
    from mlkem.parameter_set import ML_KEM_768
except ImportError:
    ML_KEM = None
    logger = logging.getLogger(__name__)
    logger.warning("mlkem library not found. Falling back to classical-only.")

# ZKP Imports
try:
    from noknow.core import ZK
except ImportError:
    ZK = None

logger = logging.getLogger(__name__)

class MerkleTree:
    """An in-memory append-only Merkle Tree for event sequence integrity."""
    def __init__(self):
        self.leaves = []

    def append_event(self, event_hash: str):
        self.leaves.append(event_hash)
        logger.info(f"Appended event hash to Merkle Tree: {event_hash}")

    def get_root(self):
        if not self.leaves:
            return None
        current_hash = hashlib.sha256(self.leaves[0].encode()).hexdigest()
        for leaf in self.leaves[1:]:
            current_hash = hashlib.sha256((current_hash + leaf).encode()).hexdigest()
        return current_hash

class CryptoShredderAPI:
    def __init__(self):
        self.merkle_tree = MerkleTree()
        self._init_hybrid_pqc()
        self.zk_system = ZK.from_params("sha256", "secp256k1") if ZK else None

    def _init_hybrid_pqc(self):
        """Initialize both Classical (X25519) and Post-Quantum (ML-KEM) key pairs."""
        logger.info("Initializing Hybrid Post-Quantum (X25519 + ML-KEM-768) architecture...")
        
        # Classical (X25519)
        self.x25519_priv = x25519.X25519PrivateKey.generate()
        self.x25519_pub = self.x25519_priv.public_key()
        
        # Post-Quantum (ML-KEM-768)
        if ML_KEM:
            self.pqc_kem = ML_KEM(ML_KEM_768)
            self.pqc_pub, self.pqc_priv = self.pqc_kem.key_gen()
        else:
            self.pqc_kem = None

    def derive_hybrid_dek(self) -> bytes:
        """
        Derives a 256-bit DEK using a Hybrid scheme:
        SharedSecret = HKDF(Classical_SS || PQC_SS)
        For this middleware simulation, we 'encapsulate' to ourselves.
        """
        # 1. Classical (X25519) shared secret simulation
        ephemeral_priv = x25519.X25519PrivateKey.generate()
        classical_ss = ephemeral_priv.exchange(self.x25519_pub)
        
        # 2. PQC (ML-KEM-768) shared secret simulation
        if self.pqc_kem:
            pqc_ss, ciphertext = self.pqc_kem.encaps(self.pqc_pub)
        else:
            pqc_ss = b"classical_fallback_only"

        # 3. Hybrid KDF (Concatenation + HKDF)
        combined_ss = classical_ss + pqc_ss
        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b"qrvef-hybrid-dek",
        )
        return hkdf.derive(combined_ss)

    def encrypt_and_log_event(self, payload: dict) -> dict:
        """
        Derives a Hybrid DEK, encrypts the payload via AES-256-GCM,
        and logs the hash to the Merkle tree.
        """
        dek_bytes = self.derive_hybrid_dek()
        
        secure_dek = SecureMemoryBuffer(len(dek_bytes))
        secure_dek.write(dek_bytes)

        aesgcm = AESGCM(secure_dek.read())
        nonce = os.urandom(12)
        
        payload_bytes = json.dumps(payload).encode('utf-8')
        ciphertext = aesgcm.encrypt(nonce, payload_bytes, None)
        
        event_hash = hashlib.sha256(ciphertext + nonce).hexdigest()
        self.merkle_tree.append_event(event_hash)

        return {
            "ciphertext": ciphertext.hex(),
            "nonce": nonce.hex(),
            "event_hash": event_hash,
            "secure_dek": secure_dek,
            "subject_id": payload.get("user", "anonymous")
        }

    def verify_and_shred(self, event_data: dict) -> dict:
        """
        Destroys the DEK and generates a ZKP Erasure Certificate.
        """
        secure_dek = event_data.get("secure_dek")
        event_hash = event_data['event_hash']
        
        # Generate ZKP Erasure Certificate before shredding
        # We prove we had the key associated with this hash
        certificate = self._generate_erasure_certificate(event_data)
        
        if secure_dek:
            secure_dek.shred()
            logger.info(f"Crypto-shredded DEK for event {event_hash}")
            del event_data["secure_dek"]
        
        return certificate

    def _generate_erasure_certificate(self, event_data: dict) -> dict:
        """
        Generates a ZKP-backed Erasure Certificate.
        Proves 'Knowledge of DEK' without revealing it.
        """
        logger.info("Generating ZKP Erasure Certificate for audit compliance...")
        
        cert = {
            "event_hash": event_data["event_hash"],
            "subject_id": event_data["subject_id"],
            "timestamp": "2026-05-29T16:45:00Z", # Placeholder
            "method": "NIST SP 800-88 Purge (Hybrid PQC Shredding)"
        }
        
        if self.zk_system:
            # We use the raw dek_bytes as the secret for the proof
            # (In a real system, this would be a specific audit secret)
            raw_dek = event_data["secure_dek"].read().hex()
            signature = self.zk_system.create_signature(raw_dek)
            proof = self.zk_system.create_proof(raw_dek, event_data["event_hash"])
            
            cert["zk_proof"] = {
                "signature": str(signature),
                "proof": str(proof),
                "token": event_data["event_hash"]
            }
            logger.info("ZKP proof attached to certificate.")
            
        return cert
