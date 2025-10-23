/**
 * InlineDiff Component
 *
 * Displays emotion markup suggestions inline with the story editor.
 * Shows original text vs. proposed text with highlighted emotion tags.
 */

'use client';

interface InlineDiffProps {
  original: string;
  proposed: string;
  explanation?: string;
  onAccept?: () => void;
  onReject?: () => void;
  className?: string;
}

/**
 * InlineDiff shows before/after emotion markup changes.
 *
 * Features:
 * - Original text (strikethrough/faded)
 * - Proposed text with emotion tags highlighted
 * - Optional explanation from agent
 * - Accept/Reject actions
 */
export function InlineDiff({
  original,
  proposed,
  explanation,
  onAccept,
  onReject,
  className = ''
}: InlineDiffProps) {
  return (
    <div className={`border-l-4 border-yellow-400 dark:border-yellow-600 bg-yellow-50 dark:bg-yellow-900/10 rounded-r-lg p-4 mb-4 ${className}`}>
      {/* Explanation */}
      {explanation && (
        <div className="mb-3 text-sm text-zinc-700 dark:text-zinc-300">
          <span className="font-semibold text-yellow-800 dark:text-yellow-200">Lelouch suggests: </span>
          {explanation}
        </div>
      )}

      {/* Original text - strikethrough */}
      <div className="mb-2">
        <div className="text-xs font-medium text-zinc-500 dark:text-zinc-400 mb-1">
          Original:
        </div>
        <div className="p-2 bg-white dark:bg-zinc-900 rounded text-sm text-zinc-500 dark:text-zinc-400 line-through">
          {original}
        </div>
      </div>

      {/* Proposed text with emotion tags highlighted */}
      <div className="mb-3">
        <div className="text-xs font-medium text-zinc-500 dark:text-zinc-400 mb-1">
          Proposed:
        </div>
        <div className="p-2 bg-white dark:bg-zinc-900 rounded">
          <div className="text-sm text-zinc-900 dark:text-zinc-100 whitespace-pre-wrap">
            {highlightEmotionTags(proposed)}
          </div>
        </div>
      </div>

      {/* Action buttons */}
      <div className="flex gap-2">
        {onAccept && (
          <button
            onClick={onAccept}
            className="px-4 py-2 bg-green-600 dark:bg-green-500 text-white rounded text-sm font-medium hover:bg-green-700 dark:hover:bg-green-600 transition-colors focus:outline-none focus:ring-2 focus:ring-green-500"
          >
            Accept
          </button>
        )}
        {onReject && (
          <button
            onClick={onReject}
            className="px-4 py-2 bg-zinc-200 dark:bg-zinc-700 text-zinc-900 dark:text-zinc-100 rounded text-sm font-medium hover:bg-zinc-300 dark:hover:bg-zinc-600 transition-colors focus:outline-none focus:ring-2 focus:ring-zinc-500"
          >
            Reject
          </button>
        )}
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
