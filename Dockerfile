# Используем официальный образ Node.js
FROM node:18-alpine

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем package.json и package-lock.json
COPY package*.json ./
COPY prisma ./prisma/

# Устанавливаем зависимости
RUN npm ci --only=production

# Генерируем Prisma клиент
RUN npx prisma generate

# Копируем исходный код
COPY . .

# Открываем порт
EXPOSE 3000

# Запускаем приложение
CMD ["node", "server.js"]