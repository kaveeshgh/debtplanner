from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Debt Planner API is running!"}
