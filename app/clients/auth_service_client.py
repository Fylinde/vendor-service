import httpx
from app.config import settings

class AuthServiceClient:
    AUTH_SERVICE_URL = settings.AUTH_SERVICE_URL # Correct base URL

    async def resend_verification_code(self, payload: dict) -> dict:
        """
        Makes an API call to auth-service to resend a verification code.
        """
        url = f"{self.AUTH_SERVICE_URL}/generate-verification-code"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                return response.json()  # Assume response contains {"message": "success"}
        except httpx.HTTPStatusError as e:
            raise Exception(f"Auth-service returned an error: {e.response.text}")
        except Exception as e:
            raise Exception(f"Failed to call auth-service: {e}")