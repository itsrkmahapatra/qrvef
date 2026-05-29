# Quantum-Resistant Verifiable Erasure Framework (QRVEF)

Hey everyone. We built this tool because trying to satisfy GDPR erasure requests across distributed database backups was an absolute nightmare. When you have PII scattered across ML training sets, edge nodes, and immutable trading logs (looking at you, MiFID II), trying to do a traditional byte-level delete just fractures your audit trails.

QRVEF is a Python middleware that implements verifiable crypto-shredding. It satisfies NIST SP 800-88 "Purge" requirements by encrypting payloads and surgically destroying the Data Encryption Keys (DEKs), leaving your Merkle-tree event logs fully intact while turning the PII into cryptographically secure noise. 

We also got tired of memory extraction attacks on our keys, so we wired up direct OS-level memory locking (`mlock`) to bypass Python's garbage collector.

### Features
- Verifiable Crypto-Shredding (AES-256-GCM)
- In-memory Append-Only Merkle Trees for audit trails
- Extreme Memory Protection (`mlock`/`munlock`)
- Anti-tampering & Debugger evasion
- Designed for hybrid Post-Quantum Cryptography (FIPS 203 / 204 integration ready)

### Setup

Install the requirements (we kept it strictly open-source):
```bash
pip install -r requirements.txt
```

*Note: If you're running this on Linux, make sure your `ulimit -l` is configured correctly, otherwise the memory locking will throw an OS error.*

### Usage
Check out `main.py` for a basic run-through of encrypting an event and then shredding the key.

### Author
Raj Kishor Mahapatra