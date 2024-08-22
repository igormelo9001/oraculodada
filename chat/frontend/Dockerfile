# Use uma imagem base do Node.js
FROM node:14

# Defina o diretório de trabalho
WORKDIR /app

# Copie o package.json e instale as dependências
COPY package.json .
RUN npm install

# Copie o restante da aplicação
COPY . .

# Comando para rodar a aplicação
CMD ["npm", "start"]
