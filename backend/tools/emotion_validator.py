"""
Emotion Tag Validator for Fish Audio

Validates emotion markup tags against Fish Audio specification.
Ensures proper tag placement, format, and validity.
"""
import re
from typing import List, Tuple
from dataclasses import dataclass


# Tag categories from emotion_control.md
BASIC_EMOTIONS = {
    "happy", "sad", "angry", "excited", "calm", "nervous", "confident",
    "surprised", "satisfied", "delighted", "scared", "worried", "upset",
    "frustrated", "depressed", "empathetic", "embarrassed", "disgusted",
    "moved", "proud", "relaxed", "grateful", "curious", "sarcastic"
}

ADVANCED_EMOTIONS = {
    "disdainful", "unhappy", "anxious", "hysterical", "indifferent",
    "uncertain", "doubtful", "confused", "disappointed", "regretful",
    "guilty", "ashamed", "jealous", "envious", "hopeful", "optimistic",
    "pessimistic", "nostalgic", "lonely", "bored", "contemptuous",
    "sympathetic", "compassionate", "determined", "resigned"
}

TONE_MARKERS = {
    "in a hurry tone", "shouting", "screaming", "whispering", "soft tone"
}

AUDIO_EFFECTS = {
    "laughing", "chuckling", "sobbing", "crying loudly", "sighing",
    "groaning", "panting", "gasping", "yawning", "snoring"
}

SPECIAL_EFFECTS = {
    "audience laughing", "background laughter", "crowd laughing",
    "break", "long-break"
}

# Combined sets for validation
ALL_EMOTION_TAGS = BASIC_EMOTIONS | ADVANCED_EMOTIONS
ALL_TONE_TAGS = TONE_MARKERS
ALL_AUDIO_EFFECTS = AUDIO_EFFECTS
ALL_SPECIAL_EFFECTS = SPECIAL_EFFECTS
ALL_VALID_TAGS = ALL_EMOTION_TAGS | ALL_TONE_TAGS | ALL_AUDIO_EFFECTS | ALL_SPECIAL_EFFECTS


@dataclass
class ValidationResult:
    """Result of emotion tag validation."""
    is_valid: bool
    errors: List[str]
    warnings: List[str] = None

    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []


def extract_tags(text: str) -> List[Tuple[str, int]]:
    """
    Extract all emotion tags from text with their positions.

    Args:
        text: Marked-up text with emotion tags

    Returns:
        List of (tag_name, position) tuples

    Example:
        "(sad)(whispering) Hello" -> [("sad", 0), ("whispering", 5)]
    """
    # Pattern matches (tag_name) format
    pattern = r'\(([^)]+)\)'
    matches = re.finditer(pattern, text)

    tags = []
    for match in matches:
        tag_name = match.group(1).strip()
        position = match.start()
        tags.append((tag_name, position))

    return tags


def get_tag_category(tag: str) -> str:
    """
    Determine which category a tag belongs to.

    Args:
        tag: Tag name (without parentheses)

    Returns:
        Category name: "emotion", "tone", "audio_effect", "special_effect", or "unknown"
    """
    if tag in ALL_EMOTION_TAGS:
        return "emotion"
    elif tag in ALL_TONE_TAGS:
        return "tone"
    elif tag in ALL_AUDIO_EFFECTS:
        return "audio_effect"
    elif tag in ALL_SPECIAL_EFFECTS:
        return "special_effect"
    else:
        return "unknown"


def validate_emotion_markup(text: str) -> ValidationResult:
    """
    Validate emotion markup in text according to Fish Audio specification.

    Checks:
    1. Tag validity (exists in official spec)
    2. Tag placement (emotion tags must be at sentence start)
    3. Tag count (max 3 tags per sentence)
    4. Format (proper parentheses)

    Args:
        text: Text with emotion markup tags

    Returns:
        ValidationResult with errors and warnings

    Example:
        >>> validate_emotion_markup("(sad) I'm leaving.")
        ValidationResult(is_valid=True, errors=[], warnings=[])

        >>> validate_emotion_markup("I'm (sad) leaving.")
        ValidationResult(is_valid=False, errors=["Emotion tag 'sad' must be at sentence start"], warnings=[])
    """
    errors = []
    warnings = []

    # Extract all tags from text
    tags = extract_tags(text)

    if not tags:
        # No tags found - this is valid (plain text)
        return ValidationResult(is_valid=True, errors=[], warnings=[])

    # Check 1: Validate tag names
    for tag_name, _ in tags:
        if tag_name not in ALL_VALID_TAGS:
            errors.append(
                f"Invalid tag '{tag_name}'. Not found in Fish Audio specification. "
                f"Check spelling or refer to emotion_control.md."
            )

    # Check 2: Validate emotion tag placement (must be at sentence start)
    # Emotion tags must appear before any actual text content

    # Strategy: Find the first non-tag character, then check if any emotion tags
    # appear after that point

    for tag_name, tag_pos in tags:
        if get_tag_category(tag_name) == "emotion":
            # Check if there's any text before this tag
            text_before_tag = text[:tag_pos].strip()

            # Remove any tags from text_before_tag to see if there's actual content
            temp_text = text_before_tag
            while '(' in temp_text:
                start_idx = temp_text.find('(')
                end_idx = temp_text.find(')', start_idx)
                if end_idx == -1:
                    break
                temp_text = temp_text[:start_idx] + temp_text[end_idx + 1:]

            # If there's any non-whitespace content before this emotion tag, it's invalid
            if temp_text.strip():
                errors.append(
                    f"Emotion tag '({tag_name})' must be at sentence start, not mid-sentence. "
                    f"Found text before tag: '{temp_text.strip()[:20]}...'"
                )

    # Check 3: Maximum 3 tags per sentence
    sentences = re.split(r'[.!?]\s*', text)
    for sentence in sentences:
        if not sentence.strip():
            continue

        sentence_tags = extract_tags(sentence)

        if len(sentence_tags) > 3:
            warnings.append(
                f"Sentence has {len(sentence_tags)} tags (max recommended: 3). "
                f"Too many tags may reduce clarity. Sentence: '{sentence[:50]}...'"
            )

    # Check 4: Format validation (proper closing parentheses)
    open_parens = text.count('(')
    close_parens = text.count(')')

    if open_parens != close_parens:
        errors.append(
            f"Mismatched parentheses: {open_parens} opening, {close_parens} closing. "
            f"Ensure all tags are properly formatted: (tag_name)"
        )

    is_valid = len(errors) == 0

    return ValidationResult(
        is_valid=is_valid,
        errors=errors,
        warnings=warnings
    )


def suggest_fix(text: str, validation_result: ValidationResult) -> str:
    """
    Suggest a corrected version of text based on validation errors.

    Args:
        text: Original marked-up text
        validation_result: Result from validate_emotion_markup

    Returns:
        Suggested fixed text (best-effort)
    """
    if validation_result.is_valid:
        return text

    # This is a simple implementation - in production you'd want more sophisticated logic
    # For now, we just remove invalid tags
    fixed_text = text

    for error in validation_result.errors:
        if "Invalid tag" in error:
            # Extract tag name from error message
            match = re.search(r"Invalid tag '([^']+)'", error)
            if match:
                invalid_tag = match.group(1)
                # Remove the tag
                fixed_text = fixed_text.replace(f"({invalid_tag})", "")

    return fixed_text.strip()


# Quick validation function for common use cases
def is_valid_emotion_tag(tag: str) -> bool:
    """
    Quick check if a single tag is valid.

    Args:
        tag: Tag name without parentheses

    Returns:
        True if tag exists in Fish Audio spec
    """
    return tag in ALL_VALID_TAGS


def is_emotion_tag(tag: str) -> bool:
    """Check if tag is an emotion tag (must be at sentence start)."""
    return tag in ALL_EMOTION_TAGS


def is_tone_or_effect(tag: str) -> bool:
    """Check if tag is a tone marker or effect (can go anywhere)."""
    return tag in (ALL_TONE_TAGS | ALL_AUDIO_EFFECTS | ALL_SPECIAL_EFFECTS)
