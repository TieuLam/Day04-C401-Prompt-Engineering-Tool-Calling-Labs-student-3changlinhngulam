import React from 'react';

export default function Home() {
  return (
    <div className="min-h-screen bg-black text-white flex flex-col items-center justify-center p-4 relative overflow-hidden">
      {/* Background gradients */}
      <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] bg-blue-600/30 blur-[120px] rounded-full pointer-events-none" />
      <div className="absolute bottom-[-20%] right-[-10%] w-[50%] h-[50%] bg-purple-600/30 blur-[120px] rounded-full pointer-events-none" />

      <main className="z-10 w-full max-w-3xl flex flex-col items-center text-center space-y-8">
        <div className="space-y-4">
          <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-purple-500 to-pink-500 animate-pulse">
            Hello World
          </h1>
          <p className="text-xl text-gray-400 max-w-xl mx-auto">
            Research Agent Interface - Phase 1 Scaffold
          </p>
        </div>

        <div className="w-full bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-6 shadow-2xl transition-all duration-300 hover:shadow-purple-500/20 hover:border-white/20">
          <div className="flex flex-col space-y-4">
            <div className="flex items-start space-x-4 p-4 rounded-xl bg-white/5">
              <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-blue-500 to-purple-500 flex items-center justify-center font-bold shadow-lg">
                AI
              </div>
              <div className="flex-1 text-left">
                <p className="text-sm font-medium text-gray-300">Research Agent</p>
                <p className="mt-1 text-gray-100">Ready for instructions. I'm connected and standing by.</p>
              </div>
            </div>
          </div>

          <div className="mt-6 flex items-center space-x-2 bg-black/40 border border-white/10 rounded-full p-2 shadow-inner">
            <input 
              type="text" 
              placeholder="Ask me anything..." 
              className="flex-1 bg-transparent px-4 py-2 outline-none text-white placeholder-gray-500"
              disabled
            />
            <button className="bg-white/10 hover:bg-white/20 text-white rounded-full p-2 transition-colors duration-200 cursor-not-allowed" disabled>
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 w-full text-left mt-8">
          {[
            { title: 'Data', desc: 'eval_group.json structure verified' },
            { title: 'UI Scaffold', desc: 'Next.js App Router & Tailwind' },
            { title: 'Status', desc: 'Phase 1 Complete' }
          ].map((item, i) => (
            <div key={i} className="p-4 rounded-xl bg-white/5 border border-white/10 hover:bg-white/10 transition-colors duration-300 cursor-default">
              <h3 className="font-semibold text-blue-400">{item.title}</h3>
              <p className="text-sm text-gray-400 mt-1">{item.desc}</p>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}
