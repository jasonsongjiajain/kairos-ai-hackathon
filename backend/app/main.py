from fastapi import FastAPI

app = FastAPI(title="Field Force Incident Assistant")


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}
