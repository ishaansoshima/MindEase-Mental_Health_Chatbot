const pool = require('../database/db');
const { v4: uuidv4 } = require('uuid');

const saveChatLog = async (req, res) => {
    const { message, isUser, sessionId, userId } = req.body;
    
    try {
        const query = `
            INSERT INTO chat_logs (user_id, message, is_user, session_id)
            VALUES ($1, $2, $3, $4)
            RETURNING *;
        `;
        
        const values = [userId, message, isUser, sessionId];
        const result = await pool.query(query, values);
        
        res.status(201).json({
            success: true,
            data: result.rows[0]
        });
    } catch (error) {
        console.error('Error saving chat log:', error);
        res.status(500).json({
            success: false,
            error: 'Failed to save chat log'
        });
    }
};

const getChatLogs = async (req, res) => {
    const { sessionId } = req.params;
    
    try {
        const query = `
            SELECT * FROM chat_logs
            WHERE session_id = $1
            ORDER BY timestamp ASC;
        `;
        
        const result = await pool.query(query, [sessionId]);
        
        res.status(200).json({
            success: true,
            data: result.rows
        });
    } catch (error) {
        console.error('Error fetching chat logs:', error);
        res.status(500).json({
            success: false,
            error: 'Failed to fetch chat logs'
        });
    }
};

module.exports = {
    saveChatLog,
    getChatLogs
}; 