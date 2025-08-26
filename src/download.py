import os
import shutil
import logging
from .minio_client import MinioClient

logger = logging.getLogger('minio_datalake_app')

# Classe responsável por toda a lógica de download de arquivos e diretórios do MinIO.
class Download:
    def __init__(self, client: MinioClient):
        # Recebe a conexão com o MinIO ao ser instanciada.
        self.client = client.client

    def download_file(self, bucket_name: str, object_name: str, local_filename: str = None) -> bool:
        """Baixa um único arquivo do MinIO."""
        try:
            # Se nenhum caminho local for fornecido, salva o arquivo na pasta "Downloads" do usuário.
            if not local_filename:
                local_filename = os.path.join(os.path.expanduser("~"), "Downloads", os.path.basename(object_name))
            
            # Garante que o diretório de destino exista antes de salvar o arquivo.
            os.makedirs(os.path.dirname(local_filename), exist_ok=True)
            
            # Método principal que baixa o objeto do MinIO para um arquivo local.
            self.client.fget_object(bucket_name, object_name, local_filename)
            logger.info(f"Arquivo '{object_name}' baixado com sucesso em '{local_filename}'.")
            return True
        except Exception as e:
            logger.error(f"Falha ao baixar arquivo '{object_name}': {e}")
            return False

    def download_directory(self, bucket_name: str, prefix: str, local_directory: str = None) -> bool:
        """Baixa todos os arquivos de um prefixo (diretório virtual) do MinIO."""
        try:
            # Define o diretório de destino padrão se não for especificado.
            if not local_directory:
                local_directory = os.path.join(os.path.expanduser("~"), "Downloads", prefix)
            os.makedirs(local_directory, exist_ok=True)

            # Lista todos os objetos no bucket/prefixo de forma recursiva.
            objects = self.client.list_objects(bucket_name, prefix=prefix, recursive=True)
            
            # Itera sobre cada objeto encontrado e faz o download.
            for obj in objects:
                # Monta o caminho de destino local, preservando a estrutura de pastas.
                obj_path = os.path.join(local_directory, os.path.relpath(obj.object_name, prefix))
                os.makedirs(os.path.dirname(obj_path), exist_ok=True)
                self.client.fget_object(bucket_name, obj.object_name, obj_path)
                logger.info(f"Arquivo '{obj.object_name}' baixado com sucesso em '{obj_path}'.")

            return True
        except Exception as e:
            logger.error(f"Falha ao baixar diretório '{prefix}': {e}")
            return False