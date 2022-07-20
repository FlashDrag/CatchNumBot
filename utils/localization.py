class Lang:
    strings = {
        'en': {
            'key_string_name': 'value_translated_string',
        },
        'ru': {
            'key_string_name': 'переведенная_строка',
        }
    }

    def __init__(self, language_key: str):
        if language_key in self.strings.keys():
            self.chosen_lang = language_key
        else:
            raise ValueError(f"No such language: {language_key}")

    def get(self, key):
        return self.strings.get(self.chosen_lang, {}).get(key, "%MISSING STRING%")
