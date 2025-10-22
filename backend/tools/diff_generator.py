"""
Diff Generator for Emotion Markup

Creates structured diffs between original text and emotion-marked text
for display in the frontend.
"""
import difflib
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import json


@dataclass
class DiffLine:
    """Single line in a diff."""
    type: str  # "unchanged", "removed", "added", "modified"
    original: str
    proposed: str
    line_number: int


@dataclass
class EmotionDiff:
    """
    Structured diff for emotion markup changes.

    Attributes:
        original_text: Original text without markup
        proposed_text: Text with emotion markup applied
        changes: List of changes made
        summary: Human-readable summary of changes
    """
    original_text: str
    proposed_text: str
    changes: List[Dict[str, str]]
    summary: str

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)

    def to_json(self) -> str:
        """Convert to JSON string for transmission."""
        return json.dumps(self.to_dict(), indent=2)


def generate_emotion_diff(
    original_text: str,
    proposed_text: str,
    explanation: Optional[str] = None
) -> EmotionDiff:
    """
    Generate a structured diff between original and emotion-marked text.

    Args:
        original_text: Text without emotion markup
        proposed_text: Text with emotion markup tags applied
        explanation: Optional explanation of why changes were made

    Returns:
        EmotionDiff object with structured changes

    Example:
        >>> original = '"I hate you," she said.'
        >>> proposed = '(sad)(soft tone) "I hate you," (sighing) she said.'
        >>> diff = generate_emotion_diff(original, proposed)
        >>> print(diff.summary)
        "Added 3 emotion tags: (sad), (soft tone), (sighing)"
    """
    # Extract added tags
    added_tags = extract_added_tags(original_text, proposed_text)

    # Generate change list
    changes = []

    if original_text != proposed_text:
        changes.append({
            "type": "emotion_markup_added",
            "original": original_text,
            "proposed": proposed_text,
            "tags_added": added_tags,
        })

    # Generate summary
    if added_tags:
        tags_str = ", ".join([f"({tag})" for tag in added_tags])
        if len(added_tags) == 1:
            summary = f"Added emotion tag: {tags_str}"
        else:
            summary = f"Added {len(added_tags)} emotion tags: {tags_str}"

        if explanation:
            summary += f"\n\nRationale: {explanation}"
    else:
        summary = "No changes made"

    return EmotionDiff(
        original_text=original_text,
        proposed_text=proposed_text,
        changes=changes,
        summary=summary
    )


def extract_added_tags(original: str, proposed: str) -> List[str]:
    """
    Extract emotion tags that were added to the text.

    Args:
        original: Original text
        proposed: Text with tags

    Returns:
        List of tag names (without parentheses)

    Example:
        >>> extract_added_tags("Hello", "(happy) Hello")
        ["happy"]
    """
    import re

    # Extract all tags from proposed text
    tag_pattern = r'\(([^)]+)\)'
    proposed_tags = re.findall(tag_pattern, proposed)

    # Extract all tags from original (in case original had tags)
    original_tags = re.findall(tag_pattern, original)

    # Find tags that were added
    added_tags = []
    for tag in proposed_tags:
        if tag not in original_tags or proposed_tags.count(tag) > original_tags.count(tag):
            added_tags.append(tag)

    return added_tags


def create_inline_diff_html(original: str, proposed: str) -> str:
    """
    Create an HTML representation of inline diff (for frontend display).

    Args:
        original: Original text
        proposed: Proposed text with markup

    Returns:
        HTML string with spans for added/removed content

    Example:
        >>> create_inline_diff_html("Hello", "(happy) Hello")
        '<span class="added">(happy) </span>Hello'
    """
    # Use difflib to find differences
    matcher = difflib.SequenceMatcher(None, original, proposed)

    html_parts = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            html_parts.append(original[i1:i2])
        elif tag == 'replace':
            html_parts.append(f'<span class="removed">{original[i1:i2]}</span>')
            html_parts.append(f'<span class="added">{proposed[j1:j2]}</span>')
        elif tag == 'delete':
            html_parts.append(f'<span class="removed">{original[i1:i2]}</span>')
        elif tag == 'insert':
            html_parts.append(f'<span class="added">{proposed[j1:j2]}</span>')

    return ''.join(html_parts)


def generate_simple_diff(original: str, proposed: str) -> Dict[str, str]:
    """
    Generate a simple diff dictionary (minimal format for API).

    Args:
        original: Original text
        proposed: Proposed text

    Returns:
        Dictionary with original, proposed, and changes

    Example:
        >>> generate_simple_diff("Hello", "(happy) Hello")
        {"original": "Hello", "proposed": "(happy) Hello", "tags_added": ["happy"]}
    """
    tags_added = extract_added_tags(original, proposed)

    return {
        "original": original,
        "proposed": proposed,
        "tags_added": tags_added,
        "tag_count": len(tags_added)
    }


def format_diff_for_display(diff: EmotionDiff) -> str:
    """
    Format EmotionDiff as human-readable text for logging or display.

    Args:
        diff: EmotionDiff object

    Returns:
        Formatted string representation

    Example output:
        ```
        ORIGINAL:
        "I hate you," she said.

        PROPOSED:
        (sad)(soft tone) "I hate you," (sighing) she said.

        SUMMARY:
        Added 3 emotion tags: (sad), (soft tone), (sighing)
        ```
    """
    output_lines = [
        "=" * 60,
        "EMOTION MARKUP DIFF",
        "=" * 60,
        "",
        "ORIGINAL:",
        diff.original_text,
        "",
        "PROPOSED:",
        diff.proposed_text,
        "",
        "SUMMARY:",
        diff.summary,
        "=" * 60,
    ]

    return "\n".join(output_lines)


# Utility function for validating diffs before sending
def is_meaningful_diff(diff: EmotionDiff) -> bool:
    """
    Check if a diff contains meaningful changes.

    Args:
        diff: EmotionDiff object

    Returns:
        True if diff has actual changes
    """
    return diff.original_text != diff.proposed_text and len(diff.changes) > 0
