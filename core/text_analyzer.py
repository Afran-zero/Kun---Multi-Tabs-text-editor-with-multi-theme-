"""
Text analysis module for Kun text editor.
Provides real-time word count, character count, and line/column tracking.
"""
import re


class TextAnalyzer:
    """Analyzes text content for statistics."""
    
    @staticmethod
    def count_words(text: str) -> int:
        """Count words in text."""
        if not text:
            return 0
        # Split by whitespace and filter empty strings
        words = text.split()
        return len(words)
    
    @staticmethod
    def count_characters(text: str, with_spaces: bool = True) -> int:
        """Count characters in text."""
        if not text:
            return 0
        if with_spaces:
            return len(text)
        else:
            # Remove all whitespace characters
            return len(re.sub(r'\s', '', text))
    
    @staticmethod
    def get_line_col(text: str, cursor_position: int) -> tuple:
        """
        Get line and column number from cursor position.
        Returns (line_number, column_number) - both 1-indexed.
        """
        if not text or cursor_position < 0:
            return (1, 1)
        
        # Limit cursor position to text length
        cursor_position = min(cursor_position, len(text))
        
        # Count lines up to cursor
        text_before = text[:cursor_position]
        line_number = text_before.count('\n') + 1
        
        # Find column (position in current line)
        last_newline = text_before.rfind('\n')
        if last_newline == -1:
            column_number = cursor_position + 1
        else:
            column_number = cursor_position - last_newline
        
        return (line_number, column_number)
    
    @staticmethod
    def count_lines(text: str) -> int:
        """Count total lines in text."""
        if not text:
            return 1
        return text.count('\n') + 1
    
    @staticmethod
    def get_statistics(text: str, cursor_position: int = 0, with_spaces: bool = True) -> dict:
        """
        Get all text statistics at once.
        Returns dictionary with words, chars, lines, line, col.
        """
        words = TextAnalyzer.count_words(text)
        chars = TextAnalyzer.count_characters(text, with_spaces)
        lines = TextAnalyzer.count_lines(text)
        line, col = TextAnalyzer.get_line_col(text, cursor_position)
        
        return {
            'words': words,
            'characters': chars,
            'total_lines': lines,
            'current_line': line,
            'current_col': col
        }
