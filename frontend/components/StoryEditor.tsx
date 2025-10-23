/**
 * StoryEditor Component
 *
 * Editable textarea for story content with localStorage persistence.
 * Allows writers to paste and edit their stories.
 */

'use client';

import { useEffect, useState } from 'react';

const STORAGE_KEY = 'storyva-story-content';

interface StoryEditorProps {
  className?: string;
}

/**
 * StoryEditor - textarea with automatic localStorage persistence.
 *
 * Features:
 * - Auto-saves to localStorage on every change
 * - Restores content on mount
 * - Placeholder text guides users
 */
export function StoryEditor({ className = '' }: StoryEditorProps) {
  const [content, setContent] = useState('');

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
        </span>
      </div>
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
