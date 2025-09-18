# src/models/auth.py
from pydantic import BaseModel

class MinioCredentials(BaseModel):
    """
    Define o modelo de dados para as credenciais de login.
    """
    access_key: str
    secret_key: str
