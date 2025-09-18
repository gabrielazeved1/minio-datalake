# src/utils/session.py
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

# configuracoes do token
ALGORITHM = "HS256"
SESSION_DURATION_MINUTES = 60
SECRET_KEY = "SUPER_SECRET_KEY"

# Define o esquema de segurança que o FastAPI usará para a documentação e extração do token.
# `tokenUrl="login"` informa que o token é gerado no endpoint /login.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Armazena sessões ativas
session_store = {}

def create_session_token(username: str):
    """Gera um token JWT para o usuário com um tempo de expiração definido."""
    expire = datetime.utcnow() + timedelta(minutes=SESSION_DURATION_MINUTES)
     # O conteúdo do token: 'sub' (subject) é o usuário e 'exp' é a data de expiração.
    token = jwt.encode({"sub": username, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_session_token(token: str):
    #Verifica a assinatura e a validade de um token. Lança erro 401 se for inválido
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return token
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

def get_current_user(token: str = Depends(oauth2_scheme)):
    return verify_session_token(token)

"""
    Dependência do FastAPI para proteger rotas. Funciona em duas etapas:
    1. `Depends(oauth2_scheme)`: Extrai o token do cabeçalho "Authorization" da requisição.
    2. `verify_session_token(token)`: Chama a função de verificação com o token extraído.
    
    Se o token for inválido, o processo é interrompido aqui e a rota protegida nem chega a ser executada.
"""