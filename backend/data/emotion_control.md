# Fish Audio Emotion Control Tags - Complete Reference

## Overview

Fish Audio TTS supports 60+ emotion tags for fine-grained control over vocal delivery.
This document serves as the authoritative reference for StoryVA emotion markup validation.

## Tag Categories

### Basic Emotions (24 tags)
- happy
- sad
- angry
- excited
- calm
- nervous
- confident
- surprised
- satisfied
- delighted
- scared
- worried
- upset
- frustrated
- depressed
- empathetic
- embarrassed
- disgusted
- moved
- proud
- relaxed
- grateful
- curious
- sarcastic

### Advanced Emotions (25 tags)
- disdainful
- unhappy
- anxious
- hysterical
- indifferent
- uncertain
- doubtful
- confused
- disappointed
- regretful
- guilty
- ashamed
- jealous
- envious
- hopeful
- optimistic
- pessimistic
- nostalgic
- lonely
- bored
- contemptuous
- sympathetic
- compassionate
- determined
- resigned

### Tone Markers (5 tags)
- in a hurry tone
- shouting
- screaming
- whispering
- soft tone

### Audio Effects (10 tags)
- laughing
- chuckling
- sobbing
- crying loudly
- sighing
- groaning
- panting
- gasping
- yawning
- snoring

### Special Effects (3 tags)
- audience laughing
- background laughter
- crowd laughing
- break
- long-break

## Placement Rules (CRITICAL for English)

### ✅ Emotion Tags - MUST be at sentence start
```
(sad) "I can't do this anymore."
(angry)(frustrated) "Why did you do that?"
```

### ✅ Tone Markers - Can go anywhere
```
"I can't (whispering) tell you."
(soft tone) "Please, listen to me."
```

### ✅ Audio Effects - Can go anywhere
```
"I can't do this," (sighing) she said.
"Ha ha!" (laughing) he exclaimed.
```

### ✅ Special Effects - Can go anywhere
```
She paused (break) before answering.
The room filled with (audience laughing) laughter.
```

### ❌ INVALID Placements
```
# Emotion tag mid-sentence (WRONG)
"I can't (sad) do this."

# Emotion tag at end (WRONG)
"I can't do this." (sad)
```

## Combining Tags

### Rules
- Maximum 3 tags per sentence
- Emotion tags stack at start: `(sad)(nervous) Text`
- Mix emotions with tone/effects: `(sad)(whispering) "Text" (sighing)`

### Examples
```
(disappointed)(soft tone) "I thought you'd understand," (sighing) she whispered.
(excited)(shouting) "We won!" (laughing) she yelled.
(regretful)(whispering) "I'm sorry," he said, (crying loudly) quietly.
```

## Validation Checklist

For StoryVA emotion validator:

1. **Tag Existence:** Is the tag in the official list above?
2. **Tag Placement:**
   - Emotion tags → Must be at sentence start
   - Tone markers → Anywhere OK
   - Audio effects → Anywhere OK
   - Special effects → Anywhere OK
3. **Tag Count:** Maximum 3 tags per sentence
4. **Format:** Tags must use parentheses: `(tag_name)`
5. **Spelling:** Exact match required (case-sensitive for some systems)

## Common Mistakes

1. **Emotion mid-sentence:** `"I'm (sad) leaving"` → `(sad) "I'm leaving"`
2. **Invalid tag name:** `(very sad)` → `(sad)` (no modifiers)
3. **Too many tags:** `(sad)(angry)(nervous)(tired)` → Max 3 tags
4. **Missing parentheses:** `sad "I'm leaving"` → `(sad) "I'm leaving"`
5. **Wrong category placement:** Treating tone markers like emotions

## Source Reference

Based on Fish Audio official emotion control specification and PRD.md Appendix A.

**Last Updated:** October 22, 2025
