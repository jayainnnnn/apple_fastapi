# start.py
import uvicorn

if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=3009, reload=True)
