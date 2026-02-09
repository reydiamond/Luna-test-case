from fastapi import FastAPI, Depends

from app.dependencies import verify_api_key
from app.api import organisations

app = FastAPI(
    title="Organisations API",
    dependencies=[Depends(verify_api_key)]
)

app.include_router(organisations.router, prefix="", tags=["Organisations"])
