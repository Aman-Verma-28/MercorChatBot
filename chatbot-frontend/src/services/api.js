import axios from 'axios';

const API_BASE_URL = '';

export const sendMessage = async (message) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/send-message`, { message });
    return response.data;
  } catch (error) {
    console.error("Error sending message:", error);
    throw error;
  }
};