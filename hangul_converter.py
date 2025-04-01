import streamlit as st
from jamo import h2j, j2hcj
import unicodedata
import streamlit.components.v1 as components

# 한글 여부 판단 함수
def is_hangul_char(char):
    return 'HANGUL' in unicodedata.name(char, '')

# 자음과 모음 기호 매핑 (중복 없는 고대 스타일)
decompose_consonants = {
    'ㄱ': '𐎀', 'ㄴ': '𐎐', 'ㄷ': '𐎂', 'ㄹ': '𐎑', 'ㅁ': '𐎄',
    'ㅂ': '𐎅', 'ㅅ': '𐎃', 'ㅇ': '𐎊', 'ㅈ': '𐎆', 'ㅊ': '𐎇',
    'ㅋ': '𐎚', 'ㅌ': '𐎛', 'ㅍ': '𐎜', 'ㅎ': '𐎟'
}

decompose_vowels = {
    'ㅏ': '𐎠', 'ㅐ': '𐎡', 'ㅑ': '𐎢', 'ㅒ': '𐎣',
    'ㅓ': '𐎤', 'ㅔ': '𐎥', 'ㅕ': '𐎦', 'ㅖ': '𐎧',
    'ㅗ': '𐎨', 'ㅛ': '𐎩', 'ㅜ': '𐎪', 'ㅠ': '𐎫',
    'ㅡ': '𐎬', 'ㅣ': '𐎭',
    'ㅘ': '𐎵', 'ㅙ': '𐎶', 'ㅚ': '𐎷', 'ㅝ': '𐎸',
    'ㅞ': '𐎹', 'ㅟ': '𐎺', 'ㅢ': '𐎻'
}

final_consonants = {
    'ㄱ': '𐎰', 'ㄴ': '𐎱', 'ㄷ': '𐎲', 'ㄹ': '𐎳', 'ㅁ': '𐎴',
    'ㅂ': '𐎽', 'ㅅ': '𐎾', 'ㅇ': '𐎿', 'ㅈ': '𐏀', 'ㅊ': '𐏁',
    'ㅋ': '𐏂', 'ㅌ': '𐏃', 'ㅍ': '𐏄', 'ㅎ': '𐏅'
}

# 구두점 기호 매핑 (복원 가능하게)
punctuation_map = {
    '?': '⸮', '!': '‼', '.': '⨀', ',': '⸲', ':': '꞉',
    ';': '⁏', '(': '⸦', ')': '⸧', '"': '⸢⸣', "'": '⸤⸥'
}

# 역변환용 딕셔너리
reverse_consonants = {v: k for k, v in decompose_consonants.items()}
reverse_vowels = {v: k for k, v in decompose_vowels.items()}
reverse_final = {v: k for k, v in final_consonants.items()}
reverse_punctuation = {v: k for k, v in punctuation_map.items()}

CHOSUNG_LIST = ["ㄱ", "ㄲ", "ㄴ", "ㄷ", "ㄸ", "ㄹ", "ㅁ", "ㅂ", "ㅃ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅉ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]
JUNGSUNG_LIST = ["ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ", "ㅔ", "ㅕ", "ㅖ", "ㅗ", "ㅘ", "ㅙ", "ㅚ", "ㅛ", "ㅜ", "ㅝ", "ㅞ", "ㅟ", "ㅠ", "ㅡ", "ㅢ", "ㅣ"]
JONGSUNG_LIST = ["", "ㄱ", "ㄲ", "ㄳ", "ㄴ", "ㄵ", "ㄶ", "ㄷ", "ㄹ", "ㄺ", "ㄻ", "ㄼ", "ㄽ", "ㄾ", "ㄿ", "ㅀ", "ㅁ", "ㅂ", "ㅄ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]

def join_jamos_manual(jamos):
    result = ""
    i = 0
    while i < len(jamos):
        if jamos[i] in CHOSUNG_LIST:
            cho = CHOSUNG_LIST.index(jamos[i])
            if i + 1 < len(jamos) and jamos[i+1] in JUNGSUNG_LIST:
                jung = JUNGSUNG_LIST.index(jamos[i+1])
                jong = 0
                if i + 2 < len(jamos) and jamos[i+2] in JONGSUNG_LIST:
                    jong = JONGSUNG_LIST.index(jamos[i+2])
                    i += 1
                code = 0xAC00 + (cho * 21 * 28) + (jung * 28) + jong
                result += chr(code)
                i += 2
            else:
                result += jamos[i]
                i += 1
        else:
            result += jamos[i]
            i += 1
    return result

st.title("🪶 고대 기호 한글 변환기")

tabs = st.tabs(["한글 → 기호", "기호 → 한글"])

if "symbol_result" not in st.session_state:
    st.session_state.symbol_result = ""
if "hangul_result" not in st.session_state:
    st.session_state.hangul_result = ""

with tabs[0]:
    input_text = st.text_area("한글 입력", height=150)
    if st.button("기호로 변환하기"):
        result = ""
        for char in input_text:
            if char in punctuation_map:
                result += punctuation_map[char]
            elif is_hangul_char(char):
                decomposed = list(j2hcj(h2j(char)))
                for j in decomposed:
                    if j in decompose_consonants:
                        result += decompose_consonants[j]
                    elif j in decompose_vowels:
                        result += decompose_vowels[j]
                    elif j in final_consonants:
                        result += final_consonants[j]
                    else:
                        result += j
            else:
                result += char
        st.session_state.symbol_result = result

    if st.session_state.symbol_result:
        st.text_area("기호 언어 출력", st.session_state.symbol_result, height=150)

with tabs[1]:
    symbol_input = st.text_area("기호 입력", height=150)
    st.markdown("<p style='color: gray; font-size: 13px;'>👉 클립보드에 복사한 기호를 여기에 붙여넣어 주세요! 🐣</p>", unsafe_allow_html=True)
    if st.button("한글로 되돌리기"):
        jamo_result = ""
        for char in symbol_input:
            if char in reverse_consonants:
                jamo_result += reverse_consonants[char]
            elif char in reverse_vowels:
                jamo_result += reverse_vowels[char]
            elif char in reverse_final:
                jamo_result += reverse_final[char]
            elif char in reverse_punctuation:
                jamo_result += reverse_punctuation[char]
            else:
                jamo_result += char
        result = join_jamos_manual(jamo_result)
        st.session_state.hangul_result = result

    if st.session_state.hangul_result:
        st.text_area("복원된 한글 출력", st.session_state.hangul_result, height=150)
