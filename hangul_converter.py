import streamlit as st
from jamo import h2j, j2hcj
import unicodedata
import html

# 한글 여부 판단 함수
def is_hangul_char(char):
    return 'HANGUL' in unicodedata.name(char, '')

# 초성, 중성, 종성 기호 매핑 (고대 스타일)
decompose_chosung = {
    'ㄱ': '𐎀', 'ㄲ': '𐎁', 'ㄴ': '𐎂', 'ㄷ': '𐎃', 'ㄸ': '𐎄',
    'ㄹ': '𐎅', 'ㅁ': '𐎆', 'ㅂ': '𐎇', 'ㅃ': '𐎈', 'ㅅ': '𐎉',
    'ㅆ': '𐎊', 'ㅇ': '𐎋', 'ㅈ': '𐎌', 'ㅉ': '𐎍', 'ㅊ': '𐎎',
    'ㅋ': '𐎏', 'ㅌ': '𐎐', 'ㅍ': '𐎑', 'ㅎ': '𐎒'
}

decompose_jungsung = {
    'ㅏ': '𐎓', 'ㅐ': '𐎔', 'ㅑ': '𐎕', 'ㅒ': '𐎖',
    'ㅓ': '𐎗', 'ㅔ': '𐎘', 'ㅕ': '𐎙', 'ㅖ': '𐎚',
    'ㅗ': '𐎛', 'ㅛ': '𐎜', 'ㅜ': '𐎝', 'ㅠ': '𐎞',
    'ㅡ': '𐎟', 'ㅣ': '𐎠', 'ㅘ': '𐎡', 'ㅙ': '𐎢', 'ㅚ': '𐎣',
    'ㅝ': '𐎤', 'ㅞ': '𐎥', 'ㅟ': '𐎦', 'ㅢ': '𐎧'
}

decompose_jongsung = {
    '': '', 'ㄱ': '𐎨', 'ㄲ': '𐎩', 'ㄳ': '𐎪', 'ㄴ': '𐎫',
    'ㄵ': '𐎬', 'ㄶ': '𐎭', 'ㄷ': '𐎮', 'ㄹ': '𐎯', 'ㄺ': '𐎰',
    'ㄻ': '𐎱', 'ㄼ': '𐎲', 'ㄽ': '𐎳', 'ㄾ': '𐎴', 'ㄿ': '𐎵',
    'ㅀ': '𐎶', 'ㅁ': '𐎷', 'ㅂ': '𐎸', 'ㅄ': '𐎹', 'ㅅ': '𐎺',
    'ㅆ': '𐎻', 'ㅇ': '𐎼', 'ㅈ': '𐎽', 'ㅊ': '𐎾', 'ㅋ': '𐎿',
    'ㅌ': '𐏀', 'ㅍ': '𐏁', 'ㅎ': '𐏂'
}

# 역변환용 딕셔너리
reverse_chosung = {v: k for k, v in decompose_chosung.items()}
reverse_jungsung = {v: k for k, v in decompose_jungsung.items()}
reverse_jongsung = {v: k for k, v in decompose_jongsung.items()}

punctuation_map = {
    '?': '☯', '!': '⚡', '.': '⨀', ',': '⋖', ':': '⸬',
    ';': '⧫', '(': '༺', ')': '༻', '"': '꧁꧂', "'": '⌯'
}
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
            if symbol_input[i] in reverse_chosung:
                cho = reverse_chosung[symbol_input[i]]
                if i+1 < len(symbol_input) and symbol_input[i+1] in reverse_jungsung:
                    jung = reverse_jungsung[symbol_input[i+1]]
                    jong = ''
                    if i+2 < len(symbol_input) and symbol_input[i+2] in reverse_jongsung:
                        jong = reverse_jongsung[symbol_input[i+2]]
                        i += 1
                    jamo_result.extend([cho, jung, jong])
                    i += 2
                    continue
                else:
                    jamo_result.append(cho)
            elif symbol_input[i] in reverse_jungsung:
                jamo_result.append(reverse_jungsung[symbol_input[i]])
            elif symbol_input[i] in reverse_jongsung:
                jamo_result.append(reverse_jongsung[symbol_input[i]])
            elif symbol_input[i] in reverse_punctuation:
                jamo_result.append(reverse_punctuation[symbol_input[i]])
            else:
                jamo_result.append(symbol_input[i])
            i += 1

        result = join_jamos_manual(jamo_result)
        st.session_state.hangul_result = result

    if st.session_state.hangul_result:
        st.text_area("복원된 한글 출력", st.session_state.hangul_result, height=150, key="output2")
