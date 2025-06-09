"""
Main entry point for the mplfontutils package.

Run this module to test font compatibility with a sample text.
Usage: python -m mplfontutils
"""

import sys

from .core import find_available_fonts


def main():
    """Main function to test font compatibility."""
    # Default test text (supports multiple languages)
    default_test_text = "Hello 中文测试"

    # Get test text from command line argument or use default
    if len(sys.argv) > 1:
        test_text = " ".join(sys.argv[1:])
    else:
        test_text = default_test_text

    print(f"Testing font compatibility for: '{test_text}'")
    print("-" * 50)

    # Find available fonts
    try:
        available_fonts = find_available_fonts(test_text)

        if available_fonts:
            print(f"Found {len(available_fonts)} compatible fonts:")
            print()
            for font in sorted(available_fonts):
                print(f"  • {font}")
        else:
            print("No compatible fonts found for the given text.")

    except Exception as e:
        print(f"Error testing fonts: {e}")
        sys.exit(1)

    print()
    print("Usage examples:")
    print("  python -m mplfontutils")
    print("  python -m mplfontutils 'Your custom text'")
    print("  python -m mplfontutils '🎨 Emoji test 🎭'")


if __name__ == "__main__":
    main()
