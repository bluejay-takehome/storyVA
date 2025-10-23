/**
 * LiveKit Token Generation API
 *
 * POST endpoint that generates access tokens for LiveKit room connections.
 * Includes agent configuration to auto-dispatch the StoryVA voice director.
 *
 * Request body:
 *   {
 *     room_config?: {
 *       agents?: [{ agent_name: string }]
 *     }
 *   }
 *
 * Response:
 *   {
 *     serverUrl: string,
 *     roomName: string,
 *     participantToken: string,
 *     participantName: string
 *   }
 */

import { NextResponse } from 'next/server';
import { AccessToken, RoomAgentDispatch } from 'livekit-server-sdk';

// LiveKit server configuration from environment variables
const LIVEKIT_URL = process.env.LIVEKIT_URL;
const LIVEKIT_API_KEY = process.env.LIVEKIT_API_KEY;
const LIVEKIT_API_SECRET = process.env.LIVEKIT_API_SECRET;

export async function POST(req: Request) {
  try {
    // Validate environment variables
    if (!LIVEKIT_URL || !LIVEKIT_API_KEY || !LIVEKIT_API_SECRET) {
      console.error('Missing LiveKit environment variables:', {
        hasUrl: !!LIVEKIT_URL,
        hasKey: !!LIVEKIT_API_KEY,
        hasSecret: !!LIVEKIT_API_SECRET,
      });
      return NextResponse.json(
        { error: 'LiveKit server not configured' },
        { status: 500 }
      );
    }

    // Parse request body
    const body = await req.json();
    const agentName = body?.room_config?.agents?.[0]?.agent_name;
    const agentMetadata = body?.room_config?.agents?.[0]?.metadata;

    // Generate unique room and participant identifiers
    const roomName = `storyva_room_${Math.floor(Math.random() * 10_000)}`;
    const participantIdentity = `writer_${Math.floor(Math.random() * 10_000)}`;

    console.log('Generating token:', { roomName, participantIdentity, agentName, hasMetadata: !!agentMetadata });

    // Create access token with participant info
    const at = new AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET, {
      identity: participantIdentity,
      name: 'Writer', // Display name in LiveKit dashboard
      ttl: '15m', // Token expires in 15 minutes
    });

    // Add room permissions
    at.addGrant({
      room: roomName,
      roomJoin: true, // Can join the room
      canPublish: true, // Can publish audio/video
      canPublishData: true, // Can publish data messages
      canSubscribe: true, // Can subscribe to other participants
    });

    // Add agent configuration to room if agent name provided
    if (agentName) {
      at.roomConfig = {
        agents: [
          new RoomAgentDispatch({
            agentName,
            metadata: agentMetadata,  // Pass story text metadata to agent
          }),
        ],
      };
      console.log('Agent configured in room:', agentName, 'with metadata:', !!agentMetadata);
    }

    // Generate JWT token
    const participantToken = await at.toJwt();

    // Return connection details
    return NextResponse.json({
      serverUrl: LIVEKIT_URL,
      roomName,
      participantToken,
      participantName: 'Writer',
    });
  } catch (error) {
    console.error('Error generating LiveKit token:', error);
    return NextResponse.json(
      {
        error: 'Failed to generate token',
        details: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 500 }
    );
  }
}
