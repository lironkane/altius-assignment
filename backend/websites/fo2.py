from typing import List
from models import Deal
from core.http_client import HttpJsonClient
from websites.base import BaseWebsite


class Fo2Website(BaseWebsite):
    def __init__(self, http: HttpJsonClient):
        self._http = http
        self._api_url = "https://fo2.api.altius.finance"

    async def login(self, username: str, password: str) -> str:
        data = await self._http.post_json(
            f"{self._api_url}/api/v0.0.2/login",
            json={"email": username, "password": password},
        )
        token = (data.get("success") or {}).get("token")
        if not token:
            raise ValueError("Token missing in response")
        return token

    async def get_deals(self, token: str) -> List[Deal]:
        data = await self._http.post_json(
            f"{self._api_url}/api/v0.0.2/deals-cards",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
            },
        )
        raw = data.get("data") or []

        deals: List[Deal] = []
        for d in raw:
            status_name = (d.get("status") or {}).get("name")
            asset_class_name = (d.get("asset_class") or {}).get("name")

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