"""
Translation Module
Handles translation to Chinese with custom glossary support
Uses multiple translation providers with automatic fallback for global accessibility
"""
import json
import re
import os

try:
    from deep_translator import GoogleTranslator, MyMemoryTranslator
    DEEP_TRANSLATOR_AVAILABLE = True
except ImportError:
    DEEP_TRANSLATOR_AVAILABLE = False

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class Translator:
    def __init__(self, glossary_file=None, target_language="zh-CN", openai_api_key=None):
        self.target_language = target_language
        self.glossary = {}
        if glossary_file:
            self.load_glossary(glossary_file)
        
        # Set up OpenAI for translation (works globally including China)
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        if self.openai_api_key and OPENAI_AVAILABLE:
            openai.api_key = self.openai_api_key
        
        # Initialize multiple translation backends for fallback
        self.translators = []
        
        # Primary: OpenAI (works globally, most reliable)
        if self.openai_api_key and OPENAI_AVAILABLE:
            self.translators.append(('openai', None))
            print("Translator: OpenAI enabled (primary)")
        
        # Fallback 1: MyMemory Translator (free, works in China)
        if DEEP_TRANSLATOR_AVAILABLE:
            try:
                self.translators.append(('mymemory', MyMemoryTranslator(source='auto', target='zh-CN')))
                print("Translator: MyMemory enabled (fallback)")
            except Exception as e:
                print(f"MyMemory translator initialization failed: {e}")
        
        # Fallback 2: Google Translate (may not work in China)
        if DEEP_TRANSLATOR_AVAILABLE:
            try:
                self.translators.append(('google', GoogleTranslator(source='auto', target=target_language)))
                print("Translator: Google Translate enabled (fallback)")
            except Exception as e:
                print(f"Google translator initialization failed: {e}")
        
        if not self.translators:
            print("Warning: No translation services available. Install dependencies or provide OpenAI API key.")
        
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
        
    def _translate_with_openai(self, text):
        """Translate using OpenAI API (works globally including China)"""
        if not self.openai_api_key or not OPENAI_AVAILABLE:
            return None
            
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional translator. Translate the following text to Simplified Chinese. Only provide the translation, no explanations."},
                    {"role": "user", "content": text}
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            translation = response.choices[0].message.content.strip()
            return translation
            
        except Exception as e:
            print(f"OpenAI translation error: {e}")
            return None
    
    def _translate_with_provider(self, provider_name, translator_obj, text):
        """Translate using a specific provider"""
        try:
            if provider_name == 'openai':
                return self._translate_with_openai(text)
            else:
                return translator_obj.translate(text)
        except Exception as e:
            print(f"{provider_name} translation error: {e}")
            return None
    
    def translate(self, text):
        """Translate text to Chinese with glossary support and multi-provider fallback"""
        if not text or not text.strip():
            return ""
            
        try:
            # Apply glossary substitutions
            modified_text, replacements = self.apply_glossary(text)
            
            # Try each translation provider in order
            translated = None
            for provider_name, translator_obj in self.translators:
                translated = self._translate_with_provider(provider_name, translator_obj, modified_text)
                if translated:
                    print(f"Translation successful via {provider_name}")
                    break
            
            # If all providers fail, return original text
            if not translated:
                print("All translation providers failed, returning original text")
                return text
                
            # Replace placeholders with glossary translations
            for placeholder, translation in replacements.items():
                translated = translated.replace(placeholder, translation)
                
            return translated
            
        except Exception as e:
            print(f"Translation error: {e}")
            # Return original text on error
            return text
            
    def translate_batch(self, texts):
        """Translate multiple texts"""
        return [self.translate(text) for text in texts]
