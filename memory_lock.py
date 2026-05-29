"""
Quantum-Resistant Verifiable Erasure Framework (QRVEF)
Author: Raj Kishor Mahapatra

Implements OS-level memory locking (mlock) via ctypes to prevent
cryptographic keys from paging to disk swap.
"""
import ctypes
import os
import logging

try:
    import resource
except ImportError:
    resource = None

logger = logging.getLogger(__name__)

def disable_core_dumps():
    """Permanently disable core dumps at runtime to prevent key extraction."""
    if resource is not None:
        try:
            resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
            logger.info("Core dumps disabled at runtime.")
        except Exception as e:
            logger.warning(f"Failed to disable core dumps: {e}")
    else:
        logger.info("resource module not available on this OS, skipping core dump disable.")

class SecureMemoryBuffer:
    def __init__(self, size: int):
        self.size = size
        self.buffer = ctypes.create_string_buffer(size)
        self.address = ctypes.addressof(self.buffer)
        self._lock_memory()

    def _lock_memory(self):
        """Locks the memory page to prevent swapping to disk."""
        if os.name == 'posix':
            try:
                libc = ctypes.CDLL("libc.so.6")
                result = libc.mlock(ctypes.c_void_p(self.address), ctypes.c_size_t(self.size))
                if result != 0:
                    logger.error("mlock failed. Check ulimit settings.")
            except Exception as e:
                logger.error(f"Could not load libc or mlock: {e}")
        elif os.name == 'nt':
            try:
                kernel32 = ctypes.windll.kernel32
                result = kernel32.VirtualLock(ctypes.c_void_p(self.address), ctypes.c_size_t(self.size))
                if result == 0:
                    logger.error("VirtualLock failed.")
            except Exception as e:
                pass

    def write(self, data: bytes):
        if len(data) > self.size:
            raise ValueError("Data exceeds buffer size")
        ctypes.memmove(self.buffer, data, len(data))

    def read(self) -> bytes:
        return ctypes.string_at(self.address, self.size)

    def shred(self):
        """Overwrites the buffer with zeroes and unlocks it."""
        # Cryptographic wipe
        ctypes.memset(self.address, 0, self.size)
        logger.info("Secure memory buffer shredded.")
        if os.name == 'posix':
            try:
                libc = ctypes.CDLL("libc.so.6")
                libc.munlock(ctypes.c_void_p(self.address), ctypes.c_size_t(self.size))
            except Exception:
                pass
        elif os.name == 'nt':
            try:
                kernel32 = ctypes.windll.kernel32
                kernel32.VirtualUnlock(ctypes.c_void_p(self.address), ctypes.c_size_t(self.size))
            except Exception:
                pass

    def __del__(self):
        self.shred()