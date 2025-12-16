from typing import List
from models import Deal
from core.http_client import HttpJsonClient
from core.errors import UnauthorizedTokenError
from websites.base import BaseWebsite


class Fo1Website(BaseWebsite):
    def __init__(self, http: HttpJsonClient):
        self._http = http
        self._api_url = "https://asd.api.altius.finance"

    async def login(self, username: str, password: str) -> str:
        data = await self._http.post_json(
            f"{self._api_url}/api/v0.0.2/login",
            json={"email": username, "password": password},
        )
        token = (data.get("success") or {}).get("token")
        if not token:
            # אם הם שינו פורמט – תעדיף להיכשל ברור
            raise UnauthorizedTokenError("Login succeeded but token missing")
        return token

    async def get_deals(self, token: str) -> List[Deal]:
        data = await self._http.post_json(
            f"{self._api_url}/api/v0.0.2/deals-list",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
            },
        )
        raw = data.get("data") or []
        return [
            Deal(
                id=d["id"],
                title=d["title"],
                status=d.get("deal_status"),
                asset_class=d.get("asset_class"),
                currency=d.get("currency"),
                minimum_ticket=d.get("minimum_ticket"),
            )
            for d in raw
        ]