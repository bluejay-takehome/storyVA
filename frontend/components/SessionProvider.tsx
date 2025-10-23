/**
 * SessionProvider Component
 *
 * Context provider that wraps LiveKit's RoomContext and manages session state.
 * Provides session control (start/end) and state to all child components.
 *
 * Based on LiveKit agent-starter-react example.
 */

'use client';

import { createContext, useContext, ReactNode } from 'react';
import { RoomContext } from '@livekit/components-react';
import { Room } from 'livekit-client';
import { AppConfig } from '@/app-config';
import { useRoom } from '@/hooks/useRoom';

interface SessionContextType {
  appConfig: AppConfig;
  isSessionActive: boolean;
  startSession: () => void;
  endSession: () => void;
  error: string | null;
}

// Create session context
const SessionContext = createContext<SessionContextType | undefined>(undefined);

// Session provider props
interface SessionProviderProps {
  appConfig: AppConfig;
  children: ReactNode;
}

/**
 * SessionProvider wraps the app with both RoomContext and session management.
 *
 * Usage:
 *   <SessionProvider appConfig={APP_CONFIG}>
 *     <YourApp />
 *   </SessionProvider>
 */
export function SessionProvider({ appConfig, children }: SessionProviderProps) {
  const { room, isSessionActive, startSession, endSession, error } = useRoom(appConfig);

  const sessionValue: SessionContextType = {
    appConfig,
    isSessionActive,
    startSession,
    endSession,
    error,
  };

  return (
    <RoomContext.Provider value={room}>
      <SessionContext.Provider value={sessionValue}>
        {children}
      </SessionContext.Provider>
    </RoomContext.Provider>
  );
}

/**
 * Hook to access session state and controls.
 *
 * Usage:
 *   const { isSessionActive, startSession, endSession } = useSession();
 */
export function useSession() {
  const context = useContext(SessionContext);
  if (context === undefined) {
    throw new Error('useSession must be used within a SessionProvider');
  }
  return context;
}
