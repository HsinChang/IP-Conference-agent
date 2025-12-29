"""
Test script for IP Conference Agent modules
Tests basic functionality without requiring live audio input
"""
import json
import os

def test_glossary_loading():
    """Test that glossary file can be loaded"""
    print("Testing glossary loading...")
    try:
        with open('ip_glossary.json', 'r', encoding='utf-8') as f:
            glossary = json.load(f)
        print(f"✓ Loaded {len(glossary)} glossary terms")
        print(f"  Sample terms: {list(glossary.items())[:3]}")
        return True
    except Exception as e:
        print(f"✗ Failed to load glossary: {e}")
        return False

def test_config_example():
    """Test that config example exists"""
    print("\nTesting config example...")
    try:
        with open('config.example.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        print(f"✓ Config example loaded with {len(config)} settings")
        required_keys = ["openai_api_key", "recognized_languages", "translation_target"]
        for key in required_keys:
            if key in config:
                print(f"  ✓ {key}: present")
            else:
                print(f"  ✗ {key}: missing")
        return True
    except Exception as e:
        print(f"✗ Failed to load config example: {e}")
        return False

def test_translator_import():
    """Test that translator module can be imported"""
    print("\nTesting translator import...")
    try:
        from translator import Translator
        print("✓ Translator module imported successfully")
        
        # Test with glossary
        translator = Translator(glossary_file='ip_glossary.json')
        print(f"✓ Translator initialized with glossary")
        
        # Test translation (this will use Google Translate API)
        test_text = "intellectual property"
        try:
            result = translator.translate(test_text)
            print(f"✓ Translation test: '{test_text}' -> '{result}'")
        except Exception as e:
            print(f"⚠ Translation API call failed (expected without internet): {e}")
        
        return True
    except Exception as e:
        print(f"✗ Failed to import translator: {e}")
        return False

def test_history_manager():
    """Test history manager functionality"""
    print("\nTesting history manager...")
    try:
        from history_manager import HistoryManager
        
        # Create test directory
        test_dir = "/tmp/test_history"
        hm = HistoryManager(history_dir=test_dir)
        print("✓ History manager initialized")
        
        # Test that directory was created
        if os.path.exists(test_dir):
            print(f"✓ History directory created: {test_dir}")
        
        # Test loading empty history
        history = hm.load_history()
        print(f"✓ History loaded: {len(history)} recordings")
        
        return True
    except Exception as e:
        print(f"✗ Failed to test history manager: {e}")
        return False

def test_audio_recorder_import():
    """Test that audio recorder can be imported"""
    print("\nTesting audio recorder import...")
    try:
        from audio_recorder import AudioRecorder
        print("✓ Audio recorder module imported successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to import audio recorder: {e}")
        print(f"  Note: PyAudio may need platform-specific installation")
        return False

def test_speech_recognizer_import():
    """Test that speech recognizer can be imported"""
    print("\nTesting speech recognizer import...")
    try:
        from speech_recognizer import SpeechRecognizer
        print("✓ Speech recognizer module imported successfully")
        
        sr = SpeechRecognizer(supported_languages=["en-US", "fr-FR"])
        print(f"✓ Speech recognizer initialized")
        
        return True
    except Exception as e:
        print(f"✗ Failed to import speech recognizer: {e}")
        return False

def test_summary_generator_import():
    """Test that summary generator can be imported"""
    print("\nTesting summary generator import...")
    try:
        from summary_generator import SummaryGenerator
        print("✓ Summary generator module imported successfully")
        
        sg = SummaryGenerator(api_key="test-key")
        print(f"✓ Summary generator initialized")
        
        return True
    except Exception as e:
        print(f"✗ Failed to import summary generator: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("IP Conference Agent - Module Tests")
    print("=" * 60)
    
    tests = [
        test_glossary_loading,
        test_config_example,
        test_translator_import,
        test_history_manager,
        test_audio_recorder_import,
        test_speech_recognizer_import,
        test_summary_generator_import,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print(f"Test Results: {sum(results)}/{len(results)} passed")
    print("=" * 60)
    
    if all(results):
        print("✓ All tests passed!")
    else:
        print("⚠ Some tests failed. Check output above for details.")
        print("\nNote: Some failures may be expected if dependencies are not installed.")
        print("Run 'pip install -r requirements.txt' to install all dependencies.")

if __name__ == "__main__":
    main()
