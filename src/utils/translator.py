import json
import os

class Translator:
    def __init__(self, language="zh"):
        self.language = language
        self.translations = self.load_translations(language)

    def load_translations(self, language):
        try:
            with open(os.path.join(os.path.dirname(__file__), f"../translations/{language}.json"), "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            # Fallback to default language if file not found
            with open(os.path.join(os.path.dirname(__file__), f"../translations/zh.json"), "r", encoding="utf-8") as file:
                return json.load(file)

    def translate(self, key, **kwargs):
        text = self.translations.get(key, key)
        return text.format(**kwargs)

    def set_language(self, language):
        self.language = language
        self.translations = self.load_translations(language)
