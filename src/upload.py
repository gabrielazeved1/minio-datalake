from fastapi import UploadFile
import shutil
import os
from .minio_client import MinioClient
import logging

logger = logging.getLogger('minio_datalake_app')

# Classe com a lógica de upload de arquivos e diretórios para o MinIO.
class Upload:
    def __init__(self, client: MinioClient):
        self.client = client.client

    def upload_file(self, bucket_name: str, file: UploadFile, prefix: str = "") -> str:
        # Define um caminho temporário para salvar o arquivo antes de enviá-lo.
        temp_path = f"/tmp/{file.filename}"
        try:
            # Salva o conteúdo do arquivo enviado em um arquivo temporário no disco.
            # Isso é eficiente para arquivos grandes, pois evita carregá-los inteiramente na memória.
            with open(temp_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            # Envia o arquivo do caminho temporário para o MinIO.
            # O nome do objeto no MinIO é construído com o prefixo (se existir).
            self.client.fput_object(bucket_name, f"{prefix}/{file.filename}" if prefix else file.filename, temp_path)
            logger.info(f"Arquivo '{file.filename}' enviado para bucket '{bucket_name}'.")

            # Retorna o nome final do objeto criado no bucket.
            return f"{prefix}/{file.filename}" if prefix else file.filename
        finally:
            # O bloco `finally` garante que o arquivo temporário seja sempre removido,
            # mesmo que o upload falhe.
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def upload_directory(self, bucket_name: str, local_directory: str, prefix: str = "") -> bool:
        try:
            # `os.walk` percorre a árvore de diretórios de forma eficiente.
            for root, _, files in os.walk(local_directory):
                for f in files:
                    file_path = os.path.join(root, f)
                    obj_name = f"{prefix}/{f}" if prefix else f
                    # Envia cada arquivo encontrado.
                    self.client.fput_object(bucket_name, obj_name, file_path)
            logger.info(f"Diretório '{local_directory}' enviado para bucket '{bucket_name}'.")
            return True
        except Exception as e:
            logger.error(f"Falha no upload do diretório: {e}")
            return False