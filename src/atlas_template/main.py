from fastapi import FastAPI

app = FastAPI(title="Atlas Template")

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "atlas-template"}