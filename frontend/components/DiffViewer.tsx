/**
 * DiffViewer Component
 *
 * Displays emotion markup suggestions in a visual diff format.
 * Shows original text vs. proposed text with Fish Audio tags.
 */

'use client';

interface DiffViewerProps {
  original: string;
  proposed: string;
  explanation?: string;
  className?: string;
}

/**
 * DiffViewer shows before/after emotion markup changes.
 *
 * Features:
 * - Original text (gray/faded)
 * - Proposed text with emotion tags highlighted
 * - Optional explanation from agent
 * - Accept/Reject actions (future phase)
 */
export function DiffViewer({ original, proposed, explanation, className = '' }: DiffViewerProps) {
  return (
    <div className={`border border-zinc-300 dark:border-zinc-700 rounded-lg p-4 bg-white dark:bg-zinc-900 ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-semibold text-zinc-900 dark:text-zinc-50">
          Emotion Markup Suggestion
        </h3>
        <span className="text-xs text-zinc-500 dark:text-zinc-400">
          Fish Audio Tags
        </span>
      </div>

      {/* Explanation */}
      {explanation && (
        <div className="mb-3 p-2 bg-zinc-50 dark:bg-zinc-800 rounded text-sm text-zinc-700 dark:text-zinc-300">
          <span className="font-medium">Lelouch: </span>
          {explanation}
        </div>
      )}

      {/* Original text */}
      <div className="mb-3">
        <div className="text-xs font-medium text-zinc-500 dark:text-zinc-400 mb-1">
          Original:
        </div>
        <div className="p-3 bg-zinc-50 dark:bg-zinc-800 rounded text-sm font-mono text-zinc-600 dark:text-zinc-400 line-through">
          {original}
        </div>
      </div>

      {/* Proposed text with emotion tags */}
      <div>
        <div className="text-xs font-medium text-zinc-500 dark:text-zinc-400 mb-1">
          Proposed:
        </div>
        <div className="p-3 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded">
          <pre className="text-sm font-mono text-zinc-900 dark:text-zinc-100 whitespace-pre-wrap">
            {highlightEmotionTags(proposed)}
          </pre>
        </div>
      </div>

      {/* Action buttons (future phase) */}
      <div className="mt-4 flex gap-2">
        <button
          disabled
          className="px-4 py-2 bg-zinc-200 dark:bg-zinc-700 text-zinc-400 dark:text-zinc-500 rounded text-sm font-medium cursor-not-allowed"
        >
          Accept (Phase 6)
        </button>
        <button
          disabled
          className="px-4 py-2 bg-zinc-200 dark:bg-zinc-700 text-zinc-400 dark:text-zinc-500 rounded text-sm font-medium cursor-not-allowed"
        >
          Reject (Phase 6)
        </button>
      </div>
    </div>
  );
}

/**
 * Highlight emotion tags in the proposed text.
 * Returns React nodes with styled emotion tags.
 */
function highlightEmotionTags(text: string) {
  // Regex to match emotion tags: (emotion) or (tone marker) or (audio effect)
  const tagRegex = /\([a-zA-Z\s]+\)/g;

  const parts = [];
  let lastIndex = 0;
  let match;

  while ((match = tagRegex.exec(text)) !== null) {
    // Add text before tag
    if (match.index > lastIndex) {
      parts.push(
        <span key={`text-${lastIndex}`}>
          {text.slice(lastIndex, match.index)}
        </span>
      );
    }

    // Add highlighted tag
    parts.push(
      <span
        key={`tag-${match.index}`}
        className="bg-yellow-200 dark:bg-yellow-700 text-yellow-900 dark:text-yellow-100 px-1 rounded font-semibold"
      >
        {match[0]}
      </span>
    );

    lastIndex = match.index + match[0].length;
  }

  // Add remaining text
  if (lastIndex < text.length) {
    parts.push(
      <span key={`text-${lastIndex}`}>
        {text.slice(lastIndex)}
      </span>
    );
  }

  return parts.length > 0 ? parts : text;
}
