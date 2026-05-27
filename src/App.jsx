import React, { useState, useEffect, useRef } from 'react';
import StationCard from './StationCard';
import { sendMessageToRouter } from './api';

export default function App() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([
    { role: 'bot', content: "Hi! I'm your Berlin Accessibility Guide. Type a station name (Hauptbahnhof, Zoo, Alexanderplatz...)" }
  ]);
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef(null);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const getMockResponse = (userInput) => {
    const query = userInput.toLowerCase();
    if (query.includes('hauptbahnhof'))
      return { text: "Berlin Hauptbahnhof is fully accessible. All platforms have working elevators today.", stations: [{ name: "Berlin Hauptbahnhof", elevatorStatus: "Operational", notes: "Clear access to all levels." }] };
    if (query.includes('alexanderplatz'))
      return { text: "Alexanderplatz is mostly accessible, but the U8 elevator is currently under maintenance.", stations: [{ name: "Alexanderplatz", elevatorStatus: "Limited", notes: "U8 elevator out until 4 PM." }] };
    if (query.includes('friedrichstrasse') || query.includes('friedrichstraße'))
      return { text: "Friedrichstraße has step-free access for S-Bahn and Regional trains.", stations: [{ name: "Friedrichstraße", elevatorStatus: "Operational", notes: "Step-free transition available." }] };
    if (query.includes('zoo') || query.includes('zoologischer') || query.includes('garten'))
      return { text: "Zoologischer Garten has full elevator access for U2, U9, and all S-Bahn lines.", stations: [{ name: "Zoologischer Garten", elevatorStatus: "Operational", notes: "Large elevators for wheelchairs." }] };
    if (query.includes('ostbahnhof'))
      return { text: "Ostbahnhof is accessible. The main hall ramp is open.", stations: [{ name: "Ostbahnhof", elevatorStatus: "Operational", notes: "Main hall ramp open." }] };
    return { text: "I don't have data for that station yet. Try Hauptbahnhof, Alexanderplatz, Friedrichstraße, Zoo, or Ostbahnhof.", stations: [] };
  };

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMsg = { role: 'user', content: input };
    setMessages(prev => [...prev, userMsg]);
    setLoading(true);
    const query = input;
    setInput('');

    try {
      const response = await sendMessageToRouter(query);
      setMessages(prev => [...prev, { role: 'bot', content: response.text, stations: response.stations }]);
    } catch {
      const fallback = getMockResponse(query);
      setMessages(prev => [...prev, { role: 'bot', content: fallback.text, stations: fallback.stations }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-screen bg-slate-50 flex flex-col items-center p-4 overflow-hidden">

      <header className="py-4 text-center">
        <h1 className="text-4xl font-black tracking-tighter text-blue-600">
          GO<span className="text-purple-600 font-light">ACCESS</span>
        </h1>
        <div className="text-[10px] font-mono bg-yellow-100 text-yellow-700 px-2 py-0.5 rounded-full inline-block uppercase tracking-tighter border border-yellow-200">
          Berlin Transit Accessibility
        </div>
      </header>

      <main className="w-full max-w-full bg-white border-4 border-blue-600 rounded-[40px] flex flex-col flex-1 overflow-hidden shadow-2xl mb-4">

        <div className="flex-1 overflow-y-auto p-10 space-y-8 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] bg-fixed">
          {messages.map((msg, i) => (
            <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-[75%] text-2xl font-bold leading-snug p-6 rounded-3xl shadow-sm ${
                msg.role === 'user'
                  ? 'bg-blue-600 text-white border-b-8 border-blue-800'
                  : 'bg-white border-4 border-purple-600 text-purple-700'
              }`}>
                {msg.content}
                {msg.stations?.map((s, idx) => <StationCard key={idx} station={s} />)}
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex justify-start">
              <div className="text-2xl font-bold p-6 rounded-3xl bg-white border-4 border-purple-600 text-purple-400">
                ...
              </div>
            </div>
          )}

          <div ref={scrollRef} />
        </div>

        <div className="p-6 border-t-4 border-blue-600 bg-white">
          <div className="flex gap-4 items-stretch h-[25vh]">
            <textarea
              className="w-1/4 text-2xl border-4 border-purple-600 rounded-[32px] px-8 py-8 text-purple-700 outline-none focus:ring-8 focus:ring-blue-100 placeholder:text-purple-200 resize-none font-bold shadow-inner"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && (e.preventDefault(), handleSend())}
              placeholder="Search station..."
              disabled={loading}
            />
            <button
              onClick={handleSend}
              disabled={loading}
              className="flex-1 bg-blue-600 text-white text-6xl font-black rounded-[32px] hover:bg-purple-600 transition-all active:scale-95 flex items-center justify-center shadow-lg border-b-8 border-blue-800 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? '...' : 'SEND'}
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}
