from __future__ import annotations
import httpx
from typing import Any, Dict, Optional

from core.errors import InvalidCredentialsError, UpstreamServiceError, UnauthorizedTokenError


class HttpJsonClient:
    def __init__(self, timeout_seconds: float = 10.0):
        self._timeout = timeout_seconds

    async def post_json(
        self,
        url: str,
        *,
        json: Dict[str, Any] | None = None,
        headers: Dict[str, str] | None = None,
        cookies: Dict[str, str] | None = None,
    ) -> Dict[str, Any]:
        return await self._request_json("POST", url, json=json, headers=headers, cookies=cookies)

    async def get_json(
        self,
        url: str,
        *,
        headers: Dict[str, str] | None = None,
        cookies: Dict[str, str] | None = None,
    ) -> Dict[str, Any]:
        return await self._request_json("GET", url, headers=headers, cookies=cookies)

    async def _request_json(
        self,
        method: str,
        url: str,
        *,
        json: Dict[str, Any] | None = None,
        headers: Dict[str, str] | None = None,
        cookies: Dict[str, str] | None = None,
    ) -> Dict[str, Any]:
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            resp = await client.request(method, url, json=json, headers=headers, cookies=cookies)

        data: Optional[Dict[str, Any]] = None
        try:
            data = resp.json()
        except Exception:
            data = None

        # ✅ אלטיוס מחזירים 400 עם {"status":"error","errors":{"login":[...]}}
        if resp.status_code == 400 and isinstance(data, dict):
            if data.get("status") == "error":
                errors = data.get("errors") or {}
                login_errors = errors.get("login") or []
                if login_errors:
                    raise InvalidCredentialsError(login_errors[0])

        if resp.status_code == 401:
            # לפעמים upstream כן יחזיר 401
            raise InvalidCredentialsError("Invalid username or password")

        if resp.status_code == 403:
            raise UnauthorizedTokenError("Forbidden")

        if resp.status_code >= 500:
            raise UpstreamServiceError(f"Upstream error: {resp.status_code}")

        # כל שאר ה-4xx שלא זיהינו -> עדיין נסמן כ-Upstream (כי לא “אשמת user” בהכרח)
        if 400 <= resp.status_code < 500:
            raise UpstreamServiceError(f"Upstream client error: {resp.status_code} ({data})")

        if not isinstance(data, dict):
            raise UpstreamServiceError("Upstream returned non-JSON response")

        return data