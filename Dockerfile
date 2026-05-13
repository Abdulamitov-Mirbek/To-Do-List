FROM node:18-slim

# Установка OpenSSL и прав
RUN apt-get update -y && apt-get install -y openssl && chmod -R 777 /usr/local/lib/node_modules

WORKDIR /app

COPY package*.json ./
COPY prisma ./prisma/

RUN npm install --production=false
RUN node ./node_modules/prisma/build/index.js generate

COPY . .

EXPOSE 10000

CMD ["node", "server.js"]