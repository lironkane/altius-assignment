from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import LoginRequest, LoginResponse
from websites.registry import get_client
from services.crawler_service import CrawlerService

from core.errors import InvalidCredentialsError, UpstreamServiceError, UnauthorizedTokenError

app = FastAPI()
service = CrawlerService()

origins = ["http://localhost:5173", "http://127.0.0.1:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/get_data", response_model=LoginResponse)
async def get_data(req: LoginRequest):
    try:
        client = get_client(req.website)
        token, deals = await service.get_data(client, req.username, req.password)
        return LoginResponse(website=req.website, token=token, deals=deals)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except InvalidCredentialsError:
        # ✅ normalized
        raise HTTPException(status_code=401, detail="Invalid username or password")

    except UnauthorizedTokenError:
        raise HTTPException(status_code=401, detail="Unauthorized")

    except UpstreamServiceError:
        raise HTTPException(status_code=502, detail="Upstream service error")

    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected server error")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)