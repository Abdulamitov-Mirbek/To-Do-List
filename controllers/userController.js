const prisma = require("../config/database");

// GET /api/user/profile
exports.getProfile = async (req, res) => {
  try {
    const user = await prisma.user.findUnique({
      where: { id: req.userId },
      select: {
        id: true,
        email: true,
        name: true,
        dateJoined: true,
        createdAt: true,
      },
    });

    if (!user) {
      return res.status(404).json({
        message: "Пользователь не найден",
      });
    }

    // Get task statistics
    const [total, completed, active] = await Promise.all([
      prisma.task.count({ where: { userId: req.userId } }),
      prisma.task.count({ where: { userId: req.userId, isCompleted: true } }),
      prisma.task.count({ where: { userId: req.userId, isCompleted: false } }),
    ]);

    const progress = total > 0 ? Math.round((completed / total) * 100) : 0;

    res.json({
      user: {
        ...user,
        stats: {
          total,
          completed,
          active,
          progress,
        },
      },
    });
  } catch (error) {
    console.error("Profile error:", error);
    res.status(500).json({
      message: "Ошибка получения профиля",
      error: process.env.NODE_ENV === "development" ? error.message : undefined,
    });
  }
};

// PUT /api/user/settings
exports.updateSettings = async (req, res) => {
  try {
    const { name } = req.body;

    const updateData = {};
    if (name) updateData.name = name;

    if (Object.keys(updateData).length === 0) {
      return res.status(400).json({
        message: "Нет данных для обновления",
      });
    }

    const user = await prisma.user.update({
      where: { id: req.userId },
      data: updateData,
      select: {
        id: true,
        email: true,
        name: true,
        dateJoined: true,
      },
    });

    res.json({
      message: "Настройки обновлены",
      user,
    });
  } catch (error) {
    console.error("Update settings error:", error);
    res.status(500).json({
      message: "Ошибка обновления настроек",
      error: process.env.NODE_ENV === "development" ? error.message : undefined,
    });
  }
};

// PUT /api/user/password
exports.changePassword = async (req, res) => {
  try {
    const { currentPassword, newPassword } = req.body;

    if (!currentPassword || !newPassword) {
      return res.status(400).json({
        message: "Текущий и новый пароль обязательны",
      });
    }

    if (newPassword.length < 8) {
      return res.status(400).json({
        message: "Пароль должен содержать минимум 8 символов",
      });
    }

    const user = await prisma.user.findUnique({
      where: { id: req.userId },
    });

    const bcrypt = require("bcryptjs");
    const isValid = await bcrypt.compare(currentPassword, user.password);

    if (!isValid) {
      return res.status(401).json({
        message: "Неверный текущий пароль",
      });
    }

    const hashedPassword = await bcrypt.hash(newPassword, 12);

    await prisma.user.update({
      where: { id: req.userId },
      data: { password: hashedPassword },
    });

    res.json({ message: "Пароль успешно изменен" });
  } catch (error) {
    console.error("Change password error:", error);
    res.status(500).json({
      message: "Ошибка смены пароля",
    });
  }
};
