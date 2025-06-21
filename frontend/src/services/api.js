const API_BASE_URL = 'http://localhost:8001';
console.log('API Base URL:', API_BASE_URL); // Debug log

export const sendMessage = async (message, chatHistory = []) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        chat_history: chatHistory.map(msg => ({
          sender: msg.sender,
          text: msg.text
        }))
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to send message');
    }

    return await response.json();
  } catch (error) {
    console.error('Error sending message:', error);
    throw error;
  }
};

export const checkServerStatus = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/`);
    return response.ok;
  } catch (error) {
    console.error('Error checking server status:', error);
    return false;
  }
};
