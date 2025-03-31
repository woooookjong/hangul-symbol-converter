import streamlit as st
from jamo import h2j, j2hcj
import unicodedata
import streamlit.components.v1 as components

# 한글 여부 판단
def is_hangul_char(char):
    return 'HANGUL' in unicodedata.name(char, '')

# 초성 기호 (initial) + 종성 기호 (final) 구분
initial_consonants = {
    'ㄱ': '𐎀', 'ㄴ': '𐎐', 'ㄷ': '𐎂', 'ㄹ': '𐎑', 'ㅁ': '𐎄',
    'ㅂ': '𐎅', 'ㅅ': '𐎃', 'ㅇ': '𐎊', 'ㅈ': '𐎆', 'ㅊ': '𐎇',
    'ㅋ': '𐎚', 'ㅌ': '𐎛', 'ㅍ': '𐎜', 'ㅎ': '𐎟'
}

final_consonants = {
    'ㄱ': '𐎰', 'ㄴ': '𐎱', 'ㄷ': '𐎲', 'ㄹ': '𐎳', 'ㅁ': '𐎴',
    'ㅂ': '𐎵', 'ㅅ': '𐎶', 'ㅇ': '𐎷', 'ㅈ': '𐎸', 'ㅊ': '𐎹',
    'ㅋ': '𐎺', 'ㅌ': '𐎻', 'ㅍ': '𐎼', 'ㅎ': '𐎽'
}

vowel_symbols = {
    'ㅏ': '𐎠', 'ㅑ': '𐎢', 'ㅓ': '𐎤', 'ㅕ': '𐎦', 'ㅗ': '𐎨',
    'ㅛ': '𐎩', 'ㅜ': '𐎪', 'ㅠ': '𐎫', 'ㅡ': '𐎬', 'ㅣ': '𐎭',
    'ㅐ': '𐎡', 'ㅒ': '𐎣', 'ㅔ': '𐎥', 'ㅖ': '𐎧'
}

# 역변환용
reverse_initial = {v: k for k, v in initial_consonants.items()}
reverse_final = {v: k for k, v in final_consonants.items()}
reverse_vowel = {v: k for k, v in vowel_symbols.items()}

# 한글 자모 리스트
CHOSUNG_LIST = ["ㄱ", "ㄲ", "ㄴ", "ㄷ", "ㄸ", "ㄹ", "ㅁ", "ㅂ", "ㅃ", "ㅅ",
                "ㅆ", "ㅇ", "ㅈ", "ㅉ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]
JUNGSUNG_LIST = ["ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ", "ㅔ", "ㅕ", "ㅖ", "ㅗ", "ㅘ",
                 "ㅙ", "ㅚ", "ㅛ", "ㅜ", "ㅝ", "ㅞ", "ㅟ", "ㅠ", "ㅡ", "ㅢ", "ㅣ"]
JONGSUNG_LIST = ["", "ㄱ", "ㄲ", "ㄳ", "ㄴ", "ㄵ", "ㄶ", "ㄷ", "ㄹ", "ㄺ", "ㄻ",
                 "ㄼ", "ㄽ", "ㄾ", "ㄿ", "ㅀ", "ㅁ", "ㅂ", "ㅄ", "ㅅ", "ㅆ",
                 "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]

# 자모 → 한글 조합
def join_jamos_manual(jamos):
    result = ""
    i = 0
    while i < len(jamos):
        if jamos[i] in CHOSUNG_LIST:
            cho = CHOSUNG_LIST.index(jamos[i])
            if i + 1 < len(jamos) and jamos[i + 1] in JUNGSUNG_LIST:
                jung = JUNGSUNG_LIST.index(jamos[i + 1])
                jong = 0
                if i + 2 < len(jamos) and jamos[i + 2] in JONGSUNG_LIST:
                    jong = JONGSUNG_LIST.index(jamos[i + 2])
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
            if is_hangul_char(char):
                decomposed = list(j2hcj(h2j(char)))
                for j in decomposed[:-1]:
                    if j in initial_consonants:
                        result += initial_consonants[j]
                    elif j in vowel_symbols:
                        result += vowel_symbols[j]
                    else:
                        result += j
                # 마지막 자모는 종성일 수 있음
                last = decomposed[-1]
                if last in final_consonants and len(decomposed) == 3:
                    result += final_consonants[last]
                else:
                    if last in initial_consonants:
                        result += initial_consonants[last]
                    elif last in vowel_symbols:
                        result += vowel_symbols[last]
                    else:
                        result += last
            else:
                result += char
        st.session_state.symbol_result = result

    if st.session_state.symbol_result:
        st.text_area("기호 언어 출력", st.session_state.symbol_result, height=150, key="output1")

        # 복사 버튼 + toast
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
        jamo_result = []
        for char in symbol_input:
            if char in reverse_initial:
                jamo_result.append(reverse_initial[char])
            elif char in reverse_final:
                jamo_result.append(reverse_final[char])
            elif char in reverse_vowel:
                jamo_result.append(reverse_vowel[char])
            else:
                jamo_result.append(char)
        result = join_jamos_manual(jamo_result)
        st.session_state.hangul_result = result

    if st.session_state.hangul_result:
        st.text_area("복원된 한글 출력", st.session_state.hangul_result, height=150, key="output2")

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
        <button onclick="copyToClipboard(`{st.session_state.hangul_result}`)"
            style='margin-top:10px; padding:8px 16px; border-radius:10px; border:1px solid #ccc; background-color:#f7f7f7; cursor:pointer;'>
            📋 복사하기
        </button>
        """
        components.html(copy_code, height=150)
