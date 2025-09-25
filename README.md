# Projeto: Data Lake Local para Pesquisa - Iniciação Científica na UFU/LMest

Este projeto foi desenvolvido como parte de uma Iniciação Científica no laboratório LMest da UFU, com o objetivo de criar uma solução de Data Lake local e acessível para a pesquisa. A plataforma utiliza o MinIO para o armazenamento de dados, complementada por scripts Python para automatizar e facilitar o acesso aos dados.

---

## Sumário do Conteúdo

1. [Problema e Solução](#1-problema-e-solução)
2. [Arquitetura do Projeto](#2-arquitetura-do-projeto)
3. [Guia de Instalação e Setup (Para Administradores)](#3-guia-de-instalação-e-setup-para-administradores)
4. [Apresentação dos Módulos](#4-apresentação-dos-módulos)
5. [Desafios e Soluções](#5-desafios-e-soluções)
6. [Próximos Passos e Futuro do Projeto](#6-próximos-passos-e-futuro-do-projeto)
7. [Anexo: Guia de Uso para Pesquisadores](#7-anexo-guia-de-uso-para-pesquisadores)

---

## **1. Problema e Solução**

* **O Problema:** A pesquisa no laboratório LMest gera e consome grandes volumes de dados que, atualmente, podem estar espalhados em diferentes computadores, dificultando o acesso, a organização e o backup centralizado.
* **A Solução:** Um Data Lake local, utilizando a plataforma de armazenamento de objetos **MinIO**. Este sistema centraliza os dados e oferece uma interface padronizada (API S3) e ferramentas Python para acesso programático e análise interativa.
## **2. Arquitetura do Projeto**

A estrutura do projeto é modular e organizada para separar as responsabilidades:
```
├── data/                       # Dados locais (entrada/saída)
│   └── Comfaulda/, ensaios/, etc.
├── docs/                       # Documentação 
├── logs/                       # Arquivos de log (gerados automaticamente)
├── researchers_scripts/        # Scripts de uso dos pesquisadores
│   ├── upload_file.py
│   ├── upload_directory.py
│   ├── download_file.py
|   ├── minio_loader.py
│   ├── read_file.py
│   ├── read_dataset.py
│   └── list_datalake.py
├── src/                        # Scripts administrativos
│   ├── main.py                 # Inicialização do Data Lake
│   ├── backup_datalake.py      # Sistema de backup
│   ├── logger.py
│   └── minio_client.py         # Wrapper Python para MinIO
├── docker-compose.yml          # Serviço do MinIO
├── requirements.txt            # Dependências Python
└── README.md                   # Este arquivo
```

---
## **3. Guia de Instalação e Setup (Para Administradores)**

Este guia é para implantar o Data Lake em um servidor.

1.  **Inicie o Servidor MinIO:**
    * Garanta que o Docker e o Docker Compose estejam instalados.
    * No diretório raiz, execute: `docker-compose up -d`

2.  **Instale as Dependências Python:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure o MinIO Client (mc) no servidor:**
    ```bash
    mc alias set localminio http://localhost:9000 minio miniol23
    ```

4.  **Inicialize o Data Lake:**
    * O script `main.py` verificará a conexão, criará os buckets essenciais (`datalake`, `backup`) e configurará o ambiente.
    ```bash
    python src/main.py
    ```

## **4. Apresentação dos Módulos**

* **`src/minio_client.py`:** É o wrapper Python que permite que todos os scripts se conectem ao MinIO e executem operações como `upload`, `download` e `listagem`. 
* **`src/backup_datalake.py`:** Implementa um sistema de backup interno robusto que usa `mc mirror` para criar cópias de segurança dos dados, com uma política de retenção automatizada.

## **5. Desafios e Soluções (Destaques para a Apresentação)**

* **Desafio do `Endpoint`:** A forma de acesso ao servidor MinIO muda dependendo do ambiente (`localhost` no seu computador, `minio-server` dentro do Docker, ou o IP real do servidor na rede).
* **Nossa Solução:** Criamos o script `login_datalake.sh` para gerenciar essa complexidade. Ele permite ao usuário definir o `endpoint` de forma flexível, garantindo que o `MinioClient` se conecte ao endereço correto sem alterar o código.

* **Acesso Interativo aos Dados (`Kaggle-like`):**
    * **O Conceito:** Acessar dados diretamente na memória RAM, sem a necessidade de downloads permanentes para o disco local.
    * **Nossa Solução:** O script `minio_loader.py` faz exatamente isso. Ele carrega arquivos CSV do MinIO para um `DataFrame` do Pandas e, em seguida, inicia um ambiente interativo (IPython) onde os pesquisadores podem usar comandos do Pandas para análise em tempo real.

## **6. Próximos Passos e Futuro do Projeto**

* **Levantamento de Requisitos no LMest:** Aprofundar o entendimento das demandas dos pesquisadores para customizar a solução (quais dados, quais ferramentas).
* **Implementação Final no Servidor:** Fazer a transição do protótipo para a instalação definitiva no servidor do laboratório.

## **7. Anexo: Guia de Uso para Pesquisadores**

Para instruções detalhadas de como utilizar os scripts de `upload`, `download`, `listagem`, `leitura` e a ferramenta de análise `minio_loader.py`, consulte o `README.md` localizado na pasta `researchers_scripts/`.
