/**
 * LiveTranscript Component
 *
 * Displays the conversation between user and agent (Lelouch).
 * Shows transcribed user speech and agent text responses.
 */

'use client';

import { useEffect, useRef, useState } from 'react';
import { useVoiceAssistant, useLocalParticipant, useRoomContext } from '@livekit/components-react';
import { Track } from 'livekit-client';

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

  // Get local participant to listen for user transcriptions
  const { localParticipant } = useLocalParticipant();

  // Get room for data channel access
  const room = useRoomContext();

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  // Listen for agent responses via data channel (immediate text, not waiting for TTS)
  useEffect(() => {
    if (!room) return;

    const handleDataReceived = (payload: Uint8Array, participant?: any) => {
      try {
        const decoder = new TextDecoder();
        const message = JSON.parse(decoder.decode(payload));

        // Handle agent text responses sent immediately (before TTS completes)
        if (message.type === 'agent_response' && message.text) {
          const messageId = message.timestamp || `agent-${Date.now()}`;

          setMessages((prev) => {
            // Check if message already exists
            const exists = prev.some(m => m.id === messageId);
            if (exists) return prev;

            console.log('Adding agent message (immediate):', message.text);
            return [
              ...prev,
              {
                id: messageId,
                role: 'agent',
                content: message.text,
                timestamp: new Date(),
              },
            ];
          });
        }
      } catch (error) {
        console.error('Failed to parse data channel message:', error);
      }
    };

    room.on('dataReceived', handleDataReceived);

    return () => {
      room.off('dataReceived', handleDataReceived);
    };
  }, [room]);

  // NOTE: Agent transcriptions now come via data channel (from TTS callback)
  // This provides immediate text display before audio completes
  // The agentTranscriptions from useVoiceAssistant are no longer used

  // Listen for user transcriptions from the local participant's microphone
  useEffect(() => {
    if (!localParticipant) return;

    const handleTranscription = (transcription: any) => {
      console.log('Transcription received:', transcription);
      
      // Handle different transcription data structures
      let finalText = '';
      let isFinal = false;
      
      if (typeof transcription === 'string') {
        finalText = transcription.trim();
        isFinal = true;
      } else if (transcription.text) {
        finalText = transcription.text.trim();
        isFinal = transcription.isFinal || transcription.final || true;
      } else if (Array.isArray(transcription)) {
        // Handle array of segments
        finalText = transcription
          .filter((s) => s.final || s.isFinal)
          .map((s) => s.text)
          .join(' ')
          .trim();
        isFinal = true;
      }
      
      if (finalText && isFinal) {
        const messageId = `user-${Date.now()}`;

        setMessages((prev) => {
          // Avoid duplicate messages
          const exists = prev.some(
            (m) => m.role === 'user' && m.content === finalText
          );
          if (exists) return prev;

          console.log('Adding user message:', finalText);
          return [
            ...prev,
            {
              id: messageId,
              role: 'user',
              content: finalText,
              timestamp: new Date(),
            },
          ];
        });
      }
    };

    // Subscribe to transcription events - try multiple event names
    localParticipant.on('transcriptionReceived', handleTranscription);
    localParticipant.on('trackTranscriptionReceived', handleTranscription);
    
    // Also listen on the room for transcription events
    const room = localParticipant.room;
    if (room) {
      room.on('transcriptionReceived', handleTranscription);
    }

    // Cleanup
    return () => {
      localParticipant.off('transcriptionReceived', handleTranscription);
      localParticipant.off('trackTranscriptionReceived', handleTranscription);
      if (room) {
        room.off('transcriptionReceived', handleTranscription);
      }
    };
  }, [localParticipant]);

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
        className="flex-1 min-h-0 overflow-y-auto space-y-4 pr-2"
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
