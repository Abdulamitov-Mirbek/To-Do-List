const { PrismaClient } = require("@prisma/client");
const bcrypt = require("bcryptjs");

const prisma = new PrismaClient();

async function main() {
  console.log("🌱 Начинаем заполнение базы данных...");

  // Очистка существующих данных (в правильном порядке из-за внешних ключей)
  await prisma.task.deleteMany();
  await prisma.refreshToken.deleteMany();
  await prisma.user.deleteMany();

  console.log("🗑️  Старые данные удалены");

  // Создание тестового пользователя
  const hashedPassword = await bcrypt.hash("password123", 12);

  const user = await prisma.user.create({
    data: {
      email: "aida@example.com",
      password: hashedPassword,
      name: "Айда Касымова",
    },
  });

  console.log("✅ Пользователь создан:", user.email);

  // Создание тестовых задач
  const tasksData = [
    {
      title: "Подготовить презентацию",
      description: "Слайды по итогам Q1",
      priority: "high",
      isCompleted: false,
      dueDate: new Date("2026-05-12T15:00:00"),
    },
    {
      title: "Купить продукты",
      description: "Молоко, хлеб, овощи, фрукты",
      priority: "medium",
      isCompleted: false,
      dueDate: new Date("2026-05-13T18:00:00"),
    },
    {
      title: "Записаться к врачу",
      description: "Плановый осмотр у терапевта",
      priority: "low",
      isCompleted: true,
    },
    {
      title: "Позвонить маме",
      description: "Поздравить с праздником",
      priority: "high",
      isCompleted: false,
      dueDate: new Date("2026-05-20T18:00:00"),
    },
    {
      title: "Оплатить счета",
      description: "Коммунальные услуги за май",
      priority: "high",
      isCompleted: true,
      dueDate: new Date("2026-05-10T12:00:00"),
    },
    {
      title: "Прочитать книгу",
      description: '"Чистый код" Роберт Мартин',
      priority: "medium",
      isCompleted: false,
      dueDate: new Date("2026-05-25T22:00:00"),
    },
    {
      title: "Сходить в спортзал",
      description: "Тренировка: спина и плечи",
      priority: "low",
      isCompleted: true,
    },
    {
      title: "Обновить резюме",
      description: "Добавить последний проект",
      priority: "medium",
      isCompleted: false,
      dueDate: new Date("2026-05-15T12:00:00"),
    },
    {
      title: "Заказать подарок",
      description: "День рождения коллеги 18 мая",
      priority: "high",
      isCompleted: false,
      dueDate: new Date("2026-05-17T20:00:00"),
    },
    {
      title: "Проверить почту",
      description: "Ответить на важные письма",
      priority: "low",
      isCompleted: true,
    },
  ];

  // Создаем все задачи для пользователя
  for (const taskData of tasksData) {
    await prisma.task.create({
      data: {
        ...taskData,
        userId: user.id,
      },
    });
  }

  console.log(`✅ Создано ${tasksData.length} задач`);

  // Выводим статистику
  const stats = await Promise.all([
    prisma.task.count({ where: { userId: user.id } }),
    prisma.task.count({ where: { userId: user.id, isCompleted: true } }),
    prisma.task.count({ where: { userId: user.id, isCompleted: false } }),
    prisma.task.count({
      where: {
        userId: user.id,
        priority: "high",
        isCompleted: false,
      },
    }),
  ]);

  console.log("\n📊 Статистика:");
  console.log(`   Всего задач: ${stats[0]}`);
  console.log(`   Выполнено: ${stats[1]}`);
  console.log(`   Активных: ${stats[2]}`);
  console.log(`   Высокий приоритет: ${stats[3]}`);

  const progress = stats[0] > 0 ? Math.round((stats[1] / stats[0]) * 100) : 0;
  console.log(`   Прогресс: ${progress}%\n`);

  console.log("📧 Тестовые учетные данные:");
  console.log("   Email: aida@example.com");
  console.log("   Пароль: password123\n");

  console.log("✅ База данных успешно заполнена!");
}

main()
  .catch((e) => {
    console.error("❌ Ошибка при заполнении базы данных:");
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
