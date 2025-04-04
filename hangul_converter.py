import streamlit as st
from jamo import h2j, j2hcj
import unicodedata

def is_hangul_char(char):
    return 'HANGUL' in unicodedata.name(char, '')

# 초성 기호
decompose_chosung = {
    'ㄱ': 'ᚠ', 'ㄲ': 'ᚡ', 'ㄴ': 'ᚢ', 'ㄷ': 'ᚣ', 'ㄸ': 'ᚤ',
    'ㄹ': 'ᚥ', 'ㅁ': 'ᚦ', 'ㅂ': 'ᚧ', 'ㅃ': 'ᚨ', 'ㅅ': 'ᚩ',
    'ㅆ': 'ᚪ', 'ㅇ': 'ᚫ', 'ㅈ': 'ᚬ', 'ㅉ': 'ᚭ', 'ㅊ': 'ᚮ',
    'ㅋ': 'ᚯ', 'ㅌ': 'ᚰ', 'ㅍ': 'ᚱ', 'ㅎ': 'ᚲ'
}

# 중성 기호 (중복 없음)
decompose_jungsung = {
    'ㅏ': '𐔀', 'ㅐ': '𐔁', 'ㅑ': '𐔂', 'ㅒ': '𐔃', 'ㅓ': '𐔄',
    'ㅔ': '𐔅', 'ㅕ': '𐔆', 'ㅖ': '𐔇', 'ㅗ': '𐔈', 'ㅛ': '𐔉',
    'ㅜ': '𐔊', 'ㅠ': '𐔋', 'ㅡ': '𐔌', 'ㅣ': '𐔍', 'ㅘ': '𐔎',
    'ㅙ': '𐔏', 'ㅚ': '𐔐', 'ㅝ': '𐔑', 'ㅞ': '𐔒', 'ㅟ': '𐔓', 'ㅢ': '𐔔'
}

# 종성 기호
decompose_jongsung = {
    '': '', 'ㄱ': 'ᚳ', 'ㄲ': 'ᚴ', 'ㄳ': 'ᚵ', 'ㄴ': 'ᚶ',
    'ㄵ': 'ᚷ', 'ㄶ': 'ᚸ', 'ㄷ': 'ᚹ', 'ㄹ': 'ᚺ', 'ㄺ': 'ᚻ',
    'ㄻ': 'ᚼ', 'ㄼ': 'ᚽ', 'ㄽ': 'ᚾ', 'ㄾ': 'ᚿ', 'ㄿ': 'ᛀ',
    'ㅀ': 'ᛁ', 'ㅁ': 'ᛂ', 'ㅂ': 'ᛃ', 'ㅄ': 'ᛄ', 'ㅅ': 'ᛅ',
    'ㅆ': 'ᛆ', 'ㅇ': 'ᛇ', 'ㅈ': 'ᛈ', 'ㅊ': 'ᛉ', 'ㅋ': 'ᛊ',
    'ㅌ': 'ᛋ', 'ㅍ': 'ᛌ', 'ㅎ': 'ᛍ'
}

# 역변환 (중성 수동 매핑)
reverse_chosung = {v: k for k, v in decompose_chosung.items()}
reverse_jongsung = {v: k for k, v in decompose_jongsung.items()}
reverse_jungsung = {
    '𐔀': 'ㅏ', '𐔁': 'ㅐ', '𐔂': 'ㅑ', '𐔃': 'ㅒ', '𐔄': 'ㅓ',
    '𐔅': 'ㅔ', '𐔆': 'ㅕ', '𐔇': 'ㅖ', '𐔈': 'ㅗ', '𐔉': 'ㅛ',
    '𐔊': 'ㅜ', '𐔋': 'ㅠ', '𐔌': 'ㅡ', '𐔍': 'ㅣ', '𐔎': 'ㅘ',
    '𐔏': 'ㅙ', '𐔐': 'ㅚ', '𐔑': 'ㅝ', '𐔒': 'ㅞ', '𐔓': 'ㅟ', '𐔔': 'ㅢ'
}

CHOSUNG_LIST = list(decompose_chosung.keys())
JUNGSUNG_LIST = list(decompose_jungsung.keys())
JONGSUNG_LIST = list(decompose_jongsung.keys())

def join_jamos_manual(jamos):
    result = ""
    i = 0
    while i < len(jamos):
        if jamos[i] in CHOSUNG_LIST:
            cho = CHOSUNG_LIST.index(jamos[i])
            jung = 0
            jong = 0
            if i + 1 < len(jamos) and jamos[i+1] in JUNGSUNG_LIST:
                jung = JUNGSUNG_LIST.index(jamos[i+1])
                if i + 2 < len(jamos) and jamos[i+2] in JONGSUNG_LIST:
                    if i + 3 == len(jamos) or jamos[i+3] in CHOSUNG_LIST:
                        jong = JONGSUNG_LIST.index(jamos[i+2])
                        result += chr(0xAC00 + (cho * 21 * 28) + (jung * 28) + jong)
                        i += 3
                        continue
                result += chr(0xAC00 + (cho * 21 * 28) + (jung * 28))
                i += 2
                continue
            else:
                result += jamos[i]
                i += 1
        else:
            result += jamos[i]
            i += 1
    return result

st.set_page_config(page_title="고대 문자 한글 변환기")
st.title("ᚠ𐔀 고대 문자 한글 변환기")

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
                result += decompose_jongsung.get(jong, jong)
        st.session_state.symbol_result = result
        st.code("기호 출력 리스트: " + str(list(result)))

    if st.session_state.symbol_result:
        st.text_area("기호 출력", st.session_state.symbol_result, height=150, key="output1")

# 기호 → 한글
with tabs[1]:
    symbol_input = st.text_area("기호 입력", height=150, key="input2")
    st.markdown("👉 기호를 붙여넣어 주세요!")

    if st.button("한글로 되돌리기", key="to_korean"):
        jamo_result = []
        i = 0
        while i < len(symbol_input):
            if symbol_input[i] in reverse_chosung:
                cho = reverse_chosung[symbol_input[i]]
                i += 1
                jung = ''
                if i < len(symbol_input) and symbol_input[i] in reverse_jungsung:
                    jung = reverse_jungsung[symbol_input[i]]
                    i += 1
                jong = ''
                if i < len(symbol_input) and symbol_input[i] in reverse_jongsung:
                    if i + 1 == len(symbol_input) or symbol_input[i+1] in reverse_chosung:
                        jong = reverse_jongsung[symbol_input[i]]
                        i += 1
                jamo_result.extend([cho, jung])
                if jong:
                    jamo_result.append(jong)
            else:
                jamo_result.append(symbol_input[i])
                i += 1

        result = join_jamos_manual(jamo_result)
        st.session_state.hangul_result = result

        # 디버그 출력
        st.code("symbol_input 리스트: " + str(list(symbol_input)))
        st.code("jamo_result 리스트: " + str(jamo_result))
        st.code("자모 디버그: " + " ".join(j2hcj(h2j(result))))
        st.code("유니코드 값: " + ", ".join(hex(ord(ch)) for ch in result))

    if st.session_state.hangul_result:
        st.markdown("### 복원된 한글:")
        st.success(st.session_state.hangul_result)
