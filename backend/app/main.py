from fastapi import FastAPI

from app.api.assistant import router as assistant_router
from app.api.auth import router as auth_router
from app.api.customers import router as customers_router
from app.api.events import router as events_router
from app.api.knowledge import router as knowledge_router
from app.api.tickets import router as tickets_router

app = FastAPI(title="Field Force Incident Assistant")
app.include_router(auth_router)
app.include_router(events_router)
app.include_router(tickets_router)
app.include_router(assistant_router)
app.include_router(customers_router)
app.include_router(knowledge_router)


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}
