import React, { useState, useEffect, useRef, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { chat, profile as profileApi } from '../api/endpoints';
import { 
  Bot, 
  Send, 
  Sparkles, 
  AlertTriangle, 
  ShieldCheck, 
  User, 
  RefreshCw, 
  HelpCircle,
  BookOpen,
  Info,
  CheckCircle2
} from 'lucide-react';

const SUGGESTIONS = [
  "Can I eat spinach/palak while taking Warfarin?",
  "Suggest a high-protein Indian breakfast without eggs",
  "What Indian foods have a low glycemic index for Diabetes?",
  "Safe snack for Chronic Kidney Disease (low potassium)",
  "What can I replace paneer with for lactose intolerance?"
];

export default function AIAssistant() {
  const { user } = useContext(AuthContext);
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'assistant',
      text: `Namaste${user?.name ? ' ' + user.name : ''}! I am your **NutriGuard Clinical AI Assistant**.\n\nI combine **ICMR-NIN Indian Food Composition Tables (IFCT 2017)** with strict clinical pharmacology rules to give you safe, authentic meal guidance.\n\nAsk me anything about Indian foods, recipe substitutions, macro targets, or drug-nutrient interactions!`,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      safety: { status: 'SAFE' }
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [userProfile, setUserProfile] = useState(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    profileApi.getProfile()
      .then(res => setUserProfile(res.data))
      .catch(() => setUserProfile(null));
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSend = async (messageText) => {
    const textToSend = messageText || input;
    if (!textToSend.trim() || loading) return;

    const userMessage = {
      id: Date.now(),
      sender: 'user',
      text: textToSend,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      // Build user context
      const userContext = {
        name: user?.name,
        dietary_pattern: userProfile?.dietary_pattern || userProfile?.diet_type || 'VEGETARIAN',
        conditions: userProfile?.conditions || [],
        medications: userProfile?.medications || [],
        allergies: userProfile?.allergies || []
      };

      const res = await chat.sendMessage(textToSend, userContext);
      const data = res.data;

      // Extract response text and safety metadata
      const replyText = data.response || data.message || data.reply || (typeof data === 'string' ? data : JSON.stringify(data));
      
      const assistantMessage = {
        id: Date.now() + 1,
        sender: 'assistant',
        text: replyText,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        safety: data.safety || (data.flagged ? { status: 'WARNING', reason: data.warning } : null),
        citations: data.citations || ["ICMR-NIN (2024)", "Indian Food Composition Tables (IFCT 2017)"]
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (err) {
      console.error("Chat error:", err);
      const errorMessage = {
        id: Date.now() + 1,
        sender: 'assistant',
        text: "I experienced a temporary network issue connecting to the nutrition intelligence engine. Please try asking again in a moment.",
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setMessages([
      {
        id: Date.now(),
        sender: 'assistant',
        text: "Conversation cleared. How can I assist you with your Indian meal planning today?",
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }
    ]);
  };

  // Helper to format response text with safe React formatting (no dangerouslySetInnerHTML)
  const formatText = (text) => {
    if (!text) return null;
    return text.split('\n').map((line, idx) => {
      const parts = line.split(/(\*\*.*?\*\*)/g);
      return (
        <span key={idx} className="block min-h-[1.2em]">
          {parts.map((part, pIdx) => {
            if (part.startsWith('**') && part.endsWith('**') && part.length >= 4) {
              return <strong key={pIdx}>{part.slice(2, -2)}</strong>;
            }
            return part;
          })}
        </span>
      );
    });
  };

  return (
    <div className="flex flex-col h-[calc(100vh-8rem)] max-w-5xl mx-auto space-y-4">
      {/* Top Header Card */}
      <div className="bg-white border rounded-2xl p-4 sm:p-5 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-500 flex items-center justify-center text-white shadow-md shadow-emerald-500/20">
            <Bot className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-lg sm:text-xl font-bold text-slate-900 flex items-center gap-2">
              NutriGuard AI Assistant
              <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 bg-emerald-100 text-emerald-800 rounded-full">
                ICMR Verified
              </span>
            </h1>
            <p className="text-xs text-slate-500">
              Deterministic clinical safety + generative Indian culinary intelligence
            </p>
          </div>
        </div>

        {/* User Context Badges */}
        <div className="flex items-center gap-2 flex-wrap">
          {userProfile?.diet_type && (
            <span className="text-xs bg-slate-100 text-slate-700 px-2.5 py-1 rounded-lg border font-medium">
              Diet: {userProfile.diet_type}
            </span>
          )}
          {userProfile?.conditions?.length > 0 && (
            <span className="text-xs bg-amber-50 text-amber-800 border border-amber-200 px-2.5 py-1 rounded-lg font-medium flex items-center gap-1">
              <AlertTriangle className="w-3 h-3 text-amber-600" />
              {userProfile.conditions.length} Condition(s) Monitored
            </span>
          )}
          <button
            onClick={handleClear}
            className="p-1.5 text-slate-400 hover:text-slate-600 rounded-lg hover:bg-slate-100 transition"
            title="Clear Chat"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Chat Messages Container */}
      <div className="flex-1 bg-white border rounded-2xl p-4 sm:p-6 overflow-y-auto space-y-4 shadow-sm">
        {messages.map((m) => (
          <div
            key={m.id}
            className={`flex items-start gap-3 ${m.sender === 'user' ? 'flex-row-reverse' : 'flex-row'}`}
          >
            {/* Avatar */}
            <div
              className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 text-xs font-bold ${
                m.sender === 'user'
                  ? 'bg-emerald-600 text-white shadow-sm'
                  : 'bg-teal-100 text-teal-800 border border-teal-200'
              }`}
            >
              {m.sender === 'user' ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
            </div>

            {/* Bubble Content */}
            <div
              className={`max-w-[82%] sm:max-w-[75%] rounded-2xl px-4 py-3 text-sm leading-relaxed ${
                m.sender === 'user'
                  ? 'bg-emerald-600 text-white rounded-tr-none shadow-sm'
                  : m.isError
                  ? 'bg-rose-50 border border-rose-200 text-rose-800 rounded-tl-none'
                  : 'bg-slate-50 border border-slate-200 text-slate-800 rounded-tl-none shadow-sm'
              }`}
            >
              {/* Safety Badge if flagged */}
              {m.safety?.status === 'WARNING' && (
                <div className="mb-2 p-2 bg-amber-100 border border-amber-300 rounded-lg text-amber-900 text-xs flex items-start gap-2">
                  <AlertTriangle className="w-4 h-4 text-amber-700 flex-shrink-0 mt-0.5" />
                  <div>
                    <span className="font-bold">Clinical Caution: </span>
                    {m.safety.reason || "Potential medication or health condition interaction detected."}
                  </div>
                </div>
              )}

              {/* Message Body */}
              <div className="space-y-1">
                {formatText(m.text)}
              </div>

              {/* Citations Footer */}
              {m.citations && (
                <div className="mt-3 pt-2 border-t border-slate-200/70 flex items-center gap-1.5 text-[11px] text-slate-500 font-medium">
                  <BookOpen className="w-3 h-3 text-emerald-600" />
                  <span>References: {m.citations.join(" • ")}</span>
                </div>
              )}

              <div
                className={`text-[10px] mt-1.5 text-right ${
                  m.sender === 'user' ? 'text-emerald-100' : 'text-slate-400'
                }`}
              >
                {m.timestamp}
              </div>
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 rounded-full bg-teal-100 text-teal-800 border border-teal-200 flex items-center justify-center">
              <Bot className="w-4 h-4" />
            </div>
            <div className="bg-slate-50 border border-slate-200 rounded-2xl rounded-tl-none px-4 py-3 text-sm text-slate-500 flex items-center space-x-2">
              <div className="w-2 h-2 rounded-full bg-emerald-500 animate-bounce" />
              <div className="w-2 h-2 rounded-full bg-emerald-500 animate-bounce [animation-delay:0.2s]" />
              <div className="w-2 h-2 rounded-full bg-emerald-500 animate-bounce [animation-delay:0.4s]" />
              <span className="text-xs text-slate-400 ml-1">Analyzing nutritional chemistry...</span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Suggested Prompt Chips */}
      <div className="flex items-center gap-2 overflow-x-auto pb-1 text-xs">
        <span className="text-slate-400 flex items-center gap-1 font-medium whitespace-nowrap pl-1">
          <Sparkles className="w-3.5 h-3.5 text-emerald-600" /> Suggestions:
        </span>
        {SUGGESTIONS.map((s, idx) => (
          <button
            key={idx}
            onClick={() => handleSend(s)}
            disabled={loading}
            className="whitespace-nowrap px-3 py-1.5 rounded-full bg-white hover:bg-emerald-50 text-slate-700 hover:text-emerald-700 border border-slate-200 hover:border-emerald-300 transition text-xs shadow-xs"
          >
            {s}
          </button>
        ))}
      </div>

      {/* Message Input Box */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleSend();
        }}
        className="bg-white border rounded-2xl p-2 sm:p-2.5 shadow-sm flex items-center gap-2"
      >
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a question about Indian recipes, macros, or drug interactions..."
          disabled={loading}
          className="flex-1 px-3 py-2 text-sm text-slate-800 placeholder-slate-400 focus:outline-none"
        />
        <button
          type="submit"
          disabled={!input.trim() || loading}
          className="p-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white disabled:opacity-40 transition shadow-sm"
        >
          <Send className="w-4 h-4" />
        </button>
      </form>
    </div>
  );
}
