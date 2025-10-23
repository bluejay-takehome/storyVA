/**
 * ViewController Component
 *
 * Switches between WelcomeView (pre-call) and SessionView (during-call)
 * based on session state.
 *
 * Based on LiveKit agent-starter-react example.
 */

'use client';

import { useSession } from './SessionProvider';
import { WelcomeView } from './WelcomeView';

/**
 * ViewController manages the main view state.
 *
 * Shows WelcomeView when session is inactive,
 * SessionView when session is active.
 *
 * Note: SessionView will be created in Phase 5B.
 */
export function ViewController() {
  const { isSessionActive, startSession } = useSession();

  // For Phase 5A, we only show WelcomeView
  // SessionView will be added in Phase 5B
  if (!isSessionActive) {
    return <WelcomeView onStartCall={startSession} />;
  }

  // Temporary placeholder for SessionView (Phase 5B)
  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-900 text-white">
      <div className="text-center">
        <h1 className="text-2xl font-bold mb-4">Session Active</h1>
        <p className="text-zinc-400">SessionView will be implemented in Phase 5B</p>
        <p className="text-zinc-500 mt-2 text-sm">
          You should see LiveKit connection logs in the console
        </p>
      </div>
    </div>
  );
}
