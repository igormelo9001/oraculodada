# oraculodada
Just a model of LLM you could make an ask and received a response completely dada. 

# Projeto Full Stack (React + Python)

Este repositório contém uma aplicação full stack com frontend em React e backend em Python. A aplicação está configurada para rodar com Docker.

## 📌 Pré-requisitos
Certifique-se de ter instalado:
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Git](https://git-scm.com/)
- [VSCode](https://code.visualstudio.com/)

## 🚀 Clonando o repositório e executando o projeto
```sh
# Clone o repositório
git clone https://github.com/seu-usuario/seu-repositorio.git

# Acesse o diretório do projeto
cd seu-repositorio

# Construa e suba os containers do backend e frontend
docker-compose up --build
```
Isso iniciará todos os serviços da aplicação.

Para parar os containers, use:
```sh
docker-compose down
```

## 🐳 Arquivo `docker-compose.yml`
O projeto utiliza `docker-compose.yml` para gerenciar os containers do backend e frontend. O arquivo deve estar na raiz do projeto e conter a seguinte configuração:

```yaml
version: '3.8'
services:
  backend:
    build: ./chat/backend
    ports:
      - "5000:5000"
  frontend:
    build: ./chat/frontend
    ports:
      - "3000:3000"
    depends_on: 
      - backend
```

Após rodar o comando `docker-compose up --build`, os serviços estarão disponíveis nos seguintes endereços:
- **Backend:** `http://localhost:5000`
- **Frontend:** `http://localhost:3000`

## 🛠 Tecnologias Utilizadas
- **Frontend:** React, JavaScript
- **Backend:** Python, Flask/Django (especifique qual está usando)
- **Banco de Dados:** PostgreSQL/MySQL/MongoDB (especifique qual está usando)
- **Gerenciamento de Containers:** Docker e Docker Compose

## 📌 Endpoints da API
Caso tenha documentado os endpoints, adicione detalhes aqui.

## 📜 Licença
Este projeto está sob a licença [MIT](LICENSE).

---
Qualquer dúvida ou problema, sinta-se à vontade para abrir uma issue no repositório!


