
from fastapi import FastAPI
from .db import init_db
from .routers import locations, remanents, labels, export

app = FastAPI(title="Remanent Backend")

@app.on_event("startup")
def on_start():
    init_db()

app.include_router(locations.router)
app.include_router(remanents.router)
app.include_router(labels.router)
app.include_router(export.router)
