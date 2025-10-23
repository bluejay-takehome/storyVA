/**
 * StoryVA Main Page
 *
 * Single-view interface for voice direction.
 * Story editor is always visible, transcript appears during session.
 */

'use client';

import { RoomAudioRenderer, StartAudio } from '@livekit/components-react';
import { SessionProvider, useSession } from '@/components/SessionProvider';
import { StoryEditor } from '@/components/StoryEditor';
import { LiveTranscript } from '@/components/LiveTranscript';
import { APP_CONFIG } from '@/app-config';

function MainView() {
  const { isSessionActive, startSession, endSession, error } = useSession();

  return (
    <div className="flex min-h-screen bg-zinc-50 dark:bg-zinc-900">
      {/* Left panel - Story Editor (always visible) */}
      <div className="flex-1 p-6">
        <div className="max-w-4xl mx-auto h-full flex flex-col">
          {/* Header */}
          <div className="mb-6">
            <h1 className="text-3xl font-bold text-zinc-900 dark:text-zinc-50 mb-2">
              StoryVA - Voice Director
            </h1>
            <p className="text-zinc-600 dark:text-zinc-400">
              Work with Lelouch to add Fish Audio emotion markup to your story
            </p>
          </div>

          {/* Error display */}
          {error && (
            <div className="mb-4 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
              <p className="text-red-800 dark:text-red-200 text-sm">
                <strong>Error:</strong> {error}
              </p>
            </div>
          )}

          {/* Story Editor */}
          <div className="flex-1 mb-6">
            <StoryEditor />
          </div>

          {/* Session Controls */}
          <div className="flex items-center gap-4">
            {!isSessionActive ? (
              <button
                onClick={startSession}
                className="px-6 py-3 bg-zinc-900 dark:bg-zinc-50 text-white dark:text-zinc-900 rounded-lg font-semibold hover:bg-zinc-700 dark:hover:bg-zinc-200 transition-colors focus:outline-none focus:ring-2 focus:ring-zinc-500 dark:focus:ring-zinc-400"
              >
                Start Direction Session
              </button>
            ) : (
              <button
                onClick={endSession}
                className="px-6 py-3 bg-red-600 dark:bg-red-500 text-white rounded-lg font-semibold hover:bg-red-700 dark:hover:bg-red-600 transition-colors focus:outline-none focus:ring-2 focus:ring-red-500"
              >
                End Session
              </button>
            )}
            {isSessionActive && (
              <span className="text-sm text-zinc-600 dark:text-zinc-400">
                Session active - Lelouch is listening
              </span>
            )}
          </div>
        </div>
      </div>

      {/* Right panel - Transcript (appears during session) */}
      {isSessionActive && (
        <div className="w-96 h-screen border-l border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-950 p-6 flex flex-col">
          <LiveTranscript className="flex-1" />
        </div>
      )}
    </div>
  );
}

export default function Home() {
  return (
    <SessionProvider appConfig={APP_CONFIG}>
      <main>
        <MainView />
      </main>

      {/* Critical audio components */}
      <StartAudio label="Click to enable audio" />
      <RoomAudioRenderer />
    </SessionProvider>
  );
}
