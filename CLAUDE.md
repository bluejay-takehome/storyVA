# CLAUDE.md

This file provides guidance to Claude Code when working with the StoryVA project.

## Project Overview

**StoryVA** is a RAG-enabled voice agent that helps writers add professional emotion markup to stories using Fish Audio's TTS system. The agent ("Lelouch") acts as an AI voice director, teaching theatrical techniques from classic voice acting texts.

**Interview Project:** Bluejay take-home assignment demonstrating LiveKit integration, RAG capabilities, tool calling, and creative storytelling.

## Core Documentation

**READ THESE FIRST** before making implementation decisions:

1. **[PRD.md](./PRD.md)** - Product Requirements Document
   - User experience flows
   - Agent personality (Lelouch)
   - Feature specifications
   - Fish Audio emotion markup rules
   - Success criteria

2. **[TDD.md](./TDD.md)** - Technical Design Document
   - Complete system architecture
   - Component designs with code examples
   - Custom Fish Audio TTS implementation
   - 7-phase development plan (23 days)
   - API configuration
   - Tool calling strategy

3. **[GUIDELINES.md](./GUIDELINES.md)** - Bluejay Interview Requirements
   - Must-have technical requirements
   - Submission criteria
   - Presentation expectations
   - Constraints (must use LiveKit)

## Repository Structure

```
storyVA/                          # Single git repository (no submodules)
├── frontend/                     # Next.js 14 + TypeScript + Tailwind
│   ├── app/                      # App Router pages
│   ├── components/               # React components (to be built)
│   └── package.json
├── backend/                      # Python + LiveKit Agents SDK
│   ├── .env                      # API keys (NOT committed)
│   ├── agent/                    # Agent logic (to be built)
│   ├── rag/                      # RAG integration (to be built)
│   ├── tts/                      # Custom Fish Audio TTS (to be built)
│   ├── tools/                    # Tool implementations (to be built)
│   ├── scripts/                  # Setup scripts
│   │   └── setup_pinecone.py    # ✅ Pinecone index creation
│   └── data/
│       └── pdfs/                 # Voice acting reference books
│           ├── an_actor_prepares.pdf
│           └── freeing_natural_voice.pdf
├── PRD.md                        # Product requirements
├── TDD.md                        # Technical design
├── GUIDELINES.md                 # Interview requirements
└── CLAUDE.md                     # This file
```

## Technology Stack

**Frontend:**
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- LiveKit React Components
- react-diff-viewer

**Backend:**
- Python 3.10+
- LiveKit Agents SDK
- LlamaIndex (RAG framework)
- Pinecone (vector database - cloud)
- Custom Fish Audio TTS integration

**Services:**
- **LiveKit Cloud:** `wss://bluejay-97zjii70.livekit.cloud`
- **STT:** Deepgram Nova-3
- **LLM:** GPT-5 (all operations)
- **TTS:** Fish Audio (custom implementation required)
- **Embeddings:** OpenAI text-embedding-3-small
- **Vector DB:** Pinecone (index: `storyva-voice-acting`)

## Environment Configuration

**Backend:** `/backend/.env`
```bash
# All API keys configured except OPENAI_API_KEY (uses system environment)
LIVEKIT_URL=wss://bluejay-97zjii70.livekit.cloud
LIVEKIT_API_KEY=<configured>
LIVEKIT_API_SECRET=<configured>
DEEPGRAM_API_KEY=<configured>
FISH_AUDIO_API_KEY=<configured>
FISH_LELOUCH_VOICE_ID=48056d090bfe4d6690ff31725075812f
FISH_MALE_VOICE_ID=802e3bc2b27e49c2995d23ef70e6ac89
FISH_FEMALE_VOICE_ID=b545c585f631496c914815291da4e893
PINECONE_API_KEY=<configured>
PINECONE_INDEX_NAME=storyva-voice-acting
```

**OpenAI API Key:** Available from system environment variables (not in `.env`)

## Development Status

**✅ Completed:**
- Repository flattened (no submodules)
- Pinecone index created (`storyva-voice-acting`)
- Backend dependencies installed (LlamaIndex, Pinecone, LiveKit)
- Frontend initialized (fresh Next.js 14 app)
- API keys configured in `.env`
- PDFs loaded (`backend/data/pdfs/`)

**🚧 To Do (See TDD.md Section 7 for detailed plan):**
- Phase 1: Foundation (folder structure, dev scripts)
- Phase 2: RAG system (ingest PDFs, test retrieval)
- Phase 3: LiveKit agent (voice pipeline, Lelouch personality)
- Phase 4: Custom Fish Audio TTS (WebSocket streaming)
- Phase 5: Frontend components (StoryEditor, CallControls, LiveTranscript, DiffViewer)
- Phase 6: Integration & testing
- Phase 7: Documentation & deployment

## Key Implementation Notes

### Fish Audio Integration
- **Custom TTS required** - Fish Audio NOT natively supported by LiveKit
- Must implement LiveKit TTS interface with WebSocket streaming
- See TDD.md Section 4.2.6 for complete implementation
- Emotion tags must be at sentence start (English rule)

### Tool Calling Strategy
- **Tool 1:** `search_acting_technique(query)` - RAG retrieval from Pinecone
- **Tool 2:** `preview_line_audio(marked_up_text, character_gender)` - Fish Audio preview
  - **Critical:** Agent must automatically infer gender from story context (pronouns, names)
  - Uses different voice_id than agent (character preview ≠ Lelouch voice)
- **Tool 3:** `suggest_emotion_markup(line, emotions, explanation)` - Diff generation

### Agent Personality
- **Lelouch:** Brilliant strategist, concise, analytical, commanding
- Keep responses 2-4 sentences
- Never speaks markup tags aloud (displayed in visual diff)
- References techniques like tactical choices
- See PRD.md Section 6 for complete personality guide

## Development Best Practices

- **NO AUTO-COMMITS:** Always explain changes and let user test first
- **Explain Changes:** Document what was fixed and why
- **Test First:** Verify changes locally before committing
- **Follow TDD:** Reference TDD.md for implementation patterns
- **Use TodoWrite:** Track multi-step tasks with the todo list

## Common Commands

**Frontend:**
```bash
cd frontend
npm run dev              # http://localhost:3000
npm run build
npm run lint
```

**Backend:**
```bash
cd backend
uv sync                  # Install dependencies
source .venv/bin/activate
python main.py           # Run agent (when implemented)
uv run python scripts/setup_pinecone.py  # Create Pinecone index
```

**Git Operations:**
```bash
# All operations from root directory (single repo)
git status
git add .
git commit -m "message"
git push origin main
```

## Important Constraints

1. **Single Git Repository** - No submodules (already flattened)
2. **Must Use LiveKit** - For voice orchestration (GUIDELINES.md requirement)
3. **Custom Fish Audio TTS** - Not in LiveKit's built-in providers
4. **Tool Calling Required** - Must demonstrate external API calls
5. **RAG Over PDFs** - Interviewer will test with random chapter/fact questions
6. **Agent Personality** - Creativity and storytelling are part of evaluation

## Quick Reference Links

- **LiveKit Agents Docs:** https://docs.livekit.io/agents/
- **LiveKit + RAG Integration:** https://docs.livekit.io/agents/build/external-data/
- **Fish Audio API:** (WebSocket streaming, emotion tags)
- **LlamaIndex Docs:** (RAG framework)
- **Pinecone Docs:** (Vector database)

## Questions? Check These First

- **"How does X feature work?"** → Read PRD.md Section 3 (Core Features)
- **"How do I implement Y?"** → Read TDD.md Section 4 (Component Design)
- **"What are the requirements?"** → Read GUIDELINES.md
- **"What's the agent personality?"** → Read PRD.md Section 6
- **"How does tool calling work?"** → Read TDD.md Section 3.3
- **"Fish Audio emotion rules?"** → Read PRD.md Appendix A

---

**Last Updated:** 2025-10-22
**Status:** Backend setup complete, frontend initialized, ready for Phase 1 implementation
