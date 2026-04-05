from fastapi import FastAPI

app = FastAPI(title="NexGen Build API")
data: dict[str,str] = {}
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post('/register')
async def register(login:str,password:str):
    data[login] = password
    print(data)
    return data