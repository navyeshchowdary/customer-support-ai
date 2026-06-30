import { useState, useRef, useEffect } from 'react'
import axios from 'axios'
import './App.css'

const API_URL = 'https://customer-support-ai-production-8eb5.up.railway.app/chat'

function App() {
    const [messages, setMessages] = useState([
        { sender: 'bot', text: "Hi! I'm TechMart's AI support assistant. How can I help you today?" }
    ])
    const [input, setInput] = useState('')
    const [loading, setLoading] = useState(false)
    const [sessionId, setSessionId] = useState(null)
    const messagesEndRef = useRef(null)

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }

    useEffect(() => {
        scrollToBottom()
    }, [messages])

    const sendMessage = async () => {
        if (!input.trim() || loading) return

        const userMessage = { sender: 'user', text: input }
        setMessages((prev) => [...prev, userMessage])
        setInput('')
        setLoading(true)

        try {
            const res = await axios.post(API_URL, { message: input })
            if (!sessionId) setSessionId(res.data.session_id)
            const botMessage = {
                sender: 'bot',
                text: res.data.response,
                intent: res.data.intent
            }
            setMessages((prev) => [...prev, botMessage])
        } catch (error) {
            setMessages((prev) => [
                ...prev,
                { sender: 'bot', text: 'Sorry, something went wrong. Please make sure the backend server is running.' }
            ])
        } finally {
            setLoading(false)
        }
    }

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault()
            sendMessage()
        }
    }

    return (
        <div className="chat-container">
            <div className="chat-header">
                <h1>TechMart Support</h1>
                <p>AI-powered multi-agent assistant</p>
            </div>

            <div className="chat-messages">
                {messages.map((msg, idx) => (
                    <div key={idx} className={`message ${msg.sender}`}>
                        {msg.sender === 'bot' && msg.intent ? (
                            <span className="intent-badge">{msg.intent}</span>
                        ) : null}
                        <div className="message-bubble">{msg.text}</div>
                    </div>
                ))}
                {loading ? (
                    <div className="message bot">
                        <div className="message-bubble typing">Typing...</div>
                    </div>
                ) : null}
                <div ref={messagesEndRef}></div>
            </div>

            <div className="chat-input-area">
                <textarea
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Type your message..."
                    rows={1}
                ></textarea>
                <button onClick={sendMessage} disabled={loading}>
                    Send
                </button>
            </div>
        </div>
    )
}

export default App