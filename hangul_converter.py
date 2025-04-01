import streamlit as st
import streamlit.components.v1 as components

# 자모 리스트
CHOSUNG_LIST = ["ㄱ", "ㄲ", "ㄴ", "ㄷ", "ㄸ", "ㄹ", "ㅁ", "ㅂ", "ㅃ",
                "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅉ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]
JUNGSUNG_LIST = ["ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ", "ㅔ", "ㅕ", "ㅖ", "ㅗ", "ㅘ",
                 "ㅙ", "ㅚ", "ㅛ", "ㅜ", "ㅝ", "ㅞ", "ㅟ", "ㅠ", "ㅡ", "ㅢ", "ㅣ"]
JONGSUNG_LIST = ["", "ㄱ", "ㄲ", "ㄳ", "ㄴ", "ㄵ", "ㄶ", "ㄷ", "ㄹ", "ㄺ", "ㄻ",
                 "ㄼ", "ㄽ", "ㄾ", "ㄿ", "ㅀ", "ㅁ", "ㅂ", "ㅄ", "ㅅ", "ㅆ",
                 "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]

# 초성, 중성, 종성 기호 매핑
initial_map = {
    'ㄱ': '𐎀', 'ㄴ': '𐎐', 'ㄷ': '𐎂', 'ㄹ': '𐎑', 'ㅁ': '𐎄',
    'ㅂ': '𐎅', 'ㅅ': '𐎃', 'ㅇ': '𐎊', 'ㅈ': '𐎆', 'ㅊ': '𐎇',
    'ㅋ': '𐎚', 'ㅌ': '𐎛', 'ㅍ': '𐎜', 'ㅎ': '𐎟'
}
final_map = {
    'ㄱ': '𐎰', 'ㄴ': '𐎱', 'ㄷ': '𐎲', 'ㄹ': '𐎳', 'ㅁ': '𐎴',
    'ㅂ': '𐎵', 'ㅅ': '𐎶', 'ㅇ': '𐎷', 'ㅈ': '𐎸', 'ㅊ': '𐎹',
    'ㅋ': '𐎺', 'ㅌ': '𐎻', 'ㅍ': '𐎼', 'ㅎ': '𐎽'
}
vowel_map = {
    'ㅏ': '𐎠', 'ㅐ': '𐎡', 'ㅑ': '𐎢', 'ㅒ': '𐎣',
    'ㅓ': '𐎤', 'ㅔ': '𐎥', 'ㅕ': '𐎦', 'ㅖ': '𐎧',
    'ㅗ': '𐎨', 'ㅛ': '𐎩', 'ㅜ': '𐎪', 'ㅠ': '𐎫',
    'ㅡ': '𐎬', 'ㅣ': '𐎭',

    # ✅ 이중 모음 추가 (고대 느낌으로 고른 기호)
    'ㅘ': '𐎮',
    'ㅙ': '𐎯',
    'ㅚ': '𐎰',
    'ㅝ': '𐎱',
    'ㅞ': '𐎲',
    'ㅟ': '𐎳',
    'ㅢ': '𐎴'
}

# 역변환용
rev_initial = {v: k for k, v in initial_map.items()}
rev_final = {v: k for k, v in final_map.items()}
rev_vowel = {v: k for k, v in vowel_map.items()}

# 유니코드 조합 함수
def combine_jamos(cho, jung, jong):
    cho_i = CHOSUNG_LIST.index(cho)
    jung_i = JUNGSUNG_LIST.index(jung)
    jong_i = JONGSUNG_LIST.index(jong) if jong else 0
    return chr(0xAC00 + (cho_i * 21 * 28) + (jung_i * 28) + jong_i)

st.title("🪶 고대 기호 한글 변환기")

tabs = st.tabs(["한글 → 기호", "기호 → 한글"])

if "symbol_result" not in st.session_state:
    st.session_state.symbol_result = ""
if "hangul_result" not in st.session_state:
    st.session_state.hangul_result = ""

with tabs[0]:
    input_text = st.text_area("한글 입력", height=150)
    if st.button("기호로 변환하기"):
        result = ""
        for ch in input_text:
            code = ord(ch)
            if 0xAC00 <= code <= 0xD7A3:
                base = code - 0xAC00
                cho = CHOSUNG_LIST[base // 588]
                jung = JUNGSUNG_LIST[(base % 588) // 28]
                jong = JONGSUNG_LIST[base % 28]

                result += initial_map.get(cho, cho)
                result += vowel_map.get(jung, jung)
                if jong:
                    result += final_map.get(jong, jong)
            else:
                result += ch
        st.session_state.symbol_result = result

    if st.session_state.symbol_result:
        st.text_area("기호 언어 출력", st.session_state.symbol_result, height=150)

        # 복사 버튼
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
    symbol_input = st.text_area("기호 입력", height=150)
    st.markdown("👉 클립보드에 복사한 기호를 여기에 붙여넣어 주세요! 🐣", unsafe_allow_html=True)

    if st.button("한글로 되돌리기"):
        jamos = []
        for ch in symbol_input:
            if ch in rev_initial:
                jamos.append(("초", rev_initial[ch]))
            elif ch in rev_vowel:
                jamos.append(("중", rev_vowel[ch]))
            elif ch in rev_final:
                jamos.append(("종", rev_final[ch]))
            else:
                jamos.append(("기타", ch))

        result = ""
        i = 0
        while i < len(jamos):
            if i + 1 < len(jamos) and jamos[i][0] == "초" and jamos[i+1][0] == "중":
                cho = jamos[i][1]
                jung = jamos[i+1][1]
                jong = ""
                if i + 2 < len(jamos) and jamos[i+2][0] == "종":
                    jong = jamos[i+2][1]
                    i += 3
                else:
                    i += 2
                result += combine_jamos(cho, jung, jong)
            else:
                result += jamos[i][1]
                i += 1

        st.session_state.hangul_result = result

    if st.session_state.hangul_result:
        st.text_area("복원된 한글 출력", st.session_state.hangul_result, height=150)

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
