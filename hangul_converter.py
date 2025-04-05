import streamlit as st
from jamo import h2j, j2hcj
import unicodedata

# 문자 분리용 기호
SPACE_SYMBOL = '𐤟'

# 초성 (룬 문자)
decompose_chosung = {
    'ㄱ': 'ᚠ', 'ㄲ': 'ᚡ', 'ㄴ': 'ᚢ', 'ㄷ': 'ᚣ', 'ㄸ': 'ᚤ',
    'ㄹ': 'ᚥ', 'ㅁ': 'ᚦ', 'ㅂ': 'ᚧ', 'ㅃ': 'ᚨ', 'ㅅ': 'ᚩ',
    'ㅆ': 'ᚪ', 'ㅇ': 'ᚫ', 'ㅈ': 'ᚬ', 'ㅉ': 'ᚭ', 'ㅊ': 'ᚮ',
    'ㅋ': 'ᚯ', 'ㅌ': 'ᚰ', 'ㅍ': 'ᚱ', 'ㅎ': 'ᚲ'
}

# 중성 (페니키아 스타일)
decompose_jungsung = {
    'ㅏ': '𐔀', 'ㅐ': '𐔁', 'ㅑ': '𐔂', 'ㅒ': '𐔃', 'ㅓ': '𐔄',
    'ㅔ': '𐔅', 'ㅕ': '𐔆', 'ㅖ': '𐔇', 'ㅗ': '𐔈', 'ㅛ': '𐔉',
    'ㅜ': '𐔍', 'ㅠ': '𐔎', 'ㅡ': '𐔒', 'ㅣ': '𐔓',
    'ㅘ': '𐔐', 'ㅙ': '𐔑', 'ㅚ': '𐔒', 'ㅝ': '𐔓', 'ㅞ': '𐔔', 'ㅟ': '𐔕', 'ㅢ': '𐔖'
}

# 종성 (룬 문자 뒤쪽)
decompose_jongsung = {
    '': '', 'ㄱ': 'ᚳ', 'ㄲ': 'ᚴ', 'ㄳ': 'ᚵ', 'ㄴ': 'ᚶ',
    'ㄵ': 'ᚷ', 'ㄶ': 'ᚸ', 'ㄷ': 'ᚹ', 'ㄹ': 'ᚺ', 'ㄺ': 'ᚻ',
    'ㄻ': 'ᚼ', 'ㄼ': 'ᚽ', 'ㄽ': 'ᚾ', 'ㄾ': 'ᚿ', 'ㄿ': 'ᛀ',
    'ㅀ': 'ᛁ', 'ㅁ': 'ᛂ', 'ㅂ': 'ᛃ', 'ㅄ': 'ᛄ', 'ㅅ': 'ᛅ',
    'ㅆ': 'ᛆ', 'ㅇ': 'ᛇ', 'ㅈ': 'ᛈ', 'ㅊ': 'ᛉ', 'ㅋ': 'ᛊ',
    'ㅌ': 'ᛋ', 'ㅍ': 'ᛌ', 'ㅎ': 'ᛍ'
}

# 역변환
reverse_chosung = {v: k for k, v in decompose_chosung.items()}
reverse_jungsung = {v: k for k, v in decompose_jungsung.items()}
reverse_jongsung = {v: k for k, v in decompose_jongsung.items()}

CHOSUNG_LIST = list(decompose_chosung.keys())
JUNGSUNG_LIST = list(decompose_jungsung.keys())
JONGSUNG_LIST = list(decompose_jongsung.keys())

# 한글 조합 함수
def join_jamos_manual(jamos):
    result = ""
    i = 0
    while i < len(jamos):
        if jamos[i] == ' ':
            result += ' '
            i += 1
            continue
        if i+1 < len(jamos) and jamos[i] in CHOSUNG_LIST and jamos[i+1] in JUNGSUNG_LIST:
            cho = CHOSUNG_LIST.index(jamos[i])
            jung = JUNGSUNG_LIST.index(jamos[i+1])
            jong = 0
            if i+2 < len(jamos) and jamos[i+2] in JONGSUNG_LIST:
                jong = JONGSUNG_LIST.index(jamos[i+2])
                i += 1
            code = 0xAC00 + (cho * 21 * 28) + (jung * 28) + jong
            result += chr(code)
            i += 2
        else:
            result += jamos[i]
            i += 1
    return result

# Streamlit 시작
st.set_page_config(page_title="기호 한글 변환기")
st.title("ᚬ𐔄 고대 기호 한글 변환기")

tabs = st.tabs(["한글 → 기호", "기호 → 한글"])

if "symbol_result" not in st.session_state:
    st.session_state.symbol_result = ""
if "hangul_result" not in st.session_state:
    st.session_state.hangul_result = ""

# 한글 → 기호
with tabs[0]:
    input_text = st.text_area("한글 입력", height=150, key="input1")
    if st.button("기호로 변환하기", key="to_symbols"):
        result = ""
        for char in input_text:
            if unicodedata.name(char).startswith("HANGUL"):
                from jamo import h2j, j2hcj
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
            elif char == ' ':
                result += SPACE_SYMBOL
            else:
                result += char
        st.session_state.symbol_result = result

    if st.session_state.symbol_result:
        st.text_area("기호 출력", st.session_state.symbol_result, height=150, key="output1")

# 기호 → 한글
with tabs[1]:
    symbol_input = st.text_area("기호 입력", height=150, key="input2")
    if st.button("한글로 되돌리기", key="to_korean"):
        jamo_result = []
        i = 0
        while i < len(symbol_input):
            if symbol_input[i] == SPACE_SYMBOL:
                jamo_result.append(" ")
                i += 1
                continue
            if symbol_input[i] in reverse_chosung:
                cho = reverse_chosung[symbol_input[i]]
                if i + 1 < len(symbol_input) and symbol_input[i+1] in reverse_jungsung:
                    jung = reverse_jungsung[symbol_input[i+1]]
                    jong = ''
                    if i + 2 < len(symbol_input) and symbol_input[i+2] in reverse_jongsung:
                        jong = reverse_jongsung[symbol_input[i+2]]
                        i += 1
                    jamo_result.extend([cho, jung])
                    if jong:
                        jamo_result.append(jong)
                    i += 2
                else:
                    jamo_result.append(cho)
                    i += 1
            else:
                jamo_result.append(symbol_input[i])
                i += 1

        result = join_jamos_manual(jamo_result)
        st.session_state.hangul_result = result

    if st.session_state.hangul_result:
        st.markdown("### 복원된 한글:")
        st.success(st.session_state.hangul_result)
