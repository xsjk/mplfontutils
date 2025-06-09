"""
Core functionality for font utilities in matplotlib.
"""

import logging
import os
import re
import warnings
from typing import Optional, Set

import matplotlib.pyplot as plt
from matplotlib.font_manager import fontManager


def load_fonts_from_directory(font_directory: str) -> None:
    """
    Load custom fonts from a specified directory.

    This function recursively searches the given directory for font files
    (.ttf and .otf) and adds them to matplotlib's font manager.

    Args:
        font_directory (str): Path to the directory containing font files

    Raises:
        None: Logs warnings if directory doesn't exist

    Example:
        >>> load_fonts_from_directory("/path/to/fonts")
    """
    if not os.path.exists(font_directory):
        logging.warning(f"Font directory '{font_directory}' does not exist.")
        return

    loaded_count = 0
    for root, _, files in os.walk(font_directory):
        for filename in files:
            if filename.endswith((".otf", ".ttf")):
                font_path = os.path.join(root, filename)
                fontManager.addfont(font_path)
                logging.debug(f"Loaded font: {filename}")
                loaded_count += 1

    logging.info(f"Successfully loaded {loaded_count} font(s) from {font_directory}")


def find_available_fonts(test_text: str, output_file: Optional[str] = None) -> Set[str]:
    """
    Find available fonts that can display the given test text.

    This function tests all available fonts in matplotlib's font manager
    to see which ones can properly display the provided test text without
    missing glyphs.

    Args:
        test_text (str): Text to test font compatibility with
        output_file (str, optional): Path to save the font test visualization.
                                   If None, no file is saved.

    Returns:
        Set[str]: Set of font names that can display the test text

    Example:
        >>> available_fonts = find_available_fonts("中文测试")
        >>> print(f"Found {len(available_fonts)} compatible fonts")

        >>> # Save visualization to file
        >>> fonts = find_available_fonts("Hello 世界", "font_test.png")
    """
    available_fonts = set()

    with warnings.catch_warnings(record=True) as caught_warnings:
        warnings.simplefilter("always")

        # Test each font
        font_names = fontManager.get_font_names()

        # Add all fonts to test set first
        for font_name in font_names:
            available_fonts.add(font_name)

        fig, ax = plt.subplots(figsize=(5, 1))

        # Always test all fonts by rendering text
        for i, font_name in enumerate(font_names):
            y = 1 - i * 0.2

            # Display font name and test text (this triggers font validation)
            ax.text(0, y, font_name, fontsize=8)
            ax.text(0.5, y, test_text, fontname=font_name, fontsize=8)

        ax.set_axis_off()
        fig.canvas.draw()

        # Save figure only if output file is requested
        if output_file:
            fig.savefig(output_file, bbox_inches="tight", pad_inches=0.1, dpi=300)

        # Remove fonts that cannot display the test text
        # Parse warnings to identify fonts with missing glyphs
        for warning in caught_warnings:
            warning_str = str(warning.message)
            if match := re.match(r"Glyph (\d+) \(.*\) missing from font\(s\) (.+)\.", warning_str):
                font_name = match.group(2)
                if font_name in available_fonts:
                    available_fonts.remove(font_name)
                    logging.debug(f"Removed font '{font_name}' due to missing glyphs")

    logging.info(f"Found {len(available_fonts)} fonts compatible with text: '{test_text}'")
    return available_fonts
