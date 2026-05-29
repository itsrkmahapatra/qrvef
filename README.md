# Quantum-Resistant Verifiable Erasure Framework (QRVEF)

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python: 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)
![Security: NIST SP 800-88](https://img.shields.io/badge/Security-NIST%20SP%20800--88-red.svg)
![Compliance: GDPR Article 17](https://img.shields.io/badge/Compliance-GDPR%20Article%2017-green.svg)

**QRVEF** is a high-performance Python middleware for **Quantum-Resistant Verifiable Erasure**, **Crypto-Shredding**, and **Impervious Memory Protection**. Built for enterprises navigating GDPR, MiFID II, and the post-quantum cybersecurity landscape.

---

Hey everyone. We built this tool because trying to satisfy GDPR erasure requests across distributed database backups was an absolute nightmare. When you have PII scattered across ML training sets, edge nodes, and immutable trading logs (looking at you, MiFID II), trying to do a traditional byte-level delete just fractures your audit trails.

QRVEF is a Python middleware that implements verifiable crypto-shredding. It satisfies NIST SP 800-88 "Purge" requirements by encrypting payloads and surgically destroying the Data Encryption Keys (DEKs), leaving your Merkle-tree event logs fully intact while turning the PII into cryptographically secure noise. 

We also got tired of memory extraction attacks on our keys, so we wired up direct OS-level memory locking (`mlock`) to bypass Python's garbage collector.

### Features
- **IETF SCITT Alignment**: Native support for `COSE_Sign1` event logging and transparency service interoperability.
- **zk-STARK Post-Quantum Auditing**: Hash-based, quantum-resistant Zero-Knowledge Proofs for verifiable erasure.
- **HSM Enclave Support**: Modular adapters for AWS CloudHSM and Azure Key Vault hardware-backed security.
- **Nuitka Binary Compilation**: C-level anti-tampering and reverse-engineering protection via optimized binary builds.
- **Hybrid Post-Quantum Key Encapsulation (FIPS 203)**: Combines X25519 and ML-KEM-768.
- **FinTech Sidecar Adapter**: FastAPI-based bridge for algorithmic trading (MT5/MQL5).
- **Extreme Memory Protection**: Kernel-level `mlock` to prevent key leakage to disk.

### Setup

Install the requirements:
```bash
pip install -r requirements.txt
```

To compile a secure binary:
```bash
python nuitka_build.py
```

*Note: For the sidecar adapter, run `python adapter.py`.*

*Note: If you're running this on Linux, make sure your `ulimit -l` is configured correctly, otherwise the memory locking will throw an OS error.*

### Usage
Check out `main.py` for a basic run-through of encrypting an event and then shredding the key.

### Author
Raj Kishor Mahapatra