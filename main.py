from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Kindergarten Meal System API is running!"}
