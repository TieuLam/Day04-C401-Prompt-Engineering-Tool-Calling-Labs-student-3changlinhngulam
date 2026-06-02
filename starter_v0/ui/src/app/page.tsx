'use client';
import React, { useState } from 'react';

type Role = 'user' | 'agent' | 'tool';

interface Message {
  id: string;
  role: Role;
  content: string;
  toolName?: string;
  toolArgs?: any;
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'agent',
      content: 'Xin chào! Tôi là Trợ lý Nghiên cứu của bạn. Tôi có thể giúp gì cho bạn hôm nay?',
    }
  ]);
  const [input, setInput] = useState('');

  const handleSend = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMsg: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
    };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');

    // Mocking an agent response with a tool call
    setTimeout(() => {
      const toolMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: 'tool',
        content: 'Đang thực thi công cụ...',
        toolName: 'social_search',
        toolArgs: { query: input, search_type: 'Latest' },
      };
      setMessages((prev) => [...prev, toolMsg]);

      setTimeout(() => {
        const agentMsg: Message = {
          id: (Date.now() + 2).toString(),
          role: 'agent',
          content: `Tôi đã tìm kiếm trên Twitter về "${input}" và tìm thấy một số cuộc thảo luận mới nhất rất thú vị!`,
        };
        setMessages((prev) => [...prev, agentMsg]);
      }, 1500);
    }, 1000);
  };

  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white flex flex-col items-center justify-center p-4 relative overflow-hidden">
      {/* Background gradients */}
      <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] bg-blue-600/20 blur-[120px] rounded-full pointer-events-none" />
      <div className="absolute bottom-[-20%] right-[-10%] w-[50%] h-[50%] bg-purple-600/20 blur-[120px] rounded-full pointer-events-none" />

      <main className="z-10 w-full max-w-4xl flex flex-col h-[90vh] bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl shadow-2xl overflow-hidden">
        
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-white/10 bg-black/20">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-blue-500 to-purple-500 flex items-center justify-center font-bold shadow-lg">
              AI
            </div>
            <div>
              <h1 className="font-semibold text-lg">Giao diện Trợ lý Nghiên cứu</h1>
              <p className="text-xs text-green-400 flex items-center">
                <span className="w-2 h-2 rounded-full bg-green-400 mr-2 animate-pulse"></span>
                Trực tuyến (Giai đoạn 3)
              </p>
            </div>
          </div>
        </div>

        {/* Chat Area */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6 scroll-smooth">
          {messages.map((msg) => (
            <div key={msg.id} className={`flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
              <div 
                className={`max-w-[80%] rounded-2xl p-4 ${
                  msg.role === 'user' 
                    ? 'bg-blue-600/80 text-white rounded-br-none' 
                    : msg.role === 'tool'
                    ? 'bg-gray-800/80 text-gray-300 font-mono text-sm border border-gray-600/50 rounded-tl-none'
                    : 'bg-white/10 text-gray-100 rounded-tl-none'
                }`}
              >
                {msg.role === 'tool' ? (
                  <div>
                    <div className="flex items-center text-purple-400 mb-2 font-semibold">
                      <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
                      Gọi Công cụ: {msg.toolName}
                    </div>
                    <pre className="bg-black/50 p-2 rounded-lg overflow-x-auto text-xs text-green-300">
                      {JSON.stringify(msg.toolArgs, null, 2)}
                    </pre>
                  </div>
                ) : (
                  <p className="whitespace-pre-wrap">{msg.content}</p>
                )}
              </div>
            </div>
          ))}
        </div>

        {/* Input Area */}
        <div className="p-4 bg-black/40 border-t border-white/10">
          <form onSubmit={handleSend} className="flex items-center space-x-2 bg-white/5 border border-white/10 rounded-full p-2 focus-within:border-white/30 transition-colors">
            <input 
              type="text" 
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Hỏi trợ lý nghiên cứu..." 
              className="flex-1 bg-transparent px-4 py-2 outline-none text-white placeholder-gray-500"
            />
            <button 
              type="submit"
              disabled={!input.trim()}
              className="bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-400 hover:to-purple-400 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-full p-2 transition-all duration-200"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
            </button>
          </form>
        </div>
      </main>
    </div>
  );
}
