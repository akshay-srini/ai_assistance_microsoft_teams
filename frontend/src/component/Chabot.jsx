import React, { useState } from "react";
import send from "../images/send.png";
import axios from "axios";
import ReactMarkdown from 'react-markdown';


export default function Chatbot() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const handleInputChange = (event) => {
    setInput(event.target.value); 
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      // Create a new message object for the user's input
      const userInputMessage = { text: input, fromUser: true };

      // Update the messages state using the functional form of setMessages
      setMessages(prevMessages => [...prevMessages, userInputMessage]);

      // Make POST request to the backend API
      const response = await axios.post('http://127.0.0.1:8000/api/chatbot/', {
        message: input,
      });

      // Create a new message object for the bot's response
      const botResponseMessage = { text: response.data.response, fromUser: false };

      // Update the messages state again using the functional form of setMessages
      setMessages(prevMessages => [...prevMessages, botResponseMessage]);

      // Clear the input field after submission
      setInput('');
    } catch (error) {
      console.error('Error sending message to API:', error);
    }
  };

  return (
    <section className="chatbot-container-section">
      <div className="chat-window">
        {messages.map((message, index) => (
          <ReactMarkdown key={index} className={`message ${message.fromUser ? 'user' : 'bot'}`}>
            {message.text}
          </ReactMarkdown>
        ))}
      </div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={handleInputChange}
          placeholder="Type your message..."
        />
        <button type="submit">
          <img src={send} alt="" className="send-icon-size" />
        </button>
      </form>
    </section>
  );
}
