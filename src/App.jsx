import React, { useState, useEffect, useRef } from 'react';
import StationCard from './StationCard';
import { sendMessageToRouter } from './api';

export default function App() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([
    { role: 'bot', content: "Hi! I'm your Berlin Accessibility Guide. Ask me anything about routes, elevators, or station access." }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef(null);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;
    const userMsg = { role: 'user', content: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);

    const data = await sendMessageToRouter(input);
    setMessages(prev => [...prev, { role: 'bot', content: data.text, stations: data.stations }]);
    setIsLoading(false);
  };

  return (
    <div className="min-h-screen bg-white flex flex-col items-center justify-center p-4">
      
      {/* Header */}
      <header className="mb-6 text-center">
        <h1 className="text-5xl font-black tracking-tighter text-blue-600">
          GO<span className="text-purple-600 font-light">ACCESS</span>
        </h1>
      </header>

      {/* Large Chatbot Box */}
      <main className="w-full max-w-3xl bg-white border-4 border-blue-600 rounded-[40px] flex flex-col h-[80vh] overflow-hidden shadow-none">
        
        {/* Chat Messages Area */}
        <div className="flex-1 overflow-y-auto p-10 space-y-8">
          {messages.map((msg, i) => (
            <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-[85%] text-xl font-bold leading-snug p-6 rounded-3xl ${
                msg.role === 'user' 
                  ? 'text-blue-600 border-2 border-blue-600' 
                  : 'text-purple-600 border-2 border-purple-600'
              }`}>
                {msg.content}
                {msg.stations?.map((s, idx) => <StationCard key={idx} station={s} />)}
              </div>
            </div>
          ))}
          {isLoading && <div className="text-purple-600 font-black animate-pulse text-lg italic">QUERYING BERLIN MCP...</div>}
          <div ref={scrollRef} />
        </div>

        {/* Big Input Area */}
        <div className="p-8 border-t-4 border-blue-600 bg-white">
          <div className="flex gap-4">
      
            <input 
              className="flex-1 text-2xl border-4 border-purple-600 rounded-2xl px-15 py-150 text-purple-700 outline-none focus:ring-4 focus:ring-blue-200 placeholder:text-purple-200"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              placeholder="Ask about your route..."
            />
            <button 
              onClick={handleSend}
              className="bg-blue-600 text-white text-2xl font-black px-12 py-6 rounded-2xl hover:bg-purple-600 transition-all active:scale-95"
            >
              SEND
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}