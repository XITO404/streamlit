import streamlit as st
from PIL import Image

# 체질량 지수 구하는 앱
# 몸무게, 키 입력받기

st.title('BMI 계산기')

height = st.number_input('키를 입력하세요. (cm)', value = 160, step = 5)
st.write(height, 'cm')

weight = st.number_input('몸무게를 입력하세요. (kg)', value = 50, step = 5)
st.write(height, 'kg')

def bmi_range(bmi):
    if bmi>=25:
        st.error('비만입니다.', icon="🚨")
    elif bmi>=23:
        st.warning('과체중입니다.')
    elif bmi>=18.5:
        st.success('정상입니다.')
    else:
        st.warning('저체중입니다.')

bmi = weight/((height/100)**2)

if st.button('계산'):
    st.balloons()
    st.write('##### 당신의 체질량 지수는', round(bmi,2), '입니다.')
    bmi_range(bmi)

image = Image.open('vege.jpg')
st.image(image, caption='오늘 저녁은 채소를 활용한 식단 어떠세요?')
