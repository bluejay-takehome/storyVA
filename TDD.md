# Technical Design Document: Voice Director Agent
**Project:** StoryVA - Voice Acting Direction Agent
**Version:** 1.1
**Date:** October 22, 2025 (Updated after repository flattening)
**Status:** In Progress - Phase 1 70% Complete

---

## Table of Contents
1. [Executive Summary](#1-executive-summary)
2. [System Architecture](#2-system-architecture)
3. [Technology Stack Decisions](#3-technology-stack-decisions)
4. [Component Design](#4-component-design)
5. [Data Flow](#5-data-flow)
6. [API Integration Specifications](#6-api-integration-specifications)
7. [Development Plan](#7-development-plan)
8. [Deployment Strategy](#8-deployment-strategy)
9. [Testing Strategy](#9-testing-strategy)
10. [Risk Analysis](#10-risk-analysis)

---

## 1. Executive Summary

### 1.1 Project Overview
Build a RAG-enabled voice agent that acts as "Lelouch," a brilliant voice director who helps writers add professional emotion markup to stories using Fish Audio's text-to-speech system with 60+ emotion tags.

### 1.2 Key Requirements (from GUIDELINES.md)
- ✅ LiveKit voice agent (real-time conversation)
- ✅ RAG over PDF documents (2 voice acting books)
- ✅ Tool calling (RAG search + Fish Audio character preview)
- ✅ React frontend (Next.js)
- ✅ Single git repository
- ✅ Creative storytelling (Lelouch personality)

### 1.3 Technical Constraints
- **Must use Python backend** (per GUIDELINES.md)
- **Must use LiveKit** for voice orchestration
- **Must submit single git repo** (no submodules)
- **Deployment:** Local first (AWS deployment is a stretch goal, not required)

### 1.4 Success Criteria
- Agent maintains Lelouch personality consistently
- RAG retrieves relevant voice acting techniques
- Fish Audio emotion tags applied correctly
- Conversation latency < 5 seconds

---

## 2. System Architecture

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend (Next.js)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────┐   │
│  │ Story Editor │  │ Live         │  │ Call Controls      │   │
│  │ (Editable)   │  │ Transcript   │  │ (Start/End)        │   │
│  │              │  │              │  │                    │   │
│  │ Diff View    │  │ Audio Player │  │ Status Indicators  │   │
│  └──────────────┘  └──────────────┘  └────────────────────┘   │
└────────────────────────────┬────────────────────────────────────┘
                             │ WebRTC/WebSocket
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                    LiveKit Cloud Server                          │
│  - Room Management                                               │
│  - Media Streaming (WebRTC)                                      │
│  - Participant Management                                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│              Python Backend (LiveKit Agent)                      │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Voice Pipeline                                          │   │
│  │  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐         │   │
│  │  │ VAD │→ │ STT │→ │ LLM │→ │ TTS │→ │Speak│         │   │
│  │  └─────┘  └─────┘  └─────┘  └─────┘  └─────┘         │   │
│  │  Silero  Deepgram  GPT-5   Fish Audio  Audio          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  RAG System                                              │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────┐         │   │
│  │  │LlamaIndex│→ │ Pinecone │← │ Query Engine │         │   │
│  │  │  Loader  │  │  Vectors │  │              │         │   │
│  │  └──────────┘  └──────────┘  └──────────────┘         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Tools (Function Calling)                                │   │
│  │  - RAG Search (Pinecone query)                          │   │
│  │  - Fish Audio Preview (different voice/character)       │   │
│  │  - Diff Generator                                        │   │
│  │  - Emotion Tag Validator                                 │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  State Management                                        │   │
│  │  - Current story text                                    │   │
│  │  - Conversation history                                  │   │
│  │  - Applied edits                                         │   │
│  └─────────────────────────────────────────────────────────┘   │
└───────────────────────────┬───────────────────────────┬─────────┘
                            │                           │
              ┌─────────────▼────────┐    ┌────────────▼──────────┐
              │   Pinecone Cloud     │    │  Fish Audio API       │
              │   (Vector Store)     │    │  (Preview TTS)        │
              └──────────────────────┘    └───────────────────────┘
```

### 2.2 Repository Structure (Single Repo)

```
storyVA/                          # Single git repository root
├── README.md                      # Main project documentation
├── .gitignore                     # Ignore node_modules, .env, etc.
├── .env.example                   # Template for environment variables
│
├── frontend/                      # Next.js application
│   ├── package.json
│   ├── next.config.js
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx              # Landing page
│   │   └── director/
│   │       └── page.tsx          # Main voice director UI
│   ├── components/
│   │   ├── StoryEditor.tsx       # Text editor with diff view
│   │   ├── LiveTranscript.tsx    # Real-time transcript
│   │   ├── CallControls.tsx      # Start/End call buttons
│   │   └── DiffViewer.tsx        # Inline diff display
│   └── lib/
│       ├── livekit.ts            # LiveKit client setup
│       └── types.ts              # TypeScript types
│
├── backend/                       # Python LiveKit agent
│   ├── .env                       # Local environment variables (not committed)
│   ├── pyproject.toml             # Dependencies with uv
│   ├── uv.lock                    # Dependency lock file
│   ├── main.py                    # Agent entry point
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── lelouch.py            # Agent class & personality
│   │   ├── voice_pipeline.py     # STT → LLM → TTS setup
│   │   └── state.py              # Session state management
│   ├── tts/
│   │   ├── __init__.py
│   │   └── fish_audio.py         # Custom Fish Audio TTS for LiveKit
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── indexer.py            # Build Pinecone index from PDFs
│   │   ├── retriever.py          # Query engine
│   │   └── embeddings.py         # OpenAI embedding wrapper
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── fish_audio_preview.py # Fish Audio HTTP API tool
│   │   ├── diff_generator.py     # Create inline diffs
│   │   └── emotion_validator.py  # Validate Fish Audio tags
│   └── data/
│       ├── pdfs/
│       │   ├── An Actor Prepares.pdf
│       │   └── Freeing the Natural Voice.pdf
│       └── emotion_control.md    # Fish Audio spec reference
│
├── docs/                          # Documentation
│   ├── PRD.md                     # Product Requirements (already exists)
│   ├── TDD.md                     # This document
│   └── DEPLOYMENT.md              # Deployment guide
│
└── scripts/                       # Utility scripts
    ├── setup.sh                   # Initial setup script
    ├── index_pdfs.py              # One-time Pinecone indexing
    └── test_components.py         # Component testing
```

---

## 3. Technology Stack Decisions

### 3.1 Final Stack

| Component | Technology | Rationale |
|-----------|------------|-----------|
| **Frontend Framework** | Next.js 14 (App Router) | React-based (meets requirements), TypeScript support, easy deployment |
| **Frontend Language** | TypeScript | Type safety, better IDE support |
| **Frontend Styling** | Tailwind CSS | Fast development, consistent UI |
| **LiveKit Client** | @livekit/components-react | Official React components |
| **Backend Language** | Python 3.10+ | Required by GUIDELINES.md |
| **Package Manager** | uv | Modern, fast Python package management |
| **Voice Orchestration** | LiveKit Cloud | Managed service, no self-hosting needed |
| **STT Provider** | Deepgram Nova-3 | Fast (<300ms), accurate, latest model (Feb 2025) |
| **LLM** | OpenAI GPT-5 | Latest model, 400K context, built-in reasoning |
| **Agent TTS** | Fish Audio (Custom) | WebSocket streaming, 60+ emotion tags, ~150ms latency |
| **Preview TTS** | Fish Audio (HTTP API) | Different voice for character preview tool call |
| **Vector Database** | Pinecone (Cloud) | Managed, free tier available, easy setup |
| **RAG Framework** | LlamaIndex | Purpose-built for RAG, simpler than LangChain |
| **Embeddings** | OpenAI text-embedding-3-small | Cost-effective, 1536 dimensions |
| **Diff Library** | react-diff-viewer | Pre-built React component, inline mode |

### 3.2 Fish Audio for Complete Voice Solution

**Decision:** Use **Fish Audio** for all TTS (both agent conversation and preview tool calls)

**Implementation Strategy:**
1. **Custom TTS Integration:** Implement Fish Audio as custom LiveKit TTS provider using WebSocket streaming
2. **Agent Voice:** Use Fish Audio with professional/commanding voice for Lelouch
3. **Preview Tool Call:** Use Fish Audio with *different* voice_id for character voice previews

**Why This Works:**
- Fish Audio supports WebSocket streaming (~150ms latency, suitable for real-time)
- Can use emotion markup in agent's own speech (demonstrates capability inline)
- Tool call distinction: Agent voice ≠ Character preview voice
- Showcases Fish Audio's multi-voice and emotion control capabilities

**Custom TTS Implementation:**
Based on research, implement `FishAudioTTS` class following LiveKit's TTS interface:
- WebSocket connection to `wss://api.fish.audio/v1/tts/live`
- msgpack protocol for messages
- Streaming audio chunks to LiveKit
- Emotion tag support in real-time

### 3.3 Tool Calling Strategy (GUIDELINES.md Requirement)

**Requirement:** Demonstrate tool calling capability

**Our Tool Calls:**

1. **`search_acting_technique(query)`** - RAG retrieval ✅
   - External API call to Pinecone vector database
   - Returns voice acting techniques from PDFs
   - **Example:** "What does Stanislavski say about emotional truth?"
   - **Tool execution:** Query → Embedding → Pinecone → LlamaIndex → Response

2. **`preview_line_audio(marked_up_text, character_gender)`** - Character voice preview ✅
   - External API call to Fish Audio HTTP endpoint
   - Uses *different voice* than agent (character vs director)
   - **Example:** User: "How would this sound?" → Agent analyzes: "she said" → infers "female" → Tool call
   - **Tool execution:** Agent infers gender → Fish Audio API (with character voice_id) → MP3 file → Play in frontend
   - **Gender inference:** Automatic from pronouns/names/attribution (he/she, character names, dialogue tags)
   - **Voices:** Male (`802e3bc2...`), Female (`b545c585...`)

3. **`suggest_emotion_markup(line, emotions, explanation)`** - Diff generation
   - Internal tool returning structured data
   - Creates inline diff for display

**Why This Satisfies Requirements:**
- **External tool calls:** RAG search and Fish Audio API
- **Clear input/output:** Structured function parameters and returns
- **Demonstrates capability:** Multiple tool types (database query, API call, structured output)
- **Voice distinction:** Agent voice (Lelouch directing) ≠ Preview voice (character)

### 3.4 API Keys Configuration

**Location:** `backend/.env`

**Required Keys:**

```bash
# LiveKit Configuration
LIVEKIT_URL=wss://bluejay-97zjii70.livekit.cloud
LIVEKIT_API_KEY=<your-livekit-api-key>
LIVEKIT_API_SECRET=<your-livekit-api-secret>

# OpenAI (GPT-5 and embeddings)
OPENAI_API_KEY=<your-openai-api-key>

# Deepgram STT
DEEPGRAM_API_KEY=<your-deepgram-api-key>

# Fish Audio TTS
FISH_AUDIO_API_KEY=<your-fish-audio-api-key>
FISH_LELOUCH_VOICE_ID=48056d090bfe4d6690ff31725075812f
FISH_MALE_VOICE_ID=802e3bc2b27e49c2995d23ef70e6ac89
FISH_FEMALE_VOICE_ID=b545c585f631496c914815291da4e893

# Pinecone Vector Database
PINECONE_API_KEY=<your-pinecone-api-key>
PINECONE_INDEX_NAME=storyva-voice-acting
```

**Frontend Keys:** (if needed)
- `NEXT_PUBLIC_LIVEKIT_URL` - LiveKit connection from browser

**Note:** All API keys stored in `.env` files (not committed to git). Voice model IDs are public and can be committed.

---

## 4. Component Design

### 4.1 Frontend Components

#### 4.1.1 StoryEditor Component
**File:** `frontend/components/StoryEditor.tsx`

**Responsibilities:**
- Editable textarea for story text
- Display inline diffs from agent suggestions
- Syntax highlighting for emotion tags
- Accept/reject diff actions

**Props:**
```typescript
interface StoryEditorProps {
  initialText: string;
  currentDiff: DiffData | null;
  onTextChange: (text: string) => void;
  onAcceptDiff: () => void;
  onRejectDiff: () => void;
}
```

**State:**
```typescript
const [text, setText] = useState<string>(initialText);
const [showDiff, setShowDiff] = useState<boolean>(false);
```

**Libraries:**
- `react-diff-viewer` for inline diff display
- `react-textarea-autosize` for auto-expanding textarea

#### 4.1.2 LiveTranscript Component
**File:** `frontend/components/LiveTranscript.tsx`

**Responsibilities:**
- Display real-time conversation transcript
- Auto-scroll to latest message
- Differentiate user vs agent speech
- Show interim results (partial transcripts)

**Data Structure:**
```typescript
interface TranscriptMessage {
  id: string;
  speaker: 'user' | 'agent';
  text: string;
  timestamp: Date;
  isFinal: boolean;
}
```

#### 4.1.3 CallControls Component
**File:** `frontend/components/CallControls.tsx`

**Responsibilities:**
- Connect/disconnect from LiveKit room
- Display connection status
- Microphone mute/unmute
- Speaker volume control

**States:**
```typescript
type ConnectionState = 'disconnected' | 'connecting' | 'connected' | 'error';
```

#### 4.1.4 DiffViewer Component
**File:** `frontend/components/DiffViewer.tsx`

**Responsibilities:**
- Render inline diffs with emotion tags highlighted
- Show original vs proposed text
- Provide accept/reject actions

**Implementation:**
```typescript
import ReactDiffViewer from 'react-diff-viewer';

const DiffViewer: React.FC<DiffViewerProps> = ({ originalText, proposedText }) => {
  return (
    <ReactDiffViewer
      oldValue={originalText}
      newValue={proposedText}
      splitView={false}
      useDarkTheme={false}
      showDiffOnly={true}
      leftTitle="Original"
      rightTitle="With Emotion Tags"
    />
  );
};
```

### 4.2 Backend Components

#### 4.2.1 Lelouch Agent Class
**File:** `backend/agent/lelouch.py`

**Responsibilities:**
- Define agent personality and instructions
- Implement tool functions
- Manage conversation state

**Implementation Outline:**
```python
from livekit.agents import Agent, function_tool, RunContext
from dataclasses import dataclass, field

@dataclass
class StoryState:
    current_text: str = ""
    pending_diff: dict | None = None
    conversation_metadata: dict = field(default_factory=dict)

class LelouchAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions="""You are Lelouch, a brilliant strategist turned voice director.

            PERSONALITY:
            - Analytical and precise
            - Concise responses (2-4 sentences)
            - Strategic framing ("This serves the narrative better")
            - Theatrical but commanding
            - Reference techniques briefly

            EMOTION MARKUP RULES:
            - Emotion tags MUST be at sentence start: (sad) "text"
            - Tone markers can go anywhere: "text (whispering) more"
            - Audio effects can go anywhere: "text," (sighing) she said.
            - Combine up to 3 tags maximum

            WORKFLOW:
            1. User describes intent
            2. You analyze story context
            3. Retrieve technique if relevant (use RAG tool)
            4. Suggest specific markup changes
            5. Present diff visually (don't speak tags)
            6. Wait for user approval

            PREVIEW TOOL USAGE:
            - When user asks "how would this sound?", call preview_line_audio
            - Automatically infer character gender from context (pronouns, names, attribution)
            - Example: "she said" → gender="female", "Marcus replied" → gender="male"
            - NEVER ask user for gender - infer it silently

            STYLE:
            - "I see. Given the context, regret serves better than sadness here."
            - "Stanislavski's emotion memory - we apply it by... Observe."
            - "Too vague. Specify the emotion's purpose."
            """,
        )

    @function_tool()
    async def search_acting_technique(
        self,
        context: RunContext[StoryState],
        query: str,
    ) -> str:
        """Search voice acting books for techniques."""
        # RAG retrieval implementation
        pass

    @function_tool()
    async def suggest_emotion_markup(
        self,
        context: RunContext[StoryState],
        line_text: str,
        emotions: list[str],
        explanation: str,
    ) -> dict:
        """Create emotion markup suggestion."""
        # Diff generation implementation
        pass

    @function_tool()
    async def preview_line_audio(
        self,
        context: RunContext[StoryState],
        marked_up_text: str,
        character_gender: str,
    ) -> str:
        """Generate audio preview with Fish Audio using character's voice.

        IMPORTANT: Agent must infer character_gender from story context automatically.
        - Analyze pronouns (he/she/they), character names, dialogue attribution
        - Example: "she said" → "female", "Marcus replied" → "male"
        - Default to "male" if ambiguous

        Args:
            marked_up_text: Text with emotion markup tags
            character_gender: "male" or "female" (MUST be inferred by agent, not asked)
        """
        # Select appropriate character voice (different from agent's voice)
        voice_map = {
            "male": os.getenv("FISH_MALE_VOICE_ID"),      # 802e3bc2b27e49c2995d23ef70e6ac89
            "female": os.getenv("FISH_FEMALE_VOICE_ID"),  # b545c585f631496c914815291da4e893
        }

        character_voice_id = voice_map.get(character_gender, voice_map["male"])

        # Fish Audio HTTP API call with different voice
        # Returns audio file path for frontend to play
        pass
```

#### 4.2.2 Voice Pipeline Setup
**File:** `backend/agent/voice_pipeline.py`

**Responsibilities:**
- Configure STT, LLM, TTS, VAD
- Set up turn detection
- Configure interruption handling

**Implementation:**
```python
from livekit.agents import AgentSession
from livekit.plugins import deepgram, openai, elevenlabs, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

async def create_agent_session(user_data: StoryState) -> AgentSession:
    session = AgentSession[StoryState](
        # Voice Activity Detection
        vad=silero.VAD.load(),

        # Speech-to-Text
        stt=deepgram.STT(
            model="nova-3",
            language="en-US",
            interim_results=True,
            punctuate=True,
            smart_format=True,
            endpointing_ms=300,
        ),

        # Large Language Model
        llm=openai.LLM(
            model="gpt-5",
            temperature=0.7,
        ),

        # Text-to-Speech (Fish Audio custom implementation)
        tts=FishAudioTTS(
            api_key=os.getenv("FISH_AUDIO_API_KEY"),
            reference_id=os.getenv("FISH_LELOUCH_VOICE_ID"),  # Lelouch voice: 48056d090bfe4d6690ff31725075812f
            latency="normal",
            format="opus",
        ),

        # Turn Detection
        turn_detection=MultilingualModel(),

        # Interruption Settings
        allow_interruptions=True,
        min_interruption_duration=0.5,
        false_interruption_timeout=2.0,
        resume_false_interruption=True,

        # User Data
        userdata=user_data,
    )

    return session
```

#### 4.2.3 RAG Indexer
**File:** `backend/rag/indexer.py`

**Responsibilities:**
- Load PDFs from disk
- Chunk documents semantically
- Generate embeddings
- Upload to Pinecone

**Implementation:**
```python
import os
from pathlib import Path
from pinecone import Pinecone, ServerlessSpec
from llama_index.core import SimpleDirectoryReader, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core import VectorStoreIndex

def index_voice_acting_books():
    """One-time indexing of PDF books into Pinecone."""

    # Initialize Pinecone
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index_name = "voice-acting-knowledge"

    # Create index if doesn't exist
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )

    pinecone_index = pc.Index(index_name)

    # Configure LlamaIndex
    embed_model = OpenAIEmbedding(model="text-embedding-3-small")
    Settings.embed_model = embed_model
    Settings.chunk_size = 512
    Settings.chunk_overlap = 50

    # Load PDFs
    pdf_dir = Path(__file__).parent.parent / "data" / "pdfs"
    documents = SimpleDirectoryReader(
        input_dir=str(pdf_dir),
        required_exts=[".pdf"]
    ).load_data()

    # Add metadata
    for doc in documents:
        if "Stanislavski" in doc.metadata.get('file_name', ''):
            doc.metadata.update({
                'author': 'Constantin Stanislavski',
                'title': 'An Actor Prepares',
                'year': 1936
            })
        elif "Linklater" in doc.metadata.get('file_name', ''):
            doc.metadata.update({
                'author': 'Kristin Linklater',
                'title': 'Freeing the Natural Voice',
                'year': 2006
            })

    # Index documents
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
    vector_index = VectorStoreIndex.from_documents(
        documents,
        vector_store=vector_store,
        show_progress=True
    )

    print(f"Indexed {len(documents)} documents successfully!")
    return vector_index
```

#### 4.2.4 RAG Query Engine
**File:** `backend/rag/retriever.py`

**Responsibilities:**
- Connect to Pinecone at runtime
- Execute semantic search queries
- Return formatted results for LLM

**Implementation:**
```python
import os
from pinecone import Pinecone
from llama_index.core import VectorStoreIndex, Settings
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.pinecone import PineconeVectorStore

class VoiceActingRetriever:
    def __init__(self):
        # Initialize Pinecone
        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        pinecone_index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))

        # Configure embeddings
        embed_model = OpenAIEmbedding(model="text-embedding-3-small")
        Settings.embed_model = embed_model

        # Create vector store and query engine
        vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
        self.vector_index = VectorStoreIndex.from_vector_store(vector_store)
        self.query_engine = self.vector_index.as_query_engine(
            similarity_top_k=5,
            verbose=False
        )

    async def search(self, query: str) -> str:
        """Search for voice acting techniques."""
        response = self.query_engine.query(query)

        # Format response with sources
        sources = [
            f"- {node.metadata.get('title', 'Unknown')} (p.{node.metadata.get('page', '?')})"
            for node in response.source_nodes
        ]

        result = f"{response.response}\n\nSources:\n" + "\n".join(sources)
        return result
```

#### 4.2.5 Fish Audio Preview Tool
**File:** `backend/tools/fish_audio_preview.py`

**Responsibilities:**
- Call Fish Audio HTTP API
- Generate single-line audio preview with character voice
- Support male/female/neutral character voices
- Return audio file path or stream

**Implementation:**
```python
import os
import aiohttp
from pathlib import Path

class FishAudioPreview:
    def __init__(self):
        self.api_key = os.getenv("FISH_AUDIO_API_KEY")
        self.base_url = "https://api.fish.audio/v1/tts"

        # Character voice IDs (different from agent's Lelouch voice)
        self.voice_ids = {
            "male": os.getenv("FISH_MALE_VOICE_ID"),      # 802e3bc2b27e49c2995d23ef70e6ac89
            "female": os.getenv("FISH_FEMALE_VOICE_ID"),  # b545c585f631496c914815291da4e893
            "neutral": os.getenv("FISH_MALE_VOICE_ID"),   # Default
        }

    async def generate_preview(
        self,
        text: str,
        character_gender: str = "neutral",
    ) -> Path:
        """Generate audio preview with Fish Audio using character voice."""

        # Select character voice (different from agent)
        reference_id = self.voice_ids.get(character_gender, self.voice_ids["neutral"])

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "text": text,
            "reference_id": reference_id,
            "format": "mp3",
            "latency": "balanced",
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.base_url,
                headers=headers,
                json=payload
            ) as response:
                if response.status == 200:
                    # Save audio to temp file
                    output_path = Path("/tmp") / f"preview_{hash(text)}.mp3"
                    with open(output_path, "wb") as f:
                        f.write(await response.read())
                    return output_path
                else:
                    raise Exception(f"Fish Audio API error: {response.status}")
```

#### 4.2.6 Custom Fish Audio TTS for LiveKit
**File:** `backend/tts/fish_audio.py`

**Responsibilities:**
- Implement LiveKit TTS interface for Fish Audio
- WebSocket streaming connection
- Real-time audio synthesis with emotion tags
- Audio frame conversion for LiveKit

**Implementation:**
```python
import os
import asyncio
import aiohttp
import ormsgpack
from typing import Optional
from livekit import rtc
from livekit.agents import tts
from livekit.agents.tts import (
    TTS,
    TTSCapabilities,
    SynthesizeStream,
)

class FishAudioTTS(tts.TTS):
    """Custom TTS implementation for Fish Audio with LiveKit."""

    def __init__(
        self,
        *,
        api_key: str,
        reference_id: str,  # Voice model ID
        model: str = "speech-1.6",
        latency: str = "normal",
        format: str = "opus",
        sample_rate: int = 24000,
        num_channels: int = 1,
    ):
        super().__init__(
            capabilities=TTSCapabilities(streaming=True),
            sample_rate=sample_rate,
            num_channels=num_channels,
        )
        self._api_key = api_key
        self._reference_id = reference_id
        self._model = model
        self._latency = latency
        self._format = format

    def synthesize(self, text: str) -> "FishAudioChunkedStream":
        """Synthesize complete text (HTTP endpoint for non-streaming)."""
        return FishAudioChunkedStream(
            tts=self,
            input_text=text,
        )

    def stream(self) -> "FishAudioSynthesizeStream":
        """Create streaming synthesis session (WebSocket)."""
        return FishAudioSynthesizeStream(tts=self)


class FishAudioSynthesizeStream(SynthesizeStream):
    """Streaming TTS using Fish Audio WebSocket API."""

    def __init__(self, tts: FishAudioTTS):
        super().__init__(tts=tts)
        self._tts = tts
        self._ws = None
        self._receive_task = None

    async def _connect(self):
        """Establish WebSocket connection to Fish Audio."""
        import websockets

        uri = "wss://api.fish.audio/v1/tts/live"
        headers = {"Authorization": f"Bearer {self._tts._api_key}"}

        self._ws = await websockets.connect(uri, extra_headers=headers)

        # Send initial configuration
        await self._ws.send(
            ormsgpack.packb({
                "event": "start",
                "request": {
                    "text": "",
                    "reference_id": self._tts._reference_id,
                    "latency": self._tts._latency,
                    "format": self._tts._format,
                },
            })
        )

    async def _push_text_impl(self, token: str):
        """Send text chunk to Fish Audio for synthesis."""
        if not self._ws:
            await self._connect()
            # Start receive task
            self._receive_task = asyncio.create_task(self._receive_audio())

        await self._ws.send(
            ormsgpack.packb({
                "event": "text",
                "text": token,
            })
        )

    async def _flush_impl(self):
        """Signal end of text segment."""
        if self._ws:
            await self._ws.send(
                ormsgpack.packb({
                    "event": "flush",
                })
            )

    async def _receive_audio(self):
        """Receive and emit audio frames from Fish Audio."""
        try:
            async for message in self._ws:
                data = ormsgpack.unpackb(message)

                if data.get("event") == "audio":
                    # Convert audio data to AudioFrame
                    audio_bytes = data["audio"]

                    # Create audio frame for LiveKit
                    frame = rtc.AudioFrame(
                        data=audio_bytes,
                        sample_rate=self._tts.sample_rate,
                        num_channels=self._tts.num_channels,
                        samples_per_channel=len(audio_bytes) // 2,
                    )

                    # Emit frame to LiveKit
                    self._event_ch.send_nowait(
                        tts.SynthesizedAudio(
                            frame=frame,
                            request_id=self._request_id,
                        )
                    )

                elif data.get("event") == "finish":
                    # Mark stream as complete
                    self._event_ch.send_nowait(
                        tts.SynthesizedAudio(
                            frame=None,
                            request_id=self._request_id,
                            is_final=True,
                        )
                    )
                    break

        except Exception as e:
            print(f"Error receiving audio: {e}")
        finally:
            if self._ws:
                await self._ws.close()

    async def aclose(self):
        """Clean up WebSocket connection."""
        if self._receive_task:
            self._receive_task.cancel()
        if self._ws:
            await self._ws.close()


class FishAudioChunkedStream:
    """Non-streaming synthesis using HTTP API."""

    def __init__(self, tts: FishAudioTTS, input_text: str):
        self._tts = tts
        self._input_text = input_text

    async def __anext__(self):
        """Generate complete audio using HTTP endpoint."""
        # Use HTTP API for batch synthesis
        # (Implementation similar to FishAudioPreview)
        raise StopAsyncIteration
```

**Usage in Voice Pipeline:**
```python
from tts.fish_audio import FishAudioTTS

tts = FishAudioTTS(
    api_key=os.getenv("FISH_AUDIO_API_KEY"),
    reference_id=os.getenv("FISH_LELOUCH_VOICE_ID"),  # 48056d090bfe4d6690ff31725075812f
    latency="normal",
    format="opus",
)
```

#### 4.2.7 Main Entry Point
**File:** `backend/main.py`

**Responsibilities:**
- Initialize LiveKit agent worker
- Connect to LiveKit Cloud
- Handle room join events
- Start agent session

**Implementation:**
```python
import os
import logging
from dotenv import load_dotenv
from livekit import agents
from livekit.agents import JobContext, WorkerOptions, cli

from agent.lelouch import LelouchAgent, StoryState
from agent.voice_pipeline import create_agent_session
from rag.retriever import VoiceActingRetriever

load_dotenv()
logger = logging.getLogger("voice-director-agent")
logger.setLevel(logging.INFO)

# Global RAG retriever (initialized once)
rag_retriever: VoiceActingRetriever | None = None

async def prewarm(proc: agents.JobProcess):
    """Preload heavy resources once per worker."""
    global rag_retriever
    logger.info("Prewarming agent...")

    # Initialize RAG system
    rag_retriever = VoiceActingRetriever()

    logger.info("Prewarm complete")

async def entrypoint(ctx: JobContext):
    """Main entry point for each room connection."""
    logger.info(f"Agent joining room: {ctx.room.name}")

    # Connect to LiveKit room
    await ctx.connect()

    # Initialize story state
    story_state = StoryState()

    # Create agent session
    session = await create_agent_session(story_state)

    # Inject RAG retriever into agent context
    agent = LelouchAgent()
    agent.rag_retriever = rag_retriever

    # Start session
    await session.start(
        room=ctx.room,
        agent=agent,
    )

    # Generate greeting
    await session.generate_reply(
        instructions="Greet the user as Lelouch. Be commanding yet welcoming."
    )

    logger.info("Agent session started successfully")

if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            prewarm_fnc=prewarm,
        )
    )
```

---

## 5. Data Flow

### 5.1 User Story Editing Flow

```
1. User pastes story text → Frontend StoryEditor
2. Text stored in React state
3. User clicks "Start Call" → LiveKit room created
4. Agent joins room → Backend session initialized
5. Agent reads current story text from context

User: "Make the breakup scene more emotional"
6. User speech → STT (Deepgram) → Text transcript
7. LLM (GPT-5) processes request with Lelouch personality
8. Agent tool call: search_acting_technique("emotional breakup scenes")
9. RAG query → Pinecone → Relevant chunks returned
10. LLM synthesizes technique with specific markup suggestion
11. Agent tool call: suggest_emotion_markup(line, emotions, explanation)
12. Diff generated: (sad)(whispering) "I can't do this anymore," (sighing) she said.
13. Diff sent to frontend via WebSocket/data channel
14. Frontend displays inline diff
15. Agent speaks: "Stanislavski's emotion memory—regret for how it ends. Soft tone, restrained. Observe."
16. User sees diff on screen (agent doesn't speak the tags)

User: "How would that sound?"
17. Agent analyzes story context: "she said" → infers female
18. Agent tool call: preview_line_audio(marked_up_text, character_gender="female")
19. Fish Audio HTTP API called with emotion tags + female voice
19. Audio file generated, sent to frontend
20. Frontend plays audio preview

User: "Perfect, apply it"
21. Frontend sends acceptance → Backend
22. Diff applied to story text
23. State updated
24. Agent: "Applied. The subtlety serves the moment better."
```

### 5.2 RAG Retrieval Flow

```
User Query → LLM determines need for technique retrieval
      ↓
Agent calls search_acting_technique(query)
      ↓
Query string → OpenAI embedding (text-embedding-3-small)
      ↓
Embedding vector → Pinecone similarity search
      ↓
Top 5 chunks retrieved with metadata
      ↓
LlamaIndex formats results with book citations
      ↓
Formatted text returned to LLM
      ↓
LLM synthesizes into conversational response
      ↓
Agent speaks: "Stanislavski talks about..."
```

### 5.3 Session State Management

**Session State Schema:**
```python
@dataclass
class StoryState:
    current_text: str = ""
    pending_diff: dict | None = None
    applied_diffs: list[dict] = field(default_factory=list)
    conversation_metadata: dict = field(default_factory=dict)
```

**State Synchronization:**
- Frontend maintains authoritative story text
- Backend receives text via context/metadata on agent join
- Agent reads `context.userdata.current_text` before suggestions
- Diffs sent from backend → frontend for display
- Accepted diffs sent from frontend → backend for confirmation

---

## 6. API Integration Specifications

### 6.1 LiveKit Room Creation (Frontend)

```typescript
import { Room, RoomEvent } from 'livekit-client';

async function connectToRoom(roomName: string, token: string) {
  const room = new Room({
    adaptiveStream: true,
    dynacast: true,
  });

  await room.connect(process.env.NEXT_PUBLIC_LIVEKIT_URL!, token);

  room.on(RoomEvent.DataReceived, (payload, participant) => {
    const data = JSON.parse(new TextDecoder().decode(payload));
    if (data.type === 'diff') {
      handleDiffReceived(data.diff);
    }
  });

  return room;
}
```

### 6.2 Fish Audio HTTP API

**Endpoint:** `POST https://api.fish.audio/v1/tts`

**Headers:**
```
Authorization: Bearer b2a92433589f4c8f9893a33003132ab4
Content-Type: application/json
```

**Request Body:**
```json
{
  "text": "(sad)(soft tone) I can't do this anymore, (sighing) she said.",
  "format": "mp3",
  "latency": "balanced",
  "reference_id": "optional_voice_model_id"
}
```

**Response:** Binary audio file (mp3)

### 6.3 Pinecone Vector Search

**Query Flow:**
```python
# Handled automatically by LlamaIndex
query_engine.query("How to convey sadness vocally?")

# Behind the scenes:
# 1. Text → OpenAI embedding
# 2. Pinecone similarity search
# 3. Top-k chunks retrieved
# 4. LLM synthesis
```

**Index Configuration:**
```python
{
  "name": "voice-acting-knowledge",
  "dimension": 1536,
  "metric": "cosine",
  "cloud": "aws",
  "region": "us-east-1"
}
```

### 6.4 OpenAI GPT-5 API

**Chat Completions:**
```python
from openai import OpenAI

client = OpenAI()
response = client.chat.completions.create(
    model="gpt-5",
    messages=[
        {"role": "system", "content": lelouch_instructions},
        {"role": "user", "content": user_query}
    ],
    tools=[search_technique, suggest_markup, preview_audio],
    stream=True
)
```

### 6.5 Deepgram STT WebSocket

**Handled by LiveKit plugin:**
```python
stt=deepgram.STT(
    model="nova-3",
    language="en-US",
    interim_results=True,
    punctuate=True,
    smart_format=True,
)
```

**Streams audio → text in real-time**

---

## 7. Development Plan

### 7.1 Phase 1: Foundation

**Goal:** Repository setup, basic infrastructure

**Tasks:**
- [x] Flatten git repo (remove submodules, commit frontend/backend directly)
- [x] Initialize Next.js 14 frontend with TypeScript, Tailwind CSS, ESLint
- [x] Set up Python backend with uv + pyproject.toml
- [x] Install backend dependencies (LiveKit, LlamaIndex, Pinecone, Fish Audio)
- [x] Install frontend dependencies (Next.js, React, Tailwind)
- [x] Create Pinecone index (`storyva-voice-acting`)
- [x] Configure environment variables in `backend/.env`
- [ ] Create unified `.gitignore` (merge existing)
- [ ] Set up environment variable templates (`.env.example`)
- [ ] Create basic folder structure in backend (`agent/`, `rag/`, `tts/`, `tools/`)
- [ ] Set up dev scripts (`npm run dev`, `python main.py start`)

**Deliverable:** Clean single repository, both frontend and backend runnable

**Status:** ~70% Complete (infrastructure done, need folder structure & dev scripts)

---

### 7.2 Phase 2: Backend Core

**Goal:** Working LiveKit agent with basic voice pipeline

**Tasks:**
- [ ] Implement `main.py` entry point
- [ ] Create LiveKit agent session with STT/LLM/TTS pipeline
- [ ] Implement Lelouch agent class with personality prompt
- [ ] Test agent in LiveKit playground (no frontend yet)
- [ ] Verify Deepgram STT works
- [ ] Implement custom Fish Audio TTS (WebSocket streaming)
- [ ] Verify Fish Audio TTS works with emotion tags
- [ ] Implement basic tool: `echo_text` (test tool calling)
- [ ] Test conversation flow in console mode

**Deliverable:** Voice agent responds conversationally with Lelouch personality

---

### 7.3 Phase 3: RAG System

**Goal:** Pinecone indexing and retrieval working

**Tasks:**
- [x] Move PDF files to `backend/data/pdfs/` (already present)
- [x] Create Pinecone index `storyva-voice-acting` (already created)
- [ ] Implement `backend/rag/indexer.py`
- [ ] Run one-time indexing script (`python scripts/index_pdfs.py`)
- [ ] Verify Pinecone index populated (check dashboard)
- [ ] Implement `backend/rag/retriever.py`
- [ ] Test retrieval with sample queries
- [ ] Integrate RAG into agent as `search_acting_technique` tool
- [ ] Test agent retrieving relevant techniques during conversation

**Deliverable:** Agent can cite Stanislavski and Linklater accurately

---

### 7.4 Phase 4: Emotion Markup Tools

**Goal:** Diff generation and Fish Audio preview

**Tasks:**
- [ ] Implement `backend/tools/emotion_validator.py`
  - Load `emotion_control.md` spec
  - Validate tag placement rules
  - Return errors if invalid
- [ ] Implement `backend/tools/diff_generator.py`
  - Take original text, suggested text
  - Generate unified diff format
  - Return structured diff object
- [ ] Implement `suggest_emotion_markup` tool in agent
- [ ] Test diff generation with sample text
- [ ] Implement `backend/tools/fish_audio_preview.py`
- [ ] Test Fish Audio API with emotion tags
- [ ] Implement `preview_line_audio` tool in agent
- [ ] Test end-to-end: suggest → preview → audio

**Deliverable:** Agent can suggest markup and generate audio previews

---

### 7.5 Phase 5: Frontend UI

**Goal:** Complete user interface with all components

**Tasks:**
- [ ] Create `app/director/page.tsx` main UI
- [ ] Implement `StoryEditor.tsx` component
  - Editable textarea
  - Character counter
  - Save state to localStorage
- [ ] Implement `CallControls.tsx` component
  - Connect to LiveKit room
  - Start/end call buttons
  - Connection status indicator
- [ ] Implement `LiveTranscript.tsx` component
  - Display messages from LiveKit
  - Auto-scroll
  - User/agent differentiation
- [ ] Implement `DiffViewer.tsx` component
  - Use react-diff-viewer library
  - Inline mode
  - Highlight emotion tags in green
- [ ] Connect frontend to LiveKit (obtain room tokens)
- [ ] Test full flow: paste text → call → conversation → diff display

**Deliverable:** Functional UI for complete user journey

---

### 7.6 Phase 6: Integration & Testing

**Goal:** End-to-end system working smoothly

**Tasks:**
- [ ] Test complete user flow (see PRD Section 4.1)
- [ ] Test RAG retrieval accuracy (10 sample queries)
- [ ] Test emotion markup validation (correct/incorrect tags)
- [ ] Test Fish Audio preview generation
- [ ] Test diff accept/reject workflow
- [ ] Performance testing (measure latency)
- [ ] Error handling (API failures, network issues)
- [ ] Polish Lelouch personality (adjust prompt if needed)

**Deliverable:** Production-ready application

---

### 7.7 Phase 7: Documentation & Deployment

**Goal:** Production-ready deployment and documentation

**Tasks:**
- [ ] Write README.md with setup instructions
- [ ] Create DEPLOYMENT.md guide
- [ ] Run frontend locally in production mode
- [ ] Run backend locally (test complete flow)
- [ ] Create `.env.example` files
- [ ] Write troubleshooting guide
- [ ] (Stretch goal) Deploy to AWS if time permits

**Deliverable:** Production-ready application with complete documentation

---

## 8. Deployment Strategy

### 8.1 Local Deployment (Primary Goal)

**Frontend:**
```bash
cd frontend
npm install
npm run build
npm run start  # Production mode on localhost:3000
```

**Backend:**
```bash
cd backend
uv sync
source .venv/bin/activate
python main.py start
```

**LiveKit:** Cloud-hosted (no deployment needed)

---

### 8.2 Cloud Deployment (Stretch Goal - Not Required)

**Note:** Cloud deployment is optional and not necessary for the primary application goals. Focus on local deployment first.

**Frontend:** Can be deployed to any Node.js hosting (Vercel, Netlify, AWS Amplify)

**Backend → AWS EC2:**

**Option A: Simple EC2 Instance**
```bash
# Launch Ubuntu instance
# SSH and install dependencies
sudo apt update
sudo apt install python3.10 python3-pip
pip install uv
git clone https://github.com/yourusername/storyVA.git
cd storyVA/backend
uv sync
# Set environment variables
export OPENAI_API_KEY=...
export DEEPGRAM_API_KEY=...
# etc.

# Run with systemd for persistence
sudo systemctl enable voice-agent
sudo systemctl start voice-agent
```

**Option B: AWS App Runner (Easier)**
- Push Docker image to ECR
- Create App Runner service
- Set environment variables in console
- Auto-scaling included

**Dockerfile:**
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy project files
COPY backend/pyproject.toml backend/uv.lock ./
RUN uv sync

COPY backend/ ./

# Run agent
CMD ["uv", "run", "python", "main.py", "start"]
```

---

## 9. Testing Strategy

### 9.1 Unit Tests

**Backend:**
```python
# tests/test_emotion_validator.py
def test_valid_emotion_tags():
    assert validate_tag("(sad)") == True
    assert validate_tag("(invalid)") == False

def test_tag_placement():
    # Emotion at start: valid
    assert validate_placement("(sad) I'm leaving.") == True
    # Emotion mid-sentence: invalid
    assert validate_placement("I'm (sad) leaving.") == False
```

**Frontend:**
```typescript
// __tests__/DiffViewer.test.tsx
test('displays inline diff correctly', () => {
  const { getByText } = render(
    <DiffViewer
      originalText="Hello"
      proposedText="(happy) Hello"
    />
  );
  expect(getByText('(happy) Hello')).toBeInTheDocument();
});
```

### 9.2 Integration Tests

**RAG System:**
```python
async def test_rag_retrieval():
    retriever = VoiceActingRetriever()
    result = await retriever.search("Stanislavski emotion memory")
    assert "emotion memory" in result.lower()
    assert "Stanislavski" in result
```

**Fish Audio API:**
```python
async def test_fish_audio_preview():
    preview = FishAudioPreview()
    audio_path = await preview.generate_preview("(happy) Test")
    assert audio_path.exists()
    assert audio_path.suffix == ".mp3"
```

### 9.3 End-to-End Test Script

**Test Scenario:**
1. User pastes story: "I hate you," she said.
2. User starts call
3. User: "Make this sadder"
4. Agent retrieves technique
5. Agent suggests: `(sad)(soft tone) "I hate you," (sighing) she said.`
6. User: "How does that sound?"
7. Agent generates Fish Audio preview
8. User: "Perfect, apply it"
9. Text updated with markup

**Verification:**
- [ ] Agent responds within 5 seconds
- [ ] RAG retrieves relevant technique
- [ ] Diff displayed correctly
- [ ] Fish Audio generates valid audio
- [ ] Text updates after acceptance

---

## 10. Risk Analysis

### 10.1 High Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Fish Audio API unreliable** | Tool call fails, poor demo | Fallback to text-only responses, test API thoroughly |
| **LiveKit free tier limits** | Can't complete demo | Monitor usage, upgrade if needed ($50) |
| **RAG retrieval poor quality** | Agent gives wrong techniques | Manual testing with 20+ queries, adjust chunking |
| **Latency too high (>5s)** | Poor user experience | Optimize chunk sizes, reduce reasoning effort |

### 10.2 Medium Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Emotion tag validation bugs** | Invalid markup applied | Extensive unit tests, reference emotion_control.md |
| **PDF indexing fails** | No RAG functionality | Test indexing early, verify in Pinecone dashboard |

### 10.3 Low Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| **TypeScript compilation errors** | Build failures | Use strict mode from start, test builds regularly |

---

## 11. Open Questions & Decisions

### 11.1 Resolved Questions

✅ **Single repo or submodules?** → Single repo (per GUIDELINES.md)
✅ **Next.js or vanilla React?** → Next.js (React-based, meets requirements)
✅ **Deployment strategy?** → Local first, AWS is stretch goal only
✅ **Fish Audio for agent voice?** → Yes, custom TTS implementation with WebSocket streaming
✅ **LLM provider?** → GPT-5 (latest, user confirmed availability)
✅ **RAG framework?** → LlamaIndex (simpler, purpose-built for RAG)
✅ **Diff display?** → react-diff-viewer (inline mode)

### 11.2 Remaining Decisions

**To be decided during implementation:**

1. ✅ **Character preview voice selection** - RESOLVED
   - Lelouch (agent) voice: `48056d090bfe4d6690ff31725075812f`
   - Male/ambiguous character voice: `802e3bc2b27e49c2995d23ef70e6ac89`
   - Female character voice: `b545c585f631496c914815291da4e893`
   - Agent automatically infers gender from story context (pronouns, character names, dialogue attribution)

2. **Chunk size optimization** - 512 or 1024 tokens?
   - Test both with sample queries
   - Measure retrieval quality

3. **Diff accept/reject persistence** - Store history or just current diff?
   - MVP: Just current diff
   - Future: History for undo

4. **Error handling strategy** - Retry logic for API failures?
   - GPT-5: Retry 3x with exponential backoff
   - Fish Audio: Fallback to text-only response
   - Pinecone: Return "no technique found" gracefully

---

## 12. Success Metrics

### 12.1 Technical Metrics

- ✅ Agent response latency < 5 seconds (median)
- ✅ RAG retrieval accuracy > 80% (relevant techniques)
- ✅ Emotion tag validation accuracy = 100%
- ✅ Fish Audio preview success rate > 95%
- ✅ Frontend load time < 2 seconds

### 12.2 Functional Requirements

- ✅ All GUIDELINES.md requirements met
- ✅ Agent maintains Lelouch personality
- ✅ Inline diffs display correctly
- ✅ User can accept/reject diffs
- ✅ Audio previews work with emotion tags
- ✅ Live transcript displays in real-time

---

## 13. Next Steps

**Completed:**
1. ✅ TDD approved
2. ✅ Repository flattened (single repo, no submodules)
3. ✅ Fresh Next.js 14 frontend initialized
4. ✅ Backend dependencies installed (uv, LiveKit, LlamaIndex, Pinecone)
5. ✅ Pinecone index created (`storyva-voice-acting`)
6. ✅ Environment variables configured

**Immediate Actions:**
1. [ ] Complete Phase 1 (folder structure, `.env.example`, dev scripts)
2. [ ] Begin Phase 2: Backend Core (LiveKit agent, voice pipeline)
3. [ ] Implement custom Fish Audio TTS integration
4. [ ] Implement RAG indexing and retrieval

**First Milestone:** Working LiveKit agent with Lelouch personality (Phase 2 complete)

**Current Status:** Phase 1 ~70% complete, ready to continue implementation

---

**Document Status:** ✅ Ready for Implementation
**Last Updated:** October 22, 2025
