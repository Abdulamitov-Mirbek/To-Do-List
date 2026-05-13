const jwt = require("jsonwebtoken");
const prisma = require("../config/database");

const auth = async (req, res, next) => {
  try {
    const authHeader = req.header("Authorization");

    if (!authHeader || !authHeader.startsWith("Bearer ")) {
      return res.status(401).json({
        message: "Требуется авторизация. Токен не предоставлен.",
        code: "AUTH_REQUIRED",
      });
    }

    const token = authHeader.replace("Bearer ", "");

    let decoded;
    try {
      decoded = jwt.verify(token, process.env.JWT_SECRET);
    } catch (jwtError) {
      if (jwtError.name === "TokenExpiredError") {
        return res.status(401).json({
          message: "Токен истек. Пожалуйста, войдите снова.",
          code: "TOKEN_EXPIRED",
        });
      }
      return res.status(401).json({
        message: "Недействительный токен.",
        code: "INVALID_TOKEN",
      });
    }

    const user = await prisma.user.findUnique({
      where: { id: decoded.userId },
      select: {
        id: true,
        email: true,
        name: true,
        dateJoined: true,
      },
    });

    if (!user) {
      return res.status(401).json({
        message: "Пользователь не найден.",
        code: "USER_NOT_FOUND",
      });
    }

    req.user = user;
    req.userId = user.id;
    next();
  } catch (error) {
    console.error("Auth middleware error:", error);
    res.status(500).json({
      message: "Ошибка аутентификации.",
      code: "AUTH_ERROR",
    });
  }
};

module.exports = auth;
