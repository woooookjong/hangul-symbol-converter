import streamlit as st
from jamo import h2j, j2hcj
import unicodedata

CHOSUNG_LIST = ['ㄱ','ㄲ','ㄴ','ㄷ','ㄸ','ㄹ','ㅁ','ㅂ','ㅃ','ㅅ','ㅆ','ㅇ','ㅈ','ㅉ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']
JUNGSUNG_LIST = ['ㅏ','ㅐ','ㅑ','ㅒ','ㅓ','ㅔ','ㅕ','ㅖ','ㅗ','ㅘ','ㅙ','ㅚ','ㅛ','ㅜ','ㅝ','ㅞ','ㅟ','ㅠ','ㅡ','ㅢ','ㅣ']
JONGSUNG_LIST = ['', 'ㄱ','ㄲ','ㄳ','ㄴ','ㄵ','ㄶ','ㄷ','ㄹ','ㄺ','ㄻ','ㄼ','ㄽ','ㄾ','ㄿ','ㅀ','ㅁ','ㅂ','ㅄ','ㅅ','ㅆ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']

decompose_chosung = {'ㄱ': 'ᚠ', 'ㄲ': 'ᚡ', 'ㄴ': 'ᚢ', 'ㄷ': 'ᚣ', 'ㄸ': 'ᚤ','ㄹ': 'ᚥ', 'ㅁ': 'ᚦ', 'ㅂ': 'ᚧ', 'ㅃ': 'ᚨ', 'ㅅ': 'ᚩ','ㅆ': 'ᚪ', 'ㅇ': 'ᚫ', 'ㅈ': 'ᚬ', 'ㅉ': 'ᚭ', 'ㅊ': 'ᚮ','ㅋ': 'ᚯ', 'ㅌ': 'ᚰ', 'ㅍ': 'ᚱ', 'ㅎ': 'ᚲ'}
decompose_jungsung = {'ㅏ': '𐔀', 'ㅐ': '𐔁', 'ㅑ': '𐔂', 'ㅒ': '𐔃', 'ㅓ': '𐔄','ㅔ': '𐔅', 'ㅕ': '𐔆', 'ㅖ': '𐔇', 'ㅗ': '𐔈', 'ㅘ': '𐔉','ㅙ': '𐔊', 'ㅚ': '𐔋', 'ㅛ': '𐔌', 'ㅜ': '𐔍', 'ㅝ': '𐔎','ㅞ': '𐔏', 'ㅟ': '𐔐', 'ㅠ': '𐔑', 'ㅡ': '𐔒', 'ㅢ': '𐔓', 'ㅣ': '𐔔'}
decompose_jongsung = {'': '', 'ㄱ': 'ᚳ', 'ㄲ': 'ᚴ', 'ㄳ': 'ᚵ', 'ㄴ': 'ᚶ','ㄵ': 'ᚷ', 'ㄶ': 'ᚸ', 'ㄷ': 'ᚹ', 'ㄹ': 'ᚺ', 'ㄺ': 'ᚻ','ㄻ': 'ᚼ', 'ㄼ': 'ᚽ', 'ㄽ': 'ᚾ', 'ㄾ': 'ᚿ', 'ㄿ': 'ᛀ','ㅀ': 'ᛁ', 'ㅁ': 'ᛂ', 'ㅂ': 'ᛃ', 'ㅄ': 'ᛄ', 'ㅅ': 'ᛅ','ㅆ': 'ᛆ', 'ㅇ': 'ᛇ', 'ㅈ': 'ᛈ', 'ㅊ': 'ᛉ', 'ㅋ': 'ᛊ','ㅌ': 'ᛋ', 'ㅍ': 'ᛌ', 'ㅎ': 'ᛍ'}

special_symbols = {'?': 'ꡞ', '!': '႟', '.': '꘏', ',': '᛬'}
reverse_special = {v: k for k, v in special_symbols.items()}
reverse_chosung = {v: k for k, v in decompose_chosung.items()}
reverse_jungsung = {v: k for k, v in decompose_jungsung.items()}
reverse_jongsung = {v: k for k, v in decompose_jongsung.items()}

def is_hangul_char(char):
    return 'HANGUL' in unicodedata.name(char, '')

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
                    next_j = jamos[i+3] if i+3 < len(jamos) else ''
                    if next_j in CHOSUNG_LIST or next_j in reverse_special or next_j == '' or next_j == ' ':
                        jong = JONGSUNG_LIST.index(jamos[i+2])
                        i += 1
                result += chr(0xAC00 + cho * 588 + jung * 28 + jong)
                i += 2
            else:
                result += jamos[i]
                i += 1
        else:
            result += jamos[i]
            i += 1
    return result

st.set_page_config(page_title="아르카키 - 고대 문자 한글 변환기")
st.title("🔤 아르카키 : 고대 문자 ↔ 한글 변환기")

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
            if char == " ":
                result += " "
            elif char in special_symbols:
                result += special_symbols[char]
            elif is_hangul_char(char):
                decomposed = list(j2hcj(h2j(char)))
                cho = decomposed[0]
                jung = decomposed[1]
                jong = decomposed[2] if len(decomposed) == 3 else ''
                result += decompose_chosung.get(cho, cho)
                result += decompose_jungsung.get(jung, jung)
                result += decompose_jongsung.get(jong, jong)
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
            ch = symbol_input[i]
            next_ch = symbol_input[i+1] if i+1 < len(symbol_input) else ''
            next_next_ch = symbol_input[i+2] if i+2 < len(symbol_input) else ''
            next_3 = symbol_input[i+3] if i+3 < len(symbol_input) else ''

            if ch == ' ':
                jamo_result.append(' ')
                i += 1
            elif ch in reverse_special:
                jamo_result.append(reverse_special[ch])
                i += 1
            elif ch in reverse_chosung and ch not in reverse_jongsung:
                if next_ch in reverse_jungsung:
                    cho = reverse_chosung[ch]
                    jung = reverse_jungsung[next_ch]
                    jong = ''
                    if next_next_ch in reverse_jongsung:
                        if next_3 in reverse_chosung or next_3 in reverse_special or next_3 == '' or next_3 == ' ':
                            jong = reverse_jongsung[next_next_ch]
                            jamo_result.extend([cho, jung, jong])
                            i += 3
                        else:
                            jamo_result.extend([cho, jung])
                            i += 2
                    else:
                        jamo_result.extend([cho, jung])
                        i += 2
                else:
                    jamo_result.append(reverse_chosung[ch])
                    i += 1
            elif ch in reverse_jongsung:
                next_char = symbol_input[i+1] if i+1 < len(symbol_input) else ''
                if next_char in reverse_chosung or next_char in reverse_special or next_char == '' or next_char == ' ':
                    jamo_result.append(reverse_jongsung[ch])
                else:
                    jamo_result.append(reverse_jongsung[ch])
                i += 1
            else:
                jamo_result.append(ch)
                i += 1

        result = join_jamos_manual(jamo_result)
        st.session_state.hangul_result = result

    if st.session_state.hangul_result:
        st.markdown("### 복원된 한글:")
        st.success(st.session_state.hangul_result)
