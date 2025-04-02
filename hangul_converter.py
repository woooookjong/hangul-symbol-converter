import streamlit as st
from jamo import h2j, j2hcj
import unicodedata

def is_hangul_char(char):
    return 'HANGUL' in unicodedata.name(char, '')

# 초성 (룬 문자)
decompose_chosung = {
    'ㄱ': 'ᚠ', 'ㄲ': 'ᚡ', 'ㄴ': 'ᚢ', 'ㄷ': 'ᚣ', 'ㄸ': 'ᚤ',
    'ㄹ': 'ᚥ', 'ㅁ': 'ᚦ', 'ㅂ': 'ᚧ', 'ㅃ': 'ᚨ', 'ㅅ': 'ᚩ',
    'ㅆ': 'ᚪ', 'ㅇ': 'ᚫ', 'ㅈ': 'ᚬ', 'ㅉ': 'ᚭ', 'ㅊ': 'ᚮ',
    'ㅋ': 'ᚯ', 'ㅌ': 'ᚰ', 'ㅍ': 'ᚱ', 'ㅎ': 'ᚲ'
}

# 중성 (페니키아 문자)
decompose_jungsung = {
    'ㅏ': '𐤀', 'ㅐ': '𐤁', 'ㅑ': '𐤂', 'ㅒ': '𐤃', 'ㅓ': '𐤄',
    'ㅔ': '𐤅', 'ㅕ': '𐤆', 'ㅖ': '𐤇', 'ㅗ': '𐤈', 'ㅛ': '𐤉',
    'ㅜ': '𐤊', 'ㅠ': '𐤋', 'ㅡ': '𐤌', 'ㅣ': '𐤍', 'ㅘ': '𐤎',
    'ㅙ': '𐤏', 'ㅚ': '𐤐', 'ㅝ': '𐤑', 'ㅞ': '𐤒', 'ㅟ': '𐤓', 'ㅢ': '𐤔'
}

# 종성 (룬 확장)
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

# 글자 구분자
LETTER_SEPARATOR = '𐎁'

# 조합 함수
def join_jamos_manual(jamos):
    result = ""
    i = 0
    while i < len(jamos):
        if jamos[i] in CHOSUNG_LIST:
            cho = CHOSUNG_LIST.index(jamos[i])
            if i+1 < len(jamos) and jamos[i+1] in JUNGSUNG_LIST:
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
        else:
            result += jamos[i]
            i += 1
    return result

# Streamlit 시작
st.set_page_config(page_title="고대 문자 한글 변환기")
st.title("ᚠ𐤀 고대 문자 한글 변환기 (글자 구분자 포함)")
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
            if is_hangul_char(char):
                decomposed = list(j2hcj(h2j(char)))
                cho = decomposed[0]
                jung = decomposed[1]
                jong = decomposed[2] if len(decomposed) == 3 else ''
                result += decompose_chosung.get(cho, cho)
                result += decompose_jungsung.get(jung, jung)
                if jong:
                    result += decompose_jongsung.get(jong, jong)
                result += LETTER_SEPARATOR
            else:
                result += char
        st.session_state.symbol_result = result

    if st.session_state.symbol_result:
        st.text_area("기호 출력", st.session_state.symbol_result, height=150, key="output1")

# 기호 → 한글
with tabs[1]:
    symbol_input = st.text_area("기호 입력", height=150, key="input2")
    st.markdown("<p style='color: gray; font-size: 13px;'>👉 기호를 입력해 주세요! (각 글자는 𐎁 로 구분됨) 🐣</p>", unsafe_allow_html=True)

    if st.button("한글로 되돌리기", key="to_korean"):
        jamo_result = []
        syllables = symbol_input.split(LETTER_SEPARATOR)
        for block in syllables:
            if len(block) >= 2 and block[0] in reverse_chosung and block[1] in reverse_jungsung:
                cho = reverse_chosung[block[0]]
                jung = reverse_jungsung[block[1]]
                jong = ''
                if len(block) == 3 and block[2] in reverse_jongsung:
                    jong = reverse_jongsung[block[2]]
                jamo_result.extend([cho, jung])
                if jong:
                    jamo_result.append(jong)
            else:
                jamo_result.extend(list(block))

        result = join_jamos_manual(jamo_result)
        st.session_state.hangul_result = result

    if st.session_state.hangul_result:
        st.text_area("복원된 한글", st.session_state.hangul_result, height=150, key="output2")
