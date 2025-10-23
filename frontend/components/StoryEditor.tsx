/**
 * StoryEditor Component
 *
 * Editable textarea for story content with localStorage persistence.
 * Displays inline diffs when agent suggests emotion markup changes.
 */

'use client';

import { useEffect, useState } from 'react';
import { useRoomContext } from '@livekit/components-react';
import { diffWordsWithSpace, Change } from 'diff';

const STORAGE_KEY = 'storyva-story-content';

interface StoryEditorProps {
  className?: string;
}

interface PendingDiff {
  id: string;
  original: string;
  proposed: string;
  unified_diff: string;  // Git-style unified diff
  summary?: string;
  explanation?: string;
}

/**
 * StoryEditor - textarea with automatic localStorage persistence and inline diff display.
 *
 * Features:
 * - Auto-saves to localStorage on every change
 * - Restores content on mount
 * - Displays inline diffs for agent suggestions
 * - Accept/reject diffs to apply or dismiss changes
 */
export function StoryEditor({ className = '' }: StoryEditorProps) {
  const [content, setContent] = useState('');
  const [pendingDiffs, setPendingDiffs] = useState<PendingDiff[]>([]);
  const room = useRoomContext();

  // Load from localStorage on mount
  useEffect(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      setContent(saved);
    }
  }, []);

  // Listen for diff suggestions from agent via data channel
  useEffect(() => {
    if (!room) return;

    const handleDataReceived = (payload: Uint8Array, participant?: any) => {
      try {
        const decoder = new TextDecoder();
        const message = JSON.parse(decoder.decode(payload));

        if (message.type === 'emotion_diff' && message.diff) {
          console.log('Received diff from agent:', message.diff);
          setPendingDiffs(prev => [...prev, message.diff]);
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

  // Save to localStorage on every change
  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const newContent = e.target.value;
    setContent(newContent);
    localStorage.setItem(STORAGE_KEY, newContent);

    // Send story update to agent via data channel (if connected)
    if (room && room.localParticipant && room.state === 'connected') {
      try {
        const encoder = new TextEncoder();
        const data = encoder.encode(JSON.stringify({
          type: 'story_update',
          text: newContent,
        }));
        room.localParticipant.publishData(data, { reliable: true });
        console.log('Story update sent to agent via data channel');
      } catch (error) {
        console.error('Failed to send story update:', error);
      }
    }
  };

  // Accept a diff - replace original text with proposed text
  const handleAcceptDiff = (diffId: string) => {
    const diff = pendingDiffs.find(d => d.id === diffId);
    if (!diff) return;

    // Replace the original text with proposed text in content
    const newContent = content.replace(diff.original, diff.proposed);
    setContent(newContent);
    localStorage.setItem(STORAGE_KEY, newContent);

    // Send story update to agent
    if (room && room.localParticipant && room.state === 'connected') {
      try {
        const encoder = new TextEncoder();
        const data = encoder.encode(JSON.stringify({
          type: 'story_update',
          text: newContent,
        }));
        room.localParticipant.publishData(data, { reliable: true });
      } catch (error) {
        console.error('Failed to send story update:', error);
      }
    }

    // Remove the diff from pending list
    setPendingDiffs(prev => prev.filter(d => d.id !== diffId));
  };

  // Reject a diff - just remove it from pending list
  const handleRejectDiff = (diffId: string) => {
    setPendingDiffs(prev => prev.filter(d => d.id !== diffId));
  };

  // Render content with inline diff highlighting (character-level)
  const renderContentWithDiff = () => {
    if (pendingDiffs.length === 0) {
      return content;
    }

    // Apply first pending diff inline
    const diff = pendingDiffs[0];
    const originalIndex = content.indexOf(diff.original);

    if (originalIndex === -1) {
      return content;
    }

    const before = content.substring(0, originalIndex);
    const after = content.substring(originalIndex + diff.original.length);

    // Compute word-level diff (respects word boundaries and spaces)
    const changes: Change[] = diffWordsWithSpace(diff.original, diff.proposed);

    return (
      <>
        {before}
        {changes.map((change, index) => {
          if (change.added) {
            // Added text - vibrant green highlight with animation
            return (
              <span
                key={index}
                className="bg-gradient-to-r from-green-200 to-emerald-200 dark:from-green-900/50 dark:to-emerald-900/50 text-green-900 dark:text-green-200 font-semibold px-1 rounded shadow-sm animate-pulse"
                style={{
                  animationDelay: `${index * 0.1}s`,
                  animationIterationCount: '3',
                }}
              >
                {change.value}
              </span>
            );
          } else if (change.removed) {
            // Removed text - red strikethrough with fade
            return (
              <span
                key={index}
                className="bg-gradient-to-r from-red-200 to-rose-200 dark:from-red-900/50 dark:to-rose-900/50 text-red-900 dark:text-red-200 line-through opacity-75 px-1 rounded"
              >
                {change.value}
              </span>
            );
          } else {
            // Unchanged text - normal
            return <span key={index}>{change.value}</span>;
          }
        })}
        {after}
      </>
    );
  };

  return (
    <div className={`flex flex-col h-full ${className}`}>
      <div className="mb-3 flex items-center justify-between">
        <label
          htmlFor="story-editor"
          className="text-base font-bold text-purple-900 dark:text-purple-300 flex items-center gap-2"
        >
          <span className="text-xl">📖</span>
          Your Story
        </label>
        <span className="text-xs font-medium px-3 py-1 rounded-full bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300">
          {content.length} characters
          {pendingDiffs.length > 0 && ` · ${pendingDiffs.length} suggestion${pendingDiffs.length > 1 ? 's' : ''}`}
        </span>
      </div>

      {/* Accept/Reject buttons with smooth collapse */}
      <div
        className="overflow-hidden transition-all duration-300 ease-in-out mb-3"
        style={{
          maxHeight: pendingDiffs.length > 0 ? '200px' : '0px',
          marginBottom: pendingDiffs.length > 0 ? '0.75rem' : '0px'
        }}
      >
        {pendingDiffs.length > 0 && (
          <div className="p-4 glass rounded-xl border-2 border-purple-500/30">
            <div className="flex items-center gap-2">
              <button
                onClick={() => handleAcceptDiff(pendingDiffs[0].id)}
                className="px-3 py-1 text-sm font-medium text-white bg-green-600 hover:bg-green-700 rounded-md transition-colors"
              >
                ✓ Accept
              </button>
              <button
                onClick={() => handleRejectDiff(pendingDiffs[0].id)}
                className="px-3 py-1 text-sm font-medium text-white bg-red-600 hover:bg-red-700 rounded-md transition-colors"
              >
                ✗ Reject
              </button>
              {pendingDiffs[0].summary && (
                <span className="text-xs text-zinc-500 dark:text-zinc-400">
                  {pendingDiffs[0].summary}
                </span>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Editor with inline diff highlighting */}
      {pendingDiffs.length > 0 ? (
        <div
          className="flex-1 w-full p-5 border-2 border-purple-500/30 rounded-xl glass text-zinc-900 dark:text-zinc-100 font-mono text-sm leading-relaxed whitespace-pre-wrap overflow-auto shadow-xl"
        >
          {renderContentWithDiff()}
        </div>
      ) : (
        <textarea
          id="story-editor"
          value={content}
          onChange={handleChange}
          placeholder="Paste your story here... Example:

&quot;I can't believe you did this,&quot; she said quietly.

He looked away, guilt washing over him. &quot;I had no choice.&quot;

Add emotion markup with Lelouch's help during your session."
          className="flex-1 w-full p-5 border-2 border-purple-500/20 hover:border-purple-500/40 rounded-xl glass text-zinc-900 dark:text-zinc-100 placeholder-purple-400/60 dark:placeholder-purple-400/40 focus:outline-none focus:border-purple-500 focus:ring-4 focus:ring-purple-500/20 resize-none font-mono text-sm leading-relaxed transition-all duration-300 shadow-lg"
        />
      )}
    </div>
  );
}
