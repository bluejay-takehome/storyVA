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
import { useEffect, useState } from 'react';

// Floating particles component
function Particles() {
  const [particles, setParticles] = useState<Array<{ id: number; left: string; delay: number; duration: number }>>([]);

  useEffect(() => {
    // Generate random particles
    const newParticles = Array.from({ length: 30 }, (_, i) => ({
      id: i,
      left: `${Math.random() * 100}%`,
      delay: Math.random() * 10,
      duration: 15 + Math.random() * 10,
    }));
    setParticles(newParticles);
  }, []);

  return (
    <div className="particle-container">
      {particles.map((particle) => (
        <div
          key={particle.id}
          className="particle"
          style={{
            left: particle.left,
            animationDelay: `${particle.delay}s`,
            animationDuration: `${particle.duration}s`,
          }}
        />
      ))}
    </div>
  );
}

function MainView() {
  const { isSessionActive, startSession, endSession, error } = useSession();

  return (
    <div className="flex min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-orange-50 dark:from-zinc-950 dark:via-purple-950/20 dark:to-zinc-900 relative overflow-hidden">
      {/* Animated particles background */}
      <Particles />

      {/* Main content */}
      <div className="flex flex-1 relative z-10">
        {/* Left panel - Story Editor (always visible) */}
        <div className="flex-1 p-6">
          <div className="max-w-4xl mx-auto h-full flex flex-col">
            {/* Header with royal styling */}
            <div className="mb-4 fade-in">
              <h1 className="text-xl font-bold text-purple-600 dark:text-purple-400 mb-1">
                StoryVA
              </h1>
              <p className="text-sm text-zinc-600 dark:text-zinc-400">
                AI Voice Director with Lelouch
              </p>
            </div>

            {/* Error display with animation */}
            {error && (
              <div className="mb-4 p-4 glass border-2 border-red-500/50 rounded-xl fade-in">
                <p className="text-red-900 dark:text-red-200 text-sm font-medium">
                  <strong>⚠️ Error:</strong> {error}
                </p>
              </div>
            )}

            {/* Story Editor with glass effect */}
            <div className="flex-1 mb-6 fade-in" style={{ animationDelay: '0.1s' }}>
              <StoryEditor />
            </div>

            {/* Session Controls with epic styling */}
            <div className="flex items-center gap-4 fade-in" style={{ animationDelay: '0.2s' }}>
              {!isSessionActive ? (
                <button
                  onClick={startSession}
                  className="px-6 py-3 bg-purple-600 hover:bg-purple-700 text-white rounded-lg font-semibold shadow-lg hover-lift transition-all duration-300"
                >
                  Start Direction Session
                </button>
              ) : (
                <button
                  onClick={endSession}
                  className="px-6 py-3 bg-red-600 hover:bg-red-700 text-white rounded-lg font-semibold shadow-lg hover-lift transition-all duration-300"
                >
                  <span className="flex items-center gap-2">
                    🛑 End Session
                  </span>
                </button>
              )}
              {isSessionActive && (
                <div className="flex items-center gap-3 px-4 py-3 glass rounded-xl glow-purple">
                  <div className="relative flex h-3 w-3">
                    <span className="animate-ping-slow absolute inline-flex h-full w-full rounded-full bg-purple-400 opacity-75"></span>
                    <span className="relative inline-flex rounded-full h-3 w-3 bg-purple-500"></span>
                  </div>
                  <span className="text-sm font-semibold text-purple-900 dark:text-purple-200">
                    Lelouch is listening...
                  </span>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Right panel - Transcript (appears during session) */}
        {isSessionActive && (
          <div className="w-96 h-screen border-l-2 border-purple-500/30 glass p-6 flex flex-col backdrop-blur-xl fade-in">
            <div className="mb-4 pb-4 border-b border-purple-500/30">
              <h2 className="text-xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 dark:from-purple-400 dark:to-pink-400 bg-clip-text text-transparent">
                Live Command Log
              </h2>
            </div>
            <LiveTranscript className="flex-1" />
          </div>
        )}
      </div>
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
