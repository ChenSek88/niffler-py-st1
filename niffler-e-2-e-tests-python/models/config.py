from pydantic import BaseModel, SecretStr


class Envs(BaseModel):
    frontend_url: str
    gateway_url: str
    auth_url: str
    spend_db_url: str
    user_db_url: str
    userdata_db_url: str
    test_username: str
    test_password: SecretStr
    auth_secret: str
