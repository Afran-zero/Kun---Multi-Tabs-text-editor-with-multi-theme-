"""
Spell checking module for Kun text editor.
Uses pyspellchecker for basic spell checking functionality.
"""
from spellchecker import SpellChecker
import re


class BasicSpellChecker:
    """Provides spell checking functionality."""
    
    def __init__(self, language: str = 'en'):
        """Initialize spell checker with specified language."""
        try:
            self.spell = SpellChecker(language=language)
            self.enabled = True
        except Exception as e:
            print(f"Error initializing spell checker: {e}")
            self.spell = None
            self.enabled = False
    
    def check_word(self, word: str) -> bool:
        """Check if a single word is spelled correctly."""
        if not self.enabled or not self.spell or not word:
            return True
        
        # Skip words with numbers or special characters
        if not word.isalpha():
            return True
        
        # Use the known() method to check if word is in dictionary
        word_lower = word.lower()
        return len(self.spell.known([word_lower])) > 0
    
    def get_suggestions(self, word: str, max_suggestions: int = 5) -> list:
        """Get spelling suggestions for a misspelled word."""
        if not self.enabled or not self.spell or not word:
            return []
        
        candidates = self.spell.candidates(word)
        if candidates:
            return list(candidates)[:max_suggestions]
        return []
    
    def find_misspelled_words(self, text: str) -> list:
        """
        Find all misspelled words in text.
        Returns list of tuples: (word, start_position, end_position)
        """
        if not self.enabled or not self.spell or not text:
            return []
        
        misspelled = []
        # Find all words with their positions
        for match in re.finditer(r'\b[a-zA-Z]+\b', text):
            word = match.group()
            if not self.check_word(word):
                misspelled.append((word, match.start(), match.end()))
        
        return misspelled
    
    def set_enabled(self, enabled: bool):
        """Enable or disable spell checking."""
        self.enabled = enabled and self.spell is not None
    
    def is_enabled(self) -> bool:
        """Check if spell checking is enabled."""
        return self.enabled
