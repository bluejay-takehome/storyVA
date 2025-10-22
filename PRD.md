# Product Requirements Document: Voice Director Agent

## 1. Overview

### 1.1 Product Vision
A RAG-enabled voice agent that helps writers add professional emotion markup to their stories using Fish Audio's advanced text-to-speech system. The agent acts as an AI voice director, teaching theatrical techniques from classic voice acting texts and applying them conversationally.

### 1.2 Business Context
**Interview Project:** Bluejay take-home assignment demonstrating LiveKit integration, RAG capabilities, tool calling, and creative storytelling.

**Real-World Application:** Feature prototype for existing multi-character narration platform. Current system auto-generates emotion steering, but power users need fine-grained control over emotional direction using Fish Audio's markup language.

### 1.3 Success Metrics
- ✅ Passes all Bluejay technical requirements (LiveKit, RAG, tool call, frontend)
- ✅ Demonstrates creative storytelling through agent personality
- ✅ Successfully retrieves specific techniques from voice acting PDFs
- ✅ Applies Fish Audio emotion markup correctly using inline diffs
- ✅ Preview tool call successfully generates audio via Fish Audio API

## 2. User Persona

### Primary User
**Creative Writer / Content Creator**
- Writes fiction, fanfiction, or narrative content
- Wants to convert text to engaging narrated audiobooks
- Needs fine-grained control over emotional delivery
- Familiar with storytelling but not necessarily voice acting techniques
- Wants conversational, iterative editing rather than batch processing

## 3. Core Features

### 3.1 Voice Agent Conversation (P0)
**Requirement:** Real-time voice conversation using LiveKit

**Specifications:**
- Agent personality: "Lelouch" - brilliant strategist turned voice director
  - Analytical and strategic approach to emotion
  - Theatrical but concise language
  - Commanding yet engaging tone
  - References voice acting techniques like tactical choices
  - Slightly arrogant but earned confidence
- Voice pipeline: STT → LLM → TTS → VAD
- Maintains context across conversation turns
- Understands user's story context and previous edits

**User Flow:**
1. User clicks "Start Call" button
2. Agent greets user: "Ah, you've come seeking my expertise. I am Lelouch. Show me your story - let us transform it into something extraordinary."
3. User describes what they want emotionally
4. Agent analyzes, suggests specific techniques with strategic framing
5. Conversational back-and-forth until user is satisfied

### 3.2 Story Text Management (P0)
**Requirement:** Display user's story with inline diff editing

**Specifications:**
- Large text input area for pasting full story
- **Text area is editable** - user can freely edit at any time
- Agent always reads current text state before making suggestions
- Inline diff display showing:
  - Original text (strikethrough or red)
  - Proposed changes (highlight or green)
  - Fish Audio markup tags in parentheses
- Side-by-side or inline diff view
- Clear visual distinction between original and emotion-tagged versions

**Example Display:**
```
Original: "I can't believe you did this," she said.
Proposed: (disappointed)(soft tone) "I can't believe you did this," she said, (sighing) sigh.
```

**Constraints:**
- No revision history tracking (MVP scope)
- Diffs are shown visually on screen, not spoken by agent
- Agent must ask permission before applying changes to actual text
- User can accept, reject, or request modifications to proposed diffs

### 3.3 RAG Integration (P0)
**Requirement:** Retrieve relevant voice acting techniques from PDF books

**Books:**
1. "An Actor Prepares" by Constantin Stanislavski
2. "Freeing the Natural Voice" by Kristin Linklater

**Specifications:**
- Vector database with chunked PDFs
- Retrieval triggered by:
  - User questions: "How do I make this sound more desperate?"
  - Agent proactively citing techniques: "Stanislavski talks about emotion memory..."
  - Specific emotional requests: "Make this sadder"
- Returned context includes:
  - Specific technique or principle
  - Book citation (chapter/page if available)
  - Practical application to user's text

**RAG Query Examples:**
- User: "How can I make this breakup scene more heartbreaking?"
  - RAG retrieves: Stanislavski's emotion memory techniques
  - Agent response: "Stanislavski's emotion memory - genuine sadness from personal truth. For this line, sadness with a sigh for weight, long pause before final words for dramatic tension. How's this?"

- User: "This character should sound more commanding"
  - RAG retrieves: Linklater's vocal power and breath support sections
  - Agent response: "Linklater - vocal power grounded in breath. Confident and loud for authority, or determined for quiet strength. Decide which serves your character."

**Implementation Notes:**
- Use LangChain or LlamaIndex for RAG framework
- Semantic chunking strategy (preserve paragraph/section context)
- Retrieve 3-5 relevant chunks per query
- Agent LLM synthesizes retrieval into conversational response

### 3.4 Emotion Markup Application (P0)
**Requirement:** Apply Fish Audio emotion tags following official spec

**Fish Audio Markup Placement Rules (Critical for English):**
- **Emotion tags** (happy, sad, angry, etc.): MUST be at the beginning of sentences
- **Tone markers** (whispering, shouting, soft tone, etc.): Can be placed anywhere in text
- **Audio effects** (laughing, sighing, sobbing, etc.): Can be placed anywhere in text
- **Special effects** (break, long-break, audience laughing): Can be placed anywhere in text
- Can combine up to 3 tags per sentence: `(emotion)(tone)(effect)`
- Format examples:
  - Emotion at start: `(sad) "I can't believe this," she said.`
  - Combined: `(sad)(whispering) "I can't believe this," she whispered, (sighing) quietly.`
  - Multiple effects: `(excited)(laughing) "We won!" she shouted. Ha ha!`

**Agent Behavior:**
- Suggests appropriate emotion tags based on:
  - Story context (surrounding text)
  - Character emotional state
  - User's described intent
  - RAG-retrieved techniques
- **Describes intent conversationally** - does NOT speak markup tags aloud
- Markup changes appear in visual diff on screen
- Explains WHY each tag is chosen
- Offers alternatives when relevant
- Validates markup follows Fish Audio spec

**Example Conversation:**
```
User: "Make the part where she leaves more emotional"
Agent: "I see the scene. Stanislavski would call this subtext - the unspoken pain
       beneath words. Not general sadness - regret for how it ends. I suggest
       whisper tone with quiet sob. Restrained, not theatrical. How's this?"
[Diff shows on screen: (regretful)(whispering) "Goodbye," she whispered, (sobbing).]

User: "Yes, but make it softer"
Agent: "Even more restrained. Observe."
[Diff updates: (sad)(soft tone) "Goodbye," she whispered, (sighing) quietly.]

User: "Perfect, apply it"
Agent: "Applied. The subtlety serves the moment better."
```

### 3.5 Tool Call: Fish Audio Preview (P0)
**Requirement:** Generate audio preview of specific dialogue line

**Specifications:**
- Triggered by user request: "How would this line sound?"
- User describes which line:
  - "The line where Marcus says 'I'm leaving'"
  - "The third line of dialogue"
  - "When she says goodbye"
- Agent:
  1. Identifies the specific line from story text
  2. Applies current emotion markup (or proposed markup)
  3. Calls Fish Audio API with marked-up text
  4. Plays audio response back to user
  5. Asks for feedback

**Fish Audio API Integration:**
- Endpoint: `/v1/tts` (or similar from Fish Audio docs)
- Requires: API key (user has credentials)
- Input: Emotion-tagged text
- Output: Audio file (mp3/wav)
- Playback: Stream audio in browser during call

**Example Flow:**
```
User: "How would the breakup line sound with those tags?"
Agent: "Let me generate that for you with the markup we discussed..."
[API call to Fish Audio: "(sad)(soft tone) I can't do this anymore, (sighing) sigh."]
[Audio plays through browser/call]
Agent: "How does that sound? Too subtle? We could add more intensity."
```

**Constraints:**
- Single line preview per request (not whole story)
- Uses default/neutral voice (character voice assignment out of scope)
- Preview is for emotion testing only

### 3.6 Live Transcript Display (P0)
**Requirement:** Real-time transcript of conversation

**Specifications:**
- Displays both user and agent speech as text
- Updates in real-time as STT processes audio
- Format:
  ```
  User: "Make this scene sadder"
  Lelouch: "Too vague. Specify the purpose - regret, loss, or despair?"
  ```
- Auto-scrolls to latest message
- Clear visual distinction between speakers
- Persists throughout call session

**UI Placement:** Side panel or bottom panel in React frontend

## 4. User Experience Flow

### 4.1 Complete User Journey

**Step 1: Setup**
1. User navigates to web app
2. Pastes story text into large text area
3. Text is visible and readable

**Step 2: Start Conversation**
4. User clicks "Start Call" button
5. LiveKit room created, agent joins
6. Agent greets user with personality
7. Live transcript begins displaying

**Step 3: Iterative Editing**
8. User: "Can you add emotion to the breakup scene?"
9. Agent uses RAG to pull relevant techniques
10. Agent suggests specific markup with explanation
11. Diff preview shows proposed changes
12. User: "Actually, make it more subtle"
13. Agent adjusts suggestion
14. User: "How would this sound?"
15. Agent calls Fish Audio API, plays preview
16. User: "Perfect, apply it"
17. Agent applies changes, diff becomes accepted text

**Step 4: Repeat**
18. User continues working through story
19. Multiple iterations on different scenes
20. Agent maintains context and story understanding

**Step 5: End Session**
21. User clicks "End Call" button
22. Final edited text available for copy/download
23. Transcript available for review

## 5. Technical Architecture

### 5.1 System Components

```
┌─────────────────────────────────────────────────────────────┐
│                      React Frontend                          │
│  - LiveKit React Components                                  │
│  - Text Editor (diff view)                                   │
│  - Live Transcript Display                                   │
│  - Start/End Call Controls                                   │
└─────────────────┬───────────────────────────────────────────┘
                  │ WebRTC/WebSocket
┌─────────────────▼───────────────────────────────────────────┐
│                   LiveKit Server (Cloud)                     │
│  - Room management                                           │
│  - Media streaming                                           │
└─────────────────┬───────────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────────┐
│              Python LiveKit Agent (Backend)                  │
│  - Voice Pipeline: STT → LLM → TTS → VAD                    │
│  - RAG Integration (LangChain/LlamaIndex)                   │
│  - Tool Calling: Fish Audio API                             │
│  - Text Diff Generation                                      │
│  - Conversation State Management                            │
└─────────────────┬───────────────────────────────────────────┘
                  │
        ┌─────────┴──────────┬───────────────┐
        │                    │               │
┌───────▼────────┐  ┌────────▼─────┐  ┌─────▼──────────┐
│ Vector Store   │  │   LLM API    │  │  Fish Audio    │
│ (Pinecone/     │  │ (OpenAI/     │  │     API        │
│  Chroma)       │  │  Anthropic)  │  │                │
│                │  │              │  │  (Preview TTS) │
│ - An Actor     │  └──────────────┘  └────────────────┘
│   Prepares PDF │
│ - Freeing the  │
│   Natural Voice│
└────────────────┘
```

### 5.2 Technology Stack

**Frontend:**
- React 18+
- LiveKit React Components SDK
- Tailwind CSS or similar for styling
- Monaco Editor or similar for diff display

**Backend:**
- Python 3.10+
- LiveKit Agents SDK (Python)
- LangChain or LlamaIndex for RAG
- OpenAI/Anthropic API for LLM
- Fish Audio API for TTS preview

**Infrastructure:**
- LiveKit Cloud (server hosting)
- Vector DB: Pinecone, Chroma, or Weaviate
- Optional: AWS deployment for bonus points

**STT/TTS/LLM Providers:**
- STT: Deepgram, AssemblyAI, or Whisper
- LLM: GPT-4, Claude 3.5 Sonnet, or similar
- TTS: ElevenLabs, PlayHT, or OpenAI TTS
- Preview TTS: Fish Audio (tool call only)

## 6. Agent Personality: Lelouch

### 6.1 Character Profile
**Name:** Lelouch

**Background (Alternate Timeline):** After mastering the art of dual personas and strategic performance, Lelouch retreated from the world stage to teach others the craft of vocal expression. Having commanded armies through voice alone as Zero while maintaining the facade of an ordinary student, he now applies his genius to voice direction - treating every emotional choice as a calculated move toward narrative perfection.

**Core Personality Traits:**
- **Brilliant Strategist:** Analyzes stories like chess games - every emotion is a tactical choice
- **Theatrical but Concise:** Dramatic flair in language, but keeps responses short and commanding
- **Analytical:** Explains the mechanics behind emotional impact with precision
- **Demanding Excellence:** High standards, doesn't sugarcoat, but pushes you to improve
- **Earned Arrogance:** Confident in expertise ("I've mastered what you're attempting to learn")
- **Intellectually Rigorous:** References techniques like battle tactics, requires intentionality
- **Charismatic:** Inspiring when you succeed, challenging when you don't

**Speaking Style Guidelines:**
- Keep responses concise (2-4 sentences typical)
- Strategic framing: "This serves the narrative better" / "Consider the alternative"
- Direct commands: "Observe" / "Listen carefully" / "Decide quickly"
- Occasional formal language: "I surmise" / "I see" / "Very well"
- References theory in one sentence max, then moves to action
- Never verbose - Lelouch doesn't waste words

**Example Phrases:**
- "Too vague. Specify the emotion's purpose."
- "I see. Given the context, regret serves better than sadness here."
- "Stanislavski calls this the magic if. We apply it by... Observe."
- "Better. Not perfect, but you're beginning to understand."
- "Listen to the pause before the final word. Do you hear its weight?"
- "Applied. The subtlety serves the moment better."

**Example Opening:**
> "Ah, you've come seeking my expertise. I am Lelouch. Show me your story - let us transform it into something extraordinary."

### 6.2 Interaction Patterns

**Making Suggestions:**
> "I surmise the character hides their true feelings here. Classic misdirection. For this line - regret masked by confidence. Observe the markup. How's this?"

**Using RAG (Concise):**
> "Stanislavski's emotion memory - accessing genuine feeling through personal truth. For your scene, we ground the sadness in specific loss, not vague emotion. The difference is everything."

**After Fish Audio Preview:**
> "Listen carefully. The emotion is present, but the timing is off. The sigh releases tension too early. Shall we adjust?"

**When User Gets It Right:**
> "Excellent. That emotional transition - hope to despair - executed with precision. This is what I expect."

**When User Resists:**
> "You doubt me? Very well. Compare both versions. Tell me which commands attention."

### 6.3 Underlying Motivation
Perfection of narrative craft through vocal mastery. Lelouch believes stories have power to change hearts and minds - he's witnessed it. Teaching others to wield voice as a storytelling tool is his quiet mission against mediocrity.

## 7. MVP Scope

### 7.1 In Scope (Must Have)
- ✅ LiveKit voice agent with personality
- ✅ RAG over 2 PDFs (An Actor Prepares, Freeing the Natural Voice)
- ✅ Fish Audio emotion markup application (inline diffs)
- ✅ Fish Audio API tool call (single line preview)
- ✅ React frontend with start/end call buttons
- ✅ Live transcript display
- ✅ Text input/display area with diff view
- ✅ Conversational iterative editing

### 7.2 Out of Scope (Future/Nice to Have)
- ❌ Revision history tracking
- ❌ PDF upload functionality (hardcode PDFs in backend)
- ❌ Multi-character voice assignment (uses default voice)
- ❌ Full story TTS generation (only single line preview)
- ❌ User authentication/accounts
- ❌ Saving stories to database
- ❌ AWS deployment (local is fine, AWS is bonus)

## 8. Non-Functional Requirements

### 8.1 Performance
- Transcript latency: < 2 seconds from speech to text display
- RAG retrieval: < 3 seconds from query to response
- Fish Audio preview: < 5 seconds from request to audio playback
- Agent response time: < 5 seconds for typical queries

### 8.2 Reliability
- Graceful error handling for API failures
- Clear error messages for user (e.g., "Fish Audio API unavailable")
- Agent stays responsive even if RAG retrieval fails

### 8.3 Usability
- Agent personality must be consistent throughout conversation
- Diff view must be easily readable
- Transcript must auto-scroll and be scannable
- Controls (start/end call) must be obvious

## 9. Testing & Demo Plan

### 9.1 Demo Script (for Interview Presentation)
**Story:** [Prepare a 2-3 paragraph emotional scene - breakup, reunion, conflict, etc.]

**Demo Flow:**
1. Show story text in UI
2. Start call, agent greets
3. Request emotion markup for specific scene
4. Agent retrieves Stanislavski technique, suggests markup
5. Preview line with Fish Audio
6. Iterate once ("make it softer/stronger")
7. Apply changes, show diff
8. Interviewer asks random question about PDF content
9. Agent successfully retrieves and explains technique
10. End call

### 9.2 RAG Testing
**Test Queries:**
- "How do I make a character sound more desperate?"
- "What techniques help with emotional authenticity?"
- "How should I approach a grief scene?"
- "What does Stanislavski say about subtext?"
- "How do I use voice to show character transformation?"

Each should retrieve relevant passages from PDFs.

### 9.3 Fish Audio Tool Call Testing
**Test Cases:**
- Single line of dialogue
- Line with multiple emotion tags
- Line with audio effects (laughing, sighing)
- Error handling if line not found in story

## 10. Success Criteria

### 10.1 Bluejay Requirements Coverage
| Requirement | Implementation |
|------------|----------------|
| LiveKit voice agent | ✅ Lelouch with full voice pipeline |
| Real-time transcription | ✅ Live transcript display in React |
| Agent personality/story | ✅ Strategic voice director, alternate timeline narrative |
| Tool call | ✅ Fish Audio preview API |
| RAG over large PDF | ✅ 2 voice acting books, semantic retrieval |
| React frontend | ✅ Text editor, controls, transcript |
| Start/End call buttons | ✅ LiveKit room management |
| Creative storytelling | ✅ Lelouch character (Code Geass), personal use case |

### 10.2 Personal Use Case Validation
- Agent successfully applies Fish Audio markup spec
- Inline diffs show clear before/after
- Conversational iteration works smoothly
- Could realistically be integrated into production platform

### 10.3 Interview Presentation Goals
- Clear, compelling story about solving personal problem
- Smooth live demo without technical issues
- Agent retrieves correct information from PDFs on demand
- Fish Audio preview works and sounds good
- Demonstrates technical sophistication and creativity

## 11. Open Questions & Decisions Needed

### 11.1 Technical Decisions
- [ ] Vector DB choice: Pinecone (hosted) vs Chroma (local)?
- [ ] LLM provider: OpenAI GPT-4 vs Anthropic Claude?
- [ ] STT provider: Deepgram vs AssemblyAI?
- [ ] TTS provider: ElevenLabs vs PlayHT?
- [ ] Diff library: react-diff-viewer vs custom implementation?

### 11.2 UX Decisions
- [ ] Diff view: inline or side-by-side?
- [ ] How to handle very long stories (scrolling, chunking)?
- [ ] Should agent proactively suggest edits or only respond to requests?
- [ ] How to visually indicate which line is being previewed?

### 11.3 Scope Decisions
- [ ] Deploy to AWS for bonus points or keep local?
- [ ] PDF upload button or hardcode PDFs?
- [ ] How many example stories to include for demo?

---

## Appendix A: Fish Audio Emotion Tags Quick Reference

**Basic Emotions (24):** happy, sad, angry, excited, calm, nervous, confident, surprised, satisfied, delighted, scared, worried, upset, frustrated, depressed, empathetic, embarrassed, disgusted, moved, proud, relaxed, grateful, curious, sarcastic

**Advanced Emotions (25):** disdainful, unhappy, anxious, hysterical, indifferent, uncertain, doubtful, confused, disappointed, regretful, guilty, ashamed, jealous, envious, hopeful, optimistic, pessimistic, nostalgic, lonely, bored, contemptuous, sympathetic, compassionate, determined, resigned

**Tone Markers (5):** in a hurry tone, shouting, screaming, whispering, soft tone

**Audio Effects (10):** laughing, chuckling, sobbing, crying loudly, sighing, groaning, panting, gasping, yawning, snoring

**Special Effects:** audience laughing, background laughter, crowd laughing, break, long-break

**Placement Rules (For English and Most Languages):**
- ✅ **Emotion tags MUST be at sentence start**: `(sad) "I can't do this."`
- ✅ **Tone markers can go anywhere**: `"I can't (whispering) do this."`
- ✅ **Audio effects can go anywhere**: `"I can't do this," (sighing) she said.`
- ✅ **Special effects can go anywhere**: `She paused (break) before answering.`
- ✅ **Combining tags**: `(sad)(whispering) "I can't do this," (sighing) she said.`
- ❌ **Wrong**: `"I can't (sad) do this."` - emotion tag mid-sentence

**Formatting Rules:**
- Always use parentheses around tags
- Combine up to 3 tags maximum per sentence
- Match exact spelling from spec (case-sensitive)
- Can stack multiple emotion tags at start: `(sad)(nervous) Text here`

---

**Document Version:** 1.2
**Last Updated:** 2025-10-21
**Status:** Ready for Implementation

**Changelog:**
- v1.2: Changed agent personality to Lelouch (Code Geass alternate timeline), made dialogue more concise and strategic
- v1.1: Clarified emotion tag placement rules, updated UX to show diffs visually (not spoken), made text area editable
- v1.0: Initial version
