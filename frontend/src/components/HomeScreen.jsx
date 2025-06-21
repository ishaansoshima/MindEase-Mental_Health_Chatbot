import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, Box, Typography } from '@mui/material';
import BrainIcon from '@mui/icons-material/Psychology';
import ChatBubbleOutlineIcon from '@mui/icons-material/ChatBubbleOutline';

const HomeScreen = () => {
  const navigate = useNavigate();

  return (
    <Box
      sx={{
        width: '100%',
        maxWidth: '500px',
        height: '90vh',
        maxHeight: '800px',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        textAlign: 'center',
        p: 4,
        backgroundColor: 'white',
        borderRadius: '16px',
        boxShadow: '0 4px 20px rgba(0, 0, 0, 0.1)',
        position: 'fixed',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        '@media (max-height: 800px)': {
          height: '95vh',
          maxHeight: 'none',
          borderRadius: 0,
          p: 3
        },
        '@media (max-width: 600px)': {
          width: '95%',
          height: '100vh',
          maxHeight: 'none',
          borderRadius: 0,
          p: 2
        }
      }}
    >
      <Box
        sx={{
          width: 120,
          height: 120,
          borderRadius: '50%',
          backgroundColor: '#f3e5f5',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          mb: 4,
          boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
        }}
      >
        <BrainIcon sx={{ fontSize: 60, color: '#7b1fa2' }} />
      </Box>
      
      <Typography 
        variant="h3" 
        component="h1" 
        sx={{ 
          fontWeight: 'bold',
          mb: 2,
          color: '#333',
        }}
      >
        MindEase
      </Typography>
      
      <Typography 
        variant="h6" 
        component="h2"
        sx={{ 
          mb: 4,
          color: '#666',
          maxWidth: '80%',
          mx: 'auto',
        }}
      >
        Your compassionate mental health companion
      </Typography>
      
      <Button
        variant="contained"
        size="large"
        startIcon={<ChatBubbleOutlineIcon />}
        onClick={() => navigate('/chat')}
        sx={{
          backgroundColor: '#1976d2',
          '&:hover': {
            backgroundColor: '#1565c0',
          },
          px: 4,
          py: 1.5,
          borderRadius: 8,
          textTransform: 'none',
          fontSize: '1.1rem',
          mb: 4,
        }}
      >
        Start Chatting
      </Button>
      
      <Typography 
        variant="caption" 
        sx={{ 
          color: '#999',
          fontSize: '0.75rem',
          maxWidth: '80%',
          mx: 'auto',
        }}
      >
        MindEase is not a substitute for professional help. In crisis? Call your local emergency number.
      </Typography>
    </Box>
  );
};

export default HomeScreen;
