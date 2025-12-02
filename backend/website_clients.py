from abc import ABC, abstractmethod
from models import Deal, LoginResult 
import httpx
from typing import List, Optional

class BaseWebsite(ABC):
    
    @abstractmethod
    async def login(self, username: str, password: str) -> LoginResult:
        raise NotImplementedError

    @abstractmethod
    async def get_deals(self, token: str):
        raise NotImplementedError

class Fo1Websit(BaseWebsite):
    def __init__(self):
        self.api_url = "https://asd.api.altius.finance"

    async def login(self, username: str, password: str) -> LoginResult:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.api_url}/api/v0.0.2/login",
                json={"email":username, "password":password},
            )
            if resp.status_code == 401:
                raise ValueError("Invalid credentials")
            
            data = resp.json()
            success = data.get("success", {})
            token = success.get("token")
            return token

    async def get_deals(self, token: str):
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.api_url}/api/v0.0.2/deals-list",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Accept": "application/json",
                }
            )
            if resp.status_code == 401:
                raise ValueError("Unauthorized, invalid or expired token")
            
            data = resp.json()
            raw_deals = data.get("data", [])
            deals: List[Deal] = [
                    Deal(
                        id=d["id"],
                        title=d["title"],
                        status=d.get("deal_status"),
                        asset_class=d.get("asset_class"),
                        currency=d.get("currency"),
                        minimum_ticket=d.get("minimum_ticket"),
                    )
                    for d in raw_deals
                ]
            return deals



class Fo2Websit(BaseWebsite):
    def __init__(self):
        self.api_url = "https://fo2.api.altius.finance"

    async def login(self, username: str, password: str) -> LoginResult:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.api_url}/api/v0.0.2/login",
                json={"email":username, "password":password},
            )
            if resp.status_code == 401:
                raise ValueError("Invalid credentials")
            
            data = resp.json()
            success = data.get("success", {})
            token = success.get("token")
            return token

    async def get_deals(self, token: str) :
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.api_url}/api/v0.0.2/deals-cards",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Accept": "application/json",
                }
            )
            if resp.status_code == 401:
                raise ValueError("Unauthorized, invalid or expired token")
            
            data = resp.json()
            raw_deals = data.get("data", [])

            deals: List[Deal] = []
            for d in raw_deals:
                status_name = None
                if d.get("status"):
                    status_name = d["status"].get("name")

                asset_class_name = None
                if d.get("asset_class"):
                    asset_class_name = d["asset_class"].get("name")

                currency = None
                currencies = d.get("currencies") or []
                if currencies:
                    currency = currencies[0].get("value")

                minimum_ticket = d.get("minimum_ticket")
                if minimum_ticket is None:
                    minimum_ticket = d.get("min_ticket")

                deals.append(
                    Deal(
                        id=d["id"],
                        title=d["title"],
                        status=status_name,
                        asset_class=asset_class_name,
                        currency=currency,
                        minimum_ticket=minimum_ticket,
                    )
                )
            return deals

CLIENTS = {
    "fo1.altius.finance": Fo1Websit(),
    "fo2.altius.finance": Fo2Websit(),
}

def get_client(website:str):
    try:
        return CLIENTS[website]
    except KeyError:
        raise ValueError("Unsupported website: {website}")


