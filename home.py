import streamlit as st


st.write('# Hi! Welcome to My App!')


if st.button('Say hello'):
    st.write('Hello!')
else:
    st.write('Goodbye')


option = st.selectbox(
    '좋아하는 동물은?',
    ('강아지', '고양이', '여우', '뱀', '토끼'))


st.write('제가 좋아하는 동물은', option, '입니다.')
st.write(f'좋아하는 동물은 {option} 입니다.')


txt = st.text_area('자신을 소개해보세요.', '''
                   
                   ''')

st.write('입력한 내용은: ', txt)


age = st.slider('나이를 선택하세요', 0, 120, 23)
st.write("저의 나이는", age, '입니다.')