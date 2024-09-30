from pydantic import BaseModel, SecretStr


class OAuthRequest(BaseModel):
    response_type: str = "code"
    client_id: str = "client"
    scope: str = "openid"
    redirect_uri: str
    code_challenge: str
    code_challenge_method: str = "S256"


class TokenRequest(BaseModel):
    code: list
    redirect_uri: str
    code_verifier: str
    grant_type: str = "authorization_code",
    client_id: str = "client"