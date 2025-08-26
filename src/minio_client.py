from minio import Minio
import logging

logger = logging.getLogger('minio_datalake_app')

# Classe que centraliza a criação da conexão com o servidor MinIO.
class MinioClient:
    def __init__(self, endpoint="127.0.0.1:9000", access_key="minio", secret_key="miniol23", secure=False):
        # Instancia o cliente da biblioteca `minio` com as configurações de conexão.
        self.client = Minio(
            endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure  # `False` para HTTP, `True` para HTTPS.
        )
        logger.info("MinioClient inicializado com endpoint: %s (secure=%s)", endpoint, secure)