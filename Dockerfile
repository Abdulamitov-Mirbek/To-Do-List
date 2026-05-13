FROM node:18

# Установка OpenSSL для Prisma
RUN apt-get update && apt-get install -y openssl libssl-dev

WORKDIR /app

COPY package*.json ./
COPY prisma ./prisma/

RUN npm ci
RUN npx prisma generate

COPY . .

EXPOSE 10000

CMD ["node", "server.js"]