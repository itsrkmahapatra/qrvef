"""
Quantum-Resistant Verifiable Erasure Framework (QRVEF)
Author: Raj Kishor Mahapatra

Implements highly aggressive anti-tampering and environmental evasion:
- Debugger detection (sys.gettrace / breakpointhook)
- Container/Sandbox detection
- Self-hashing File Integrity Monitoring (FIM)
"""
import sys
import os
import hashlib
import logging

logger = logging.getLogger(__name__)

# Hardcoded baseline hash of main.py for FIM (this would normally be dynamically injected during build)
# To simulate this, we'll allow an environment variable or fallback to a dynamic read if it's "DEV" mode.
EXPECTED_HASH = os.environ.get("QRVEF_EXPECTED_HASH", None)

def detect_debugger():
    """Detects if a debugger is attached via sys trace hooks."""
    gettrace = getattr(sys, 'gettrace', None)
    
    if gettrace is not None and gettrace() is not None:
        logger.critical("Debugger detected via sys.gettrace(). Terminating execution.")
        _retaliatory_kill()
        
    if getattr(sys, 'breakpointhook', None).__module__ != 'sys':
        logger.critical("Debugger detected via sys.breakpointhook. Terminating execution.")
        _retaliatory_kill()

def _retaliatory_kill():
    """Aggressively terminates the process."""
    if os.name == 'nt':
        try:
            sys.exit(0xC000001F)
        except Exception:
            sys.exit(1)
    else:
        sys.exit(1)

def detect_container():
    """Fingerprints the environment to determine if it's running in a Docker container."""
    if os.path.exists('/.dockerenv'):
        logger.error("Execution within a Docker container detected (/.dockerenv). Virtualization blocked.")
        sys.exit(1)
        
    try:
        with open('/proc/self/cgroup', 'r') as f:
            if 'docker' in f.read():
                logger.error("Execution within a Docker container detected (/proc/self/cgroup). Virtualization blocked.")
                sys.exit(1)
    except FileNotFoundError:
        pass

def enforce_fim(file_path: str):
    """Computes a runtime hash of the provided file and checks it against a baseline."""
    # To prevent brute-forcing, we would use PBKDF2 here, but SHA-256 for demo
    if not os.path.exists(file_path):
        return
        
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
        
    current_hash = hasher.hexdigest()
    logger.debug(f"Computed FIM hash for {file_path}: {current_hash}")
    
    # In a real deployed artifact, EXPECTED_HASH would be hardcoded.
    if EXPECTED_HASH and current_hash != EXPECTED_HASH:
        logger.critical(f"File Integrity Monitor (FIM) failure! {file_path} has been modified.")
        sys.exit(1)

def enforce_security_profile(main_file: str):
    """Runs all environmental and integrity checks."""
    detect_debugger()
    detect_container()
    enforce_fim(main_file)
    logger.info("Security profile enforced. Environment is clean.")
