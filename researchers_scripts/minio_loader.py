# researchers_scripts/minio_loader.py
import os
import IPython
from dotenv import load_dotenv
from loader import Loader

def main():
    load_dotenv()

    loader = Loader(
        endpoint=os.getenv("MINIO_ENDPOINT"),
        access_key=os.getenv("MINIO_ACCESS_KEY"),
        secret_key=os.getenv("MINIO_SECRET_KEY"),
        secure=os.getenv("MINIO_SECURE", "False").lower() == "true"
    )

    # Escolha do bucket
    buckets = loader.list_buckets()
    print("Buckets disponíveis:")
    for b in buckets:
        print(f" - {b}")

    bucket_name = input("\nDigite o bucket desejado: ").strip()
    if bucket_name not in buckets:
        print(f"[✖] Bucket '{bucket_name}' não encontrado.")
        return

    # Exploração interativa e carregamento do CSV
    df = loader.explore_bucket(bucket_name)

    # IPython shell interativo
    print("\nAbrindo shell interativo. O DataFrame está disponível como 'df'.")
    IPython.embed()


if __name__ == "__main__":
    main()
