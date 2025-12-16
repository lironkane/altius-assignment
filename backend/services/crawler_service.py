from websites.base import BaseWebsite
from models import LoginResponse


class CrawlerService:
    async def get_data(self, client: BaseWebsite, username: str, password: str) -> tuple[str, list]:
        token = await client.login(username, password)
        deals = await client.get_deals(token)
        return token, deals