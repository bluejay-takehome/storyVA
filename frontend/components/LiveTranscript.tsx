/**
 * LiveTranscript Component
 *
 * Displays the conversation between user and agent (Lelouch).
 * Shows transcribed user speech and agent text responses.
 */

'use client';

import { useEffect, useRef, useState } from 'react';
import { useVoiceAssistant } from '@livekit/components-react';

export interface TranscriptMessage {
  id: string;
  role: 'user' | 'agent';
  content: string;
  timestamp: Date;
}

interface LiveTranscriptProps {
  className?: string;
}

/**
 * LiveTranscript displays conversation messages.
 *
 * Features:
 * - Shows user speech (transcribed)
 * - Shows agent text responses
 * - Auto-scrolls to latest message
 * - Different styling for user vs agent
 */
export function LiveTranscript({ className = '' }: LiveTranscriptProps) {
  const [messages, setMessages] = useState<TranscriptMessage[]>([]);
  const scrollRef = useRef<HTMLDivElement>(null);

  // Use LiveKit's useVoiceAssistant hook to get agent state
  const { state, agentTranscriptions } = useVoiceAssistant();

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  // Listen for new transcriptions
  useEffect(() => {
    if (agentTranscriptions && agentTranscriptions.length > 0) {
      // Get the latest transcription
      const latest = agentTranscriptions[agentTranscriptions.length - 1];

      // Add to messages if it's a final transcription and not already added
      if (latest.isFinal) {
        const messageId = `agent-${latest.timestamp || Date.now()}`;

        // Check if message already exists
        setMessages((prev) => {
          const exists = prev.some(m => m.id === messageId);
          if (exists) return prev;

          return [
            ...prev,
            {
              id: messageId,
              role: 'agent',
              content: latest.text,
              timestamp: new Date(),
            },
          ];
        });
      }
    }
  }, [agentTranscriptions]);

  // TODO: Listen for user transcriptions (when microphone is enabled)
  // This will require listening to room track events

  return (
    <div className={`flex flex-col h-full ${className}`}>
      {/* Header */}
      <div className="mb-4">
        <h2 className="text-xl font-semibold text-zinc-900 dark:text-zinc-50">
          Conversation
        </h2>
        <p className="text-sm text-zinc-500 dark:text-zinc-400 mt-1">
          {state === 'listening' && 'Lelouch is listening...'}
          {state === 'thinking' && 'Lelouch is thinking...'}
          {state === 'speaking' && 'Lelouch is speaking...'}
          {!state && 'Waiting for connection...'}
        </p>
      </div>

      {/* Messages */}
      <div
        ref={scrollRef}
        className="flex-1 overflow-y-auto space-y-4 pr-2"
      >
        {messages.length === 0 ? (
          <div className="text-center text-zinc-500 dark:text-zinc-400 text-sm mt-8">
            <p className="mb-2">No messages yet</p>
            <p className="text-xs">
              Start speaking to begin the conversation
            </p>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${
                message.role === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              <div
                className={`max-w-[80%] rounded-lg px-4 py-2 ${
                  message.role === 'user'
                    ? 'bg-zinc-200 dark:bg-zinc-700 text-zinc-900 dark:text-zinc-100'
                    : 'bg-zinc-900 dark:bg-zinc-100 text-white dark:text-zinc-900'
                }`}
              >
                <div className="flex items-baseline gap-2 mb-1">
                  <span className="text-xs font-semibold opacity-75">
                    {message.role === 'user' ? 'You' : 'Lelouch'}
                  </span>
                  <span className="text-xs opacity-50">
                    {message.timestamp.toLocaleTimeString([], {
                      hour: '2-digit',
                      minute: '2-digit',
                    })}
                  </span>
                </div>
                <p className="text-sm leading-relaxed whitespace-pre-wrap">
                  {message.content}
                </p>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
