import { articleType } from "../types";
import { authors, authorSlugs } from "../authors";
import { categories, categorySlugs } from "../categories";
import { styles } from "../styles";
import { Citation, ReferenceList } from "../components/Citation";
import { ModelInfoTable } from "@/components/generate/ModelInfoTable";
import { MultilingualSupport } from "@/components/generate/MultilingualSupport";
import headerImg from "@/public/blog/how-[app name]-works/header.png";

// Define your references array for citations
const references = [
  {
    number: 1,
    text: "OpenAI Platform - Text-to-Speech Guide",
    url: "https://platform.openai.com/docs/guides/text-to-speech"
  },
  {
    number: 2,
    text: "Fish Audio - Text-to-Speech Platform",
    url: "https://fish.audio/"
  },
  {
    number: 3,
    text: "Zyphra - Zonos v0.1",
    url: "https://www.zyphra.com/post/beta-release-of-zonos-v0-1"
  },
  {
    number: 4,
    text: "RVC-Project - Retrieval-based Voice Conversion WebUI",
    url: "https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI"
  },
  {
    number: 5,
    text: "OpenAI Whisper - Automatic Speech Recognition",
    url: "https://github.com/openai/whisper"
  },
  {
    number: 6,
    text: "Modal - Serverless GPU Computing Platform",
    url: "https://modal.com/"
  },
  {
    number: 7,
    text: "Groq - Fast AI Inference Platform",
    url: "https://www.groq.com"
  },
  {
    number: 8,
    text: "SparkAudio - Spark TTS",
    url: "https://github.com/SparkAudio/Spark-TTS"
  },
];

const article: articleType = {
  slug: "how-[app name]-works",

  title: "How [app name] Works: The Tech Behind AI Voice Stories",

  description: "A dive into how [app name] works, from story parsing to AI voice cloning. Learn how we turn fanfiction and light-novels into immersive audio experiences.",

  categories: [
    categories.find(c => c.slug === categorySlugs.feature)!,
    categories.find(c => c.slug === categorySlugs.tutorial)!,
  ],

  author: authors.find(a => a.slug === authorSlugs.pranav)!,

  publishedAt: "2025-09-27",

  image: {
    src: headerImg,
    urlRelative: "/blog/how-[app name]-works/header.png",
    alt: "[app name] architecture diagram showing the flow from text to audio with AI voice cloning",
  },

  content: (
    <>
      {/* Introduction section */}
      <section>
        <p className={styles.p}>
          <strong>Hi! I&apos;m Pranav, the creator of [app name].</strong> I want to show you exactly how [app name] transforms your written stories into immersive audio experiences with distinct character voices. What started as a side project to fuel my desire to listen rather than read, has evolved into a sophisticated AI system that can handle hundreds of dialogue clips concurrently.
        </p>
      </section>

      <section>
        <h2 className={styles.h2}>The Core Challenge: Multicharacter Voice Cloned Emotive Narration</h2>
        <p className={styles.p}>
          The fundamental problem [app name] solves is simple to state but complex to execute: how do you take a written story with multiple characters and generate audio where each character has their own high quality, consistent voice associated with them? 
        </p>
        <p className={styles.p}>
          Ideally we want all of the following qualities in our system:
        </p>
        <ul className={styles.ul}>
          <li className={styles.li}>Multilingual</li>
          <li className={styles.li}>Accurate cloning</li>
          <li className={styles.li}>Excelling at nonlexical vocalizations</li>
          <li className={styles.li}>Clear</li>
          <li className={styles.li}>Emotive</li>
          <li className={styles.li}>Fun to listen to over a long period</li>
          <li className={styles.li}>Stable in long form</li>
          <li className={styles.li}>Supporting multiple overlapping speakers</li>
          <li className={styles.li}>Controllable</li>
          <li className={styles.li}>Fast</li>
          <li className={styles.li}>Affordable</li>
        </ul>
        <p className={styles.p}>We&apos;ll get into how to achieve all of these qualities in another article. First, let&apos;s understand how [app name] works.</p>
      </section>

      <section>
        <h2 className={styles.h2}>Step 1: Understanding Your Story with AI</h2>
        <p className={styles.p}>
          When you paste your story into [app name], the first thing that happens is <strong>AI-powered story parsing</strong>.
        </p>

        <h3 className={styles.h3}>Character Detection</h3>
        <p className={styles.p}>
          The system uses AI to identify every unique character in your story. It&apos;s smart enough to recognize when &quot;Harry&quot;, &quot;Mr. Potter&quot;, and &quot;The Boy Who Lived&quot; all refer to the same character.
        </p>

        <h3 className={styles.h3}>Dialogue Extraction & Attribution</h3>
        <p className={styles.p}>
          Next comes: extracting dialogue. In order to narrate, we need to know what each speaking character is saying. [app name] uses AI alongside the character list from the previous step to extract the dialogue. This is quite tricky, as dialogue attribution is not always obvious. Consider this challenging example which a user submitted for debugging:
        </p>

        <div className={styles.code}>
{`"We need to get this to Dumbledore," Harry said urgently.

"Are you mad?" The response was immediate. "It's past midnight."

Ron glanced nervously at the corridor. "What if we get caught?"

"We won't," he followed.

Hermione had been quiet up till now. "This is incredibly dangerous."

"So is doing nothing," he muttered.

"Fine," she muttered. "But if we end up in detention..."

"We won't," Harry repeated, already moving toward the portrait hole.`}
        </div>

        <p className={styles.p}>
          While humans can do a decent job following the conversation flow, several lines lack explicit speaker tags. Who gave the &quot;immediate&quot; response? Who said &quot;We won&apos;t&quot;? Who muttered &quot;So is doing nothing&quot;?
          </p>
          <p className={styles.p}>
          Hermione and Ron are the most likely to say &quot;Are you mad?&quot; but since Ron later says &quot;What if we get caught?&quot; we can attribute the previous dialogue to him. Regarding the &quot;So is doing nothing,&quot; we know it is said by a &quot;he&quot;, so it could be either Ron or Harry, but given Harry&apos;s decisiveness, we can attribute it to him.
          </p>
          <p className={styles.p}>
          [app name]&apos;s AI analyzes conversation patterns, character personalities, and contextual clues to correctly parse this into individual dialogue clips:
        </p>

        <div className="max-h-48 overflow-y-auto border border-base-300 rounded-box mb-4">
          <pre className="text-sm font-mono bg-neutral text-neutral-content p-4 m-0 overflow-x-scroll select-all">
{`[
  {
    "text": "We need to get this to Dumbledore,",
    "speaker": "Harry"
  },
  {
    "text": "Harry said urgently.",
    "speaker": "Narrator"
  },
  {
    "text": "Are you mad?",
    "speaker": "Ron"
  },
  {
    "text": "The response was immediate.",
    "speaker": "Narrator"
  },
  {
    "text": "It's past midnight.",
    "speaker": "Ron"
  },
  {
    "text": "Ron glanced nervously at the corridor.",
    "speaker": "Narrator"
  },
  {
    "text": "What if we get caught?",
    "speaker": "Ron"
  },
  {
    "text": "We won't,",
    "speaker": "Harry"
  },
  {
    "text": "he followed.",
    "speaker": "Narrator"
  },
  {
    "text": "Hermione had been quiet up till now.",
    "speaker": "Narrator"
  },
  {
    "text": "This is incredibly dangerous.",
    "speaker": "Hermione"
  },
  {
    "text": "So is doing nothing,",
    "speaker": "Harry"
  },
  {
    "text": "he muttered.",
    "speaker": "Narrator"
  },
  {
    "text": "Fine,",
    "speaker": "Hermione"
  },
  {
    "text": "she muttered.",
    "speaker": "Narrator"
  },
  {
    "text": "But if we end up in detention...",
    "speaker": "Hermione"
  },
  {
    "text": "We won't,",
    "speaker": "Harry"
  },
  {
    "text": "Harry repeated, already moving toward the portrait hole.",
    "speaker": "Narrator"
  }
]`}
          </pre>
        </div>

        <p className={styles.p}>
          This step might take 1-2 minutes, or longer for longer stories. There are further optimizations that could be made to cut this down to ~10 seconds. i.e. finetuning an LLM on this task and running it on groq<Citation number={7} />. As [app name] gets more popular, I&apos;ll work on adding this.
          </p>
          <p className={styles.p}>
          Now then, each dialogue speaker pair is almost ready to be narrated.
        </p>

      <h3 className={styles.h3}>Voice Assignment</h3>
      <p className={styles.p}>
        Ok, we know that Harry said &quot;We need to get this to Dumbledore,&quot; but... who is Harry? Harry is more than just a name. Harry is a character, with a personality, a voice, and a role in the story. In order to narrate immersively, we can&apos;t just assign a random voice to Harry. We need to assign a voice that is appropriate for Harry&apos;s personality and role in the story.
      </p>
      <p className={styles.p}>There are two scenarios:</p>

      <ol className="list-decimal list-outside text-base-content/90 leading-relaxed mb-4 pl-6">
        <li className="mb-2">Some user has added a public voice for &quot;Harry Potter&quot; on <a href="https://[app name].com/dashboard/voices" className={styles.a}>My Voices</a></li>
        <li className="mb-2">No one has added a voice for &quot;Harry Potter&quot;</li>
      </ol>

      <p className={styles.p}>In the first scenario, AI is smart enough to associate &quot;Harry Potter&quot; the voice to &quot;Harry&quot; the character in the story.</p>
      <p className={styles.p}>In the second scenario, AI uses the name, description, and tags of each public voice to assign the most appropriate voice to &quot;Harry&quot;. It will, for example, opt for a male british accented voice, if such a voice is available.</p>
      <p className={styles.p}>And of course privately set voices are also available only to you.</p>

      <p className={styles.p}>Here&apos;s what the AI suggested for our Harry Potter example:</p>

      <div className="max-h-48 overflow-y-auto border border-base-300 rounded-box mb-4">
        <pre className="text-sm font-mono bg-neutral text-neutral-content p-4 m-0 overflow-x-scroll select-all">
{`{
  "suggested_character_voices": {
    "Ron": {
      "model": "LW3",
      "voice_id": "b4cddece-a29d-4652-94cf-1c0d80b4f380",
      "voice_name": "Draco Malfoy"
    },
    "Harry": {
      "model": "LW6",
      "voice_id": "b03285ef-ade9-4785-aff1-ec07accc1735",
      "voice_name": "Harry Potter"
    },
    "Hermione": {
      "model": "LW3",
      "voice_id": "1f9b9aef-41af-455c-822d-5dd0b4cc257e",
      "voice_name": "Alice (Alice in Wonderland)"
    },
    "Narrator": {
      "model": "LW3",
      "voice_id": "5591864d-cfaf-490e-88e5-586e956847c3",
      "voice_name": "Narrator"
    },
    "Dumbledore": {
      "model": "LW3",
      "voice_id": "76370ff9-1de1-48ab-9d64-a5b345584d1b",
      "voice_name": "Zhongli"
    }
  }
}`}
        </pre>
      </div>

      <p className={styles.p}>Notice how the AI found a &quot;Harry Potter&quot; voice match, but creatively assigned &quot;Draco Malfoy&quot; to Ron and &quot;Alice&quot; to Hermione based on voice characteristics and availability. Even Dumbledore gets paired with &quot;Zhongli&quot; - a wise, authoritative voice that fits the character. This is because no user has uploaded a Ron/Hermione/Dumbledore voice.</p>

      <p className={styles.p}>Also note the voice ids: There can be multiple voices with the same name, so voice ids are used to uniquely identify a voice during assignment.</p>

      <p className={styles.p}>Additionally, you can see the models that were suggested for each voice. Different AI labs release different models for voice cloning and text to speech, and these different models perform differently on different voices. The AI is not too good at suggesting models right now, so before you generate audio, you have the option to tweak the AI&apos;s suggestions, both the voice model and the voice itself.</p>

      <p className={styles.p}>Here&apos;s a breakdown of the voice models available in [app name] and their characteristics:</p>

      <div className="my-6 flex justify-center">
        <ModelInfoTable availableAliases={['LW1', 'LW2', 'LW3', 'LW6', 'LW7']} showBorders={true} />
      </div>

      <p className={styles.p}>As you can see, each model has different strengths. LW3 (gpt-4o-mini-tts+rvc) excels at emotion and character accuracy, while LW1 (tts-1+rvc) offers the best quality and reliability. The AI tries to match the best model for each voice, but you have the final say in the generation process.</p>

      <MultilingualSupport />

      </section>

      <section>
        <h2 className={styles.h2}>Step 2: Narrating Your Story with AI</h2>
        <p className={styles.p}>
          Now that we have the dialogue and the voices selected, we can start narrating the story.
        </p>
        <h3 className={styles.h3}>Narration</h3>
        <p className={styles.p}>
          When you click Generate Audio, each Speaker, Dialogue, Text, Voice, and Voice Model combo is sent to the specified voice model to be synthesized.
          However, that&apos;s not enough. Context is crucial for emotionally immersive TTS. Take the following example:
        </p>

        <div className={styles.code}>
{`"I can't believe this is happening," Donald said.

Donald's face crumpled, and he turned away from her, his shoulders shaking with sobs. "I can't believe you're doing this to me."

Ariana reached out to touch his arm, but he pulled away from her. "Donald, please. Don't be like this."

Donald spun around to face her, his eyes blazing with anger. "No, Ariana. We can't. You've made your decision, and I have to respect that."`}
        </div>

        <p className={styles.p}>
          Notice how Donald&apos;s first &quot;I can&apos;t believe this is happening&quot; should be voiced with devastation and tears (&quot;his shoulders shaking with sobs&quot;), while his later dialogue should sound cold and angry (&quot;his eyes blazing with anger&quot;). Without the surrounding context, a TTS system might generate both lines with the same emotional tone, missing the dramatic arc of the conversation.
        </p>

        <p className={styles.p}>
          [app name]&apos;s AI analyzes the emotional context surrounding each line to guide the voice model&apos;s emotional expression. Here&apos;s which models support emotional steering:
        </p>

        <h4 className={styles.h3}>Models WITH Emotional Control:</h4>
        <ul className={styles.ul}>
          <li className={styles.li}><strong>LW2 (zyphra zonos-v0.1)</strong><Citation number={3} />: Uses 8-dimensional emotion weights including happiness, sadness, anger, fear, surprise, disgust, neutral, and other. The AI analyzes story context to automatically set appropriate emotion levels for each dialogue line. One shot voice cloning.</li>
          <li className={styles.li}><strong>LW3 (gpt-4o-mini-tts)</strong><Citation number={1} />: Employs contextual instructions based on story analysis. The system examines surrounding dialogue and narrative to generate natural language instructions that guide emotional delivery. Training based voice cloning.</li>
        </ul>

        <h4 className={styles.h3}>Models WITHOUT Emotional Control:</h4>
        <ul className={styles.ul}>
          <li className={styles.li}><strong>LW1 (tts-1+rvc)</strong><Citation number={1} /><Citation number={4} />: Training based voice cloning</li>
          <li className={styles.li}><strong>LW6 (fishaudio)</strong><Citation number={2} />: One shot voice cloning</li>
          <li className={styles.li}><strong>LW7 (sparktts)</strong><Citation number={8} />: One shot voice cloning. While the underlying technology supports 24 emotion categories, [app name]&apos;s current implementation doesn&apos;t use contextual emotion analysis.</li>
        </ul>

        <p className={styles.p}>
          That&apos;s not to say tts-1 or fishaudio are bad by any means because they don&apos;t get context-dependent emotional steering, they are great. There are tradeoffs to be made. I myself prefer tts-1 for the Narrator for the cadence consistency.
        </p>

        <h3 className={styles.h3}>Error Handling</h3>
        <p className={styles.p}>What do you do when the voice model messes up? Zyphra zonos-v0.1 for example often cuts out syllables near the start or end of the line. We use whisper<Citation number={5} /> to transcribe the audio and check if the generation was successful. If not, we try again a few times. If it continues to fail, we fall back to a different voice model. That&apos;s the core -- try again, and fallback if needed.</p>
        <p className={styles.p}>
          Retries slow things down, but ultimately we want high quality results. Usually it&apos;s not too bad. Though zonos is quite unreliable. I actually interviewed with them -- shoutout to them! They built a good product, though they totally should have hired me to make things reliable.
        </p>
        <p>And of course, error tracking! Errors are logged for review.</p>

        <h3 className={styles.h3}>Speed</h3>
        <p>Some of these models run on external services, some run on serverless infrastructure. Nonetheless requests are distributed for speed! Shoutout to Modal<Citation number={6} />. Originally I used Runpod and Google Cloud Run, but --- they were too slow. + Modal gave me a bunch of free credits. I love them. When each request completes, the client (your browser) pulls in the audio and concatenates it. As soon as the first dialogue clip is complete, you can start listening!</p>

        <h3 className={styles.h3}>Time to listen!</h3>
        <p>Your audio is ready to listen to, and you can optionally download as a .wav or download the .srt file as desired.</p>
      </section>


      <section>
        <h2 className={styles.h2}>Try It Yourself!</h2>
        <p className={styles.p}>
          The best way to understand [app name] is to experience it. Head over to the <strong><a href="https://[app name].com/generate" className={styles.a}>Generate page</a></strong>, paste in your favorite fanfiction, light novel, or short story, and watch as AI brings your favorite characters into the audio domain with immersion. We have a generous English-supported free tier with SparkTTS, so you can experiment without any commitment.
        </p>
        <p className={styles.p}>
          Whether you&apos;re a fanfiction writer wanting to hear your stories aloud, a light novel reader looking for narration tools, or just curious about AI voice technology, [app name] offers something unique: the ability to transform any text into an immersive audio experience with distinct character voices, all in just a few clicks.
        </p>
        <p className={styles.p}>
          <strong>Happy story telling!</strong> And if you have any questions or feedback, feel free to reach out. I&apos;m always excited to hear how people are using [app name] and what features they&apos;d like to see next.
        </p>

        <h3 className={styles.h3}>Note</h3>
        <p>Impersonation or nefarious use is not allowed! This is for recreation and personal use. [app name] is not affiliated with, nor does it claim ownership of, any user-uploaded voices. As highlighted in this article, [app name] is input and voice agnostic system. Examples given are for illustration purposes only.</p>
      </section>

      {/* References section - automatically styled */}
      <ReferenceList references={references} />
    </>
  ),
};

export default article;