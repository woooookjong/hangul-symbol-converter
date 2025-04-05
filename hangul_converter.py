import streamlit as st
from jamo import h2j, j2hcj
import unicodedata

SPACE_SYMBOL = '𐤟'

decompose_chosung = {
    'ㄱ': 'ᚠ', 'ㄲ': 'ᚡ', 'ㄴ': 'ᚢ', 'ㄷ': 'ᚣ', 'ㄸ': 'ᚤ',
    'ㄹ': 'ᚥ', 'ㅁ': 'ᚦ', 'ㅂ': 'ᚧ', 'ㅃ': 'ᚨ', 'ㅅ': 'ᚩ',
    'ㅆ': 'ᚪ', 'ㅇ': 'ᚫ', 'ㅈ': 'ᚬ', 'ㅉ': 'ᚭ', 'ㅊ': 'ᚮ',
    'ㅋ': 'ᚯ', 'ㅌ': 'ᚰ', 'ㅍ': 'ᚱ', 'ㅎ': 'ᚲ'
}

decompose_jungsung = {
    'ㅏ': '𐔀', 'ㅐ': '𐔁', 'ㅑ': '𐔂', 'ㅒ': '𐔃', 'ㅓ': '𐔄',
    'ㅔ': '𐔅', 'ㅕ': '𐔆', 'ㅖ': '𐔇', 'ㅗ': '𐔈', 'ㅛ': '𐔉',
    'ㅜ': '𐔊', 'ㅠ': '𐔋', 'ㅡ': '𐔌', 'ㅣ': '𐔍',
    'ㅘ': '𐔎', 'ㅙ': '𐔏', 'ㅚ': '𐔐', 'ㅝ': '𐔑',
    'ㅞ': '𐔒', 'ㅟ': '𐔓', 'ㅢ': '𐔔'
}

decompose_jongsung = {
    '': '', 'ㄱ': 'ᛅ', 'ㄲ': 'ᛆ', 'ㄳ': 'ᛇ', 'ㄴ': 'ᛈ',
    'ㄵ': 'ᛉ', 'ㄶ': 'ᛊ', 'ㄷ': 'ᛋ', 'ㄹ': 'ᛌ', 'ㄺ': 'ᛍ',
    'ㄻ': 'ᛎ', 'ㄼ': 'ᛏ', 'ㄽ': 'ᛐ', 'ㄾ': 'ᛑ', 'ㄿ': 'ᛒ',
    'ㅀ': 'ᛓ', 'ㅁ': 'ᛔ', 'ㅂ': 'ᛕ', 'ㅄ': 'ᛖ', 'ㅅ': 'ᛗ',
    'ㅆ': 'ᛘ', 'ㅇ': 'ᛙ', 'ㅈ': 'ᛚ', 'ㅊ': 'ᛛ', 'ㅋ': 'ᛜ',
    'ㅌ': 'ᛝ', 'ㅍ': 'ᛞ', 'ㅎ': 'ᛟ'
}

reverse_chosung = {v: k for k, v in decompose_chosung.items()}
reverse_jungsung = {v: k for k, v in decompose_jungsung.items()}
reverse_jongsung = {v: k for k, v in decompose_jongsung.items()}

CHOSUNG_LIST = list(decompose_chosung.keys())
JUNGSUNG_LIST = list(decompose_jungsung.keys())
JONGSUNG_LIST = list(decompose_jongsung.keys())

def join_jamos_manual_groups(jamo_groups):
    result = ""
    for group in jamo_groups:
        if group == [" "]:
            result += " "
            continue
        cho, jung = group[0], group[1]
        jong = group[2] if len(group) == 3 else ""
        cho_idx = CHOSUNG_LIST.index(cho)
        jung_idx = JUNGSUNG_LIST.index(jung)
        jong_idx = JONGSUNG_LIST.index(jong) if jong else 0
        result += chr(0xAC00 + cho_idx * 588 + jung_idx * 28 + jong_idx)
    return result

st.set_page_config(page_title="기호 한글 변환기")
st.title("ᚠ𐔀 고대 기호 한글 변환기")

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
            if unicodedata.name(char, '').startswith("HANGUL"):
                decomposed = list(j2hcj(h2j(char)))
                if len(decomposed) == 3:
                    cho, jung, jong = decomposed
                    result += decompose_chosung.get(cho, cho)
                    result += decompose_jungsung.get(jung, jung)
                    result += decompose_jongsung.get(jong, jong)
                elif len(decomposed) == 2:
                    cho, jung = decomposed
                    result += decompose_chosung.get(cho, cho)
                    result += decompose_jungsung.get(jung, jung)
            elif char == " ":
                result += SPACE_SYMBOL
            else:
                result += char
        st.session_state.symbol_result = result

    st.text_area("기호 출력", st.session_state.symbol_result, height=150)

with tabs[1]:
    symbol_input = st.text_area("기호 입력", height=150)
    if st.button("한글로 되돌리기"):
        jamo_groups = []
        i = 0
        while i < len(symbol_input):
            if symbol_input[i] == SPACE_SYMBOL:
                jamo_groups.append([" "])
                i += 1
                continue
            if symbol_input[i] in reverse_chosung:
                cho = reverse_chosung[symbol_input[i]]
                jung = ''
                jong = ''
                i += 1
                if i < len(symbol_input) and symbol_input[i] in reverse_jungsung:
                    jung = reverse_jungsung[symbol_input[i]]
                    i += 1
                    if i < len(symbol_input) and symbol_input[i] in reverse_jongsung:
                        lookahead = symbol_input[i+1] if i+1 < len(symbol_input) else ''
                        if lookahead in reverse_chosung or lookahead == SPACE_SYMBOL or lookahead == '':
                            jong = reverse_jongsung[symbol_input[i]]
                            i += 1
                group = [cho, jung] + ([jong] if jong else [])
                jamo_groups.append(group)
            else:
                i += 1
        st.session_state.hangul_result = join_jamos_manual_groups(jamo_groups)

    st.text_area("복원된 한글", st.session_state.hangul_result, height=150)
