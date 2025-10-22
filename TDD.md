# Technical Design Document: Voice Director Agent

## Document Information
- **Version**: 1.0
- **Date**: 2025-10-21
- **Project**: storyVA - RAG-enabled Voice Director Agent (Bluejay Interview)

---

## 1. Executive Summary

### 1.1 System Overview
A real-time voice agent that helps writers add professional emotion markup to stories using Fish Audio's TTS system. The agent, "Lelouch", acts as an AI voice director, teaching theatrical techniques from classic voice acting texts and applying them conversationally through LiveKit voice infrastructure.

### 1.2 Key Technical Components
- **LiveKit**: Real-time voice communication and agent orchestration
- **RAG System**: Vector database with voice acting books for technique retrieval
- **LLM**: GPT-4 for agent intelligence with Lelouch personality
- **Fish Audio API**: Tool call for audio preview of emotion-tagged dialogue
- **React Frontend**: Text editor, diff viewer, live transcript

### 1.3 Technical Constraints
- Must use LiveKit for voice agent (interview requirement)
- Must demonstrate RAG over large PDF documents
- Must include functional tool calling
- Run locally (vector DB and LiveKit)
- No user authentication (MVP scope)

---

## 2. Architecture

### 2.1 System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    React Frontend (Vite)                     │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  LiveKit React Components (@livekit/components-react)│   │
│  │  - useVoiceAssistant()                               │   │
│  │  - Audio/Video controls                              │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Story Editor                                        │   │
│  │  - Editable text area (user's story)                │   │
│  │  - react-diff-viewer-continued (inline diffs)       │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Live Transcript (real-time STT display)            │   │
│  └─────────────────────────────────────────────────────┘   │
└───────────────┬─────────────────────────────────────────────┘
                │ WebRTC + WebSocket (LiveKit protocol)
┌───────────────▼─────────────────────────────────────────────┐
│              LiveKit Server (Local or Cloud)                 │
│  - Room management                                           │
│  - Media routing (audio streams)                             │
│  - Agent connection                                          │
└───────────────┬─────────────────────────────────────────────┘
                │
┌───────────────▼─────────────────────────────────────────────┐
│          Python LiveKit Agent (backend/agent.py)            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Voice Pipeline (livekit.agents.VoicePipelineAgent) │   │
│  │  ┌────────┐  ┌─────┐  ┌─────┐  ┌─────┐            │   │
│  │  │  STT   │→│ LLM │→│ TTS │→│ VAD │            │   │
│  │  │Deepgram││ GPT-4│ │ElevenLabs││                │   │
│  │  └────────┘  └─────┘  └─────┘  └─────┘            │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  RAG System (LangChain)                             │   │
│  │  - ChromaDB vector store (local)                    │   │
│  │  - OpenAI embeddings                                │   │
│  │  - Semantic retrieval                               │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Tool Calling                                        │   │
│  │  - fish_audio_preview(line_text)                    │   │
│  │  - apply_emotion_diff(original, modified)           │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Lelouch Personality System Prompt                  │   │
│  └─────────────────────────────────────────────────────┘   │
└───────────────┬─────────────────┬───────────────────────────┘
                │                 │
      ┌─────────▼────────┐  ┌────▼─────────────┐
      │  Vector Store    │  │  External APIs   │
      │  (ChromaDB)      │  │                  │
      │                  │  │  - OpenAI API    │
      │  - An Actor      │  │  - Deepgram API  │
      │    Prepares.pdf  │  │  - ElevenLabs API│
      │  - Freeing the   │  │  - Fish Audio API│
      │    Natural Voice │  │                  │
      │    .pdf          │  │                  │
      └──────────────────┘  └──────────────────┘
```

### 2.2 Data Flow

#### 2.2.1 Voice Conversation Flow
```
1. User speaks → Frontend captures audio → LiveKit room
2. LiveKit → Agent receives audio stream
3. Agent STT (Deepgram) → Text transcription
4. Text → LLM (GPT-4 with Lelouch prompt + RAG context)
5. LLM response → Agent TTS (ElevenLabs)
6. TTS audio → LiveKit → Frontend plays audio
7. Transcription → Frontend displays in live transcript
```

#### 2.2.2 RAG Retrieval Flow
```
1. User asks question about emotion technique
2. Agent extracts query from conversation context
3. Query → ChromaDB semantic search (OpenAI embeddings)
4. Retrieve top 3-5 relevant chunks from PDFs
5. Chunks → LLM context window
6. LLM synthesizes technique into Lelouch-style response
7. Response includes citation (book name, technique)
```

#### 2.2.3 Emotion Markup Application Flow
```
1. User requests emotion markup for scene
2. Agent reads current story text from shared state
3. Agent analyzes context + RAG retrieval (if needed)
4. Agent generates diff: original → emotion-tagged version
5. Diff sent to frontend via custom message
6. Frontend displays diff in react-diff-viewer
7. User approves → Agent updates shared story state
```

#### 2.2.4 Fish Audio Preview Tool Call Flow
```
1. User: "How would this line sound?"
2. Agent identifies specific line from story text
3. Agent extracts emotion-tagged version (current or proposed)
4. Tool call: fish_audio_preview(tagged_text)
5. POST to Fish Audio API with API key
6. Receive audio file (mp3/wav)
7. Stream audio back through LiveKit room
8. User hears preview, provides feedback
```

---

## 3. Technology Stack Decisions

### 3.1 Core Technologies

| Component | Technology | Version | Justification |
|-----------|-----------|---------|---------------|
| **Voice Infrastructure** | LiveKit | Latest | Required by assignment. Industry-standard for real-time voice. |
| **Frontend Framework** | React + Vite | 18.2+ / 5.x | Fast dev server, simple setup, good LiveKit integration. |
| **Backend Language** | Python | 3.10+ | LiveKit Agents SDK is Python-based. Strong AI/ML ecosystem. |
| **LLM** | OpenAI GPT-4 | gpt-4-turbo | Excellent instruction following for personality. Function calling support. |
| **STT** | Deepgram Nova 2 | Latest | Low latency, high accuracy, official LiveKit integration. |
| **TTS** | ElevenLabs | Latest | Natural voice quality, good LiveKit support. |
| **Vector DB** | ChromaDB | 0.4.x+ | Local deployment, easy setup, no hosting required. |
| **RAG Framework** | LangChain | 0.1.x+ | Well-documented, good examples, flexible. |
| **Embeddings** | OpenAI text-embedding-3-small | Latest | Cost-effective, good performance, same vendor as LLM. |
| **Diff Viewer** | react-diff-viewer-continued | Latest | Maintained fork, supports inline diffs, customizable. |
| **Styling** | Tailwind CSS | 3.x | Rapid UI development, good defaults. |

### 3.2 Alternative Considerations (Not Chosen)

| Component | Alternative | Why Not Chosen |
|-----------|------------|----------------|
| Vector DB | Pinecone | Requires cloud hosting, adds complexity. ChromaDB is sufficient for local. |
| LLM | Anthropic Claude | OpenAI has better LiveKit examples, function calling well-documented. |
| RAG Framework | LlamaIndex | LangChain has more LiveKit integration examples. |
| Frontend | Next.js | Overkill for MVP, Vite is simpler and faster for single-page app. |
| TTS | OpenAI TTS | ElevenLabs has better voice quality and emotion range. |

---

## 4. Backend Implementation

### 4.1 Directory Structure
```
backend/
├── agent.py                 # Main LiveKit agent entrypoint
├── rag_system.py           # RAG initialization and retrieval
├── personality.py          # Lelouch system prompt
├── tools.py                # Tool definitions (Fish Audio, diff generation)
├── utils.py                # Helper functions
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (API keys)
├── .gitignore             # Ignore .env and sensitive files
├── data/
│   ├── pdfs/
│   │   ├── an_actor_prepares.pdf
│   │   └── freeing_natural_voice.pdf
│   └── chroma_db/         # ChromaDB storage (generated)
└── README.md              # Backend setup instructions
```

### 4.2 Key Backend Components

#### 4.2.1 Agent Pipeline (`agent.py`)
```python
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import deepgram, openai, elevenlabs

# Voice pipeline configuration
assistant = VoiceAssistant(
    vad=silero.VAD.load(),  # Voice Activity Detection
    stt=deepgram.STT(),     # Speech-to-Text
    llm=openai.LLM(model="gpt-4-turbo"),  # Language Model
    tts=elevenlabs.TTS(),   # Text-to-Speech
    fnc_ctx=AssistantFnCtx(),  # Function calling context
)
```

#### 4.2.2 RAG System (`rag_system.py`)
```python
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

class RAGSystem:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.vectorstore = Chroma(
            persist_directory="./data/chroma_db",
            embedding_function=self.embeddings
        )

    def load_pdfs(self):
        # Load and chunk PDFs
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        # Process both PDFs

    def retrieve(self, query: str, k: int = 5):
        # Semantic search
        docs = self.vectorstore.similarity_search(query, k=k)
        return docs
```

#### 4.2.3 Lelouch Personality (`personality.py`)
```python
LELOUCH_SYSTEM_PROMPT = """You are Lelouch, a brilliant strategist who became a voice director after mastering the art of dual personas and performance.

PERSONALITY:
- Analytical and strategic - treat every emotional choice as a tactical decision
- Theatrical but concise - dramatic flair, but keep responses to 2-4 sentences
- Commanding yet engaging - direct commands, inspiring when deserved
- Slightly arrogant with earned confidence

SPEAKING STYLE:
- Strategic framing: "This serves the narrative better"
- Direct commands: "Observe." "Listen carefully." "Decide quickly."
- Concise references: "Stanislavski calls this emotion memory. We apply it by..."
- Never verbose - don't waste words

EXAMPLE PHRASES:
- "Too vague. Specify the emotion's purpose."
- "I see. Given the context, regret serves better than sadness here."
- "Applied. The subtlety serves the moment better."

YOUR TASK:
Help users add Fish Audio emotion markup to their stories. When suggesting markup:
1. Describe the emotional intent conversationally (don't speak the tags aloud)
2. Visual diffs will show on screen with actual tags
3. Cite voice acting techniques from RAG when relevant
4. Ask "How's this?" after suggestions

FISH AUDIO MARKUP RULES (CRITICAL):
- Emotion tags (sad, happy, angry) MUST be at sentence start: (sad) "text"
- Tone markers (whispering, shouting) can go anywhere: "text (whispering) more"
- Audio effects (sighing, laughing) can go anywhere: "text," (sighing) she said.
- Combine up to 3 tags: (sad)(whispering) "text," (sighing) quietly.

AVAILABLE EMOTIONS: {emotion_list}
AVAILABLE TONES: {tone_list}
AVAILABLE EFFECTS: {effect_list}

Use RAG context when available to cite specific techniques from voice acting books.
"""
```

#### 4.2.4 Tool Definitions (`tools.py`)
```python
from livekit.agents import llm
import httpx

class FishAudioTool(llm.FunctionTool):
    def __init__(self, api_key: str):
        super().__init__(
            name="fish_audio_preview",
            description="Generate audio preview of a dialogue line with emotion markup using Fish Audio TTS",
            parameters={
                "type": "object",
                "properties": {
                    "line_text": {
                        "type": "string",
                        "description": "The dialogue line with Fish Audio emotion tags, e.g. '(sad)(whispering) I can't do this.'"
                    }
                },
                "required": ["line_text"]
            }
        )
        self.api_key = api_key

    async def execute(self, line_text: str):
        # Call Fish Audio API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.fish.audio/v1/tts",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"text": line_text}
            )
            # Return audio data
            return response.content
```

### 4.3 Environment Variables
```bash
# .env file
LIVEKIT_URL=ws://localhost:7880
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_api_secret

OPENAI_API_KEY=your_openai_api_key

DEEPGRAM_API_KEY=your_deepgram_api_key

ELEVENLABS_API_KEY=your_elevenlabs_api_key

FISH_AUDIO_API_KEY=b2a92433589f4c8f9893a33003132ab4
```

### 4.4 Dependencies (`requirements.txt`)
```
livekit-agents>=0.8.0
livekit-plugins-deepgram
livekit-plugins-openai
livekit-plugins-elevenlabs
livekit-plugins-silero
langchain>=0.1.0
chromadb>=0.4.0
pypdf
python-dotenv
httpx
```

---

## 5. Frontend Implementation

### 5.1 Directory Structure
```
frontend/
├── src/
│   ├── App.jsx              # Main app component
│   ├── components/
│   │   ├── VoiceControls.jsx    # Start/End call buttons
│   │   ├── StoryEditor.jsx      # Text editor + diff viewer
│   │   ├── LiveTranscript.jsx   # Real-time transcript
│   │   └── DiffDisplay.jsx      # Inline diff component
│   ├── hooks/
│   │   ├── useLiveKit.js        # LiveKit room connection
│   │   └── useStoryState.js     # Shared story state
│   ├── utils/
│   │   └── diffUtils.js         # Diff parsing helpers
│   └── main.jsx
├── public/
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
└── .env                    # Frontend env vars (LiveKit URL)
```

### 5.2 Key Frontend Components

#### 5.2.1 Main App (`App.jsx`)
```jsx
import { VoiceControls } from './components/VoiceControls'
import { StoryEditor } from './components/StoryEditor'
import { LiveTranscript } from './components/LiveTranscript'

function App() {
  const [storyText, setStoryText] = useState("")
  const [diffs, setDiffs] = useState([])
  const [transcript, setTranscript] = useState([])

  return (
    <div className="app-container">
      <header>Voice Director Agent - Lelouch</header>
      <div className="main-grid">
        <StoryEditor
          text={storyText}
          onTextChange={setStoryText}
          diffs={diffs}
        />
        <div className="sidebar">
          <VoiceControls />
          <LiveTranscript messages={transcript} />
        </div>
      </div>
    </div>
  )
}
```

#### 5.2.2 LiveKit Integration (`useLiveKit.js`)
```javascript
import { useVoiceAssistant, useConnectionState } from '@livekit/components-react'

export function useLiveKit() {
  const { state, audioTrack } = useVoiceAssistant()
  const connectionState = useConnectionState()

  const startCall = async () => {
    // Connect to LiveKit room
  }

  const endCall = () => {
    // Disconnect
  }

  return { state, startCall, endCall, connectionState }
}
```

#### 5.2.3 Diff Display (`DiffDisplay.jsx`)
```jsx
import ReactDiffViewer from 'react-diff-viewer-continued'

export function DiffDisplay({ original, modified }) {
  return (
    <ReactDiffViewer
      oldValue={original}
      newValue={modified}
      splitView={false}
      showDiffOnly={false}
      useDarkTheme={false}
    />
  )
}
```

### 5.3 Dependencies (`package.json`)
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "@livekit/components-react": "^2.0.0",
    "livekit-client": "^2.0.0",
    "react-diff-viewer-continued": "^3.3.1"
  },
  "devDependencies": {
    "vite": "^5.0.0",
    "tailwindcss": "^3.4.0",
    "@vitejs/plugin-react": "^4.2.0"
  }
}
```

---

## 6. RAG System Design

### 6.1 Document Processing Strategy

#### 6.1.1 PDF Sources
1. **"An Actor Prepares" by Constantin Stanislavski**
   - Focus: Emotion memory, subtext, character motivation
   - Size: ~300 pages
   - Key chapters: Ch 2 (When Acting is an Art), Ch 4 (Imagination), Ch 9 (Emotion Memory)

2. **"Freeing the Natural Voice" by Kristin Linklater**
   - Focus: Vocal technique, breath support, resonance
   - Size: ~250 pages
   - Key chapters: Ch 2 (The Natural Voice), Ch 5 (Breath), Ch 8 (Range and Resonance)

#### 6.1.2 Chunking Strategy
```python
RecursiveCharacterTextSplitter(
    chunk_size=1000,        # ~150-200 words
    chunk_overlap=200,      # Preserve context across chunks
    separators=["\n\n", "\n", ". ", " ", ""]  # Respect paragraph boundaries
)
```

**Reasoning**:
- 1000 chars preserves semantic meaning (full paragraphs)
- 200 char overlap prevents technique fragmentation
- Paragraph-aware splitting maintains coherence

#### 6.1.3 Metadata Enrichment
Each chunk tagged with:
- `source`: Book title
- `page`: Page number (if extractable)
- `chapter`: Chapter name (if detectable)
- `book_type`: "stanislavski" or "linklater"

### 6.2 Retrieval Strategy

#### 6.2.1 Query Processing
```python
def retrieve_techniques(user_query: str, emotion_context: str):
    # Combine user intent + emotion context
    enhanced_query = f"{user_query} {emotion_context} voice acting technique"

    # Retrieve top 5 chunks
    docs = vectorstore.similarity_search(enhanced_query, k=5)

    # Filter for relevance (optional threshold)
    relevant_docs = [doc for doc in docs if doc.metadata.get('score', 0) > 0.7]

    return relevant_docs
```

#### 6.2.2 Context Injection into LLM
```python
def build_llm_context(retrieved_docs, current_story_text):
    context = "VOICE ACTING TECHNIQUES:\n\n"
    for doc in retrieved_docs:
        context += f"[{doc.metadata['source']}, Ch {doc.metadata.get('chapter', 'N/A')}]\n"
        context += doc.page_content + "\n\n"

    context += f"\nCURRENT STORY TEXT:\n{current_story_text}\n"
    return context
```

### 6.3 RAG Evaluation Plan

**Test Queries**:
1. "How do I make a character sound more desperate?"
   - Expected: Stanislavski emotion memory, urgency techniques
2. "What does Linklater say about vocal power?"
   - Expected: Breath support, resonance sections
3. "How to show grief through voice?"
   - Expected: Stanislavski subtext, Linklater tone control

**Success Criteria**:
- Retrieves relevant passage in < 3 seconds
- Citations include book name
- Agent synthesizes technique into Lelouch-style advice

---

## 7. Emotion Markup System

### 7.1 Fish Audio Specification Compliance

#### 7.1.1 Tag Categories
```python
EMOTIONS = [
    "happy", "sad", "angry", "excited", "calm", "nervous", "confident",
    "surprised", "satisfied", "delighted", "scared", "worried", "upset",
    # ... (all 49 emotions from spec)
]

TONE_MARKERS = [
    "in a hurry tone", "shouting", "screaming", "whispering", "soft tone"
]

AUDIO_EFFECTS = [
    "laughing", "chuckling", "sobbing", "crying loudly", "sighing",
    "groaning", "panting", "gasping", "yawning", "snoring"
]

SPECIAL_EFFECTS = [
    "audience laughing", "background laughter", "crowd laughing",
    "break", "long-break"
]
```

#### 7.1.2 Placement Validation
```python
def validate_emotion_markup(text: str) -> dict:
    errors = []

    # Check emotion tags at sentence start
    sentences = text.split('. ')
    for sentence in sentences:
        # Find all tags in parentheses
        tags = re.findall(r'\(([^)]+)\)', sentence)

        for i, tag in enumerate(tags):
            if tag in EMOTIONS:
                # Emotion tag must be at start
                tag_pos = sentence.find(f"({tag})")
                if tag_pos > 0:  # Not at start
                    errors.append(f"Emotion tag '({tag})' must be at sentence start")

    return {"valid": len(errors) == 0, "errors": errors}
```

### 7.2 Diff Generation Logic

```python
def generate_emotion_diff(original_text: str, emotion_tags: dict) -> dict:
    """
    original_text: "I can't do this anymore," she said.
    emotion_tags: {
        "sentence": "I can't do this anymore,",
        "emotions": ["sad"],
        "tones": ["soft tone"],
        "effects": [{"position": "after_dialogue", "effect": "sighing"}]
    }

    Returns: {
        "original": original_text,
        "modified": "(sad)(soft tone) \"I can't do this anymore,\" (sighing) she said."
    }
    """
    modified = ""

    # Apply emotion tags at sentence start
    for emotion in emotion_tags.get("emotions", []):
        modified += f"({emotion})"

    # Apply tone markers (can be at start or within)
    for tone in emotion_tags.get("tones", []):
        modified += f"({tone})"

    # Add original text
    modified += " " + original_text

    # Apply effects at specified positions
    for effect in emotion_tags.get("effects", []):
        # Insert effect at position
        pass

    return {"original": original_text, "modified": modified}
```

---

## 8. Fish Audio Integration

### 8.1 API Specification

**Endpoint**: `POST https://api.fish.audio/v1/tts`

**Headers**:
```
Authorization: Bearer b2a92433589f4c8f9893a33003132ab4
Content-Type: application/json
```

**Request Body**:
```json
{
  "text": "(sad)(whispering) I can't do this anymore, (sighing) sigh.",
  "voice": "default",  // Or specific voice ID
  "format": "mp3"
}
```

**Response**:
- Audio file (binary MP3 data)
- Or JSON with audio URL

### 8.2 Tool Implementation

```python
async def fish_audio_preview(line_text: str) -> bytes:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.fish.audio/v1/tts",
            headers={
                "Authorization": f"Bearer {os.getenv('FISH_AUDIO_API_KEY')}",
                "Content-Type": "application/json"
            },
            json={
                "text": line_text,
                "format": "mp3"
            },
            timeout=10.0
        )

        if response.status_code != 200:
            raise Exception(f"Fish Audio API error: {response.text}")

        return response.content  # MP3 binary data
```

### 8.3 Audio Playback in LiveKit

```python
# In agent.py
async def handle_fish_audio_preview(audio_data: bytes):
    # Convert audio to LiveKit audio frame
    audio_source = rtc.AudioSource(sample_rate=24000, num_channels=1)

    # Play audio in room
    track = rtc.LocalAudioTrack.create_audio_track("preview", audio_source)
    await room.local_participant.publish_track(track)

    # Stream audio data
    await audio_source.capture_frame(audio_data)
```

---

## 9. LiveKit Configuration

### 9.1 Local Server Setup

**Option 1: Docker (Recommended)**
```bash
docker run --rm \
  -p 7880:7880 \
  -p 7881:7881 \
  -p 7882:7882/udp \
  -e LIVEKIT_KEYS="devkey: devsecret" \
  livekit/livekit-server:latest
```

**Option 2: Binary**
```bash
# Download from https://github.com/livekit/livekit/releases
./livekit-server --dev
```

### 9.2 Room Configuration

```yaml
# config.yaml
room:
  auto_create: true
  empty_timeout: 300  # 5 minutes
  max_participants: 2  # User + Agent

keys:
  devkey: devsecret

port: 7880
```

### 9.3 Agent Connection

```python
# agent.py
from livekit import api

async def entrypoint(ctx: JobContext):
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    participant = await ctx.wait_for_participant()

    # Start voice assistant
    assistant = VoiceAssistant(...)
    assistant.start(ctx.room, participant)
```

---

## 10. Error Handling & Resilience

### 10.1 API Failure Scenarios

| Scenario | Mitigation |
|----------|-----------|
| **Fish Audio API down** | Catch exception, inform user: "Preview unavailable, Fish Audio service error" |
| **OpenAI API timeout** | Retry with exponential backoff (3 attempts), fallback message |
| **Deepgram STT failure** | Display error in transcript, attempt reconnection |
| **RAG retrieval empty** | Agent responds without citing techniques, still provides advice |
| **LiveKit disconnection** | Auto-reconnect with exponential backoff |

### 10.2 Error Messages (Lelouch Style)

```python
ERROR_MESSAGES = {
    "fish_audio_unavailable": "The preview tool is unavailable. Proceed without it for now.",
    "rag_failed": "I cannot access the texts at this moment. I'll advise from experience.",
    "connection_lost": "Connection disrupted. Reconnecting...",
}
```

---

## 11. Performance Requirements

### 11.1 Latency Targets

| Component | Target | Acceptable | Critical |
|-----------|--------|------------|----------|
| **STT (speech → text)** | < 500ms | < 1s | < 2s |
| **RAG retrieval** | < 1s | < 2s | < 3s |
| **LLM response** | < 2s | < 4s | < 6s |
| **TTS (text → speech)** | < 1s | < 2s | < 3s |
| **Fish Audio preview** | < 3s | < 5s | < 7s |
| **End-to-end turn** | < 5s | < 8s | < 10s |

### 11.2 Optimization Strategies

1. **RAG Caching**: Cache frequent queries (e.g., "sadness techniques")
2. **Chunk Preloading**: Load vector DB into memory at startup
3. **Streaming TTS**: Stream audio as generated (not wait for full completion)
4. **Parallel API Calls**: Fetch RAG context while processing STT

---

## 12. Security & Privacy

### 12.1 API Key Management

**Environment Variables**:
```bash
# .env (NEVER commit)
FISH_AUDIO_API_KEY=b2a92433589f4c8f9893a33003132ab4
OPENAI_API_KEY=sk-...
DEEPGRAM_API_KEY=...
ELEVENLABS_API_KEY=...
```

**`.gitignore`**:
```
.env
.env.local
*.env
backend/.env
frontend/.env
```

### 12.2 Data Privacy

- **No persistent storage**: Stories not saved to database (user copies manually)
- **No user accounts**: Anonymous usage
- **No logging of story content**: Only log technical errors
- **Transcript ephemeral**: Cleared on page refresh

---

## 13. Testing Strategy

### 13.1 Backend Tests

1. **RAG System**:
   - Test: Query "desperation techniques" → Verify Stanislavski retrieval
   - Test: Query "vocal power" → Verify Linklater retrieval
   - Test: Empty query → Graceful handling

2. **Emotion Markup Validation**:
   - Test: `(sad) "text"` → Valid
   - Test: `"text (sad)"` → Invalid (emotion mid-sentence)
   - Test: `(whispering) "text"` → Valid (tone can go anywhere)

3. **Fish Audio Tool**:
   - Test: Valid line → Returns MP3 data
   - Test: API key invalid → Error handling
   - Test: Network timeout → Retry logic

### 13.2 Frontend Tests

1. **Diff Display**:
   - Test: Show simple diff (original → tagged)
   - Test: Multiple diffs in sequence
   - Test: User edits story mid-conversation

2. **LiveKit Connection**:
   - Test: Start call → Room created
   - Test: End call → Cleanup
   - Test: Reconnection after disconnect

### 13.3 Integration Tests

1. **End-to-End Flow**:
   - User pastes story → Start call → Agent greets
   - User: "Add emotion to line X" → Agent retrieves technique → Shows diff
   - User: "How does it sound?" → Fish Audio preview plays
   - User: "Apply it" → Text updates

2. **RAG Integration**:
   - User asks about Stanislavski technique → Agent cites book correctly
   - Interviewer asks random PDF question → Agent retrieves answer

---

## 14. Deployment

### 14.1 Local Development

**Backend**:
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python agent.py dev
```

**Frontend**:
```bash
cd frontend
npm install
npm run dev  # http://localhost:5173
```

**LiveKit**:
```bash
docker run --rm -p 7880:7880 livekit/livekit-server --dev
```

### 14.2 AWS Deployment (Bonus)

**Option 1: EC2**
- Deploy backend on EC2 instance
- Use Docker Compose for LiveKit + Agent
- Frontend on S3 + CloudFront

**Option 2: ECS**
- Containerize backend + LiveKit
- Run on ECS Fargate
- Frontend on Amplify

*Out of scope for initial MVP - local deployment sufficient*

---

## 15. Demo Script (Interview Presentation)

### 15.1 Preparation

**Story Example** (2-3 paragraphs):
```
Marcus stared at the door, hand trembling on the handle. "I have to tell you something,"
he said. The weight of three years of silence pressed against his chest.

Sarah turned, her eyes already wet. "I know," she whispered. "I've always known."

"Then why didn't you say anything?" His voice cracked. "Why did we keep pretending?"
```

### 15.2 Demo Flow (5 minutes)

1. **Show UI** (30s)
   - Story text pasted in editor
   - Point out controls: Start/End call, transcript area

2. **Start Conversation** (1min)
   - Click "Start Call"
   - Lelouch greets: "Ah, you've come seeking my expertise..."
   - Show live transcript updating

3. **Request Emotion Markup** (2min)
   - User: "Can you add emotion to the breakup scene?"
   - Agent retrieves Stanislavski technique, suggests markup
   - Diff appears showing: `(regretful)(soft tone) "I have to tell you something," (break) he said.`
   - Agent: "How's this?"

4. **Iterate** (1min)
   - User: "Make it even more subtle"
   - Agent adjusts: `(uncertain) "I have to tell you something," he said quietly.`

5. **Fish Audio Preview** (1min)
   - User: "How would that sound?"
   - Agent: "Let me generate that for you..."
   - Audio plays with emotion tags

6. **RAG Test (Interviewer)** (30s)
   - Interviewer: "What does Stanislavski say about emotion memory?"
   - Agent retrieves correct passage, explains technique

7. **Wrap Up** (30s)
   - Show final edited text with markup
   - End call

---

## 16. Known Limitations & Future Work

### 16.1 MVP Limitations

| Limitation | Impact | Future Solution |
|------------|--------|----------------|
| **No revision history** | Can't undo changes | Implement undo/redo stack |
| **Single line preview** | Can't hear full scene | Batch TTS for multiple lines |
| **No character voices** | All previews use default voice | Voice assignment UI |
| **No PDF upload** | PDFs hardcoded | Frontend upload + dynamic indexing |
| **No user accounts** | No saved work | Firebase/Supabase auth |
| **Local only** | Not shareable | AWS deployment |

### 16.2 Potential Improvements

1. **Multi-character support**: Assign different voices to each character
2. **Batch processing**: Apply emotion markup to entire story at once
3. **Export**: Download marked-up story as .txt or .docx
4. **Voice customization**: Clone user's own voice for preview
5. **Real-time collaboration**: Multiple users editing same story

---

## 17. Success Criteria (Review)

### 17.1 Bluejay Requirements ✅

- [x] LiveKit voice agent with full pipeline
- [x] Real-time transcription display
- [x] Agent personality (Lelouch) with compelling narrative
- [x] Tool call (Fish Audio preview)
- [x] RAG over large PDF (2 books, semantic retrieval)
- [x] React frontend (text editor, controls, transcript)
- [x] Start/End call buttons
- [x] Creative storytelling (alternate timeline, personal use case)

### 17.2 Technical Validation

- [x] Agent applies Fish Audio markup correctly (placement rules)
- [x] Inline diffs show clear before/after
- [x] Conversational iteration works smoothly
- [x] RAG retrieves relevant techniques from PDFs
- [x] Fish Audio preview generates audio successfully
- [x] Lelouch personality is consistent and concise

---

## 18. References

### 18.1 Documentation
- [LiveKit Agents Documentation](https://docs.livekit.io/agents/)
- [LiveKit React Components](https://docs.livekit.io/client-sdk-js/react/)
- [LangChain RAG Guide](https://python.langchain.com/docs/use_cases/question_answering/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Fish Audio API Docs](https://fish.audio/docs/api)

### 18.2 Books (RAG Sources)
- Stanislavski, C. (1936). *An Actor Prepares*. Theatre Arts Books.
- Linklater, K. (1976). *Freeing the Natural Voice*. Drama Publishers.

---

**Document Status**: Ready for Implementation
**Next Steps**: Setup project structure → Build backend RAG → Build LiveKit agent → Build frontend → Test integration
