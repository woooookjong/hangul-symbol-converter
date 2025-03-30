import streamlit as st
from jamo import h2j, j2hcj
import unicodedata

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

# 한글 조합 함수
def join_jamos_manual(jamos):
    from jamo import assemble
    result = ""
    buffer = []
    for j in jamos:
        buffer.append(j)
        try:
            result += assemble(buffer)
            buffer = []
        except:
            continue
    return result

st.title("🪶 고대 기호 한글 변환기")
st.write("한글을 고대문자 스타일의 기호 언어로 바꾸거나, 다시 되돌릴 수 있습니다.")

tab1, tab2 = st.tabs(["한글 → 기호", "기호 → 한글"])

with tab1:
    input_text = st.text_area("한글 입력", height=150)

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
        st.text_area("기호 언어 출력", result, height=150)
        st.code(result, language='text')

with tab2:
    symbol_input = st.text_area("기호 입력", height=150)

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
        st.text_area("복원된 한글 출력", result, height=150)
        st.code(result, language='text')
