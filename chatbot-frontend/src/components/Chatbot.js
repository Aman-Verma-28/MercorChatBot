import React, { useState } from 'react';
import './Chatbot.css';  
import sendMessageToApi from './Apicall';

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');

  const handleSendMessage = async () => {
    if (newMessage.trim() === '') return;

    const userMessage = { text: newMessage, isUser: true };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setNewMessage('');

    try {
      const apiResponse = await sendMessageToApi(newMessage); 
      console.log(apiResponse)
      const botMessage = { text: apiResponse, isUser: false };
      setMessages((prevMessages) => [...prevMessages, botMessage]);
    } catch (error) {
      console.error("Error sending message:", error);
      const errorMessage = { text: 'Failed to get response from the bot.', isUser: false };
      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    }
  };

  return (
    <div className="chatbot-container">
      <div className="chatbot-header">
        <img src="https://via.placeholder.com/30" alt="Bot Icon" className="bot-icon" />
        <h2 className="chatbot-title">Mercor Assist</h2>
      </div>
      <div className="chatbot-messages">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`chatbot-message ${message.isUser ? 'user-message' : 'bot-message'}`}
          >
            {message.text}
          </div>
        ))}
      </div>
      <div className="chatbot-input-container">
        <input
          type="text"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          placeholder="Type a message"
          className="chatbot-input"
        />
        <button
          onClick={handleSendMessage}
          className="chatbot-send-button"
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default Chatbot;
