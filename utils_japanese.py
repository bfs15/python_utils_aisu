
import re
import pykakasi
import romajitable
from python_utils_aisu import utils

logger = utils.loggingGetLogger(__name__)
logger.setLevel('INFO')

kakasi = pykakasi.kakasi()


re_kanji = "\u3400-\u4DB5\u4E00-\u9FCB\uF900-\uFA6A"
re_hiragana = "\u3041-\u3096"
re_katakana = "\u30A0-\u30FF"
re_katakana_half_and_punctuation = "\uFF5F-\uFF9F"
re_unicode_points = "\u2E80-\u2FD5"
re_symbols_and_punctuations = "\u3000-\u303F"
re_symbols_miscellaneous = "\u31F0-\u31FF\u3220-\u3243\u3280-\u337F゛゜ゝゞゟ"

re_japanese = fr'{re_kanji}{re_hiragana}{re_katakana}{re_katakana_half_and_punctuation}{re_unicode_points}{re_symbols_and_punctuations}{re_symbols_miscellaneous}'

# re_kanji = r"一-龠"
# re_hiragana = r"ぁ-ゔ"
# re_katakana = r"ァ-ヴー"
# re_ideo = r"々〆〤ヶ"
# re_japanese = fr'{re_kanji}{re_hiragana}{re_katakana}{re_ideo}'
re_japanese_plus = fr'[{re_japanese}]+'
re_japanese_kanji_plus = fr'[{re_kanji}]+'

re_japanese_voiced = fr'{re_kanji}{re_hiragana}{re_katakana}'
re_voiced_plus = fr'[A-Za-z0-9{re_japanese_voiced}]+'
re_voiced_plus_c = re.compile(re_voiced_plus, re.U)

keep_orig = {"「", "！", "」"}

def get_romaji(item):
    if any((k in item['orig'] for k in keep_orig)):
        return item['orig']
    return item['hepburn']

def kanji_to_romaji(text):
    result = kakasi.convert(text)
    return ' '.join(get_romaji(i) for i in result)

def replace_japanese_with_romaji(match):
    return " " + kanji_to_romaji(match.group())

def convert_japanese_to_romaji(text, kanji_only=False):
    _japanese_text_regex = re_japanese_plus
    if kanji_only:
        _japanese_text_regex = re_japanese_kanji_plus
    return re.sub(_japanese_text_regex, replace_japanese_with_romaji, text)

english_text_regex = fr'[A-Za-z_\-]+'

def replace_match_with_katakana(match):
    result = romajitable.to_kana(match.group())
    return result.katakana

def replace_match_with_engrish(match):
    return english_to_engrish(r'\b' + match.group() + r'\b')


def english_replace_with_f(text, replace_f=replace_match_with_katakana):
    return re.sub(english_text_regex, replace_f, text)

vowel_combos = {
    'a': 'ァ',
    'e': 'ェ',
    'i': 'ィ',
    'o': 'ォ',
    'u': 'ゥ'
}

katakana_map = {
    'a': 'ア', 'ba': 'バ', 'be': 'ベ', 'bi': 'ビ', 'bo': 'ボ', 'bu': 'ブ', 'chi': 'チ', 'da': 'ダ', 'de': 'デ', 'do': 'ド', 'e': 'エ', 'fu': 'フ', 'ga': 'ガ', 'ge': 'ゲ', 'gi': 'ギ', 'go': 'ゴ', 'gu': 'グ', 'ha': 'ハ', 'he': 'ヘ', 'hi': 'ヒ', 'ho': 'ホ', 'i': 'イ', 'ja': 'ジャ', 'ji': 'ヂ', 'jo': 'ジョ', 'ju': 'ジュ', 'ka': 'カ', 'ke': 'ケ', 'ki': 'キ', 'ko': 'コ', 'ku': 'ク', 'ma': 'マ', 'me': 'メ', 'mi': 'ミ', 'mo': 'モ', 'mu': 'ム', 'n': 'ン', 'na': 'ナ', 'ne': 'ネ', 'ni': 'ニ', 'no': 'ノ', 'nu': 'ヌ', 'o': 'オ', 'pa': 'パ', 'pe': 'ペ', 'pi': 'ピ', 'po': 'ポ', 'pu': 'プ', 'ra': 'ラ', 're': 'レ', 'ri': 'リ', 'ro': 'ロ', 'ru': 'ル', 'sa': 'サ', 'se': 'セ', 'shi': 'シ', 'so': 'ソ', 'su': 'ス', 'ta': 'タ', 'te': 'テ', 'to': 'ト', 'tsu': 'ツ', 'u': 'ウ', 'wa': 'ワ', 'wo': 'ヲ', 'ya': 'ヤ', 'yo': 'ヨ', 'yu': 'ユ', 'za': 'ザ', 'ze': 'ゼ', 'zo': 'ゾ', 'zu': 'ヅ',
}

katakana_map_1 = {
    'a': 'ア', 'i': 'イ', 'u': 'ウ', 'e': 'エ', 'o': 'オ',
    'ka': 'カ', 'ki': 'キ', 'ku': 'ク', 'ke': 'ケ', 'ko': 'コ',
    'sa': 'サ', 'shi': 'シ', 'su': 'ス', 'se': 'セ', 'so': 'ソ',
    'ta': 'タ', 'chi': 'チ', 'tsu': 'ツ', 'te': 'テ', 'to': 'ト',
    'na': 'ナ', 'ni': 'ニ', 'nu': 'ヌ', 'ne': 'ネ', 'no': 'ノ',
    'ha': 'ハ', 'hi': 'ヒ', 'fu': 'フ', 'he': 'ヘ', 'ho': 'ホ',
    'ma': 'マ', 'mi': 'ミ', 'mu': 'ム', 'me': 'メ', 'mo': 'モ',
    'ya': 'ヤ', 'yu': 'ユ', 'yo': 'ヨ',
    'ra': 'ラ', 'ri': 'リ', 'ru': 'ル', 're': 'レ', 'ro': 'ロ',
    'wa': 'ワ', 'wi': 'ウィ', 'we': 'ウェ', 'wo': 'ヲ',
    'n': 'ン',
    'ga': 'ガ', 'gi': 'ギ', 'gu': 'グ', 'ge': 'ゲ', 'go': 'ゴ',
    'za': 'ザ', 'ji': 'ジ', 'zu': 'ズ', 'ze': 'ゼ', 'zo': 'ゾ',
    'da': 'ダ', 'dzi': 'ヂ', 'zu': 'ヅ', 'de': 'デ', 'do': 'ド',
    'ba': 'バ', 'bi': 'ビ', 'bu': 'ブ', 'be': 'ベ', 'bo': 'ボ',
    'pa': 'パ', 'pi': 'ピ', 'pu': 'プ', 'pe': 'ペ', 'po': 'ポ',
    'dri': 'ドライ', 've': 'ブ',
    'li': 'リ', 'ce': 'ス'
}


katakana_engrish_map = {
    'ba': 'バ', 'be': 'ベ', 'bi': 'ビ', 'bo': 'ボ', 'bu': 'ブ', 'ca': 'カ', 'ce': 'セ', 'ci': 'シ', 'co': 'コ', 'cu': 'ク', 'da': 'ダ', 'de': 'デ', 'di': 'ヂ', 'do': 'ド', 'du': 'ヅ', 'fa': 'ファ', 'fe': 'フェ', 'fi': 'フィ', 'fo': 'フォ', 'fu': 'フ', 'ga': 'ガ', 'ge': 'ゲ', 'gi': 'ギ', 'go': 'ゴ', 'gu': 'グ', 'ha': 'ハ', 'he': 'ヘ', 'hi': 'ヒ', 'ho': 'ホ', 'hu': 'フ', 'ja': 'ジャ', 'je': 'ジェ', 'ji': 'ジ', 'jo': 'ジョ', 'ju': 'ジュ', 'ka': 'カ', 'ke': 'ケ', 'ki': 'キ', 'ko': 'コ', 'ku': 'ク', 'la': 'ラ', 'le': 'レ', 'li': 'リ', 'lo': 'ロ', 'lu': 'ル', 'ma': 'マ', 'me': 'メ', 'mi': 'ミ', 'mo': 'モ', 'mu': 'ム', 'n': 'ン', 'na': 'ナ', 'ne': 'ネ', 'ni': 'ニ', 'no': 'ノ', 'nu': 'ヌ', 'pa': 'パ', 'pe': 'ペ', 'pi': 'ピ', 'po': 'ポ', 'pu': 'プ', 'qa': 'クァ', 'qe': 'クェ', 'qi': 'クィ', 'qo': 'クォ', 'qu': 'ク', 'ra': 'ラ', 're': 'レ', 'ri': 'リ', 'ro': 'ロ', 'ru': 'ル', 'sa': 'サ', 'se': 'セ', 'si': 'スィ', 'so': 'ソ', 'su': 'ス', 'ta': 'タ', 'te': 'テ', 'th': 'テ', 'ti': 'ティ', 'to': 'ト', 'tu': 'トゥ', 'va': 'ヴァ', 've': 'ヴェ', 'vi': 'ヴィ', 'vo': 'ヴォ', 'vu': 'ヴ', 'wa': 'ワ', 'we': 'ウェ', 'wi': 'ウィ', 'wo': 'ヲ', 'wu': 'ウ', 'xa': 'ザ', 'xe': 'ゼ', 'xi': 'ジ', 'xo': 'ゾ', 'xu': 'ズ', 'ya': 'ヤ', 'ye': 'イェ', 'yi': 'イ', 'yo': 'ヨ', 'yu': 'ユ', 'za': 'ザ', 'ze': 'ゼ', 'zi': 'ジ', 'zo': 'ゾ', 'zu': 'ズ',
}

katakana_engrish_compound_map = {
    'bya': 'ビャ', 'bye': 'ビェ', 'byi': 'ビィ', 'byo': 'ビョ', 'byu': 'ビュ', 'cchi': 'ッチ', 'cha': 'チャ', 'che': 'チェ', 'chi': 'チィ', 'cho': 'チョ', 'chu': 'チュ', 'dha': 'デャ', 'dhe': 'デェ', 'dho': 'デョ', 'dhu': 'デュ', 'dwa': 'ドァ', 'dwe': 'ドェ', 'dwi': 'ドィ', 'dwo': 'ドォ', 'gya': 'ギャ', 'gye': 'ギェ', 'gyi': 'ギィ', 'gyo': 'ギョ', 'gyu': 'ギュ', 'hya': 'ヒャ', 'hye': 'ヒェ', 'hyi': 'ヒィ', 'hyo': 'ヒョ', 'hyu': 'ヒュ', 'kka': 'ッカ', 'kke': 'ッケ', 'kki': 'ッキ', 'kko': 'ッコ', 'kku': 'ック', 'kwa': 'クァ', 'kwe': 'クェ', 'kwi': 'クィ', 'kwo': 'クォ', 'kya': 'キャ', 'kye': 'キェ', 'kyi': 'キィ', 'kyo': 'キョ', 'kyu': 'キュ', 'mya': 'ミャ', 'mye': 'ミェ', 'myi': 'ミィ', 'myo': 'ミョ', 'myu': 'ミュ', 'nya': 'ニャ', 'nye': 'ニェ', 'nyi': 'ニィ', 'nyo': 'ニョ', 'nyu': 'ニュ', 'ppa': 'ッパ', 'ppe': 'ッペ', 'ppi': 'ッピ', 'ppo': 'ッポ', 'ppu': 'ップ', 'pya': 'ピャ', 'pye': 'ピェ', 'pyi': 'ピィ', 'pyo': 'ピョ', 'pyu': 'ピュ', 'rya': 'リャ', 'rye': 'リェ', 'ryi': 'リィ', 'ryo': 'リョ', 'ryu': 'リュ', 'sha': 'シャ', 'she': 'シェ', 'shi': 'シィ', 'sho': 'ショ', 'shu': 'シュ', 'ssa': 'ッサ', 'sse': 'ッセ', 'sshi': 'ッシ', 'sso': 'ッソ', 'ssu': 'ッス', 'swa': 'スァ', 'swe': 'スェ', 'swi': 'スィ', 'swo': 'スォ', 'tha': 'テャ', 'the': 'テェ', 'tho': 'テョ', 'thu': 'テュ', 'tsa': 'ツァ', 'tse': 'ツェ', 'tsi': 'ツィ', 'tso': 'ツォ', 'tta': 'ッタ', 'tte': 'ッテ', 'tto': 'ット', 'ttsu': 'ッツ', 'twa': 'トァ', 'twe': 'トェ', 'twi': 'トィ', 'two': 'トォ', 'zwa': 'ズァ', 'zwe': 'ズェ', 'zwi': 'ズィ', 'zwo': 'ズォ',
}


def generate_katakana_dict_vowel_combo(consonant_pronunciations, blacklist_keys = {'ld'}):
    katakana_dict = {}
    for key in consonant_pronunciations:
        for vowel in vowel_combos.keys():
            # combo must be against non-vowel
            if len(key) <= 2 and key[-1] not in vowel_combos.keys() and key not in blacklist_keys:
                combo = key + vowel
                katakana_dict[combo] = consonant_pronunciations[key] + \
                    vowel_combos[vowel]
    return katakana_dict


def generate_katakana_dict_vowel_h(consonant_pronunciations):
    katakana_dict = {}
    for key in consonant_pronunciations:
        if key[-1] in vowel_combos.keys():
            combo = key + "h"
            katakana_dict[combo] = consonant_pronunciations[key] + 'ー'
    return katakana_dict


def generate_katakana_dict_vowel_extend(consonant_pronunciations):
    katakana_dict = {}
    for key in consonant_pronunciations:
        if key[-1] in vowel_combos.keys():
            combo = key + key[-1]
            katakana_dict[combo] = consonant_pronunciations[key] + 'ー'
    return katakana_dict


def generate_katakana_dict_double_consonant(katakana_engrish_map):
    katakana_engrish_compound_map = {}

    for key in katakana_engrish_map:
        for consonant in ['b', 'c', 'd', 'f', 'g', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 's', 't', 'v', 'x', 'z', 'h', 'r', 'w', 'y']:
            if consonant == key[0] and (len(key) >= 2 and consonant != key[1]):
                compound_key = consonant + key
                if compound_key not in katakana_engrish_compound_map:
                    # print(compound_key, katakana_engrish_map[key])
                    katakana_engrish_compound_map[compound_key] = 'ッ' + \
                        katakana_engrish_map[key]

    return katakana_engrish_compound_map

from . import utils
from . import engrish_map

english_to_engrish_map = utils.merge_dictionaries(
    engrish_map.english_to_engrish_map_,
    engrish_map.english_to_engrish_custom_map,
)


english_to_engrish_map = {
    **generate_katakana_dict_vowel_combo(english_to_engrish_map), **english_to_engrish_map}
english_to_engrish_map = {
    **generate_katakana_dict_vowel_h(english_to_engrish_map), **english_to_engrish_map}
english_to_engrish_map = {
    **generate_katakana_dict_vowel_extend(english_to_engrish_map), **english_to_engrish_map}

english_to_engrish_max_length = max(
    map(len, list(english_to_engrish_map.keys())))




katakana_map = {**katakana_map, **katakana_engrish_map}

katakana_engrish_compound_map_p = generate_katakana_dict_double_consonant(
    katakana_map)

katakana_engrish_compound_map = {**katakana_engrish_compound_map_p, **katakana_engrish_compound_map}

katakana_map = {**katakana_engrish_compound_map, **katakana_map}

katakana_map_max = max(map(len, list(katakana_map.keys())))





def english_to_engrish(text, mapping=english_to_engrish_map, mapping_max_length=english_to_engrish_max_length, keep_not_found=True):
    text = text.lower()
    engrish_text = ''
    logger.info(f"english_to_engrish {text}")

    i = 0
    while i < len(text):
        found_substring = False
        for sub_length in range(mapping_max_length, 0, -1):
            j = i + sub_length
            substring = text[i:j]
            if substring in mapping:
                logger.info(f'{substring} {mapping[substring]} {sub_length}')
                engrish_text += mapping[substring]
                i = j
                found_substring = True
                break
        
        if not found_substring:
            if text[i:i + 2] == r"\b":
                i += 1
            elif text[i:i + 1] != " ":
                logger.warn(
                    f"WARN: in english_to_engrish not found `{text[i:i+mapping_max_length]}`")
                if keep_not_found:
                    engrish_text += text[i]
            i += 1

    return engrish_text


def english_to_engrish_r(text, mapping=english_to_engrish_map, mapping_max_length=english_to_engrish_max_length):
    text = text.lower()
    engrish_text = ''

    i = len(text) - 1
    while i >= 0:
        found_substring = False
        for sub_length in range(mapping_max_length, 0, -1):
            j = i - sub_length + 1
            j = max(j, 0)
            substring = text[j:i + 1]
            if substring in mapping:
                # print(substring, mapping[substring], sub_length)
                engrish_text = mapping[substring] + engrish_text
                i = j - 1
                found_substring = True
                break

        if not found_substring:
            if text[i:i + 1] != " ":
                print(
                    f"WARN: in english_to_engrish not found `{text[i-mapping_max_length:i+1]}`")
            i -= 1

    return engrish_text
