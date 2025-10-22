# Emotion Control

> Add natural emotions and expressions to your AI-generated speech

## Overview

Fish Audio models support 64+ emotional expressions and voice styles that can be controlled through text markers in your input. Add natural pauses, laughter, and other human-like elements to make speech more engaging and realistic.

## How It Works

Simply wrap emotion tags in parentheses within your text:

```
(happy) What a beautiful day!
(sad) I'm sorry to hear that.
(excited) This is amazing news!
```

The TTS models will automatically recognize these markers and adjust the voice accordingly.

## Complete Emotion Reference

### Basic Emotions (24 expressions)

| Emotion     | Tag             | Description             | Example Context             |
| ----------- | --------------- | ----------------------- | --------------------------- |
| Happy       | `(happy)`       | Cheerful, upbeat tone   | Good news, greetings        |
| Sad         | `(sad)`         | Melancholic, downcast   | Sympathy, bad news          |
| Angry       | `(angry)`       | Frustrated, aggressive  | Complaints, warnings        |
| Excited     | `(excited)`     | Energetic, enthusiastic | Announcements, celebrations |
| Calm        | `(calm)`        | Peaceful, relaxed       | Instructions, meditation    |
| Nervous     | `(nervous)`     | Anxious, uncertain      | Disclaimers, apologies      |
| Confident   | `(confident)`   | Assertive, self-assured | Presentations, sales        |
| Surprised   | `(surprised)`   | Shocked, amazed         | Reactions, discoveries      |
| Satisfied   | `(satisfied)`   | Content, pleased        | Confirmations, reviews      |
| Delighted   | `(delighted)`   | Very pleased, joyful    | Celebrations, compliments   |
| Scared      | `(scared)`      | Frightened, fearful     | Warnings, horror stories    |
| Worried     | `(worried)`     | Concerned, troubled     | Concerns, questions         |
| Upset       | `(upset)`       | Disturbed, distressed   | Complaints, problems        |
| Frustrated  | `(frustrated)`  | Annoyed, exasperated    | Technical issues, delays    |
| Depressed   | `(depressed)`   | Very sad, hopeless      | Serious topics              |
| Empathetic  | `(empathetic)`  | Understanding, caring   | Support, counseling         |
| Embarrassed | `(embarrassed)` | Ashamed, awkward        | Apologies, mistakes         |
| Disgusted   | `(disgusted)`   | Repelled, revolted      | Negative reviews            |
| Moved       | `(moved)`       | Emotionally touched     | Heartfelt moments           |
| Proud       | `(proud)`       | Accomplished, satisfied | Achievements, praise        |
| Relaxed     | `(relaxed)`     | At ease, casual         | Casual conversation         |
| Grateful    | `(grateful)`    | Thankful, appreciative  | Thanks, appreciation        |
| Curious     | `(curious)`     | Inquisitive, interested | Questions, exploration      |
| Sarcastic   | `(sarcastic)`   | Ironic, mocking         | Humor, criticism            |

### Advanced Emotions (25 expressions)

| Emotion       | Tag               | Description              | Example Context        |
| ------------- | ----------------- | ------------------------ | ---------------------- |
| Disdainful    | `(disdainful)`    | Contemptuous, scornful   | Criticism, rejection   |
| Unhappy       | `(unhappy)`       | Discontent, dissatisfied | Complaints, feedback   |
| Anxious       | `(anxious)`       | Very worried, uneasy     | Urgent matters         |
| Hysterical    | `(hysterical)`    | Uncontrollably emotional | Extreme reactions      |
| Indifferent   | `(indifferent)`   | Uncaring, neutral        | Neutral responses      |
| Uncertain     | `(uncertain)`     | Doubtful, unsure         | Speculation, questions |
| Doubtful      | `(doubtful)`      | Skeptical, questioning   | Disbelief, questioning |
| Confused      | `(confused)`      | Puzzled, perplexed       | Clarification requests |
| Disappointed  | `(disappointed)`  | Let down, dissatisfied   | Unmet expectations     |
| Regretful     | `(regretful)`     | Sorry, remorseful        | Apologies, mistakes    |
| Guilty        | `(guilty)`        | Culpable, responsible    | Confessions, apologies |
| Ashamed       | `(ashamed)`       | Deeply embarrassed       | Serious mistakes       |
| Jealous       | `(jealous)`       | Envious, resentful       | Comparisons            |
| Envious       | `(envious)`       | Wanting what others have | Admiration with desire |
| Hopeful       | `(hopeful)`       | Optimistic about future  | Future plans           |
| Optimistic    | `(optimistic)`    | Positive outlook         | Encouragement          |
| Pessimistic   | `(pessimistic)`   | Negative outlook         | Warnings, doubts       |
| Nostalgic     | `(nostalgic)`     | Longing for the past     | Memories, stories      |
| Lonely        | `(lonely)`        | Isolated, alone          | Emotional content      |
| Bored         | `(bored)`         | Uninterested, weary      | Disinterest            |
| Contemptuous  | `(contemptuous)`  | Showing contempt         | Strong criticism       |
| Sympathetic   | `(sympathetic)`   | Showing sympathy         | Condolences            |
| Compassionate | `(compassionate)` | Showing deep care        | Support, help          |
| Determined    | `(determined)`    | Resolved, decided        | Goals, commitments     |
| Resigned      | `(resigned)`      | Accepting defeat         | Giving up, acceptance  |

### Tone Markers (5 expressions)

Control volume and intensity:

| Tone       | Tag                 | Description          | When to Use                |
| ---------- | ------------------- | -------------------- | -------------------------- |
| Hurried    | `(in a hurry tone)` | Rushed, urgent       | Time-sensitive information |
| Shouting   | `(shouting)`        | Loud, calling out    | Getting attention          |
| Screaming  | `(screaming)`       | Very loud, panicked  | Emergencies, fear          |
| Whispering | `(whispering)`      | Very soft, secretive | Secrets, quiet scenes      |
| Soft       | `(soft tone)`       | Gentle, quiet        | Comfort, lullabies         |

### Audio Effects (10 expressions)

Add natural human sounds:

| Effect        | Tag               | Description                  | Suggested Text |
| ------------- | ----------------- | ---------------------------- | -------------- |
| Laughing      | `(laughing)`      | Full laughter                | Ha, ha, ha     |
| Chuckling     | `(chuckling)`     | Light laugh                  | Heh, heh       |
| Sobbing       | `(sobbing)`       | Crying heavily               | (optional)     |
| Crying Loudly | `(crying loudly)` | Intense crying               | (optional)     |
| Sighing       | `(sighing)`       | Exhale of relief/frustration | sigh           |
| Groaning      | `(groaning)`      | Sound of frustration         | ugh            |
| Panting       | `(panting)`       | Out of breath                | huff, puff     |
| Gasping       | `(gasping)`       | Sharp intake of breath       | gasp           |
| Yawning       | `(yawning)`       | Tired sound                  | yawn           |
| Snoring       | `(snoring)`       | Sleep sound                  | zzz            |

### Special Effects

Additional markers for atmosphere and context:

| Effect              | Tag                     | Description              |
| ------------------- | ----------------------- | ------------------------ |
| Audience Laughter   | `(audience laughing)`   | Crowd laughing sound     |
| Background Laughter | `(background laughter)` | Ambient laughter         |
| Crowd Laughter      | `(crowd laughing)`      | Large group laughing     |
| Short Pause         | `(break)`               | Brief pause in speech    |
| Long Pause          | `(long-break)`          | Extended pause in speech |

You can also use natural expressions like "Ha,ha,ha" for laughter without tags.

## Usage Guidelines

### Placement Rules

**For English and Most Languages:**

* Emotion tags MUST go at the beginning of sentences
* Tone controls can go anywhere in the text
* Sound effects can go anywhere in the text

**Correct:**

```
(happy) What a wonderful day!
```

**Incorrect:**

```
What a (happy) wonderful day!
```

### Combining Effects

You can layer multiple emotions for complex expressions:

```
(sad)(whispering) I miss you so much.
(angry)(shouting) Get out of here now!
(excited)(laughing) We won! Ha ha!
```

### Sequential Emotions

Change emotions throughout your text:

```
(excited) We're launching tomorrow!
(nervous) I hope everything goes smoothly.
(confident) But I know we're ready!
```

## Advanced Techniques

### Emotion Transitions

Create natural emotional progressions:

```
(happy) I got the promotion!
(uncertain) But... it means relocating.
(sad) I'll miss everyone here.
(hopeful) Though it's a great opportunity.
(determined) I'm going to make it work!
```

### Background Effects

Add atmospheric sounds:

```
The comedy show was amazing (audience laughing)
Everyone was having fun (background laughter)
The crowd loved it (crowd laughing)
```

### Intensity Modifiers

Fine-tune emotional intensity with descriptive modifiers:

```
(slightly sad) I'm a bit disappointed.
(very excited) This is absolutely amazing!
(extremely angry) This is unacceptable!
```

## Language Support

All 30+ supported languages can use emotion markers:

* **English, Spanish, French, German**: Emotions must be at sentence start
* **Chinese, Japanese, Korean**: More flexible placement allowed
* **Arabic, Hebrew**: Right-to-left text considerations apply

## Best Practices

### Do's

* Use one primary emotion per sentence
* Test different emotion combinations
* Match emotions to context logically
* Add appropriate text after sound effects (e.g., "Ha ha" after laughing)
* Use natural expressions when possible
* Space out emotional changes for realism

### Don'ts

* Don't overuse emotion tags in short text
* Don't mix conflicting emotions
* Don't create custom tags - use only supported ones
* Don't forget parentheses
* Don't place emotion tags mid-sentence in English

## Common Use Cases

### Customer Service

```
(friendly) Hello! How can I help you today?
(empathetic) I understand your frustration.
(confident) I'll resolve this for you right away.
(grateful) Thank you for your patience!
```

### Storytelling

```
(narrator) Once upon a time...
(mysterious)(whispering) The old house stood silent.
(scared) "Is anyone there?" she called out.
(relieved)(sighing) No one answered. Phew.
```

### Educational Content

```
(enthusiastic) Welcome to today's lesson!
(curious) Have you ever wondered why?
(encouraging) That's a great question!
(proud) Excellent work!
```

### Marketing & Sales

```
(excited) Introducing our newest product!
(confident) You won't find better quality anywhere.
(urgent) Limited time offer!
(satisfied) Join thousands of happy customers!
```

## Troubleshooting

### Emotion Not Working?

1. **Check placement** - Emotions must be at the beginning of sentences for English
2. **Verify spelling** - Tags must match exactly as listed
3. **Include parentheses** - Tags must be wrapped in parentheses

### Unnatural Sound?

* Space out emotional changes
* Use appropriate intensity
* Test with different voices
* Add context text after sound effects

### Performance Notes

* Emotion markers don't count toward token limits
* No additional latency for emotion processing
* All emotions available on all pricing tiers
* Maximum of 3 combined emotions per sentence recommended

## Quick Reference Tables

### Emotion Intensity Scale

| Base Emotion | Mild         | Moderate | Intense   |
| ------------ | ------------ | -------- | --------- |
| Happy        | satisfied    | happy    | delighted |
| Sad          | disappointed | sad      | depressed |
| Angry        | frustrated   | angry    | furious   |
| Scared       | nervous      | scared   | terrified |
| Excited      | interested   | excited  | ecstatic  |

### Common Combinations

| Scenario         | Emotion Combo            | Example                               |
| ---------------- | ------------------------ | ------------------------------------- |
| Whispered Secret | (mysterious)(whispering) | "I have something to tell you..."     |
| Angry Shout      | (angry)(shouting)        | "Stop right there!"                   |
| Sad Sigh         | (sad)(sighing)           | "I wish things were different. Sigh." |
| Excited Laugh    | (excited)(laughing)      | "We did it! Ha ha!"                   |
| Nervous Question | (nervous)(uncertain)     | "Are you sure about this?"            |

## See Also

* [Emotion Reference Guide](/resources/emotion-reference) - Complete emotion list with examples
* [API Reference](/api-reference/introduction) - Implementation details
* [Text-to-Speech Best Practices](/resources/best-practices/text-to-speech)
