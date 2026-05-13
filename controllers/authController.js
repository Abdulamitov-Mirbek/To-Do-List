const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const crypto = require('crypto');
const prisma = require('../config/database');

const generateTokens = async (userId) => {
  const accessToken = jwt.sign(
    { userId },
    process.env.JWT_SECRET,
    { expiresIn: process.env.JWT_EXPIRE }
  );

  const refreshToken = crypto.randomBytes(40).toString('hex');
  const expiresAt = new Date();
  expiresAt.setDate(expiresAt.getDate() + 7);

  await prisma.refreshToken.create({
    data: {
      token: refreshToken,
      userId,
      expiresAt
    }
  });

  return { accessToken, refreshToken };
};

// POST /api/auth/register/
exports.register = async (req, res) => {
  try {
    const { email, password, name } = req.body;

    // Валидация
    if (!email || !password || !name) {
      return res.status(400).json({ 
        message: 'Email, пароль и имя обязательны' 
      });
    }

    if (password.length < 8) {
      return res.status(400).json({ 
        message: 'Пароль должен содержать минимум 8 символов' 
      });
    }

    if (!email.includes('@')) {
      return res.status(400).json({ 
        message: 'Некорректный email' 
      });
    }

    // Проверка существующего пользователя
    const existingUser = await prisma.user.findUnique({
      where: { email }
    });

    if (existingUser) {
      return res.status(409).json({ 
        message: 'Пользователь с таким email уже существует' 
      });
    }

    // Хеширование пароля
    const salt = await bcrypt.genSalt(12);
    const hashedPassword = await bcrypt.hash(password, salt);

    // Создание пользователя
    const user = await prisma.user.create({
      data: {
        email,
        password: hashedPassword,
        name
      },
      select: {
        id: true,
        email: true,
        name: true,
        dateJoined: true
      }
    });

    // Генерация токенов
    const tokens = await generateTokens(user.id);

    res.status(201).json({
      message: 'Регистрация успешна',
      user,
      tokens
    });
  } catch (error) {
    console.error('Registration error:', error);
    res.status(500).json({ 
      message: 'Ошибка регистрации',
      error: process.env.NODE_ENV === 'development' ? error.message : undefined
    });
  }
};

// POST /api/auth/login/
exports.login = async (req, res) => {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({ 
        message: 'Email и пароль обязательны' 
      });
    }

    // Поиск пользователя
    const user = await prisma.user.findUnique({
      where: { email }
    });

    if (!user) {
      return res.status(401).json({ 
        message: 'Неверный email или пароль' 
      });
    }

    // Проверка пароля
    const isPasswordValid = await bcrypt.compare(password, user.password);
    if (!isPasswordValid) {
      return res.status(401).json({ 
        message: 'Неверный email или пароль' 
      });
    }

    // Генерация токенов
    const tokens = await generateTokens(user.id);

    // Удаляем пароль из ответа
    const { password: _, ...userWithoutPassword } = user;

    res.json({
      message: 'Вход выполнен успешно',
      user: userWithoutPassword,
      tokens
    });
  } catch (error) {
    console.error('Login error:', error);
    res.status(500).json({ 
      message: 'Ошибка входа',
      error: process.env.NODE_ENV === 'development' ? error.message : undefined
    });
  }
};

// POST /api/auth/refresh/
exports.refreshToken = async (req, res) => {
  try {
    const { refreshToken } = req.body;

    if (!refreshToken) {
      return res.status(400).json({ 
        message: 'Refresh токен обязателен' 
      });
    }

    const storedToken = await prisma.refreshToken.findUnique({
      where: { token: refreshToken }
    });

    if (!storedToken) {
      return res.status(401).json({ 
        message: 'Недействительный refresh токен' 
      });
    }

    if (new Date() > storedToken.expiresAt) {
      await prisma.refreshToken.delete({
        where: { id: storedToken.id }
      });
      
      return res.status(401).json({ 
        message: 'Refresh токен истек' 
      });
    }

    // Удаляем старый токен
    await prisma.refreshToken.delete({
      where: { id: storedToken.id }
    });

    // Генерируем новые токены
    const tokens = await generateTokens(storedToken.userId);

    res.json({
      message: 'Токен обновлен',
      tokens
    });
  } catch (error) {
    console.error('Refresh token error:', error);
    res.status(500).json({ 
      message: 'Ошибка обновления токена' 
    });
  }
};