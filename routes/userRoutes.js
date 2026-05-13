const express = require('express');
const router = express.Router();
const auth = require('../middleware/auth');
const userController = require('../controllers/userController');

// Проверяем, что контроллер содержит нужные функции
console.log('User controller methods:', Object.keys(userController));

router.use(auth);

router.get('/profile', userController.getProfile);
router.put('/settings', userController.updateSettings);

module.exports = router;