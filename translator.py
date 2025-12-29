"""
Translation Module
Handles translation to Chinese with custom glossary support
"""
from deep_translator import GoogleTranslator
import json
import re


class Translator:
    def __init__(self, glossary_file=None, target_language="zh-CN"):
        self.target_language = target_language
        self.glossary = {}
        if glossary_file:
            self.load_glossary(glossary_file)
        self.translator = GoogleTranslator(source='auto', target=target_language)
        
    def load_glossary(self, glossary_file):
        """Load custom glossary from JSON file"""
        try:
            with open(glossary_file, 'r', encoding='utf-8') as f:
                self.glossary = json.load(f)
            print(f"Loaded {len(self.glossary)} glossary terms")
        except Exception as e:
            print(f"Error loading glossary: {e}")
            self.glossary = {}
            
    def apply_glossary(self, text):
        """Apply glossary substitutions before translation"""
        modified_text = text
        # Store glossary terms with placeholders
        replacements = {}
        
        for i, (term, translation) in enumerate(self.glossary.items()):
            # Case-insensitive replacement
            pattern = re.compile(re.escape(term), re.IGNORECASE)
            if pattern.search(modified_text):
                placeholder = f"__GLOSSARY_{i}__"
                replacements[placeholder] = translation
                modified_text = pattern.sub(placeholder, modified_text)
                
        return modified_text, replacements
        
    def translate(self, text):
        """Translate text to Chinese with glossary support"""
        if not text or not text.strip():
            return ""
            
        try:
            # Apply glossary substitutions
            modified_text, replacements = self.apply_glossary(text)
            
            # Translate the text
            if modified_text:
                translated = self.translator.translate(modified_text)
                
                # Replace placeholders with glossary translations
                for placeholder, translation in replacements.items():
                    translated = translated.replace(placeholder, translation)
                    
                return translated
            return ""
            
        except Exception as e:
            print(f"Translation error: {e}")
            # Return original text on error
            return text
            
    def translate_batch(self, texts):
        """Translate multiple texts"""
        return [self.translate(text) for text in texts]
