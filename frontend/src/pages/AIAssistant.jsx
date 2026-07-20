import { useState } from "react";
import api from "../services/api";

function AIAssistant() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content:
        "Hello! I'm your AI-HCP CRM Assistant. I can log, edit, and search interactions, summarize HCP history, and recommend follow-up actions.",
    },
  ]);

  const [loading, setLoading] = useState(false);

  const sendMessage = async (text) => {
    const userMessage = text || message.trim();

    if (!userMessage || loading) {
      return;
    }

    setMessages((previous) => [
      ...previous,
      {
        role: "user",
        content: userMessage,
      },
    ]);

    setMessage("");
    setLoading(true);

    try {
      const response = await api.post("/ai/chat", {
        message: userMessage,
      });

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content:
            response.data.response ||
            "The request was processed successfully.",
        },
      ]);
    } catch (error) {
      console.error(error);

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content:
            "I couldn't process that request. Please check that the backend is running and try again.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    sendMessage();
  };

  const examples = [
    "Log a Call interaction for HCP ID 1. The doctor requested product information.",
    "Edit interaction ID 1. Change the type to Follow-up Call and update the notes to Doctor requested another discussion next week.",
    "Search for Follow-up Call interactions.",
    "Summarize all interactions for HCP ID 1.",
    "Recommend the next follow-up action for HCP ID 1.",
  ];

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>AI Assistant</h1>
          <p>
            Manage your CRM using natural language with Groq and
            LangGraph.
          </p>
        </div>

        <div className="ai-status">
          <span className="status-dot"></span>
          AI Online
        </div>
      </div>

      <div className="ai-layout">
        <div className="chat-card">
          <div className="chat-header">
            <div>
              <h2>CRM Assistant</h2>
              <p>Ask the AI to manage your HCP interactions.</p>
            </div>
          </div>

          <div className="chat-messages">
            {messages.map((item, index) => (
              <div
                key={index}
                className={`message-row ${item.role}`}
              >
                <div className={`message-bubble ${item.role}`}>
                  {item.content}
                </div>
              </div>
            ))}

            {loading && (
              <div className="message-row assistant">
                <div className="message-bubble assistant">
                  Thinking...
                </div>
              </div>
            )}
          </div>

          <form
            className="chat-input-area"
            onSubmit={handleSubmit}
          >
            <textarea
              value={message}
              onChange={(event) =>
                setMessage(event.target.value)
              }
              placeholder="Ask your AI CRM assistant..."
              rows="2"
            />

            <button
              type="submit"
              disabled={loading || !message.trim()}
            >
              Send
            </button>
          </form>
        </div>

        <div className="ai-tools-card">
          <h2>AI Tools</h2>

          <p className="tools-description">
            Try one of these example commands:
          </p>

          <div className="example-list">
            {examples.map((example, index) => (
              <button
                key={index}
                onClick={() => sendMessage(example)}
                disabled={loading}
                className="example-command"
              >
                {example}
              </button>
            ))}
          </div>

          <div className="capabilities">
            <h3>Capabilities</h3>

            <div className="capability-item">
              <strong>Log Interaction</strong>
              <span>Create CRM records with AI</span>
            </div>

            <div className="capability-item">
              <strong>Edit Interaction</strong>
              <span>Update existing records</span>
            </div>

            <div className="capability-item">
              <strong>Search</strong>
              <span>Find relevant interaction history</span>
            </div>

            <div className="capability-item">
              <strong>Meeting Summary</strong>
              <span>Generate AI-powered summaries</span>
            </div>

            <div className="capability-item">
              <strong>Follow-up</strong>
              <span>Recommend the next action</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default AIAssistant;