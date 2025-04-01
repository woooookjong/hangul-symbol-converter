import streamlit as st
from jamo import h2j, j2hcj
import unicodedata
import html

# 한글 여부 판단 함수
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
    'ㅏ': '𐤀', 'ㅐ': '𐤁', 'ㅑ': '𐤂', 'ㅒ': '𐤃',
    'ㅓ': '𐤄', 'ㅔ': '𐤅', 'ㅕ': '𐤆', 'ㅖ': '𐤇',
    'ㅗ': '𐤈', 'ㅛ': '𐤉', 'ㅜ': '𐤊', 'ㅠ': '𐤋',
    'ㅡ': '𐤌', 'ㅣ': '𐤍', 'ㅘ': '𐤎', 'ㅙ': '𐤏',
    'ㅚ': '𐤐', 'ㅝ': '𐤑', 'ㅞ': '𐤒', 'ㅟ': '𐤓', 'ㅢ': '𐤔'
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

# 기호도 기호 느낌이 안 나도록 (유니코드 문자 스타일로 대체)
punctuation_map = {
    '?': '⸮', '!': '⸘', '.': '꞉', ',': '‚', ':': '⁚',
    ';': '⁏', '(': '❨', ')': '❩', '"': 'ˮ', "'": 'ʼ'
}

# 역변환용 딕셔너리
reverse_chosung = {v: k for k, v in decompose_chosung.items()}
reverse_jungsung = {v: k for k, v in decompose_jungsung.items()}
reverse_jongsung = {v: k for k, v in decompose_jongsung.items()}
reverse_punctuation = {v: k for k, v in punctuation_map.items()}

CHOSUNG_LIST = list(decompose_chosung.keys())
JUNGSUNG_LIST = list(decompose_jungsung.keys())
JONGSUNG_LIST = list(decompose_jongsung.keys())

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
                    i += 1  # 종성 스킵
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

st.title("ᚠ𐤀 고대 문자 한글 변환기")

tabs = st.tabs(["한글 → 기호", "기호 → 한글"])

if "symbol_result" not in st.session_state:
    st.session_state.symbol_result = ""
if "hangul_result" not in st.session_state:
    st.session_state.hangul_result = ""

with tabs[0]:
    input_text = st.text_area("한글 입력", height=150, key="input1")
    if st.button("기호로 변환하기", key="to_symbols"):
        result = ""
        for char in input_text:
            if char in punctuation_map:
                result += punctuation_map[char]
            elif is_hangul_char(char):
                decomposed = list(j2hcj(h2j(char)))
                if len(decomposed) == 3:
                    result += decompose_chosung.get(decomposed[0], decomposed[0])
                    result += decompose_jungsung.get(decomposed[1], decomposed[1])
                    result += decompose_jongsung.get(decomposed[2], decomposed[2])
                elif len(decomposed) == 2:
                    result += decompose_chosung.get(decomposed[0], decomposed[0])
                    result += decompose_jungsung.get(decomposed[1], decomposed[1])
                else:
                    result += ''.join(decomposed)
            else:
                result += char
        st.session_state.symbol_result = result

    if st.session_state.symbol_result:
        st.text_area("기호 언어 출력", st.session_state.symbol_result, height=150, key="output1")

with tabs[1]:
    symbol_input = st.text_area("기호 입력", height=150, key="input2")
    st.markdown("<p style='color: gray; font-size: 13px;'>👉 클립보드에 복사한 기호를 여기에 붙여넣어 주세요! (Ctrl+V 또는 ⌘+V) 🐣</p>", unsafe_allow_html=True)
    if st.button("한글로 되돌리기", key="to_korean"):
        jamo_result = []
        i = 0
        while i < len(symbol_input):
            c = symbol_input[i]
            if c in reverse_chosung:
                cho = reverse_chosung[c]
                jung = ''
                jong = ''
                if i + 1 < len(symbol_input) and symbol_input[i+1] in reverse_jungsung:
                    jung = reverse_jungsung[symbol_input[i+1]]
                    if i + 2 < len(symbol_input) and symbol_input[i+2] in reverse_jongsung:
                        jong = reverse_jongsung[symbol_input[i+2]]
                        i += 1
                    jamo_result.extend([cho, jung, jong])
                    i += 2
                else:
                    jamo_result.append(cho)
                    i += 1
            elif c in reverse_jungsung:
                jamo_result.append(reverse_jungsung[c])
                i += 1
            elif c in reverse_jongsung:
                jamo_result.append(reverse_jongsung[c])
                i += 1
            elif c in reverse_punctuation:
                jamo_result.append(reverse_punctuation[c])
                i += 1
            else:
                jamo_result.append(c)
                i += 1

        result = join_jamos_manual(jamo_result)
        st.session_state.hangul_result = result

    if st.session_state.hangul_result:
        st.text_area("복원된 한글 출력", st.session_state.hangul_result, height=150, key="output2")
