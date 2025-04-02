import streamlit as st
from jamo import h2j, j2hcj
import unicodedata

def is_hangul_char(char):
    return 'HANGUL' in unicodedata.name(char, '')

# 자모 → 고대 문자 기호
decompose_chosung = {
    'ㄱ': 'ᚠ', 'ㄲ': 'ᚡ', 'ㄴ': 'ᚢ', 'ㄷ': 'ᚣ', 'ㄸ': 'ᚤ',
    'ㄹ': 'ᚥ', 'ㅁ': 'ᚦ', 'ㅂ': 'ᚧ', 'ㅃ': 'ᚨ', 'ㅅ': 'ᚩ',
    'ㅆ': 'ᚪ', 'ㅇ': 'ᚫ', 'ㅈ': 'ᚬ', 'ㅉ': 'ᚭ', 'ㅊ': 'ᚮ',
    'ㅋ': 'ᚯ', 'ㅌ': 'ᚰ', 'ㅍ': 'ᚱ', 'ㅎ': 'ᚲ'
}
decompose_jungsung = {
    'ㅏ': '𐤀', 'ㅐ': '𐤁', 'ㅑ': '𐤂', 'ㅒ': '𐤃', 'ㅓ': '𐤄',
    'ㅔ': '𐤅', 'ㅕ': '𐤆', 'ㅖ': '𐤇', 'ㅗ': '𐤈', 'ㅛ': '𐤉',
    'ㅜ': '𐤊', 'ㅠ': '𐤋', 'ㅡ': '𐤌', 'ㅣ': '𐤍', 'ㅘ': '𐤎',
    'ㅙ': '𐤏', 'ㅚ': '𐤐', 'ㅝ': '𐤑', 'ㅞ': '𐤒', 'ㅟ': '𐤓', 'ㅢ': '𐤔'
}
decompose_jongsung = {
    '': '', 'ㄱ': 'ᚳ', 'ㄲ': 'ᚴ', 'ㄳ': 'ᚵ', 'ㄴ': 'ᚶ',
    'ㄵ': 'ᚷ', 'ㄶ': 'ᚸ', 'ㄷ': 'ᚹ', 'ㄹ': 'ᚺ', 'ㄺ': 'ᚻ',
    'ㄻ': 'ᚼ', 'ㄼ': 'ᚽ', 'ㄽ': 'ᚾ', 'ㄾ': 'ᚿ', 'ㄿ': 'ᛀ',
    'ㅀ': 'ᛁ', 'ㅁ': 'ᛂ', 'ㅂ': 'ᛃ', 'ㅄ': 'ᛄ', 'ㅅ': 'ᛅ',
    'ㅆ': 'ᛆ', 'ㅇ': 'ᛇ', 'ㅈ': 'ᛈ', 'ㅊ': 'ᛉ', 'ㅋ': 'ᛊ',
    'ㅌ': 'ᛋ', 'ㅍ': 'ᛌ', 'ㅎ': 'ᛍ'
}

# 고대 문자 기호 → 자모
reverse_chosung = {v: k for k, v in decompose_chosung.items()}
reverse_jungsung = {v: k for k, v in decompose_jungsung.items()}
reverse_jongsung = {v: k for k, v in decompose_jongsung.items()}

CHOSUNG_LIST = list(decompose_chosung.keys())
JUNGSUNG_LIST = list(decompose_jungsung.keys())
JONGSUNG_LIST = list(decompose_jongsung.keys())

# 한글 자모 합치기 함수
def join_jamos_manual(jamos):
    result = ""
    i = 0
    while i < len(jamos):
        chosung = jamos[i]
        i += 1
        if i < len(jamos):
            jungsung = jamos[i]

            i += 1
            jongsung = ''
            # 종성인지 다음 글자 초성인지 확인
            if i < len(jamos) :
                jongsung = jamos[i]
                i += 1
                if i < len(jamos) :
                    next_chr = jamos[i]

                    if ord("ㄱ") > ord(next_chr) or ord(next_chr) > ord("ㅎ") :  # 자음 범위가 아님 (jongsung은 다음 글자 초성)
                        jongsung = ""
                        i -= 1

            # 한글 문자로 합치기
            result += chr(0xAC00 + ((chosung * 21) + jungsung) * 28 + jongsung)
        else:
            break  # 중성이 없는 경우
    return result

st.set_page_config(page_title="고대 문자 한글 변환기")
st.title("ᚠ𐤀 고대 문자 한글 변환기")

tabs = st.tabs(["한글 → 기호", "기호 → 한글"])

if "symbol_result" not in st.session_state:
    st.session_state.symbol_result = ""
if "hangul_result" not in st.session_state:
    st.session_state.hangul_result = ""

# 🔤 한글 → 기호
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
            else:
                result += char
        st.session_state.symbol_result = result

    if st.session_state.symbol_result:
        st.text_area("기호 출력", st.session_state.symbol_result, height=150, key="output1")

# 🔁 기호 → 한글
with tabs[1]:
    symbol_input = st.text_area("기호 입력", height=150, key="input2")
    st.markdown("<p style='color: gray; font-size: 13px;'>👉 기호를 붙여넣어 주세요!</p>", unsafe_allow_html=True)

    if st.button("한글로 되돌리기", key="to_korean"):
        jamo_result = []
        i = 0
        while i < len(symbol_input):
            if symbol_input[i] in reverse_chosung:
                cho = reverse_chosung[symbol_input[i]]
                i += 1
                if i < len(symbol_input) and symbol_input[i] in reverse_jungsung:
                    jung = reverse_jungsung[symbol_input[i]]
                    i += 1
                    if i < len(symbol_input) and symbol_input[i] in reverse_jongsung:
                        if i+1 == len(symbol_input) or symbol_input[i+1] in reverse_chosung:
                            jong = reverse_jongsung[symbol_input[i]]
                            i += 1
                            jamo_result.extend([cho, jung, jong])
                        else:
                            jamo_result.extend([cho, jung])
                    else:
                        jamo_result.extend([cho, jung])
                else:
                    jamo_result.append(cho)
            else:
                jamo_result.append(symbol_input[i])
                i += 1

        result = join_jamos_manual(jamo_result)
        st.session_state.hangul_result = result

    if st.session_state.hangul_result:
        st.markdown("### 복원된 한글:")
        st.success(st.session_state.hangul_result)
