from fastapi import FastAPI, HTTPException
from models import LoginRequest, LoginResponse, LoginResult
from website_clients import get_client 
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/get_data")
async def execute(req: LoginRequest, response_model=LoginResponse):
    try:
        client = get_client(req.website)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    token = await client.login(req.username, req.password)
    deals = await client.get_deals(token)
    return LoginResponse(
        website=req.website,
        token=token,
        deals=deals,
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)