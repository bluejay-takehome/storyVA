# StoryVA - Voice Director Agent

A RAG-enabled voice agent that helps writers add professional Fish Audio emotion markup to their stories through natural conversation. The agent, "Lelouch," acts as a strategic voice director, teaching theatrical techniques from classic voice acting texts and applying them interactively.

Lelouch is a character from the anime Code Geass known for his strategic thinking and dramatic flair. He once took control over the world to save it from itself.
To save the world, he got the whole world to hate him instead of eachother, and then faked his death. By doing so, their hatred resolved.

In this context, Lelouch went into hiding after faking his death and now teaches disciples the way of persuasion.

---

## Table of Contents

- [Demo](#demo)
- [System Architecture](#system-architecture)
- [How It Works (End-to-End)](#how-it-works-end-to-end)
- [RAG Integration](#rag-integration)
- [Technology Stack](#technology-stack)
- [Setup Instructions](#setup-instructions)
- [Design Decisions & Trade-offs](#design-decisions--trade-offs)
- [Hosting Assumptions](#hosting-assumptions)
- [RAG Assumptions](#rag-assumptions)
- [LiveKit Agent Design](#livekit-agent-design)

---

**Demo Flow:**
1. User pastes story text into editor
2. Clicks "Start Direction Session"
3. Agent (Lelouch) greets user with personality
4. User requests emotion markup: "Make the breakup scene more emotional"
5. Agent retrieves technique from Stanislavski, suggests specific Fish Audio tags
6. Inline diff displays proposed changes with Accept/Reject buttons
7. User accepts → text updates with emotion markup

---

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Frontend (Next.js 16)                       │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐ │
│  │ Story Editor│  │ Live         │  │ Session       │ │
│  │ (editable)  │  │ Transcript   │  │ Controls      │ │
│  │ + Inline    │  │              │  │ (Start/End)   │ │
│  │ Diffs       │  │              │  │               │ │
│  └─────────────┘  └──────────────┘  └───────────────┘ │
└────────────────────┬────────────────────────────────────┘
                     │ WebRTC + Data Channel
┌────────────────────▼────────────────────────────────────┐
│            LiveKit Cloud (Media Server)                  │
│  - Room management                                       │
│  - WebRTC streaming                                      │
│  - Agent dispatch                                        │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│       Python Backend (LiveKit Agent Worker)              │
│                                                           │
│  ┌────────────────────────────────────────────────────┐ │
│  │  Voice Pipeline                                     │ │
│  │  VAD (Silero) → STT (Deepgram) → LLM (GPT-5)      │ │
│  │                ↓                                    │ │
│  │          TTS (Fish Audio SDK)                       │ │
│  └────────────────────────────────────────────────────┘ │
│                                                           │
│  ┌────────────────────────────────────────────────────┐ │
│  │  LelouchAgent (Class-based)                        │ │
│  │  - search_acting_technique (RAG)                   │ │
│  │  - apply_emotion_diff (validation + diff)          │ │
│  └────────────────────────────────────────────────────┘ │
│                                                           │
│  ┌────────────────────────────────────────────────────┐ │
│  │  RAG System                                         │ │
│  │  LlamaIndex → Pinecone (1173 vectors)             │ │
│  │  Embeddings: text-embedding-3-large                │ │
│  └────────────────────────────────────────────────────┘ │
└────────────────────┬────────────────────┬────────────────┘
                     │                    │
         ┌───────────▼─────────┐  ┌──────▼──────────┐
         │ Pinecone Cloud      │  │ Fish Audio API  │
         │ (Vector Store)      │  │ (TTS Service)   │
         │ - 4 PDF books       │  │ - Emotion tags  │
         │ - Top-k=5 retrieval │  │ - Streaming     │
         └─────────────────────┘  └─────────────────┘
```

**Key Components:**
- **Frontend**: React-based UI with LiveKit components
- **Backend**: Python agent with voice pipeline + tools
- **LiveKit Cloud**: Handles WebRTC media and agent dispatch
- **Pinecone**: Stores embedded voice acting knowledge
- **External APIs**: OpenAI (LLM + embeddings), Deepgram (STT), Fish Audio (TTS)

---

## How It Works (End-to-End)

### 1. Frontend Session Start

**User Actions:**
- Pastes story text into Story Editor component
- Text auto-saves to localStorage
- Clicks "Start Direction Session"

**What Happens:**
1. `useRoom` hook calls `/api/livekit-token` (POST)
2. Token endpoint generates:
   - Unique room name
   - Participant access token
   - Room configuration with `RoomAgentDispatch` (agent_name: "storyva-voice-director")
   - Metadata containing initial story text
3. Frontend connects to LiveKit room
4. Enables microphone
5. Agent automatically joins room (dispatched by LiveKit)

**Code Flow:**
```
frontend/app/page.tsx (Start button click)
  ↓
hooks/useRoom.ts (fetch token + connect)
  ↓
api/livekit-token/route.ts (generate token with agent dispatch)
  ↓
LiveKit Cloud (create room, dispatch agent)
```

### 2. Backend Agent Initialization

**Worker Startup (Once per process):**
- `prewarm()` function initializes global RAG retriever
- Connects to Pinecone index `storyva-voice-acting`
- Sets up LlamaIndex query engine

**Per-Room Connection:**
1. `entrypoint()` function called when agent joins room
2. Creates `StoryState` (session state management)
3. Parses job metadata for initial story text
4. Sets up data channel listener for real-time story updates
5. Creates `on_text_synthesizing` callback for synchronized transcript
6. Initializes voice pipeline:
   - VAD: Silero (voice activity detection)
   - STT: Deepgram Nova-3 (300ms endpointing)
   - LLM: GPT-5 (with reasoning effort)
   - TTS: Fish Audio SDK (mp3 format, normal latency)
7. Starts session with `LelouchAgent` instance
8. Connects to LiveKit room

**Code Flow:**
```
backend/main.py (worker start)
  ↓
agent/lelouch.py::prewarm() (initialize RAG)
  ↓
agent/lelouch.py::entrypoint() (per-room setup)
  ↓
agent/voice_pipeline.py (create AgentSession)
  ↓
LelouchAgent initialized with 2 tools
```

### 3. Conversation Loop

**User Speaks:**
1. Microphone captures audio
2. VAD detects speech
3. Deepgram transcribes in real-time
4. User speech logged in backend: `👤 User: {transcript}`
5. User transcription appears in frontend LiveTranscript

**Agent Processes:**
1. GPT-5 receives transcript + system instructions
2. `on_user_turn_completed` hook injects `<current_story>{text}</current_story>` into context
3. Agent analyzes with Lelouch personality (strategic, concise)
4. If technique needed → calls `search_acting_technique(query)`
   - RAG retrieves top-5 passages from Pinecone
   - Returns with citations (author, title, page)
5. If emotion markup needed → calls `apply_emotion_diff(diff_patch, explanation)`
   - Validates Fish Audio tags (60+ emotions, tones, effects)
   - Checks original text exists in current story (exact match)
   - Generates unified diff
   - Sends `emotion_diff` message via data channel to frontend

**Agent Responds:**
1. GPT-5 generates response text
2. Fish Audio SDK synthesizes with Lelouch voice
3. After first audio chunk is pushed → `on_text_synthesizing` callback fires
4. Agent text sent via data channel to frontend
5. Frontend displays in LiveTranscript synchronized with audio
6. User hears agent voice through `RoomAudioRenderer`

### 4. Diff Application

**Frontend Receives Diff:**
1. StoryEditor listens for `emotion_diff` messages on data channel
2. Displays inline diff with word-level highlighting:
   - Removed text: red strikethrough
   - Added text: green highlight
3. Shows Accept/Reject buttons above editor

**User Accepts:**
1. Clicks Accept button
2. Original text replaced with proposed text
3. Updated text saved to localStorage
4. `story_update` message sent via data channel to backend
5. Agent's `StoryState` updated with new text
6. Diff removed from pending list

**User Rejects:**
1. Clicks Reject button
2. Diff dismissed (no changes applied)

---

## RAG Integration

**Purpose:** Retrieve relevant voice acting techniques from classic texts to support agent's suggestions.

**Vector Database:**
- **Service**: Pinecone Cloud
- **Index**: `storyva-voice-acting`
- **Vectors**: 1173 chunks from 4 PDF books
- **Metric**: Cosine similarity

**Source Documents:**
1. "An Actor Prepares" by Constantin Stanislavski
2. "Freeing the Natural Voice" by Kristin Linklater
3. "The Voice Director's Handbook Volume 1"
4. "The Voice Director's Handbook Volume 2"

**Embeddings:**
- **Model**: OpenAI `text-embedding-3-large`
- **Dimensions**: 1536
- **Why this model**: Better quality for nuanced acting concepts vs `-small`

**Framework:**
- **LlamaIndex**: Query engine with Pinecone vector store
- **Retrieval**: Top-k=5 (balances relevance vs context length)
- **Response**: LLM synthesizes passages into conversational answer

**Indexing Process:**
```bash
# One-time setup (already completed)
cd backend
uv run python scripts/index_pdfs.py
```

**Code:**
- Indexer: `backend/rag/indexer.py`
- Retriever: `backend/rag/retriever.py`
- Tool: `LelouchAgent.search_acting_technique()`

**Query Examples:**
- "How do I make a character sound more desperate?"
- "What techniques help with emotional authenticity?"
- "What does Stanislavski say about subtext?"

**Response Format:**
```
[Synthesized answer based on retrieved passages]

Sources:
- An Actor Prepares by Constantin Stanislavski (p.42)
- Freeing the Natural Voice by Kristin Linklater (p.89)
```

---

## Technology Stack

### Frontend
Next.js, TypeScript, Tailwind CSS, LiveKit components, livekit-client, livekit-server-sdk, diff

### Backend
Python, livekit-agents, fish-audio-sdk, llama-index, pinecone-client

### External Services
LiveKit Cloud, Pinecone, OpenAI, Deepgram, Fish Audio


---

## Setup Instructions

### Prerequisites

- **Node.js**: 18.x or higher
- **Python**: 3.10 or higher
- **uv**: Python package manager ([install](https://github.com/astral-sh/uv))
- **API Keys**: LiveKit, OpenAI, Deepgram, Fish Audio, Pinecone

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd storyVA
```

### 2. Backend Setup

```bash
cd backend

# Install dependencies with uv
uv sync

# Copy environment template
cp .env.example .env

# Edit .env and add your API keys:
# - LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET
# - OPENAI_API_KEY (or use system environment)
# - DEEPGRAM_API_KEY
# - FISH_AUDIO_API_KEY
# - PINECONE_API_KEY
# - PINECONE_INDEX_NAME=storyva-voice-acting
```

**Environment Variables:**
```bash
# LiveKit
LIVEKIT_URL=wss://your-instance.livekit.cloud
LIVEKIT_API_KEY=your_key
LIVEKIT_API_SECRET=your_secret

# OpenAI (GPT-5 + embeddings)
OPENAI_API_KEY=your_key

# Deepgram (STT)
DEEPGRAM_API_KEY=your_key

# Fish Audio (TTS)
FISH_AUDIO_API_KEY=your_key
FISH_LELOUCH_VOICE_ID=48056d090bfe4d6690ff31725075812f

# Pinecone (Vector DB)
PINECONE_API_KEY=your_key
PINECONE_INDEX_NAME=storyva-voice-acting
```

### 3. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Copy environment template (create if needed)
cp .env.example .env.local

# Edit .env.local and add LiveKit credentials:
LIVEKIT_URL=wss://your-instance.livekit.cloud
LIVEKIT_API_KEY=your_key
LIVEKIT_API_SECRET=your_secret
```

### 4. (Optional) Index PDFs

If you're using a fresh Pinecone index or want to re-index the PDF books:

```bash
cd backend

# Run indexing script (one-time)
uv run python scripts/index_pdfs.py

# Verify indexing in Pinecone dashboard
# Should see ~1173 vectors in index
```

### 5. Run Backend Agent

```bash
cd backend

# Start LiveKit agent worker
uv run python main.py start

# You should see:
# ✅ Environment configuration verified
# ✅ Worker ready
# Agent worker started
```

### 6. Run Frontend (Separate Terminal)

```bash
cd frontend

# Start Next.js dev server
npm run dev

# Open browser at http://localhost:3000
```

### 7. Test the Application

1. Open http://localhost:3000 in browser
2. Paste example story text:
   ```
   "I can't believe you did this," she said quietly.

   He looked away, guilt washing over him. "I had no choice."
   ```
3. Click "Start Direction Session"
4. Wait for agent to connect (see "Session active" indicator)
5. Click "Click to enable audio" if prompted (browser autoplay policy)
6. Speak to agent: "Make this scene more emotional"
7. Agent retrieves technique and suggests emotion markup
8. Accept or reject inline diff

---

## Design Decisions & Trade-offs

### 1. Custom Fish Audio TTS Integration

**Decision**: Implement custom LiveKit TTS plugin using `fish-audio-sdk`

**Rationale:**
- Fish Audio not available as built-in LiveKit plugin
- Supports 60+ emotion tags (core feature requirement)
- Official SDK more reliable than manual WebSocket protocol

**Trade-offs:**
- ✅ Gets emotion markup capability (essential)
- ✅ Stable SDK maintained by Fish Audio
- ❌ More complex than using built-in TTS
- ❌ Requires understanding LiveKit TTS interface

**Implementation**: `backend/tts/fish_audio.py` (using ChunkedStream pattern)

### 2. Story State Synchronization

**Decision**: Bidirectional data channel for real-time story updates

**Architecture:**
- Frontend sends `story_update` messages on every edit
- Backend maintains `StoryState` with current text
- Agent injects `<current_story>` into LLM context before each response

**Rationale:**
- Agent needs latest story text to suggest accurate diffs
- Exact text matching required for diff validation
- Editable textarea (user can modify during session)

**Trade-offs:**
- ✅ Always in sync, no stale data
- ✅ Supports real-time editing
- ❌ Slight network latency on updates
- ❌ More complex state management

### 3. Unified Diff Format

**Decision**: Git-style unified diffs for emotion markup changes

**Format Example:**
```
@@ -1 +1 @@
-"I can't believe this," she said.
+(sad)(soft tone) "I can't believe this," she said.
```

**Rationale:**
- Precise, unambiguous change representation
- Handles multi-line changes
- Familiar to developers

**Trade-offs:**
- ✅ Clear, professional format
- ✅ Works with any text length
- ❌ Requires exact character-for-character matching
- ❌ Fails if user edits text between suggestion and acceptance

**Validation**: `backend/tools/diff_generator.py` + `emotion_validator.py`

### 4. Single-View UI

**Decision**: Story editor always visible, transcript appears on right during session

**Rationale:**
- Simpler than separate welcome/session views
- User can see story while conversing
- Faster to implement

**Trade-offs:**
- ✅ Straightforward UX
- ✅ Less state management
- ❌ Less polished than multi-view
- ❌ Tight screen space on small displays

**Alternative considered**: Separate WelcomeView/SessionView with transitions (rejected for MVP scope)

### 5. Synchronized Transcript

**Decision**: Send agent text via data channel when first audio chunk plays

**Flow:**
```
LLM generates → TTS synthesizes → First chunk sent →
Callback fires → Text sent to frontend → Display immediately
```

**Rationale:**
- User sees text as they hear agent speak (better UX)
- No waiting for full TTS completion
- Synchronized experience

**Trade-offs:**
- ✅ Real-time feel
- ✅ Text + audio aligned
- ❌ Added callback complexity in TTS
- ❌ Text appears even if interrupted (acceptable)

**Implementation**: `on_text_synthesizing` callback in `fish_audio.py`

### 6. No Revision History

**Decision**: Only track current pending diff, no undo functionality

**Rationale:**
- MVP scope limitation
- Time constraints
- localStorage provides manual rollback (user can copy old version)

**Trade-offs:**
- ✅ Simpler implementation
- ✅ Less state management
- ❌ User can't undo accepted changes
- ❌ No history log

**Future enhancement**: Store `applied_diffs` array in `StoryState` for potential undo

---

## Hosting Assumptions

### Deployment Model: Local Development

**Primary Use Case**: Local testing and demonstration

**Components:**
- **Frontend**: Runs on `localhost:3000` (Next.js dev server)
- **Backend**: Runs as local agent worker, connects to LiveKit Cloud
- **LiveKit**: Cloud-hosted (no self-hosting required)
- **Pinecone**: Cloud-hosted vector database
- **External APIs**: All cloud services (OpenAI, Deepgram, Fish Audio)


### Production Deployment (Future)

If deploying to production:

**Option A: AWS EC2**
- Ubuntu instance with Python + Node.js
- systemd service for backend agent
- Nginx reverse proxy for frontend
- S3 for PDF storage

**Option B: Vercel (Frontend) + AWS (Backend)**
- Vercel for Next.js frontend (zero-config)
- AWS App Runner for backend agent (containerized)
- Environment variables via platform UIs

**Not Implemented**: AWS deployment intentionally skipped (documented in TDD as stretch goal)

---

## RAG Assumptions

### Chunking Strategy

**Approach**: LlamaIndex default chunking (semantic splitting)

**Parameters:**
- Chunk size: ~512 tokens (default)
- Chunk overlap: ~50 tokens (default)
- Preserves paragraph/section context

**Rationale:**
- LlamaIndex defaults work well for prose
- No custom splitting needed for voice acting books
- Semantic boundaries preserved

**Trade-offs:**
- ✅ Fast implementation
- ✅ Good retrieval quality in testing
- ❌ No domain-specific splitting (e.g., by technique, chapter)

### Vector Database Choice

**Selected**: Pinecone Cloud

**Alternatives Considered:**
- Chroma (local, embedded)
- Weaviate (self-hosted)
- Qdrant (self-hosted)

**Why Pinecone:**
- Managed service (no infrastructure)
- Free tier sufficient (100k vectors, we use 1173)
- Easy setup with LlamaIndex
- Reliable, production-ready

**Trade-offs:**
- ✅ Zero maintenance
- ✅ Fast queries
- ❌ Requires internet connection
- ❌ Vendor lock-in

### Embedding Model

**Selected**: OpenAI `text-embedding-3-large` (1536 dimensions)

**Why this model:**
- Better quality for nuanced concepts than `-small`
- Matches retrieval quality needs (acting techniques are complex)
- Worth the slight cost/latency increase

**Trade-offs:**
- ✅ Better retrieval accuracy
- ❌ Slower than `-small` (~10% more latency)
- ❌ Slightly more expensive per query

### Retrieval Parameters

**Top-k**: 5 chunks per query

**Rationale:**
- Balances relevance (enough context) vs context length (LLM limits)
- Testing showed 5 provides sufficient citations
- Allows 1-2 sources with ~3 passages each

**Trade-offs:**
- ✅ Good coverage of relevant techniques
- ❌ Higher k would increase latency/cost

### Query Processing

**Flow:**
```
User query → OpenAI embedding → Pinecone similarity search →
Top-5 chunks → LlamaIndex synthesis → Conversational response
```

**Synthesis**: LLM (GPT-5) combines retrieved passages into coherent answer with citations

---

### Tool Calling

**Tool 1: search_acting_technique**
- **Purpose**: RAG retrieval from voice acting books
- **Input**: Natural language query (e.g., "How to convey desperation?")
- **Process**: Query → Embedding → Pinecone search → LlamaIndex synthesis
- **Output**: Formatted answer with citations
- **Trigger**: User asks about techniques, or agent proactively cites sources

**Tool 2: apply_emotion_diff**
- **Purpose**: Validate and apply Fish Audio emotion markup
- **Input**: Unified diff string + explanation
- **Validation**:
  1. Parse diff to extract original/proposed text
  2. Check original exists in current story (exact match)
  3. Validate emotion tags against Fish Audio spec (60+ tags)
  4. Check tag placement rules (emotions at sentence start)
- **Output**: JSON result with diff data
- **Side Effect**: Sends `emotion_diff` message via data channel to frontend
- **Trigger**: User requests emotion markup for specific text