import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  TextField,
  Button,
  Paper,
  Avatar,
  CircularProgress,
  Alert,
  Chip,
} from '@mui/material';
import { Send, SmartToy, Person, Psychology } from '@mui/icons-material';
import { api } from '../services/api';

interface Message {
  id: number;
  text: string;
  sender: 'user' | 'ai';
  timestamp: Date;
  ai_provider?: string;
}

const Chat = () => {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      text: "Hello! I'm your Construction AI Assistant. I can help you with:\n\n• Material takeoffs and quantities\n• Cost estimation using Estonian prices\n• BOQ generation\n• Construction document analysis\n\nHow can I assist you today?",
      sender: 'ai',
      timestamp: new Date()
    },
  ]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [aiStatus, setAiStatus] = useState<{ provider: string; gemini_configured: boolean } | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Check AI status on mount
    const checkStatus = async () => {
      try {
        const response = await api.get('/v1/chat/status');
        setAiStatus(response.data);
      } catch (err) {
        console.error('Failed to check AI status:', err);
      }
    };
    checkStatus();
  }, []);

  const handleSend = async () => {
    if (!message.trim() || loading) return;

    const userMessage: Message = {
      id: Date.now(),
      text: message,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setMessage('');
    setLoading(true);
    setError(null);

    try {
      const response = await api.post('/v1/chat', {
        message: message,
        session_id: 'default'
      });

      const aiMessage: Message = {
        id: Date.now() + 1,
        text: response.data.response,
        sender: 'ai',
        timestamp: new Date(response.data.timestamp),
        ai_provider: response.data.ai_provider
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (err: any) {
      setError(err.message || 'Failed to get response');
      // Add error message to chat
      const errorMessage: Message = {
        id: Date.now() + 1,
        text: "I'm sorry, I encountered an error processing your request. Please try again.",
        sender: 'ai',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <Box sx={{ height: 'calc(100vh - 200px)', display: 'flex', flexDirection: 'column' }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Box>
          <Typography variant="h4" fontWeight={700} gutterBottom>
            AI Assistant Chat
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Ask questions about construction, materials, and cost estimation
          </Typography>
        </Box>
        {aiStatus && (
          <Chip
            icon={<Psychology />}
            label={aiStatus.provider === 'gemini' ? 'Gemini AI' : 'Fallback Mode'}
            color={aiStatus.provider === 'gemini' ? 'success' : 'default'}
            variant="outlined"
          />
        )}
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {aiStatus && !aiStatus.gemini_configured && (
        <Alert severity="info" sx={{ mb: 2 }}>
          Running in fallback mode. Set GEMINI_API_KEY environment variable for full AI capabilities.
        </Alert>
      )}

      <Card sx={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
        <CardContent sx={{ flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column' }}>
          {messages.map(msg => (
            <Box
              key={msg.id}
              sx={{
                display: 'flex',
                mb: 2,
                justifyContent: msg.sender === 'user' ? 'flex-end' : 'flex-start'
              }}
            >
              {msg.sender === 'ai' && (
                <Avatar sx={{ mr: 1, bgcolor: '#FF6B00' }}>
                  <SmartToy />
                </Avatar>
              )}
              <Paper
                elevation={1}
                sx={{
                  p: 2,
                  maxWidth: '70%',
                  bgcolor: msg.sender === 'user' ? '#1E3A5F' : '#f5f5f5',
                  color: msg.sender === 'user' ? 'white' : 'text.primary',
                  borderRadius: 2,
                }}
              >
                <Typography sx={{ whiteSpace: 'pre-wrap' }}>{msg.text}</Typography>
                {msg.ai_provider && (
                  <Typography variant="caption" sx={{ opacity: 0.7, display: 'block', mt: 1 }}>
                    via {msg.ai_provider}
                  </Typography>
                )}
              </Paper>
              {msg.sender === 'user' && (
                <Avatar sx={{ ml: 1, bgcolor: '#1E3A5F' }}>
                  <Person />
                </Avatar>
              )}
            </Box>
          ))}
          {loading && (
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Avatar sx={{ bgcolor: '#FF6B00' }}>
                <SmartToy />
              </Avatar>
              <Paper sx={{ p: 2, bgcolor: '#f5f5f5', display: 'flex', alignItems: 'center', gap: 1 }}>
                <CircularProgress size={16} />
                <Typography variant="body2" color="text.secondary">
                  Thinking...
                </Typography>
              </Paper>
            </Box>
          )}
          <div ref={messagesEndRef} />
        </CardContent>

        <Box sx={{ p: 2, borderTop: '1px solid #e0e0e0', display: 'flex', gap: 1 }}>
          <TextField
            fullWidth
            placeholder="Ask about your construction project..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            disabled={loading}
            multiline
            maxRows={3}
          />
          <Button
            variant="contained"
            onClick={handleSend}
            endIcon={loading ? <CircularProgress size={16} color="inherit" /> : <Send />}
            disabled={!message.trim() || loading}
            sx={{ minWidth: 100 }}
          >
            Send
          </Button>
        </Box>
      </Card>
    </Box>
  );
};

export default Chat;
