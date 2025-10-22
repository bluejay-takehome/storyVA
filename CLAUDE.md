# CLAUDE.md

Guidance for Claude Code when working with the StoryVA project.

## Core Documentation

**READ THESE FIRST** before making implementation decisions:

- **[PRD.md](./PRD.md)** - Product requirements, user flows, agent personality, Fish Audio emotion rules
- **[TDD.md](./TDD.md)** - System architecture, component designs, implementation code examples, development plan
- **[GUIDELINES.md](./GUIDELINES.md)** - Bluejay interview requirements, must-haves, submission criteria

## Quick Context

**StoryVA:** RAG-enabled voice agent (Lelouch) helping writers add Fish Audio emotion markup to stories.

**Status:** Phase 1 ~70% complete (repo flattened, frontend/backend initialized, Pinecone created)

## Tech Stack

- **Frontend:** Next.js 14 (TypeScript, Tailwind)
- **Backend:** Python (LiveKit Agents SDK, LlamaIndex)
- **TTS:** Fish Audio (custom implementation required)
- **Vector DB:** Pinecone (`storyva-voice-acting` index)
- **LLM:** GPT-5

See **TDD.md Section 2** for full architecture and repository structure.

## Environment

All API keys configured in `/backend/.env` (OpenAI key uses system environment).

See **TDD.md Section 3.4** for complete configuration details.

## Critical Implementation Notes

1. **Fish Audio TTS** - Custom implementation required (not in LiveKit built-ins). See **TDD.md Section 4.2.6**.
2. **Tool Calling** - Agent must auto-infer gender for preview tool (no asking user). See **TDD.md Section 3.3**.
3. **Agent Personality** - Lelouch is concise (2-4 sentences), strategic, commanding. See **PRD.md Section 6**.
4. **Emotion Tags** - Must be at sentence start (English rule). See **PRD.md Appendix A**.

## Development Best Practices

- **NO AUTO-COMMITS:** Always explain changes and let user test first
- **Explain Changes:** Document what was fixed and why
- **Test First:** Verify changes locally before committing
- **Follow TDD:** Reference TDD.md for implementation patterns
- **Use TodoWrite:** Track multi-step tasks with the todo list
- **Keep TDD Updated:** When completing tasks or making design changes, update TDD.md to reflect current state

## Dev Commands

```bash
# Frontend
cd frontend && npm run dev        # http://localhost:3000

# Backend
cd backend && uv sync             # Install deps
python main.py                    # Run agent (when ready)
```

## Key Constraints

- Must use LiveKit (GUIDELINES.md)
- Single git repo
- Custom Fish Audio TTS required (not built-in)
- Interviewer will test RAG with random PDF questions

## When You Need Help

| Question | Document | Section |
|----------|----------|---------|
| How does feature X work? | PRD.md | Section 3 |
| How to implement Y? | TDD.md | Section 4 |
| What are requirements? | GUIDELINES.md | - |
| Agent personality? | PRD.md | Section 6 |
| Tool calling strategy? | TDD.md | Section 3.3 |
| Fish Audio rules? | PRD.md | Appendix A |

---

**Last Updated:** 2025-10-22
