from fastapi import FastAPI

from backend.app.api.users import router as user_router

app=FastAPI(
    title="FINNECT Finance OS",
    version="1.0.0",
    description="Digital operating system for local finance businesses."
)

app.include_router(user_router)

@app.get("/")
def root():
    return{
        "project":"FINNECT Finance OS",
        "status":"Running"
    }