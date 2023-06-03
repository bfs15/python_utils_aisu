
import utils_japanese

if __name__ == "__main__":
    for eng_text in [
        # "Sega's Mega Drive",
        # "Alice",
        # "Hymph",
        # "Solemn",
        # "Autumn",
        # "Column",
        # "Condemn",
        # "Damn",
        # "Hymn",
        # "Limn",
        # "Consonant",
        # "Damned",
        # "Phony",

        # "Xylophone",
        # "Xenon",
        # "Xerox",
        # "Xavier",
        # "Xmas",
        # "Sex",

        # "Rhythm",
        # "chrome",
        # "chris",
        # "cheese",

        # "new",
        # "Frankfurt",
        # "velvet",
        # "water",
        # "other",
        # "Philip",
        # "center",
        # "Twitch",
        # "coffee",
        # "mindbreak",
        # "cool",
        # "Sarah",
        "Shelly",

        # "ireland",
        "daughter",
        "sleigh",
        "rayleigh",
        "Blue Archive",
        "rape",
        "europe",
        "aerial",
        "rap",
        "translate_retries",
        "replace_match_with_engrish",
        "tts content",
        "higher",
        "colder",
        "fixes ", # - 'es' -> 'ズ' (e.g. 'fixes' -> 'フィクシズ')
    ]:
        print(f"=== {eng_text}")
        engrish_text = utils_japanese.english_to_engrish(eng_text)
        engrish_text_r = utils_japanese.english_to_engrish_r(eng_text)
        print(engrish_text)
        if engrish_text != engrish_text_r:
            print(f"WARN: {eng_text}: {engrish_text} != {engrish_text_r}")
