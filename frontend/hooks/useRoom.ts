/**
 * useRoom Hook
 *
 * Manages LiveKit room connection lifecycle:
 * - Creates Room instance
 * - Fetches tokens from API
 * - Handles connection/disconnection
 * - Manages session state
 *
 * Based on LiveKit agent-starter-react example.
 */

import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Room, RoomEvent, TokenSource } from 'livekit-client';
import { AppConfig } from '@/app-config';

interface ConnectionDetails {
  serverUrl: string;
  roomName: string;
  participantToken: string;
  participantName: string;
}

export function useRoom(appConfig: AppConfig) {
  const aborted = useRef(false);
  const room = useMemo(() => new Room(), []);
  const [isSessionActive, setIsSessionActive] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Handle room disconnection
  useEffect(() => {
    function onDisconnected() {
      console.log('Room disconnected');
      setIsSessionActive(false);
    }

    function onMediaDevicesError(error: Error) {
      console.error('Media devices error:', error);
      setError(`Media error: ${error.message}`);
    }

    room.on(RoomEvent.Disconnected, onDisconnected);
    room.on(RoomEvent.MediaDevicesError, onMediaDevicesError);

    return () => {
      room.off(RoomEvent.Disconnected, onDisconnected);
      room.off(RoomEvent.MediaDevicesError, onMediaDevicesError);
    };
  }, [room]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      aborted.current = true;
      room.disconnect();
    };
  }, [room]);

  // Token source - fetches from our API
  const tokenSource = useMemo(
    () =>
      TokenSource.custom(async () => {
        const url = new URL('/api/livekit-token', window.location.origin);

        console.log('Fetching LiveKit token from:', url.toString());

        try {
          const res = await fetch(url.toString(), {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              room_config: appConfig.agentName
                ? {
                    agents: [{ agent_name: appConfig.agentName }],
                  }
                : undefined,
            }),
          });

          if (!res.ok) {
            const errorData = await res.json();
            throw new Error(
              `Token fetch failed: ${errorData.error || res.statusText}`
            );
          }

          const details: ConnectionDetails = await res.json();
          console.log('Token received:', {
            serverUrl: details.serverUrl,
            roomName: details.roomName,
          });

          return details;
        } catch (error) {
          console.error('Error fetching connection details:', error);
          throw new Error(
            error instanceof Error ? error.message : 'Failed to fetch token'
          );
        }
      }),
    [appConfig]
  );

  // Start session - enable microphone and connect to room
  const startSession = useCallback(() => {
    console.log('Starting session...');
    setIsSessionActive(true);
    setError(null);

    if (room.state === 'disconnected') {
      Promise.all([
        // Enable microphone (with buffer for better experience)
        room.localParticipant.setMicrophoneEnabled(true, undefined, {
          preConnectBuffer: true,
        }),
        // Fetch token and connect
        tokenSource
          .fetch({ agentName: appConfig.agentName })
          .then((connectionDetails) => {
            console.log('Connecting to room:', connectionDetails.roomName);
            return room.connect(
              connectionDetails.serverUrl,
              connectionDetails.participantToken
            );
          }),
      ])
        .then(() => {
          console.log('✅ Successfully connected to LiveKit room');
        })
        .catch((error) => {
          if (aborted.current) {
            // Effect cleaned up, drop errors from previous runs
            return;
          }

          console.error('Connection error:', error);
          setError(
            error instanceof Error
              ? error.message
              : 'Failed to connect to agent'
          );
          setIsSessionActive(false);
        });
    }
  }, [room, appConfig, tokenSource]);

  // End session - disconnect from room
  const endSession = useCallback(() => {
    console.log('Ending session...');
    setIsSessionActive(false);
    room.disconnect();
  }, [room]);

  return { room, isSessionActive, startSession, endSession, error };
}
