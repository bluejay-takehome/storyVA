/**
 * StoryVA Application Configuration
 *
 * This configuration defines the app metadata and agent settings
 * that connect the frontend to the LiveKit backend.
 */

export interface AppConfig {
  /**
   * Page title shown in browser tab
   */
  pageTitle: string;

  /**
   * Page description for SEO and metadata
   */
  pageDescription: string;

  /**
   * Agent name that matches backend/main.py worker registration
   * This must match the agent name registered in LiveKit
   */
  agentName: string;

  /**
   * Text shown on the start button in WelcomeView
   */
  startButtonText: string;

  /**
   * Introductory text shown to users before starting
   */
  welcomeMessage: string;

  /**
   * Agent personality description (shown in UI)
   */
  agentDescription: string;
}

export const APP_CONFIG: AppConfig = {
  pageTitle: 'StoryVA - Voice Director',
  pageDescription: 'AI voice director powered by Lelouch - Add Fish Audio emotion markup to your stories',
  agentName: 'storyva-voice-director',
  startButtonText: 'Start Direction Session',
  welcomeMessage: 'Welcome to StoryVA',
  agentDescription:
    'Lelouch is a brilliant strategist turned voice director. ' +
    'He helps writers add professional emotion markup to their stories using Fish Audio\'s TTS system. ' +
    'Paste your story below, then start a session to receive expert guidance.',
};
