// src/components/Chatbot.jsx
import { useState } from 'react';
import axios from 'axios';

function Chatbot() {
    const [userMessage, setUserMessage] = useState('');
    const [messages, setMessages] = useState([]);
    const [isLoading, setIsLoading] = useState(false);

    // Function to handle form submission (sending message)
    const handleSendMessage = async (e) => {
        e.preventDefault();

        // Add user's message to the chat
        setMessages([...messages, { sender: 'user', text: userMessage }]);
        setIsLoading(true);  // Show loading indicator while awaiting response
        setUserMessage('');

        try {
            // Send user message to the Django backend (chatbot API)
            const response = await axios.post('http://127.0.0.1:8000/chatbot/', { user_message: userMessage });

            // Add bot's response to the chat
            setMessages((prevMessages) => [
                ...prevMessages,
                { sender: 'bot', text: response.data.bot_response },
            ]);
        } catch (error) {
            console.error('Error fetching chatbot response:', error);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="chatbot">
            <h2>Chat with our Assistant</h2>
            <div className="chat-window">
                <div className="messages">
                    {messages.map((message, index) => (
                        <div key={index} className={message.sender}>
                            <p>{message.text}</p>
                        </div>
                    ))}
                </div>
                {isLoading && <p>Bot is typing...</p>}
            </div>
            <form onSubmit={handleSendMessage} className="chat-form">
                <input
                    type="text"
                    value={userMessage}
                    onChange={(e) => setUserMessage(e.target.value)}
                    placeholder="Type your message..."
                    required
                />
                <button type="submit">Send</button>
            </form>
        </div>
    );
}

export default Chatbot;
