# researchers_scripts/loader.py
import os
import logging
import pandas as pd
from minio import Minio
from minio.error import S3Error

class Loader:
    def __init__(self, endpoint, access_key, secret_key, secure=False):
        self.client = Minio(
            endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure
        )
        self.logger = logging.getLogger("minio_loader")
        logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    def list_buckets(self):
        try:
            return [b.name for b in self.client.list_buckets()]
        except S3Error as e:
            self.logger.error(f"Erro ao listar buckets: {e}")
            return []

    def list_objects(self, bucket_name, prefix=""):
        objects = list(self.client.list_objects(bucket_name, prefix=prefix, recursive=False))
        folders = sorted(set([obj.object_name.split("/")[0] + "/" for obj in objects if obj.object_name.endswith("/") or "/" in obj.object_name]))
        files = sorted([obj.object_name for obj in objects if obj.object_name.endswith(".csv")])
        return folders, files

    def explore_bucket(self, bucket_name):
        prefix = ""
        while True:
            folders, files = self.list_objects(bucket_name, prefix)

            print("\nPastas disponíveis:" if folders else "\nArquivos disponíveis:")
            for f in folders:
                print(f" - {f}")
            for f in files:
                print(f" - {f}")

            choice = input("\nEscolha uma pasta ou arquivo (digite 'back' para voltar, 'exit' para sair): ").strip()
            if choice.lower() == "exit":
                exit(0)
            elif choice.lower() == "back":
                if "/" in prefix.rstrip("/"):
                    prefix = "/".join(prefix.rstrip("/").split("/")[:-1]) + "/"
                else:
                    prefix = ""
                continue
            elif choice.endswith(".csv"):
                final_path = f"{prefix}{choice}" if not choice.startswith(prefix) else choice
                return self.load_csv(bucket_name, final_path)
            else:
                # navegar para subpasta
                prefix = f"{prefix}{choice}" if not choice.startswith(prefix) else choice
                if not prefix.endswith("/"):
                    prefix += "/"

    def load_csv(self, bucket_name, path):
        try:
            self.logger.info(f"Lendo arquivo '{path}' do bucket '{bucket_name}'...")
            response = self.client.get_object(bucket_name, path)
            df = pd.read_csv(response)
            response.close()
            response.release_conn()
            self.logger.info(f"Arquivo '{path}' carregado com sucesso ({len(df)} linhas).")
            return df
        except S3Error as e:
            self.logger.error(f"Erro ao acessar arquivo: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Erro ao ler CSV: {e}")
            raise
