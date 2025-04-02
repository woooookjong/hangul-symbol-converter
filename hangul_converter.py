import streamlit as st
from jamo import h2j, j2hcj
import unicodedata

def is_hangul_char(char):
    return 'HANGUL' in unicodedata.name(char, '')

# 초성, 중성, 종성 기호 (초성과 종성은 겹치지 않음)
decompose_chosung = { 'ㄱ': 'ᚠ', 'ㄲ': 'ᚡ', 'ㄴ': 'ᚢ', 'ㄷ': 'ᚣ', 'ㄸ': 'ᚤ',
    'ㄹ': 'ᚥ', 'ㅁ': 'ᚦ', 'ㅂ': 'ᚧ', 'ㅃ': 'ᚨ', 'ㅅ': 'ᚩ',
    'ㅆ': 'ᚪ', 'ㅇ': 'ᚫ', 'ㅈ': 'ᚬ', 'ㅉ': 'ᚭ', 'ㅊ': 'ᚮ',
    'ㅋ': 'ᚯ', 'ㅌ': 'ᚰ', 'ㅍ': 'ᚱ', 'ㅎ': 'ᚲ' }

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

punctuation_map = {
    '?': '⸮', '!': '⸘', '.': '꞉', ',': '‚', ':': '⁚',
    ';': '⁏', '(': '❨', ')': '❩', '"': 'ˮ', "'": 'ʼ'
}

reverse_chosung = {v: k for k, v in decompose_chosung.items()}
reverse_jungsung = {v: k for k, v in decompose_jungsung.items()}
reverse_jongsung = {v: k for k, v in decompose_jongsung.items()}
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
            if i+1 < len(jamos) and jamos[i+1] in JUNGSUNG_LIST:
                jung = JUNGSUNG_LIST.index(jamos[i+1])
                jong = 0
                if i+2 < len(jamos) and jamos[i+2] in JONGSUNG_LIST:
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

# Streamlit 디버그
st.set_page_config(page_title="기호 복원 디버그")
st.title("🔍 기호 → 한글 복원 디버깅")

symbol_input = st.text_area("기호 입력", height=150)
if st.button("복원 디버그 시작"):
    jamo_result = []
    logs = []
    i = 0
    while i < len(symbol_input):
        current = symbol_input[i]
        logs.append(f"[{i}] 문자: {current}")

        if current in reverse_chosung:
            cho = reverse_chosung[current]
            logs.append(f"  ↳ 초성: {cho}")

            if i + 1 < len(symbol_input) and symbol_input[i+1] in reverse_jungsung:
                jung = reverse_jungsung[symbol_input[i+1]]
                logs.append(f"  ↳ 중성: {jung}")

                if (
                    i + 2 < len(symbol_input)
                    and symbol_input[i+2] in reverse_jongsung
                    and symbol_input[i+2] not in reverse_chosung
                    and (i + 3 >= len(symbol_input) or symbol_input[i+3] not in reverse_jungsung)
                ):
                    jong = reverse_jongsung[symbol_input[i+2]]
                    logs.append(f"  ↳ 종성: {jong}")
                    jamo_result.extend([cho, jung, jong])
                    i += 3
                    continue
                else:
                    jamo_result.extend([cho, jung])
                    i += 2
                    continue
            else:
                jamo_result.append(cho)
                i += 1
                continue

        elif current in reverse_punctuation:
            logs.append(f"  ↳ 구두점: {reverse_punctuation[current]}")
            jamo_result.append(reverse_punctuation[current])
            i += 1
        else:
            logs.append("  ↳ 기타: 그대로 추가")
            jamo_result.append(current)
            i += 1

    result = join_jamos_manual(jamo_result)
    st.subheader("🔁 복원 결과:")
    st.write(result)

    st.subheader("📝 디버그 로그:")
    for line in logs:
        st.text(line)
