import React from 'react';

const Message = ({ text, sender }) => {
  return (
    <div style={{ textAlign: sender === 'user' ? 'right' : 'left' }}>
      <p>{text}</p>
    </div>
  );
};

export default Message;

