from fastapi import HTTPException
from minio.error import S3Error

# Classe que encapsula as operações de listagem de buckets e objetos.
class List:
    def __init__(self, minio_client):
        self.client = minio_client.client

    def list_all_buckets(self):
        """Retorna uma lista com o nome de todos os buckets existentes."""
        try:
            # Usa uma list comprehension para extrair apenas os nomes dos buckets.
            return {"buckets": [b.name for b in self.client.list_buckets()]}
        except S3Error as err:
            # Converte um erro específico do MinIO em um erro HTTP 500.
            raise HTTPException(status_code=500, detail=f"Erro ao listar buckets: {err}")

    def list_content(self, bucket_name: str, prefix: str = ""):
        """Lista os objetos na raiz de um bucket ou dentro de um prefixo."""
        try:
            # `recursive=False` para listar apenas o nível atual, como um `ls` no terminal.
            return {"objects": [o.object_name for o in self.client.list_objects(bucket_name, prefix=prefix, recursive=False)]}
        except S3Error as err:
            raise HTTPException(status_code=500, detail=f"Erro ao listar conteúdo: {err}")