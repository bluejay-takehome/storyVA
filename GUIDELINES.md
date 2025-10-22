0:00 Hey guys, I'm Faraz, one of the co-founders here at BlueJ, and I'll be taking you through our BlueJ take home interview.
0:06 Um, so, in this interview, you're gonna be building a rag-enabled voice agent. As you know, BlueJ is the end-to-entesting platform for voice, and now text AI agents.
0:14 Um, so, as part of our take home process, you're gonna be- building your own voice agent, uhm, yourself. So, uh, as a quick high-level overview, what you're gonna be building here is a rag-enabled voice agent.
0:24 Uh, the idea is that it's gonna solve a personal problem in your life. So spend some time thinking about this.
0:29 Creativity's a really big part of this to take home interview, and I'm really interested to see what kind of cool stuff that you guys come up with.
0:34 Uhm, so here's some objectives. Overall, you're gonna create a voice agent with LiveKit, so that you can use to converse on a simple front-end, meaning that you have create a back-end, a front-end, and probably some kind of vector store integration for your rag-based approach.
0:48 Uh, you'll have to do tr- a transcription in speech, uh, in, uh, speech transcription in real time, so basically you're maintaining a live transcript that you're displaying in a React front-end.
0:55 Uhm, and this is, like, the really important part here, like, I want you to give your agent a personality to spin some kind of story and be creative.
1:02 Uhm, really put time into this part because I really- Really. I enjoy the creativity and the storytelling, uh, in this entire process, and it's really what puts you apart from other technical applicants, because a lot of people who are technically sound applied to the position, the ones who I think, 
1:13 uhm, get the position, uhm, in our books are the people- the people who are creative, the people who can tell a story and present, uhm, what they've built and- and the fun manner.
1:21 Um, so in the call, I want you to make a tool call of your choice that fits in with the narrative of your voice agent.
1:27 So, for example, if you're building, like, let's say, a basketball, uhm, voice agent, right, uhm, then- and then you're building a basketball coach, for example, the tool call could be like a list of nearby courts, right?
1:36 And that would be, like, a really cool way of, uh, enabling tool calls. So I do want to see your agent's ability to make a tool call based upon, you know, what the customer, what, basically, I say, throughout the call.
1:46 Um, then, of course, I want you to use RAG. So, enable your voice agent to answer a question from a large PDF document related to- your story.
1:53 So, for example, going back to this basketball coach voice, voice agent example, right, if you were building a voice agent that is a basketball coach, maybe one example of a RAG enabling- a RAG enabling tool, it would be like, uh, or one- one example of, you know, a way you can use RAG is by using a 
2:08 PDF of a book on s- Steve Kerr, uhm, and maybe you can ask your voice agent, hey, by the way, I need some tips on how to become better at basketball and Steve- in- in your voice agent could basically quote Steve Kerr, uh, in a paragraph from his book and say like, hey, by the way, Steve says to do this
2:21 , uhm, when you're in overtime. For example, right. Uh, to give optimal overtime strategies. So that's kind of like the objectives of the, uh, of the take home.
2:30 It's a high level. Um, but we also have some hardcore technical requirements. You know, this is what needs to be done for the back end.
2:35 This is what needs to be done for RAG right here. And this is what needs to be done for the front end.
2:41 There are a couple of strict requirements that we ask for you guys to use, uh, or to have inside the end of implementation.
2:46 But the general idea, once again, is that your back end is going to be built on LiveKit. You're going to be creating an agent.
2:51 Um, I want you to have a good understanding of the voice agent pipeline. So speech to text, uh, language models, of course.
2:57 Text to speech, voice activity detection, or VAD. Right. Uh, I want you guys to use RAG, of course. Um, and here's some like, you know, encouragement on stuff that you could use to make the RAG process easier for you.
3:07 This link right here is also going to be really useful. It's how you integrate your RAG system with LiveKit. Um, so that's going to be like the connector.
3:13 It's a for you. It's really simple. It's a couple lines of code. Um, and then the front end, of course, is going to be a React-based client.
3:19 Um, and it's going to have a start call button, a Live transcript, and an end call button. Um, optionally, if you would like, and it fits in with the story of your, you know, narrative.
3:27 Um, with a narrative. If it fits in with your narrative. Basically, you can add a PDF upload button that allows you to dynamically upload PDFs, as opposed to just hard coding it, but totally up to you.
3:36 Um, there are only a couple constraints here. You basically have to use LiveKit, uh, for the voice agent piece or the orchestration.
3:41 And then you have to use, and you can use whatever AI tools you want. Um, you can use Christian. So you can use, you know, like chat, GPT, whatever, the topic.
3:48 Do it, do whatever you need. Um, and, um, but, but if you do do it, just like, just document it.
3:53 I don't really care. We use AI tools tooling a lot here. I'm just curious to see how you guys are developing your take home.
3:59 Um, in terms of deliverables, right? The full, uhm, application code. So we're talking your Python backend with LiveKit, of course, your React frontend, and also a Vector Store, right?
4:09 I have that available for me to kind of review. The Vector Store itself, you don't have to like send me like, you know, a link to it.
4:14 You just have to have your backend connected. So I'll know that it existed, right? Umm, and I read meat, which is a short design document that explains how your system works, uhhm, your rag integration, and any trade-offs that you guys made, uhh, throughout the product, throughout the take-home.
4:28 So for example, if you decided to do like, you know, uhh, a certain chunking strategy that was like non-tradition. Or a certain, like, system design that was not traditional, uhh, please let me know about that and talk through the decisions.
4:38 Uhh, the actual, uhh, presentation portion will look like this. You'll come in, you'll tell me a story of what you built, you'll tell me why it was impactful to your life, you'll present it, you'll, like, live, so you'll have a conversation with it, we'll test your- ragged live and I will test your ragged
4:51 by asking one part of the PDF transcript, uhh, that I just randomly choose throughout the call. Uhm, and yeah, submit your, uhh, repo to my email, thanks.

## Overview

Build a RAG-enabled voice agent that solves a personal problem in your life. Use **LiveKit Cloud** for hosting the server.

## Objectives

- Create a voice agent with LiveKit that you can converse with on a custom (simple) frontend.
- Transcribe speech in real time, and maintain a live transcript.
- Give your agent a personality, **spin a story**. Be creative. **Put time into this part!** I will consider the creativity / story-telling to be your behavioral!
- In the call, **make a tool call of your choice** that fits in with the narrative of your voice agent.
    - EX: If you are building a basketball coach voice agent, tool call could be a list of nearby courts.
- Use RAG to enable your voice agent to answer a question from a large PDF document related to your story
    - EX: If you are building a basketball coach voice agent, use a PDF of a book on Steve Kerr to have your voice agent give advice on optimal OT strategies.
- Bonus points if you deploy your Agent on **AWS** instead of running it locally.

## Technical Requirements

### 1. [Backend] LiveKit Setup

- Deploy a LiveKit server or use LiveKit Cloud for server hosting.
- Build a LiveKit Agent that is capable of joining the room and having a live conversation with the user about a topic of your choice.
- The LiveKit agent can either be hosted locally or on AWS (bonus points for AWS).
- Use a voice agent pipeline with configurable STT, LLM, TTS, VAD.

### 2. [Backend] RAG Over Uploaded PDF

- Enable your voice agent to retrieve information from a large PDF of your choosing. Ensure the PDF is relevant to your overall voice agent story.
- Once uploaded, your agent should be able to **run Retrieval-Augmented Generation (RAG)** over the content of the PDF and answer questions about it **in real-time voice conversation**.
- I will ask about a **specific fact in a specific chapter**, so a proper RAG setup is essential — not just keyword search or summarization.
- You are **encouraged to use an existing RAG framework** (like LangChain, LlamaIndex, or OpenAI's retrieval tools) instead of building a vector store from scratch.
- This documentation will help you integrate the RAG system into your LiveKit Agent: [LiveKit Agents + External Data (Docs)](https://docs.livekit.io/agents/build/external-data/)

### 3. [Frontend] Chat Interface with Real-Time Transcription

- Build a **React-based client** with:
    - “Start Call” button.
    - **Live transcript** display that updates as participants speak.
    - “End Call” button.
    - Optionally, add a **PDF upload button** to the frontend *if* it fits your UX flow. No points lost if this feature is not there.

## Constraints

- Must use **LiveKit**.
- Use any AI tools you need/want, just document them.

## Deliverables

Submit a single **Git repository** containing:

1. **Full Application Code**
    - LiveKit Python backend (including RAG logic).
    - React frontend.
    - Vector store.
2. [**README.md**](http://readme.md/)
    - A short **design document** explaining:
        - How your system works end-to-end.
        - How RAG was integrated.
        - The tools/frameworks used.
    - **Setup instructions** to run the project locally or on the web.
3. **Design Decisions / Assumptions**
    - Describe:
        - Any trade-offs or limitations.
        - Hosting assumptions.
        - RAG assumptions (e.g., vector DB choice, chunking strategy, frameworks).
        - LiveKit agent design.

## Submission

Please **share the GitHub repo with `farazs27@gmail.com`** when you're done.