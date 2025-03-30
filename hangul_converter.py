import streamlit as st
from jamo import h2j, j2hcj
import unicodedata
import streamlit.components.v1 as components

# 한글 여부 판단 함수
def is_hangul_char(char):
    return 'HANGUL' in unicodedata.name(char, '')

# 자음과 모음 기호 매핑 (정방향)
decompose_consonants = {
    'ㄱ': '𐎀', 'ㄴ': '𐎐', 'ㄷ': '𐎂', 'ㄹ': '𐎑', 'ㅁ': '𐎄',
    'ㅂ': '𐎅', 'ㅅ': '𐎃', 'ㅇ': '𐎊', 'ㅈ': '𐎆', 'ㅊ': '𐎇',
    'ㅋ': '𐎚', 'ㅌ': '𐎛', 'ㅍ': '𐎜', 'ㅎ': '𐎟'
}

decompose_vowels = {
    'ㅏ': '𐎠', 'ㅑ': '𐎢', 'ㅓ': '𐎤', 'ㅕ': '𐎦', 'ㅗ': '𐎨',
    'ㅛ': '𐎩', 'ㅜ': '𐎪', 'ㅠ': '𐎫', 'ㅡ': '𐎬', 'ㅣ': '𐎭',
    'ㅐ': '𐎡', 'ㅒ': '𐎣', 'ㅔ': '𐎥', 'ㅖ': '𐎧'
}

reverse_consonants = {v: k for k, v in decompose_consonants.items()}
reverse_vowels = {v: k for k, v in decompose_vowels.items()}

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

# 세션 초기화
if "symbol_result" not in st.session_state:
    st.session_state.symbol_result = ""
if "hangul_result" not in st.session_state:
    st.session_state.hangul_result = ""

with tabs[0]:
    input_text = st.text_area("한글 입력", height=150, key="input1")
    if st.button("기호로 변환하기", key="to_symbols"):
        result = ""
        for char in input_text:
            if is_hangul_char(char):
                decomposed = list(j2hcj(h2j(char)))
                for j in decomposed:
                    if j in decompose_consonants:
                        result += decompose_consonants[j]
                    elif j in decompose_vowels:
                        result += decompose_vowels[j]
                    else:
                        result += j
            else:
                result += char
        st.session_state.symbol_result = result

    if st.session_state.symbol_result:
        st.text_area("기호 언어 출력", st.session_state.symbol_result, height=150, key="output1")

        # 복사 버튼 + JS toast 안내 메시지
        copy_code = f"""
        <script>
        function copyToClipboard(text) {{
            navigator.clipboard.writeText(text);
            let toast = document.createElement("div");
            toast.innerText = "📋 복사 완료!";
            toast.style.position = "fixed";
            toast.style.bottom = "30px";
            toast.style.right = "30px";
            toast.style.backgroundColor = "#333";
            toast.style.color = "white";
            toast.style.padding = "10px 20px";
            toast.style.borderRadius = "10px";
            toast.style.boxShadow = "0 4px 6px rgba(0,0,0,0.1)";
            toast.style.zIndex = 1000;
            document.body.appendChild(toast);
            setTimeout(() => document.body.removeChild(toast), 2000);
        }}
        </script>
        <button onclick="copyToClipboard(`{st.session_state.symbol_result}`)"
            style='margin-top:10px; padding:8px 16px; border-radius:10px; border:1px solid #ccc; background-color:#f7f7f7; cursor:pointer;'>
            📋 복사하기
        </button>
        """
        components.html(copy_code, height=150)

with tabs[1]:
    symbol_input = st.text_area("기호 입력", height=150, key="input2")
    st.markdown("<p style='color: gray; font-size: 13px;'>👉 클립보드에 복사한 기호를 여기에 붙여넣어 주세요! (Ctrl+V 또는 ⌘+V) 🐣</p>", unsafe_allow_html=True)
    if st.button("한글로 되돌리기", key="to_korean"):
        jamo_result = ""
        for char in symbol_input:
            if char in reverse_consonants:
                jamo_result += reverse_consonants[char]
            elif char in reverse_vowels:
                jamo_result += reverse_vowels[char]
            else:
                jamo_result_
