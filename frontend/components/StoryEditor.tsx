/**
 * StoryEditor Component
 *
 * Editable textarea for story content with localStorage persistence.
 * Displays inline diffs when agent suggests emotion markup changes.
 */

'use client';

import { useEffect, useState } from 'react';
import { useRoomContext } from '@livekit/components-react';
import { InlineDiff } from './InlineDiff';

const STORAGE_KEY = 'storyva-story-content';

interface StoryEditorProps {
  className?: string;
}

interface PendingDiff {
  id: string;
  original: string;
  proposed: string;
  explanation?: string;
  lineNumber?: number;
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

  // Save to localStorage on every change
  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const newContent = e.target.value;
    setContent(newContent);
    localStorage.setItem(STORAGE_KEY, newContent);

    // Send story update to agent via data channel (if connected)
    if (room && room.localParticipant) {
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

    // Remove the diff from pending list
    setPendingDiffs(prev => prev.filter(d => d.id !== diffId));
  };

  // Reject a diff - just remove it from pending list
  const handleRejectDiff = (diffId: string) => {
    setPendingDiffs(prev => prev.filter(d => d.id !== diffId));
  };

  // TODO: This will be populated by agent suggestions in Phase 6
  // For now, exposed for future integration
  const addPendingDiff = (diff: PendingDiff) => {
    setPendingDiffs(prev => [...prev, diff]);
  };

  return (
    <div className={`flex flex-col h-full ${className}`}>
      <div className="mb-2 flex items-center justify-between">
        <label
          htmlFor="story-editor"
          className="text-sm font-medium text-zinc-700 dark:text-zinc-300"
        >
          Your Story
        </label>
        <span className="text-xs text-zinc-500 dark:text-zinc-400">
          {content.length} characters
          {pendingDiffs.length > 0 && ` · ${pendingDiffs.length} suggestion${pendingDiffs.length > 1 ? 's' : ''}`}
        </span>
      </div>

      {/* Pending diffs displayed above editor */}
      {pendingDiffs.length > 0 && (
        <div className="mb-4 space-y-3 max-h-64 overflow-y-auto">
          {pendingDiffs.map(diff => (
            <InlineDiff
              key={diff.id}
              original={diff.original}
              proposed={diff.proposed}
              explanation={diff.explanation}
              onAccept={() => handleAcceptDiff(diff.id)}
              onReject={() => handleRejectDiff(diff.id)}
            />
          ))}
        </div>
      )}

      <textarea
        id="story-editor"
        value={content}
        onChange={handleChange}
        placeholder="Paste your story here... Example:

&quot;I can't believe you did this,&quot; she said quietly.

He looked away, guilt washing over him. &quot;I had no choice.&quot;

Add emotion markup with Lelouch's help during your session."
        className="flex-1 w-full p-4 border border-zinc-300 dark:border-zinc-700 rounded-lg bg-white dark:bg-zinc-900 text-zinc-900 dark:text-zinc-100 placeholder-zinc-400 dark:placeholder-zinc-500 focus:outline-none focus:ring-2 focus:ring-zinc-500 dark:focus:ring-zinc-400 resize-none font-mono text-sm"
      />
    </div>
  );
}
