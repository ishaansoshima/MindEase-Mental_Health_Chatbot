const express = require('express');
const router = express.Router();
const { saveChatLog, getChatLogs } = require('../controllers/chatLogsController');

router.post('/logs', saveChatLog);
router.get('/logs/:sessionId', getChatLogs);

module.exports = router; 