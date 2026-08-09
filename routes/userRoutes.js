const express = require('express');
const router = express.Router();
const auth = require('../middleware/auth');
const userController = require('../controllers/userController');

router.use(auth);

router.get('/profile', userController.getProfile);
router.put('/settings', userController.updateSettings);

module.exports = router;