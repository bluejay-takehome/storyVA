"""
Session state management for StoryVA agent.

Tracks story text, pending diffs, and conversation metadata.
"""
from dataclasses import dataclass, field


@dataclass
class StoryState:
    """User session state for voice director conversation."""

    # Current story text (editable by user)
    current_text: str = ""

    # Pending diff suggestion from agent
    pending_diff: dict | None = None

    # History of applied diffs (for potential undo feature)
    applied_diffs: list[dict] = field(default_factory=list)

    # Conversation metadata (context, preferences, etc.)
    conversation_metadata: dict = field(default_factory=dict)

    def __repr__(self):
        """String representation for debugging."""
        return (
            f"StoryState("
            f"text_length={len(self.current_text)}, "
            f"has_pending_diff={self.pending_diff is not None}, "
            f"applied_diffs_count={len(self.applied_diffs)}"
            f")"
        )
