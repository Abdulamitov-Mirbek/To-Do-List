const express = require("express");
const router = express.Router();
const authController = require("../controllers/authController");

// Проверяем, что контроллер содержит нужные функции
console.log("Auth controller methods:", Object.keys(authController));

router.post("/register", authController.register);
router.post("/login", authController.login);
router.post("/refresh", authController.refreshToken);

module.exports = router;
