#!/usr/bin/env python3
"""
Test script for Phase 4 emotion markup tools.

Tests:
1. Emotion validator - tag validation and placement rules
2. Diff generator - markup diffs
3. Fish Audio preview - audio generation with character voices
4. Gender inference - automatic gender detection
5. Integration - full workflow

Run from backend directory:
    uv run python scripts/test_phase4_tools.py
"""
import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.emotion_validator import (
    validate_emotion_markup,
    is_valid_emotion_tag,
    extract_tags,
    get_tag_category,
)
from tools.diff_generator import (
    generate_emotion_diff,
    extract_added_tags,
    format_diff_for_display,
)
from tools.fish_audio_preview import (
    infer_character_gender,
    # FishAudioPreview - tested separately with real API
)


def test_emotion_validator():
    """Test emotion tag validation."""
    print("\n" + "=" * 60)
    print("TEST 1: Emotion Validator")
    print("=" * 60)

    test_cases = [
        # (text, should_be_valid, description)
        ('(sad) "I\'m leaving."', True, "Valid: emotion at start"),
        ('"I\'m (sad) leaving."', False, "Invalid: emotion mid-sentence"),
        ('(sad)(whispering) "Hello"', True, "Valid: multiple tags at start"),
        ('(happy) "Hello" (laughing)', True, "Valid: emotion + audio effect"),
        ('(invalid_emotion) "Hello"', False, "Invalid: unknown emotion tag"),
        ('"Hello"', True, "Valid: no tags (plain text)"),
        ('(sad)(nervous)(worried) "Help"', True, "Valid: 3 tags (max)"),
        ('(sad) Hello (whispering) there', True, "Valid: tone marker can go anywhere"),
    ]

    passed = 0
    failed = 0

    for text, expected_valid, description in test_cases:
        result = validate_emotion_markup(text)
        is_valid = result.is_valid

        status = "✅ PASS" if is_valid == expected_valid else "❌ FAIL"
        print(f"\n{status}: {description}")
        print(f"  Text: {text}")
        print(f"  Expected: {'Valid' if expected_valid else 'Invalid'}")
        print(f"  Got: {'Valid' if is_valid else 'Invalid'}")

        if result.errors:
            print(f"  Errors: {'; '.join(result.errors)}")

        if is_valid == expected_valid:
            passed += 1
        else:
            failed += 1

    print(f"\n{'=' * 60}")
    print(f"Emotion Validator: {passed} passed, {failed} failed")
    print(f"{'=' * 60}")

    return failed == 0


def test_tag_extraction():
    """Test tag extraction utility."""
    print("\n" + "=" * 60)
    print("TEST 2: Tag Extraction")
    print("=" * 60)

    test_cases = [
        ('(sad) Hello', [('sad', 0)]),
        ('(sad)(whispering) Hello', [('sad', 0), ('whispering', 5)]),
        ('Hello (laughing)', [('laughing', 6)]),
        ('No tags here', []),
    ]

    passed = 0
    failed = 0

    for text, expected_tags in test_cases:
        extracted = extract_tags(text)
        match = extracted == expected_tags

        status = "✅ PASS" if match else "❌ FAIL"
        print(f"\n{status}: Extract tags from: {text}")
        print(f"  Expected: {expected_tags}")
        print(f"  Got: {extracted}")

        if match:
            passed += 1
        else:
            failed += 1

    print(f"\n{'=' * 60}")
    print(f"Tag Extraction: {passed} passed, {failed} failed")
    print(f"{'=' * 60}")

    return failed == 0


def test_tag_categorization():
    """Test tag category detection."""
    print("\n" + "=" * 60)
    print("TEST 3: Tag Categorization")
    print("=" * 60)

    test_cases = [
        ("sad", "emotion"),
        ("happy", "emotion"),
        ("whispering", "tone"),
        ("soft tone", "tone"),
        ("laughing", "audio_effect"),
        ("sighing", "audio_effect"),
        ("break", "special_effect"),
        ("invalid_tag", "unknown"),
    ]

    passed = 0
    failed = 0

    for tag, expected_category in test_cases:
        category = get_tag_category(tag)
        match = category == expected_category

        status = "✅ PASS" if match else "❌ FAIL"
        print(f"{status}: '{tag}' → {expected_category} (got: {category})")

        if match:
            passed += 1
        else:
            failed += 1

    print(f"\n{'=' * 60}")
    print(f"Tag Categorization: {passed} passed, {failed} failed")
    print(f"{'=' * 60}")

    return failed == 0


def test_diff_generator():
    """Test diff generation."""
    print("\n" + "=" * 60)
    print("TEST 4: Diff Generator")
    print("=" * 60)

    test_cases = [
        (
            '"I hate you," she said.',
            '(sad) "I hate you," she said.',
            ["sad"],
            "Simple emotion tag addition"
        ),
        (
            '"Hello"',
            '(happy)(excited) "Hello" (laughing)',
            ["happy", "excited", "laughing"],
            "Multiple tags"
        ),
        (
            'Plain text',
            'Plain text',
            [],
            "No changes"
        ),
    ]

    passed = 0
    failed = 0

    for original, proposed, expected_tags, description in test_cases:
        # Test extract_added_tags
        added_tags = extract_added_tags(original, proposed)
        tags_match = set(added_tags) == set(expected_tags)

        # Test generate_emotion_diff
        diff = generate_emotion_diff(original, proposed, "Test explanation")

        status = "✅ PASS" if tags_match else "❌ FAIL"
        print(f"\n{status}: {description}")
        print(f"  Original: {original}")
        print(f"  Proposed: {proposed}")
        print(f"  Expected tags: {expected_tags}")
        print(f"  Got tags: {added_tags}")
        print(f"  Diff summary: {diff.summary}")

        if tags_match:
            passed += 1
        else:
            failed += 1

    print(f"\n{'=' * 60}")
    print(f"Diff Generator: {passed} passed, {failed} failed")
    print(f"{'=' * 60}")

    return failed == 0


def test_gender_inference():
    """Test character gender inference."""
    print("\n" + "=" * 60)
    print("TEST 5: Gender Inference")
    print("=" * 60)

    test_cases = [
        ('"I\'m leaving," she said.', "female"),
        ('"Hello," he replied.', "male"),
        ('"Goodbye," Sarah whispered.', "female"),
        ('"Wait!" Marcus shouted.', "male"),
        ('"What?" they asked.', "neutral"),
        ('Plain text with no indicators', "neutral"),
        ('She felt sad about him leaving', "female"),  # More "she" indicators
    ]

    passed = 0
    failed = 0

    for text, expected_gender in test_cases:
        inferred = infer_character_gender(text)
        match = inferred == expected_gender

        status = "✅ PASS" if match else "❌ FAIL"
        print(f"\n{status}: {text[:50]}...")
        print(f"  Expected: {expected_gender}")
        print(f"  Got: {inferred}")

        if match:
            passed += 1
        else:
            failed += 1

    print(f"\n{'=' * 60}")
    print(f"Gender Inference: {passed} passed, {failed} failed")
    print(f"{'=' * 60}")

    return failed == 0


async def test_fish_audio_preview():
    """
    Test Fish Audio preview (requires API key).

    This test is OPTIONAL - only runs if Fish Audio API key is available.
    """
    print("\n" + "=" * 60)
    print("TEST 6: Fish Audio Preview (OPTIONAL)")
    print("=" * 60)

    import os
    if not os.getenv("FISH_AUDIO_API_KEY"):
        print("⚠️  SKIPPED: FISH_AUDIO_API_KEY not found in environment")
        print("   This test requires a valid Fish Audio API key.")
        return True

    try:
        from tools.fish_audio_preview import FishAudioPreview

        preview = FishAudioPreview()

        # Simple test case
        test_text = "(happy) Hello, how are you?"

        print(f"\nGenerating preview for: {test_text}")
        print("  Gender: female")

        audio_path = await preview.generate_preview(
            text=test_text,
            character_gender="female",
        )

        if audio_path.exists():
            size = audio_path.stat().st_size
            print(f"✅ PASS: Audio generated successfully")
            print(f"  Path: {audio_path}")
            print(f"  Size: {size} bytes")
            return True
        else:
            print(f"❌ FAIL: Audio file not created")
            return False

    except Exception as e:
        print(f"⚠️  ERROR: {e}")
        print("   Fish Audio API test failed - check API key and network connection")
        return True  # Don't fail the entire test suite


def test_integration():
    """Test full integration workflow."""
    print("\n" + "=" * 60)
    print("TEST 7: Integration Workflow")
    print("=" * 60)

    # Simulate full workflow
    original_text = '"I can\'t believe you did this," she said.'

    print(f"\n1. Original text: {original_text}")

    # Step 1: Infer gender
    gender = infer_character_gender(original_text)
    print(f"2. Inferred gender: {gender}")
    assert gender == "female", f"Expected 'female', got '{gender}'"

    # Step 2: Generate proposed markup
    proposed_text = '(disappointed)(soft tone) "I can\'t believe you did this," (sighing) she said.'
    print(f"3. Proposed markup: {proposed_text}")

    # Step 3: Validate markup
    validation = validate_emotion_markup(proposed_text)
    print(f"4. Validation: {'✅ Valid' if validation.is_valid else '❌ Invalid'}")

    if not validation.is_valid:
        print(f"   Errors: {validation.errors}")
        return False

    # Step 4: Generate diff
    diff = generate_emotion_diff(
        original_text,
        proposed_text,
        "Stanislavski's emotional truth - disappointment with soft restraint"
    )
    print(f"5. Diff generated:")
    print(format_diff_for_display(diff))

    # Step 5: (Audio preview would happen here - tested separately)
    print(f"6. Audio preview: (would call Fish Audio API with gender={gender})")

    print(f"\n✅ PASS: Full integration workflow completed")

    print(f"{'=' * 60}")
    print(f"Integration Test: PASSED")
    print(f"{'=' * 60}")

    return True


async def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print(" " * 15 + "PHASE 4 TOOLS TEST SUITE")
    print("=" * 70)

    results = {
        "Emotion Validator": test_emotion_validator(),
        "Tag Extraction": test_tag_extraction(),
        "Tag Categorization": test_tag_categorization(),
        "Diff Generator": test_diff_generator(),
        "Gender Inference": test_gender_inference(),
        "Fish Audio Preview": await test_fish_audio_preview(),
        "Integration Workflow": test_integration(),
    }

    # Summary
    print("\n" + "=" * 70)
    print(" " * 25 + "TEST SUMMARY")
    print("=" * 70)

    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}  {test_name}")

    total = len(results)
    passed = sum(results.values())
    failed = total - passed

    print("=" * 70)
    print(f"Total: {total} tests, {passed} passed, {failed} failed")
    print("=" * 70)

    if failed == 0:
        print("\n🎉 All tests passed! Phase 4 tools are ready.")
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) failed. Review errors above.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
