"""
Diff Generator for Emotion Markup

Creates git-style unified diffs between original text and emotion-marked text
for display in the frontend.
"""
import difflib
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import json
import hashlib


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
    Git-style unified diff for emotion markup changes.

    Attributes:
        original_text: Original text without markup
        proposed_text: Text with emotion markup applied
        unified_diff: Unified diff string (like git diff output)
        summary: Human-readable summary of changes
        explanation: Optional rationale for the changes
    """
    original_text: str
    proposed_text: str
    unified_diff: str
    summary: str
    explanation: Optional[str] = None

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
    Generate a git-style unified diff between original and emotion-marked text.

    Args:
        original_text: Text without emotion markup
        proposed_text: Text with emotion markup tags applied
        explanation: Optional explanation of why changes were made

    Returns:
        EmotionDiff object with unified diff string

    Example:
        >>> original = '"I hate you," she said.'
        >>> proposed = '(sad) "I hate you," she said.'
        >>> diff = generate_emotion_diff(original, proposed)
        >>> print(diff.unified_diff)
        @@ -1 +1 @@
        -"I hate you," she said.
        +(sad) "I hate you," she said.
    """
    # Extract added tags for summary
    added_tags = extract_added_tags(original_text, proposed_text)

    # Generate unified diff (git style)
    original_lines = original_text.splitlines(keepends=True)
    proposed_lines = proposed_text.splitlines(keepends=True)

    # Use difflib to create unified diff
    unified_diff_lines = list(difflib.unified_diff(
        original_lines,
        proposed_lines,
        fromfile='original',
        tofile='proposed',
        lineterm='',
        n=3  # Context lines
    ))

    # Join diff lines into string
    unified_diff = '\n'.join(unified_diff_lines)

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
        unified_diff=unified_diff,
        summary=summary,
        explanation=explanation
    )


def parse_unified_diff(diff_patch: str) -> tuple[str, str]:
    """
    Parse unified diff format to extract original and proposed text.

    Supports both single-line and multi-line diffs.

    Args:
        diff_patch: Unified diff string (git-style format)

    Returns:
        Tuple of (original_text, proposed_text)

    Raises:
        ValueError: If diff format is invalid or missing original/proposed

    Example:
        >>> diff = '''@@ -1 +1 @@
        ... -(nervous) Miku: "Hello"
        ... +(calm) Miku: "Hello"
        ... '''
        >>> original, proposed = parse_unified_diff(diff)
        >>> print(original)
        (nervous) Miku: "Hello"
        >>> print(proposed)
        (calm) Miku: "Hello"

    Multi-line example:
        >>> diff = '''@@ -1,2 +1,2 @@
        ... -Line 1 old
        ... -Line 2 old
        ... +Line 1 new
        ... +Line 2 new
        ... '''
        >>> original, proposed = parse_unified_diff(diff)
    """
    import re

    lines = diff_patch.strip().split('\n')

    # Extract lines marked with - (original) and + (proposed)
    original_lines = []
    proposed_lines = []

    for line in lines:
        # Skip header lines (---, +++, @@)
        if line.startswith('---') or line.startswith('+++') or line.startswith('@@'):
            continue
        # Extract original lines (start with -)
        elif line.startswith('-'):
            original_lines.append(line[1:])  # Remove '-' prefix
        # Extract proposed lines (start with +)
        elif line.startswith('+'):
            proposed_lines.append(line[1:])  # Remove '+' prefix
        # Context lines (no prefix) are ignored for our purposes

    # Join multi-line content
    original_text = '\n'.join(original_lines) if original_lines else ''
    proposed_text = '\n'.join(proposed_lines) if proposed_lines else ''

    # Validate we got both
    if not original_text and not proposed_text:
        raise ValueError(
            "Invalid diff format: No original (-) or proposed (+) lines found. "
            "Expected unified diff format with lines starting with - and +"
        )

    if not original_text:
        raise ValueError(
            "Invalid diff format: No original (-) lines found. "
            "Diff must include original text to replace."
        )

    if not proposed_text:
        raise ValueError(
            "Invalid diff format: No proposed (+) lines found. "
            "Diff must include proposed text."
        )

    return original_text, proposed_text


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
