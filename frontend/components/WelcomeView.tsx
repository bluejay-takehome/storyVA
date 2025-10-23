/**
 * WelcomeView Component
 *
 * Pre-call view shown before starting a voice direction session.
 * Displays intro message and start button.
 *
 * Will be enhanced in Phase 5B with StoryEditor.
 */

'use client';

import { useSession } from './SessionProvider';

interface WelcomeViewProps {
  onStartCall: () => void;
}

/**
 * WelcomeView displays the pre-session UI.
 *
 * Shows:
 * - Welcome message
 * - Agent description (Lelouch personality)
 * - Start button
 * - Error messages if any
 *
 * In Phase 5B, we'll add StoryEditor here.
 */
export function WelcomeView({ onStartCall }: WelcomeViewProps) {
  const { appConfig, error } = useSession();

  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 dark:bg-black p-8">
      <div className="w-full max-w-2xl">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold mb-4 text-zinc-900 dark:text-zinc-50">
            {appConfig.welcomeMessage}
          </h1>
          <p className="text-lg text-zinc-600 dark:text-zinc-400 leading-relaxed">
            {appConfig.agentDescription}
          </p>
        </div>

        {/* Error display */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
            <p className="text-red-800 dark:text-red-200 text-sm">
              <strong>Error:</strong> {error}
            </p>
          </div>
        )}

        {/* Placeholder for StoryEditor (Phase 5B) */}
        <div className="mb-8 p-6 bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-lg">
          <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-2">
            Story Editor (Coming in Phase 5B)
          </p>
          <p className="text-xs text-zinc-400 dark:text-zinc-500">
            You'll be able to paste your story text here
          </p>
        </div>

        {/* Start button */}
        <div className="flex justify-center">
          <button
            onClick={onStartCall}
            className="px-8 py-4 bg-zinc-900 dark:bg-zinc-50 text-white dark:text-zinc-900 rounded-full font-semibold text-lg hover:bg-zinc-700 dark:hover:bg-zinc-200 transition-colors focus:outline-none focus:ring-2 focus:ring-zinc-500 dark:focus:ring-zinc-400"
          >
            {appConfig.startButtonText}
          </button>
        </div>

        {/* Instructions */}
        <div className="mt-8 text-center">
          <p className="text-sm text-zinc-500 dark:text-zinc-400">
            Click the button above to start a voice session with Lelouch.
            <br />
            Make sure your microphone is enabled.
          </p>
        </div>
      </div>
    </div>
  );
}
