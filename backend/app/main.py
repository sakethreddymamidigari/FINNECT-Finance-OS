from fastapi import FastAPI

app=FastAPI(
    title="FINNECT Finance OS",
    version="1.0.0",
    description="Digital operating system for local finance businesses."
)

@app.get("/")
def root():
    return{
        "project":"FINNECT Finance OS",
        "status":"Running"
    }