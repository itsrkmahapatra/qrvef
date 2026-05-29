# Quantum-Resistant Verifiable Erasure Framework (QRVEF)

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python: 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)
![Security: NIST SP 800-88](https://img.shields.io/badge/Security-NIST%20SP%20800--88-red.svg)
![Compliance: GDPR Article 17](https://img.shields.io/badge/Compliance-GDPR%20Article%2017-green.svg)
![PQC: FIPS 203](https://img.shields.io/badge/PQC-FIPS%20203-blueviolet.svg)

**QRVEF** is a mission-critical Python middleware designed to resolve the paradox between the **GDPR Right to Erasure** and **MiFID II Immutable Logging** mandates. By utilizing hybrid post-quantum crypto-shredding, QRVEF enables organizations to surgically destroy PII while maintaining a mathematically perfect audit trail.

---

## 🌐 Live Architecture Page
View our interactive whitepaper and visual paradox resolution at:
**[https://itsrkmahapatra.github.io/qrvef/](https://itsrkmahapatra.github.io/qrvef/)**

---

## 🚀 Key Features

- **Hybrid Post-Quantum KEM (FIPS 203)**: Defense-in-depth combining X25519 and ML-KEM-768 to protect against "harvest now, decrypt later" attacks.
- **IETF SCITT Alignment**: Events are structured as `COSE_Sign1` envelopes for interoperability with global transparency services.
- **zk-STARK Auditing**: Post-quantum, hash-based Zero-Knowledge Proofs (STARKs) for verifiable erasure without trusted setups.
- **Hardware Enclave (HSM) Adapters**: Modular support for AWS CloudHSM and Azure Key Vault (FIPS 140-2/3 Level 3).
- **Impervious Runtime Security**: 
  - Kernel-level memory locking (`mlock`) via `ctypes`.
  - Nuitka-compiled standalone C binaries for anti-tampering.
  - Runtime debugger evasion and Self-Hashing File Integrity Monitoring (FIM).

---

## 🛠️ Quick Start

### 1. Installation
QRVEF relies on standard, open-source cryptographic libraries.
```bash
git clone https://github.com/itsrkmahapatra/qrvef.git
cd qrvef
pip install -r requirements.txt
```

### 2. Execution
Run the demo to ingest a trade log and execute a verifiable crypto-shredding purge.
```bash
python main.py
```

### 3. Sidecar Adapter
Start the FastAPI adapter for MT5/MQL5 or external algorithmic engine integration.
```bash
python adapter.py
```

---

## 🏗️ Architectural Flow

1. **Ingestion**: Payload is received via Sidecar Adapter.
2. **Encryption**: A Hybrid DEK (ML-KEM + X25519) is generated and locked in protected RAM.
3. **Logging**: The encrypted event is wrapped in a SCITT COSE_Sign1 envelope and appended to an immutable Merkle tree.
4. **Erasure**: Upon request, the specific DEK is shredded in the HSM/RAM.
5. **Certification**: A zk-STARK proof is generated, proving the deletion occurred while the log's hash chain remains valid.

---

## 🗺️ Future Roadmap

- [ ] **Native C++ Core**: Transitioning high-performance cryptographic operations to a dedicated C++ engine.
- [ ] **VeritasChain Integration**: Direct support for the VeritasChain transparency protocol.
- [ ] **Multi-Tenant Sharding**: Scalable vaulting for global-scale financial data subjects.

---

## 💖 Support the Project
If you find QRVEF useful for your compliance or security needs, consider supporting its development. You can donate via the **"Donate via UPI"** button on the [Live Architecture Page](https://itsrkmahapatra.github.io/qrvef/).

---

## ⚖️ License & Attribution

- **Author**: Raj Kishor Mahapatra
- **License**: MIT
- **Copyright**: © 2026 Raj Kishor Mahapatra. All Rights Reserved.

*Disclaimer: QRVEF is a specialized middleware. Always consult with legal and compliance experts regarding specific regulatory requirements in your jurisdiction.*
