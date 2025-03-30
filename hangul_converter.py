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

# 역변환용 매핑 (기호 → 자모)
reverse_consonants = {v: k for k, v in decompose_consonants.items()}
reverse_vowels = {v: k for k, v in decompose_vowels.items()}

# 초성, 중성, 종성 테이블
CHOSUNG_LIST = ["ㄱ", "ㄲ", "ㄴ", "ㄷ", "ㄸ", "ㄹ", "ㅁ", "ㅂ", "ㅃ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅉ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]
JUNGSUNG_LIST = ["ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ", "ㅔ", "ㅕ", "ㅖ", "ㅗ", "ㅘ", "ㅙ", "ㅚ", "ㅛ", "ㅜ", "ㅝ", "ㅞ", "ㅟ", "ㅠ", "ㅡ", "ㅢ", "ㅣ"]
JONGSUNG_LIST = ["", "ㄱ", "ㄲ", "ㄳ", "ㄴ", "ㄵ", "ㄶ", "ㄷ", "ㄹ", "ㄺ", "ㄻ", "ㄼ", "ㄽ", "ㄾ", "ㄿ", "ㅀ", "ㅁ", "ㅂ", "ㅄ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]

# 자모 → 완성형 한글 조합 함수
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

st.markdown("""
<style>
.button-box {
    display: flex;
    gap: 10px;
    margin-top: 10px;
    margin-bottom: 10px;
}
.button-box button {
    background-color: #f0f0f0;
    border: 1px solid #ccc;
    border-radius: 5px;
    padding: 6px 12px;
    cursor: pointer;
    font-size: 14px;
}
.button-box button:hover {
    background-color: #e0e0e0;
}
</style>
""", unsafe_allow_html=True)

st.title("🪶 고대 기호 한글 변환기")
st.write("한글을 고대문자 스타일의 기호 언어로 바꾸거나, 다시 되돌릴 수 있습니다.")

tab1, tab2 = st.tabs(["한글 → 기호", "기호 → 한글"])

with tab1:
    input_text = st.text_area("한글 입력", height=150, key="input1")

    components.html("""
        <div class='button-box'>
            <button onclick="navigator.clipboard.readText().then(t => window.parent.postMessage({type: 'paste1', text: t}, '*'))">📥 붙여넣기</button>
        </div>
        <script>
        window.addEventListener('message', (event) => {
            if (event.data.type === 'paste1') {
                const textarea = window.parent.document.querySelector('textarea[data-streamlit-key="input1"]');
                if (textarea) textarea.value = event.data.text;
            }
        });
        </script>
    """, height=60)

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
        st.text_area("기호 언어 출력", result, height=150, key="output1")

        components.html(f"""
            <div class='button-box'>
                <button onclick=\"navigator.clipboard.writeText('{result}')\">📋 복사하기</button>
            </div>
        """, height=60)

with tab2:
    symbol_input = st.text_area("기호 입력", height=150, key="input2")

    components.html("""
        <div class='button-box'>
            <button onclick="navigator.clipboard.readText().then(t => window.parent.postMessage({type: 'paste2', text: t}, '*'))">📥 붙여넣기</button>
        </div>
        <script>
        window.addEventListener('message', (event) => {
            if (event.data.type === 'paste2') {
                const textarea = window.parent.document.querySelector('textarea[data-streamlit-key="input2"]');
                if (textarea) textarea.value = event.data.text;
            }
        });
        </script>
    """, height=60)

    if st.button("한글로 되돌리기", key="to_korean"):
        jamo_result = ""
        for char in symbol_input:
            if char in reverse_consonants:
                jamo_result += reverse_consonants[char]
            elif char in reverse_vowels:
                jamo_result += reverse_vowels[char]
            else:
                jamo_result += char

        result = join_jamos_manual(jamo_result)
        st.text_area("복원된 한글 출력", result, height=150, key="output2")

        components.html(f"""
            <div class='button-box'>
                <button onclick=\"navigator.clipboard.writeText('{result}')\">📋 복사하기</button>
            </div>
        """, height=60)
