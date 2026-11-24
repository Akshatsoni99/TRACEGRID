'use client';

import React, { useState, useRef, useEffect } from 'react';
import {
  Send,
  Bot,
  User,
  Sparkles,
  ShieldAlert,
  FileCheck2,
  HelpCircle,
  RefreshCw,
  Copy,
  ExternalLink
} from 'lucide-react';
import { AIChatMessage, Investigation } from '@/lib/types';
import { askAIAssistant } from '@/lib/api';

interface AIAssistantViewProps {
  activeCase?: Investigation;
}

export default function AIAssistantView({ activeCase }: AIAssistantViewProps) {
  const [messages, setMessages] = useState<AIChatMessage[]>([
    {
      sender: 'assistant',
      text: `### TRACEGRID AI Forensic Assistant Initialized\n\nI am connected to the active evidence repository for Case **${
        activeCase?.case_number || 'RJ-EOW-2026-0042'
      }** (${activeCase?.title || 'Active Investigation'}).\n\nI analyze transaction ledgers, mule flow ratios, circular routing hops, and corroborated digital infrastructure without speculating on unverified facts.\n\n*Select a prompt below or ask a specific question.*`,
      suggested_actions: [
        'Explore Money-Trail Graph for structural visualization',
        'Review Flagged Transactions under Transaction Analysis module'
      ],
      confidence_level: 'HIGH (EVIDENCE GROUNDED)',
      limitations_disclaimer:
        'All AI outputs are investigative leads requiring sworn officer verification under CrPC guidelines.'
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const sampleQuestions = [
    'Summarise this investigation.',
    'Which transactions were flagged and why?',
    'Show the accounts with the most connections.',
    'Explain the suspicious transaction pattern.',
    'What evidence is missing to complete the charge sheet?'
  ];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSendMessage = async (textToSend?: string) => {
    const q = textToSend || input;
    if (!q.trim() || !activeCase) return;

    const userMsg: AIChatMessage = { sender: 'user', text: q };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const resp = await askAIAssistant(activeCase.id, q);
      const assistantMsg: AIChatMessage = {
        sender: 'assistant',
        text: resp.reply,
        references: resp.evidence_references,
        suggested_actions: resp.suggested_actions,
        confidence_level: resp.confidence_level,
        limitations_disclaimer: resp.limitations_disclaimer
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        {
          sender: 'assistant',
          text: `Error connecting to Assistant: ${err.message}`,
          confidence_level: 'LOW'
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex-1 flex flex-col h-full max-w-4xl mx-auto p-4 space-y-3">
      {/* Statutory Guidance Banner */}
      <div className="bg-slate-50 border border-slate-200 rounded px-4 py-2.5 flex items-start space-x-2.5 text-xs text-slate-700">
        <ShieldAlert className="w-4 h-4 text-tg-primary flex-shrink-0 mt-0.5" />
        <div className="flex-1">
          <strong className="text-tg-primary">ASSISTANT COGNITIVE BOUNDARY: </strong>
          TRACEGRID AI operates strictly on factual case holdings. It never autonomously declares guilt, 
          fabricates counterparty identities, or hallucinates external evidence.
        </div>
      </div>

      {/* Chat Messages Scroll Window */}
      <div className="flex-1 bg-white border border-tg-border rounded-lg p-5 overflow-y-auto space-y-5 shadow-inner">
        {messages.map((m, idx) => {
          const isUser = m.sender === 'user';

          return (
            <div
              key={idx}
              className={`flex items-start space-x-3 ${isUser ? 'flex-row-reverse space-x-reverse' : ''}`}
            >
              {/* Avatar */}
              <div
                className={`w-7 h-7 rounded-full flex items-center justify-center flex-shrink-0 text-xs font-bold ${
                  isUser
                    ? 'bg-tg-primary text-white'
                    : 'bg-tg-sidebar text-sky-400 border border-sky-800'
                }`}
              >
                {isUser ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
              </div>

              {/* Message Bubble */}
              <div
                className={`max-w-[85%] rounded-lg p-4 text-xs space-y-2.5 leading-relaxed shadow-sm ${
                  isUser
                    ? 'bg-tg-primary text-white font-medium'
                    : 'bg-slate-50 text-slate-800 border border-slate-200'
                }`}
              >
                {/* Text Content */}
                <div className="prose prose-xs max-w-none text-xs whitespace-pre-line font-sans">
                  {m.text}
                </div>

                {/* Evidence References Pill Box */}
                {m.references && m.references.length > 0 && (
                  <div className="pt-2 border-t border-slate-200/70 text-[11px] font-mono">
                    <span className="text-slate-500 font-semibold block mb-1">
                      Evidentiary Cross-References:
                    </span>
                    <div className="flex flex-wrap gap-1">
                      {m.references.map((ref, rIdx) => (
                        <span
                          key={rIdx}
                          className="bg-white border border-slate-300 text-slate-700 px-1.5 py-0.5 rounded font-bold"
                        >
                          {ref}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {/* Suggested Procedural Actions */}
                {m.suggested_actions && m.suggested_actions.length > 0 && (
                  <div className="pt-2 border-t border-slate-200/70 text-[11px] text-slate-700">
                    <span className="font-semibold text-tg-primary block mb-1">
                      Recommended Procedural Steps:
                    </span>
                    <ul className="list-disc list-inside space-y-0.5 pl-1">
                      {m.suggested_actions.map((act, aIdx) => (
                        <li key={aIdx}>{act}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Confidence & Limitations Disclaimer */}
                {m.confidence_level && (
                  <div className="pt-2 border-t border-slate-200/60 flex flex-col space-y-0.5 text-[10px] text-slate-400 font-mono">
                    <div className="flex justify-between">
                      <span>Reasoning Confidence:</span>
                      <span className="text-slate-600 font-bold">{m.confidence_level}</span>
                    </div>
                    {m.limitations_disclaimer && (
                      <p className="text-[9px] text-slate-400 italic pt-0.5">
                        {m.limitations_disclaimer}
                      </p>
                    )}
                  </div>
                )}
              </div>
            </div>
          );
        })}

        {loading && (
          <div className="flex items-center space-x-2 text-slate-500 text-xs pl-10">
            <RefreshCw className="w-3.5 h-3.5 animate-spin text-tg-primary" />
            <span>Analyzing case repository & correlating evidentiary graphs...</span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Suggested Quick Prompts */}
      <div className="flex flex-wrap gap-1.5 pt-1">
        {sampleQuestions.map((q, idx) => (
          <button
            key={idx}
            onClick={() => handleSendMessage(q)}
            disabled={loading}
            className="text-[11px] bg-white hover:bg-slate-50 text-slate-700 px-2.5 py-1 rounded border border-slate-200 transition-colors font-medium shadow-2xs"
          >
            {q}
          </button>
        ))}
      </div>

      {/* Input Bar */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleSendMessage();
        }}
        className="flex items-center space-x-2"
      >
        <input
          type="text"
          placeholder="Ask about flagged transactions, high-centrality accounts, circular routing..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={loading}
          className="flex-1 bg-white border border-slate-300 rounded px-4 py-2.5 text-xs focus:outline-none focus:border-tg-primary shadow-sm"
        />
        <button
          type="submit"
          disabled={loading || !input.trim()}
          className="bg-tg-primary text-white hover:bg-tg-primaryHover px-4 py-2.5 rounded text-xs font-semibold flex items-center space-x-1.5 shadow-sm disabled:bg-slate-300"
        >
          <span>Send Query</span>
          <Send className="w-3.5 h-3.5" />
        </button>
      </form>
    </div>
  );
}

