# API de Gerenciamento para Datalake MinIO

Bem-vindo! Este projeto fornece uma API robusta construída com **FastAPI** para gerenciar arquivos e diretórios em um servidor de armazenamento de objetos **MinIO**. Além da API, inclui um script interativo em Python para que pesquisadores e cientistas de dados possam explorar e carregar datasets diretamente do datalake para análise.

---

## Papel de Cada Código

### Diretório Principal

- `docker-compose.yml`: Define e configura o serviço do **servidor MinIO** usando Docker, facilitando a criação de um ambiente de desenvolvimento local.  
- `pyproject.toml`: Arquivo de configuração do **Poetry**, que gerencia as dependências do Python e o ambiente virtual do projeto.  
- `.env`: Arquivo de configuração local (que você deve criar) para armazenar **variáveis de ambiente**, como credenciais e o endereço do MinIO. **Nunca** envie este arquivo para o Git.  
- `.gitignore`: Especifica quais arquivos e pastas devem ser ignorados pelo Git.  

### `/src` - O Coração da API

- `main.py`: O ponto de entrada da aplicação **FastAPI**. Define todas as rotas da API (endpoints), como `/login`, `/buckets`, `/upload`, e `/download`, e conecta-as à sua lógica de negócios.  
- `minio_client.py`: Centraliza a **conexão com o MinIO**. Cria e configura o cliente que será usado por outros módulos para interagir com o servidor.  
- `upload.py`, `download.py`, `list.py`: Módulos de serviço que contêm a **lógica de negócios** para as operações de upload, download e listagem de arquivos, mantendo o `main.py` limpo e organizado.  
- `utils/session.py`: Contém toda a lógica de **autenticação e gerenciamento de sessão** usando tokens JWT (JSON Web Tokens). É responsável por criar, verificar e proteger as rotas.  
- `models/auth.py`: Define os **modelos de dados** (usando Pydantic) para validação de requisições, como a estrutura das credenciais de login.  

### `/researchers_scripts` - Ferramentas para Análise

- `loader.py`: Define a classe `Loader`, uma ferramenta poderosa que encapsula a lógica para **navegar interativamente** pelos buckets e pastas do MinIO e carregar arquivos `.csv` diretamente em um DataFrame do Pandas.  
- `minio_loader.py`: Um **script executável** que utiliza a classe `Loader`. Ele foi projetado para ser usado por pesquisadores no terminal para selecionar um bucket, navegar até o arquivo desejado e iniciar uma sessão interativa de análise de dados com o `IPython`.  

---

## Como Usar o Projeto

### 1. Pré-requisitos

- **Docker** e **Docker Compose**  
- **Python 3.11+**  
- **Poetry** (gerenciador de pacotes para Python)  

### 2. Configuração do Ambiente

1. **Inicie o Servidor MinIO:**

   ```bash
   docker-compose up -d
   ```

- A API do MinIO estará disponível em `localhost:9000`.  
- A interface web do MinIO estará em `http://localhost:9001`.  
- Use as credenciais `minio / miniol23` para acessar.  

---

## 3. Instale as Dependências

```bash
poetry install
```

---

## 4. Crie o Arquivo `.env`

```bash
MINIO_ENDPOINT=127.0.0.1:9000  
MINIO_ACCESS_KEY=minio  
MINIO_SECRET_KEY=miniol23  
MINIO_SECURE=False  
```

---

## 5. Utilização

Você pode interagir com o projeto de duas maneiras: através da **API RESTful** ou do **Script Interativo**.

---

### A. Usando a API RESTful

#### 1. Inicie a API:
```bash
poetry run uvicorn src.main:app --reload
```

- A API estará disponível em `http://127.0.0.1:8000`.  
- A documentação interativa (Swagger UI) pode ser acessada em `http://127.0.0.1:8000/docs`.  

---

#### 2. Exemplos de Requisições (curl):

**Login (para obter o token de sessão):**
```bash
SESSION_TOKEN=$(curl -s -X POST "http://127.0.0.1:8000/login" \
  -H "Content-Type: application/json" \
  -d '{"access_key":"amanda","secret_key":"amanda123"}' | jq -r '.session_token')
```

echo "Token: $SESSION_TOKEN"

---

**Listar Buckets:**
```bash
curl -H "Authorization: Bearer $SESSION_TOKEN" "http://127.0.0.1:8000/buckets"
```
---

**Upload de Arquivo:**
```bash
curl -X POST -H "Authorization: Bearer $SESSION_TOKEN" \
  -F "file=@/caminho/para/seu/arquivo.csv" \
  "http://127.0.0.1:8000/upload/file?bucket_name=datalake&prefix=docs"
```
---

**Download de Arquivo:**
```bash
curl -H "Authorization: Bearer $SESSION_TOKEN" \
  "http://127.0.0.1:8000/download/file?bucket_name=datalake&object_name=docs/arquivo.csv" \
  -o ~/Downloads/arquivo_baixado.csv
```
---

**Download de Diretório Completo:**
```bash
curl -H "Authorization: Bearer $SESSION_TOKEN" \
  "http://127.0.0.1:8000/download/directory?bucket_name=datalake&prefix=docs"
```
*(Este comando não baixa os arquivos diretamente via curl, mas aciona a API para salvá-los no servidor onde a API está rodando, na pasta `~/Downloads` por padrão).*

## Usando o Script Interativo para Pesquisadores

Esta é a forma mais fácil de explorar e carregar dados para análise sem usar a API.

---

## 1. Execute o Script

No terminal, na raiz do projeto, execute:
```bash
poetry run python researchers_scripts/minio_loader.py
```
---

## 2. Siga as Instruções no Terminal

- O script listará os buckets disponíveis e pedirá que você escolha um.  
- Em seguida, ele mostrará as pastas e arquivos `.csv` no diretório atual.  
- Você pode navegar pelas pastas digitando seus nomes ou selecionar um arquivo `.csv`.  
- Use `back` para voltar um nível ou `exit` para sair.  

---

## 3. Análise de Dados

Ao selecionar um arquivo `.csv`, o script o carregará em um **DataFrame do Pandas** e abrirá um **shell interativo do IPython**.  
O DataFrame estará pronto para uso na variável `df`.

# O shell IPython será aberto aqui
In [1]: df.head()

In [2]: df.describe()

In [3]: exit()  # Para sair do shell
