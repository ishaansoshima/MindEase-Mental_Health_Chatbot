const express = require('express');
const cors = require('cors');
const chatLogsRouter = require('./routes/chatLogs');

const app = express();
const port = process.env.PORT || 8000;

// Middleware
app.use(cors());
app.use(express.json());

// Routes
app.use('/api/chat', chatLogsRouter);

// Error handling middleware
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({
        success: false,
        error: 'Something went wrong!'
    });
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
}); 