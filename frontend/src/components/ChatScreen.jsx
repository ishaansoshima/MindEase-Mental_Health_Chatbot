import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Box, 
  TextField, 
  IconButton, 
  Typography, 
  Paper, 
  Avatar,
  Container,
  AppBar,
  Toolbar,
  CircularProgress,
  Snackbar,
  Alert
} from '@mui/material';
import { Send, ArrowBack } from '@mui/icons-material';
import PsychologyIcon from '@mui/icons-material/Psychology';
import { sendMessage, checkServerStatus } from '../services/api';

const ChatScreen = () => {
  const [messages, setMessages] = useState([
    { text: "Hello! I'm MindEase, your mental health companion. How can I help you today?", sender: 'bot' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);
  const navigate = useNavigate();
  
  // Check server status on component mount
  useEffect(() => {
    const checkServer = async () => {
      const isServerUp = await checkServerStatus();
      if (!isServerUp) {
        setError('Unable to connect to the server. Please try again later.');
      }
    };
    checkServer();
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (input.trim() === '' || isLoading) return;

    try {
      // Add user message
      const userMessage = { text: input, sender: 'user' };
      const updatedMessages = [...messages, userMessage];
      setMessages(updatedMessages);
      setInput('');
      setIsLoading(true);
      setError(null);

      // Send message to API
      const response = await sendMessage(input, messages);
      
      // Add bot response
      setMessages([...updatedMessages, { text: response.response, sender: 'bot' }]);
    } catch (err) {
      console.error('Error sending message:', err);
      setError(err.message || 'Failed to get response from the server');
      // Revert to previous state if there's an error
      setMessages(messages);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Box sx={{ 
      width: '100%',
      maxWidth: '800px',
      height: '90vh',
      maxHeight: '900px',
      display: 'flex',
      flexDirection: 'column',
      backgroundColor: 'white',
      borderRadius: '16px',
      boxShadow: '0 4px 20px rgba(0, 0, 0, 0.1)',
      overflow: 'hidden',
      position: 'fixed',
      top: '50%',
      left: '50%',
      transform: 'translate(-50%, -50%)',
      '@media (max-height: 800px)': {
        height: '95vh',
        maxHeight: 'none',
        borderRadius: 0
      },
      '@media (max-width: 900px)': {
        width: '95%',
        maxWidth: 'none',
        height: '100vh',
        maxHeight: 'none',
        borderRadius: 0
      }
    }}>
      {/* Header */}
      <Box sx={{ 
        backgroundColor: '#1976d2',
        color: 'white',
        p: 2,
        display: 'flex',
        alignItems: 'center',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
      }}>
        <IconButton
          edge="start"
          color="inherit"
          aria-label="back to home"
          onClick={() => navigate('/')}
          sx={{ mr: 1 }}
        >
          <ArrowBack />
        </IconButton>
        <PsychologyIcon sx={{ mr: 1.5 }} />
        <Typography variant="h6" component="h1" sx={{ fontWeight: 'bold' }}>
          MindEase Chat
        </Typography>
      </Box>

      {/* Messages container */}
      <Box sx={{ 
        flex: 1, 
        overflowY: 'auto', 
        p: 2,
        backgroundColor: '#f5f9ff',
        display: 'flex',
        flexDirection: 'column',
        gap: 1.5
      }}>
        {messages.map((message, index) => (
          <Box
            key={index}
            sx={{
              maxWidth: '85%',
              alignSelf: message.sender === 'user' ? 'flex-end' : 'flex-start',
              display: 'flex',
              alignItems: 'flex-end',
              gap: 1,
              mb: 1.5
            }}
          >
            {message.sender === 'bot' && (
              <Avatar sx={{ 
                width: 32, 
                height: 32, 
                bgcolor: '#9c27b0',
                alignSelf: 'flex-end',
                mb: 0.5
              }}>
                <PsychologyIcon sx={{ fontSize: 18 }} />
              </Avatar>
            )}
            <Paper
              elevation={0}
              sx={{
                p: 1.5,
                backgroundColor: message.sender === 'user' ? '#bbdefb' : 'white',
                borderRadius: message.sender === 'user' 
                  ? '18px 18px 0 18px' 
                  : '18px 18px 18px 4px',
                boxShadow: '0 1px 2px rgba(0,0,0,0.1)',
              }}
            >
              <Typography variant="body1" sx={{ lineHeight: 1.4 }}>
                {message.text}
              </Typography>
            </Paper>
          </Box>
        ))}
        <div ref={messagesEndRef} />
      </Box>

      {/* Message input */}
      <Paper
        component="form"
        onSubmit={handleSend}
        sx={{
          p: '2px 4px',
          display: 'flex',
          alignItems: 'center',
          width: '100%',
          borderRadius: '24px',
          boxShadow: '0 2px 10px rgba(0,0,0,0.1)'
        }}
      >
        <TextField
          fullWidth
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          variant="outlined"
          size="small"
          disabled={isLoading}
          sx={{
            '& .MuiOutlinedInput-root': {
              borderRadius: '24px',
              '& fieldset': {
                border: 'none',
              },
            },
          }}
        />
        <IconButton 
          type="submit" 
          color="primary" 
          sx={{ 
            p: '10px',
            backgroundColor: '#9c27b0',
            color: 'white',
            '&:hover': {
              backgroundColor: '#7b1fa2',
            },
            '&:disabled': {
              backgroundColor: '#e0e0e0',
            }
          }}
          disabled={!input.trim() || isLoading}
        >
          {isLoading ? <CircularProgress size={24} color="inherit" /> : <Send />}
        </IconButton>
      </Paper>
      
      <Snackbar 
        open={!!error} 
        autoHideDuration={6000} 
        onClose={() => setError(null)}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert onClose={() => setError(null)} severity="error" sx={{ width: '100%' }}>
          {error}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default ChatScreen;
