from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import Any
from urllib.parse import quote

import httpx
from fastapi import HTTPException, status

from .config_zoom import settings


@dataclass(frozen=True)
class CachedZoomToken:
    access_token: str
    expires_at: float


class ZoomApiClient:
    def __init__(self) -> None:
        self._token: CachedZoomToken | None = None
        self._token_lock = threading.Lock()

    def _token_is_valid(self) -> bool:
        if self._token is None:
            return False

        refresh_before = self._token.expires_at - settings.ZOOM_TOKEN_CACHE_SKEW_SECONDS

        return time.time() < refresh_before

    def _clear_token(self) -> None:
        with self._token_lock:
            self._token = None

    def _raise_zoom_error(
        self,
        response: httpx.Response,
        fallback_status_code: int = status.HTTP_502_BAD_GATEWAY,
    ) -> None:
        try:
            payload = response.json()
        except ValueError:
            payload = {
                "message": response.text,
            }

        zoom_message = payload.get("message") if isinstance(payload, dict) else None
        zoom_code = payload.get("code") if isinstance(payload, dict) else None

        detail = {
            "zoom_status_code": response.status_code,
            "zoom_code": zoom_code,
            "zoom_message": zoom_message or payload,
        }

        if response.status_code in {
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
            status.HTTP_409_CONFLICT,
            status.HTTP_429_TOO_MANY_REQUESTS,
        }:
            raise HTTPException(
                status_code=response.status_code,
                detail=detail,
            )

        raise HTTPException(
            status_code=fallback_status_code,
            detail=detail,
        )

    def _request_new_access_token(self) -> CachedZoomToken:
        try:
            response = httpx.post(
                settings.ZOOM_OAUTH_TOKEN_URL,
                data={
                    "grant_type": "account_credentials",
                    "account_id": settings.ZOOM_ACCOUNT_ID,
                },
                auth=(
                    settings.ZOOM_CLIENT_ID,
                    settings.ZOOM_CLIENT_SECRET,
                ),
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                timeout=20.0,
            )
        except httpx.HTTPError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"No fue posible conectar con Zoom OAuth: {exc}",
            ) from exc

        if response.status_code != status.HTTP_200_OK:
            self._raise_zoom_error(response)

        payload = response.json()

        access_token = payload.get("access_token")
        expires_in = int(payload.get("expires_in", 3600))

        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Zoom no devolvió access_token.",
            )

        return CachedZoomToken(
            access_token=access_token,
            expires_at=time.time() + expires_in,
        )

    def get_access_token(self) -> str:
        if self._token_is_valid():
            return self._token.access_token  # type: ignore[union-attr]

        with self._token_lock:
            if self._token_is_valid():
                return self._token.access_token  # type: ignore[union-attr]

            self._token = self._request_new_access_token()

            return self._token.access_token

    def request(
        self,
        method: str,
        path: str,
        *,
        expected_status_codes: set[int],
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        retry_on_unauthorized: bool = True,
    ) -> dict[str, Any]:
        url = f"{settings.ZOOM_API_BASE_URL}/{path.lstrip('/')}"

        try:
            response = httpx.request(
                method=method,
                url=url,
                headers={
                    "Authorization": f"Bearer {self.get_access_token()}",
                    "Content-Type": "application/json",
                },
                json=json,
                params=params,
                timeout=30.0,
            )
        except httpx.HTTPError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"No fue posible conectar con Zoom API: {exc}",
            ) from exc

        if (
            response.status_code == status.HTTP_401_UNAUTHORIZED
            and retry_on_unauthorized
        ):
            self._clear_token()

            return self.request(
                method,
                path,
                expected_status_codes=expected_status_codes,
                json=json,
                params=params,
                retry_on_unauthorized=False,
            )

        if response.status_code not in expected_status_codes:
            self._raise_zoom_error(response)

        if response.status_code == status.HTTP_204_NO_CONTENT or not response.content:
            return {}

        return response.json()

    def create_meeting(
        self,
        user_id: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        safe_user_id = quote(str(user_id), safe="")

        return self.request(
            "POST",
            f"/users/{safe_user_id}/meetings",
            expected_status_codes={status.HTTP_201_CREATED},
            json=payload,
        )

    def list_meetings(
        self,
        user_id: str,
        meeting_type: str = "scheduled",
    ) -> dict[str, Any]:
        safe_user_id = quote(str(user_id), safe="")

        return self.request(
            "GET",
            f"/users/{safe_user_id}/meetings",
            expected_status_codes={status.HTTP_200_OK},
            params={
                "type": meeting_type,
                "page_size": 100,
            },
        )

    def get_meeting(
        self,
        meeting_id: str,
    ) -> dict[str, Any]:
        safe_meeting_id = quote(str(meeting_id), safe="")

        return self.request(
            "GET",
            f"/meetings/{safe_meeting_id}",
            expected_status_codes={status.HTTP_200_OK},
        )

    def update_meeting(
        self,
        meeting_id: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        safe_meeting_id = quote(str(meeting_id), safe="")

        self.request(
            "PATCH",
            f"/meetings/{safe_meeting_id}",
            expected_status_codes={status.HTTP_204_NO_CONTENT},
            json=payload,
        )

        return self.get_meeting(meeting_id)

    def delete_meeting(
        self,
        meeting_id: str,
    ) -> None:
        safe_meeting_id = quote(str(meeting_id), safe="")

        self.request(
            "DELETE",
            f"/meetings/{safe_meeting_id}",
            expected_status_codes={status.HTTP_204_NO_CONTENT},
        )


zoom_client = ZoomApiClient()
