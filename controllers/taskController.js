const prisma = require("../config/database");

// GET /api/tasks/
exports.getTasks = async (req, res) => {
  try {
    const { status, priority, search, sort, page = 1, limit = 10 } = req.query;

    // Базовый фильтр - только задачи пользователя
    const where = {
      userId: req.userId,
    };

    // Фильтр по статусу
    if (status === "active") {
      where.isCompleted = false;
    } else if (status === "completed") {
      where.isCompleted = true;
    }

    // Фильтр по приоритету
    if (priority && ["low", "medium", "high"].includes(priority)) {
      where.priority = priority;
    }

    // Поиск по заголовку
    if (search) {
      where.title = {
        contains: search,
        mode: "insensitive",
      };
    }

    // Сортировка
    let orderBy = { createdAt: "desc" };
    if (sort === "dueDate") orderBy = { dueDate: "asc" };
    else if (sort === "priority") {
      orderBy = { priority: "desc" };
    } else if (sort === "title") {
      orderBy = { title: "asc" };
    }

    // Пагинация
    const skip = (parseInt(page) - 1) * parseInt(limit);
    const take = parseInt(limit);

    // Получение задач и общего количества
    const [tasks, totalCount] = await Promise.all([
      prisma.task.findMany({
        where,
        orderBy,
        skip,
        take,
      }),
      prisma.task.count({ where }),
    ]);

    // Статистика
    const [activeCount, completedCount] = await Promise.all([
      prisma.task.count({
        where: { userId: req.userId, isCompleted: false },
      }),
      prisma.task.count({
        where: { userId: req.userId, isCompleted: true },
      }),
    ]);

    res.json({
      tasks,
      stats: {
        total: totalCount,
        active: activeCount,
        completed: completedCount,
        progress:
          totalCount > 0 ? Math.round((completedCount / totalCount) * 100) : 0,
      },
      pagination: {
        currentPage: parseInt(page),
        totalPages: Math.ceil(totalCount / take),
        totalCount,
        hasMore: skip + tasks.length < totalCount,
      },
    });
  } catch (error) {
    console.error("Get tasks error:", error);
    res.status(500).json({
      message: "Ошибка получения задач",
      error: process.env.NODE_ENV === "development" ? error.message : undefined,
    });
  }
};

// POST /api/tasks/
exports.createTask = async (req, res) => {
  try {
    const { title, description, dueDate, priority = "medium" } = req.body;

    // Валидация
    if (!title || !title.trim()) {
      return res.status(400).json({
        message: "Заголовок задачи обязателен",
      });
    }

    if (title.length > 200) {
      return res.status(400).json({
        message: "Заголовок не должен превышать 200 символов",
      });
    }

    if (!["low", "medium", "high"].includes(priority)) {
      return res.status(400).json({
        message: "Приоритет должен быть low, medium или high",
      });
    }

    const task = await prisma.task.create({
      data: {
        title: title.trim(),
        description: description?.trim(),
        dueDate: dueDate ? new Date(dueDate) : null,
        priority,
        userId: req.userId,
      },
    });

    res.status(201).json({
      message: "Задача создана",
      task,
    });
  } catch (error) {
    console.error("Create task error:", error);
    res.status(500).json({
      message: "Ошибка создания задачи",
      error: process.env.NODE_ENV === "development" ? error.message : undefined,
    });
  }
};

// GET /api/tasks/:id/
exports.getTask = async (req, res) => {
  try {
    const { id } = req.params;

    const task = await prisma.task.findFirst({
      where: {
        id,
        userId: req.userId,
      },
    });

    if (!task) {
      return res.status(404).json({
        message: "Задача не найдена",
      });
    }

    res.json({ task });
  } catch (error) {
    console.error("Get task error:", error);
    res.status(500).json({
      message: "Ошибка получения задачи",
      error: process.env.NODE_ENV === "development" ? error.message : undefined,
    });
  }
};

// PUT /api/tasks/:id/
exports.updateTask = async (req, res) => {
  try {
    const { id } = req.params;
    const { title, description, dueDate, priority, isCompleted } = req.body;

    // Проверка существования задачи
    const existingTask = await prisma.task.findFirst({
      where: { id, userId: req.userId },
    });

    if (!existingTask) {
      return res.status(404).json({
        message: "Задача не найдена",
      });
    }

    // Валидация
    if (title && title.length > 200) {
      return res.status(400).json({
        message: "Заголовок не должен превышать 200 символов",
      });
    }

    if (priority && !["low", "medium", "high"].includes(priority)) {
      return res.status(400).json({
        message: "Приоритет должен быть low, medium или high",
      });
    }

    const task = await prisma.task.update({
      where: { id },
      data: {
        title: title?.trim() || existingTask.title,
        description:
          description !== undefined
            ? description?.trim()
            : existingTask.description,
        dueDate: dueDate ? new Date(dueDate) : existingTask.dueDate,
        priority: priority || existingTask.priority,
        isCompleted:
          isCompleted !== undefined ? isCompleted : existingTask.isCompleted,
      },
    });

    res.json({
      message: "Задача обновлена",
      task,
    });
  } catch (error) {
    console.error("Update task error:", error);
    res.status(500).json({
      message: "Ошибка обновления задачи",
      error: process.env.NODE_ENV === "development" ? error.message : undefined,
    });
  }
};

// PATCH /api/tasks/:id/
exports.patchTask = async (req, res) => {
  try {
    const { id } = req.params;
    const updates = req.body;

    // Разрешенные поля для частичного обновления
    const allowedFields = [
      "title",
      "description",
      "dueDate",
      "priority",
      "isCompleted",
    ];
    const updateData = {};

    Object.keys(updates).forEach((key) => {
      if (allowedFields.includes(key)) {
        if (key === "dueDate") {
          updateData[key] = updates[key] ? new Date(updates[key]) : null;
        } else {
          updateData[key] = updates[key];
        }
      }
    });

    if (Object.keys(updateData).length === 0) {
      return res.status(400).json({
        message: "Нет допустимых полей для обновления",
      });
    }

    // Проверка существования задачи
    const existingTask = await prisma.task.findFirst({
      where: { id, userId: req.userId },
    });

    if (!existingTask) {
      return res.status(404).json({
        message: "Задача не найдена",
      });
    }

    const task = await prisma.task.update({
      where: { id },
      data: updateData,
    });

    res.json({
      message: "Задача частично обновлена",
      task,
    });
  } catch (error) {
    console.error("Patch task error:", error);
    res.status(500).json({
      message: "Ошибка обновления задачи",
      error: process.env.NODE_ENV === "development" ? error.message : undefined,
    });
  }
};

// DELETE /api/tasks/:id/
exports.deleteTask = async (req, res) => {
  try {
    const { id } = req.params;

    const task = await prisma.task.findFirst({
      where: { id, userId: req.userId },
    });

    if (!task) {
      return res.status(404).json({
        message: "Задача не найдена",
      });
    }

    await prisma.task.delete({
      where: { id },
    });

    res.json({
      message: "Задача удалена",
      taskId: id,
    });
  } catch (error) {
    console.error("Delete task error:", error);
    res.status(500).json({
      message: "Ошибка удаления задачи",
      error: process.env.NODE_ENV === "development" ? error.message : undefined,
    });
  }
};
