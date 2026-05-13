const { PrismaClient } = require('@prisma/client');

const prisma = new PrismaClient({
  log: process.env.NODE_ENV === 'development' 
    ? ['query', 'error', 'warn'] 
    : ['error'],
});

// Test database connection
async function testConnection() {
  try {
    await prisma.$connect();
    console.log('✅ Подключение к базе данных установлено');
  } catch (error) {
    console.error('❌ Ошибка подключения к базе данных:', error);
    process.exit(1);
  }
}

testConnection();

module.exports = prisma;