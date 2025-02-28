import requests
import time
import os

# Language mapping for better prompting
LANGUAGE_NAMES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "nl": "Dutch",
    "ru": "Russian",
    "zh": "Chinese",
    "ja": "Japanese",
    "ko": "Korean",
    "ar": "Arabic",
    "hi": "Hindi",
    "tr": "Turkish",
    "fa": "Persian"
}

class TranslationService:
    """Service for handling text translations using OpenAI API."""

    def __init__(self, api_key=None, model=None, temperature=None):
        """
        Initialize the translation service.

        Args:
            api_key (str, optional): OpenAI API key. If None, will try to get from environment.
            model (str, optional): GPT model to use. If None, will try to get from environment.
            temperature (float, optional): Model temperature. If None, will try to get from environment.
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.model = model or os.getenv("GPT_MODEL", "gpt-4o-mini")

        # Parse temperature from environment or use default
        temp_str = os.getenv("GPT_TEMPERATURE", "0.3")
        try:
            self.temperature = temperature or float(temp_str)
        except ValueError:
            print(f"WARNING: Invalid GPT_TEMPERATURE value '{temp_str}', using default 0.3", flush=True)
            self.temperature = 0.3

        if not self.api_key:
            print("WARNING: No OpenAI API key provided for translation service", flush=True)
        else:
            print(f"Translation service initialized with model: {self.model}, temperature: {self.temperature}", flush=True)

    def translate(self, text, target_language):
        """
        Translate text to the target language.

        Args:
            text (str): The text to translate
            target_language (str): The target language code (e.g., 'en', 'es')

        Returns:
            dict: The translation result with text and processing time, or None if failed
        """
        if not text or not target_language or not self.api_key:
            return None

        try:
            start_time = time.time()

            # Get full language name for better prompting
            target_language_name = LANGUAGE_NAMES.get(target_language, target_language)

            # Create the API request for translation
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [
                        {
                            "role": "system",
                            "content": f"You are a professional translator. Translate the following text to {target_language_name}. Only respond with the translation, nothing else."
                        },
                        {
                            "role": "user",
                            "content": text
                        }
                    ],
                    "temperature": self.temperature
                }
            )

            processing_time = time.time() - start_time

            if response.status_code == 200:
                result = response.json()
                translated_text = result['choices'][0]['message']['content'].strip()

                return {
                    "text": translated_text,
                    "processing_time": processing_time,
                    "model": self.model
                }
            else:
                print(f"Translation API Error: {response.text}", flush=True)
                return None

        except Exception as e:
            print(f"Translation Error: {e}", flush=True)
            return None