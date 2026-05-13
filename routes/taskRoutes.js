const express = require("express");
const router = express.Router();
const auth = require("../middleware/auth");
const taskController = require("../controllers/taskController");

// Проверяем, что контроллер и middleware корректны
console.log("Task controller methods:", Object.keys(taskController));
console.log("Auth middleware type:", typeof auth);

// Все маршруты задач требуют аутентификации
router.use(auth);

router.get("/", taskController.getTasks);
router.post("/", taskController.createTask);
router.get("/:id", taskController.getTask);
router.put("/:id", taskController.updateTask);
router.patch("/:id", taskController.patchTask);
router.delete("/:id", taskController.deleteTask);

module.exports = router;
