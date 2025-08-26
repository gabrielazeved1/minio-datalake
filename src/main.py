from fastapi import FastAPI, HTTPException, Depends, File, UploadFile
from .models.auth import MinioCredentials
# Assumindo que as funções de sessão e session_store estão em 'utils.session'
from .utils.session import get_current_user, create_session_token, session_store
from .minio_client import MinioClient
from .upload import Upload
from .list import List
from .download import Download

# Cria a instância principal da aplicação FastAPI.
app = FastAPI()

# Simulação de um banco de dados de usuários para o login.
fake_db = {
    "minio": "miniol23",
    "amanda": "amanda123",
    "pedro": "pedro456"
}

# Rota principal da API.
@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API do Datalake MinIO!"}

# Rota de login.
@app.post("/login")
def login(credentials: MinioCredentials):
    # Valida as credenciais contra o banco de dados simulado.
    if not (credentials.access_key in fake_db and fake_db[credentials.access_key] == credentials.secret_key):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    # Cria um token de sessão para o usuário autenticado.
    token = create_session_token(credentials.access_key)
    # Armazena as credenciais associadas ao token (simulando uma sessão ativa).
    session_store[token] = {
        "access_key": credentials.access_key,
        "secret_key": credentials.secret_key
    }
    return {"session_token": token}

# --- Funções de Dependência ---
# Cada função abaixo é uma "dependência" que o FastAPI pode injetar nas rotas.
# Elas garantem que o usuário está autenticado e criam um serviço com as credenciais corretas.

def get_upload_instance(token: str = Depends(get_current_user)) -> Upload:
    # `Depends(get_current_user)` primeiro valida o token do usuário.
    # Usa o token validado para buscar as credenciais da sessão.
    session = session_store.get(token)
    if not session:
        raise HTTPException(status_code=401, detail="Sessão inválida ou expirada")
    # Cria um cliente MinIO com as credenciais específicas do usuário logado.
    client = MinioClient(access_key=session["access_key"], secret_key=session["secret_key"])
    # Retorna o serviço de Upload pronto para ser usado na rota.
    return Upload(client)

def get_list_instance(token: str = Depends(get_current_user)) -> List:
    # A mesma lógica da dependência anterior, mas para o serviço de Listagem.
    session = session_store.get(token)
    if not session:
        raise HTTPException(status_code=401, detail="Sessão inválida ou expirada")
    client = MinioClient(access_key=session["access_key"], secret_key=session["secret_key"])
    return List(client)

def get_download_instance(token: str = Depends(get_current_user)) -> Download:
    # A mesma lógica da dependência anterior, mas para o serviço de Download.
    session = session_store.get(token)
    if not session:
        raise HTTPException(status_code=401, detail="Sessão inválida ou expirada")
    client = MinioClient(access_key=session["access_key"], secret_key=session["secret_key"])
    return Download(client)



# --- Rotas da API ---

# Rotas de listagem que usam a dependência `get_list_instance`.
@app.get("/buckets")
def list_buckets(list_service: List = Depends(get_list_instance)):
    return list_service.list_all_buckets()

@app.get("/buckets/{bucket_name}")
def list_buckets_content(bucket_name: str, prefix: str = "", list_service: List = Depends(get_list_instance)):
    return list_service.list_content(bucket_name, prefix)

# Rotas de upload que usam a dependência `get_upload_instance`.
@app.post("/upload/file")
async def upload_file_api(bucket_name: str, file: UploadFile = File(...), prefix: str = "", upload_service: Upload = Depends(get_upload_instance)):
    result = upload_service.upload_file(bucket_name, file, prefix)
    if not result:
        raise HTTPException(status_code=500, detail="Falha no upload do arquivo")
    return {"message": "Arquivo enviado com sucesso", "object_name": result}

@app.post("/upload/directory")
def upload_directory_api(bucket_name: str, local_directory: str, prefix: str = "", upload_service: Upload = Depends(get_upload_instance)):
    success = upload_service.upload_directory(bucket_name, local_directory, prefix)
    if not success:
        raise HTTPException(status_code=500, detail="Falha no upload do diretório")
    return {"message": "Diretório enviado com sucesso"}

# Rotas de download que usam a dependência `get_download_instance`.
@app.get("/download/file")
def download_file_api(bucket_name: str, object_name: str, local_filename: str = None, download_service: Download = Depends(get_download_instance)):
    success = download_service.download_file(bucket_name, object_name, local_filename)
    if not success:
        raise HTTPException(status_code=500, detail="Falha ao baixar arquivo")
    return {"message": f"Arquivo '{object_name}' baixado com sucesso"}

@app.get("/download/directory")
def download_directory_api(bucket_name: str, prefix: str, local_directory: str = None, download_service: Download = Depends(get_download_instance)):
    success = download_service.download_directory(bucket_name, prefix, local_directory)
    if not success:
        raise HTTPException(status_code=500, detail="Falha ao baixar diretório")
    return {"message": f"Diretório '{prefix}' baixado com sucesso"}