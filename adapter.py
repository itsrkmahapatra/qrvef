"""
Quantum-Resistant Verifiable Erasure Framework (QRVEF)
Author: Raj Kishor Mahapatra

Sidecar Adapter: A lightweight FastAPI server that bridges algorithmic 
trading platforms (like MT5/MQL5) with the QRVEF middleware.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from crypto_core import CryptoShredderAPI
import logging

app = FastAPI(title="QRVEF Sidecar Adapter")
shredder = CryptoShredderAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IngestPayload(BaseModel):
    user: str
    trade_id: str
    symbol: str
    action: str
    volume: float
    price: float

class ShredRequest(BaseModel):
    event_hash: str
    # Reference to the encrypted event object (in a real system, this comes from a DB)
    # For the sidecar, we'll maintain a simple in-memory cache for the demo.
    
# In-memory store for demo purposes
event_store = {}

@app.post("/ingest")
async def ingest_trade(payload: IngestPayload):
    """
    Encrypts a trade log and stores the event.
    MQL5 would call this via WebRequest.
    """
    try:
        event_data = shredder.encrypt_and_log_event(payload.model_dump())
        event_hash = event_data["event_hash"]
        event_store[event_hash] = event_data
        
        return {
            "status": "success",
            "event_hash": event_hash,
            "merkle_root": shredder.merkle_tree.get_root()
        }
    except Exception as e:
        logger.error(f"Ingestion failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/shred")
async def shred_pii(request: ShredRequest):
    """
    Executes crypto-shredding for a specific event hash.
    Used for GDPR Article 17 compliance.
    """
    event_data = event_store.get(request.event_hash)
    if not event_data:
        raise HTTPException(status_code=404, detail="Event hash not found in active store.")
    
    try:
        certificate = shredder.verify_and_shred(event_data)
        # In a real system, we'd archive the certificate and purge the store
        del event_store[request.event_hash]
        
        return {
            "status": "shredded",
            "certificate": certificate
        }
    except Exception as e:
        logger.error(f"Shredding failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "impervious", "pqc": shredder.pqc_kem is not None}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
