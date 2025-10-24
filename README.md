# StoryVA - Voice Director Agent

A RAG-enabled voice agent that helps writers add professional Fish Audio emotion markup to their stories through natural conversation. The agent, "Lelouch," acts as a strategic voice director, teaching theatrical techniques from classic voice acting texts and applying them interactively.

Lelouch is a character from the anime Code Geass known for his strategic thinking and dramatic flair. He once took control over the world to save it from itself.
To save the world, he got the whole world to hate him instead of eachother, and then faked his death. By doing so, their hatred resolved.

In this context, Lelouch went into hiding after faking his death and now teaches disciples the way of persuasion.

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

**Session Start:**
User pastes story into editor → clicks "Start Direction Session" → frontend requests LiveKit token with room metadata → agent auto-joins room via LiveKit dispatch → microphone enabled.

**Agent Initialization:**
Worker preloads RAG (Pinecone + LlamaIndex) on startup. Per-room: agent parses story from metadata, sets up data channel for story updates, initializes voice pipeline (Silero VAD → Deepgram STT → GPT-5 LLM → Fish Audio TTS), connects to room.

**Conversation Loop:**
User speaks → VAD detects → Deepgram transcribes → GPT-5 processes with current story context + Lelouch personality → optionally calls tools:
- `search_acting_technique`: RAG retrieves top-5 passages from voice acting books with citations
- `apply_emotion_diff`: Validates Fish Audio tags, checks text match, generates unified diff, sends to frontend via data channel

Agent responds → Fish Audio synthesizes → audio + transcript sent to frontend (synchronized).

**Diff Application:**
Frontend displays inline diff (red strikethrough for removed, green highlight for added) with Accept/Reject buttons. User accepts → text updated in editor + localStorage → `story_update` sent to backend. User rejects → diff dismissed.

---

## RAG System

**Purpose**: Retrieve voice acting techniques from 4 classic texts to support agent suggestions with authoritative citations.

**Architecture**: LlamaIndex query engine → Pinecone Cloud (`storyva-voice-acting` index, 1173 vectors) → OpenAI `text-embedding-3-large` (1536 dims) → Top-k=5 retrieval → GPT-5 synthesis with citations.

**Source Documents**:
1. "An Actor Prepares" by Constantin Stanislavski
2. "Freeing the Natural Voice" by Kristin Linklater
3. "The Voice Director's Handbook Volume 1"
4. "The Voice Director's Handbook Volume 2"

**Chunking**: LlamaIndex defaults (~512 tokens, ~50 overlap, semantic splitting). Works well for prose without custom domain splitting.

**Why This Stack**:
- Pinecone: Managed service, free tier covers 1173 vectors, zero maintenance
- `text-embedding-3-large`: Better quality for nuanced acting concepts vs `-small`
- Top-k=5: Balances relevance vs context length

**Tool**: `search_acting_technique(query)` - RAG retrieves passages, LLM synthesizes answer with author/title/page citations.

**Query Examples**: "How to sound desperate?", "What does Stanislavski say about subtext?"

**Indexing** (one-time, already complete): `cd backend && uv run python scripts/index_pdfs.py`

**Code**: `backend/rag/indexer.py`, `backend/rag/retriever.py`, `agent/lelouch.py`

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

**Custom Fish Audio TTS**: Built custom LiveKit TTS plugin using `fish-audio-sdk` since Fish Audio isn't available as a built-in plugin. Required for 60+ emotion tags (core feature). Trade-off: more complexity vs essential emotion capability.

**Have Lelouch use fishaudio instead of a call to fishaudio for emotion narration**: Originally planned to have Lelouch make a tool call to fishaudio when the user wanted to hear how a line would sound with emotion. Decided to just have Lelouch use fishaudio directly, telling him to avoid using parentheses when explaining, and only use parentheses when performing the line.

**Decided not to use multicharacter narration**: Time constraint.

**Story State Sync**: Bidirectional data channel keeps story text synchronized—frontend sends `story_update` on edits, backend injects `<current_story>` into LLM context. Enables real-time editing but adds state management complexity.

**Unified Diff Format**: Git-style diffs for emotion markup changes (clear, handles multi-line). Requires exact text matching— which can fail if user edits between suggestion and acceptance. Can also fail if the LLM sends an improper diff edit request.

**Synchronized Transcript**: Agent text sent via data channel when first audio chunk plays (`on_text_synthesizing` callback). User sees text as they hear agent—better UX, slight complexity trade-off.

**No Revision History**: Only tracks current pending diff, no undo (MVP scope limitation). Simpler implementation but user can't undo accepted changes.

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

## Agent Tools

**search_acting_technique(query)**: RAG retrieval from voice acting books. Returns synthesized answer with author/title/page citations. Triggered when user asks about techniques or agent proactively cites sources.

**apply_emotion_diff(diff_patch, explanation)**: Validates Fish Audio emotion tags (60+ emotions), checks original text exists in current story (exact match), generates unified diff, sends to frontend via data channel. Triggered when user requests emotion markup.