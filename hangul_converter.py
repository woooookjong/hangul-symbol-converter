import streamlit as st
import jamo
from jamo import h2j, j2hcj

# 자음과 모음 기호 매핑
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

st.title("🪶 고대 기호 한글 변환기")
st.write("한글을 고대문자 스타일의 기호 언어로 바꿔줍니다.")

input_text = st.text_area("한글 입력", height=150)

if st.button("변환하기"):
    result = ""
    for char in input_text:
        if jamo.is_hangul(char):
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
