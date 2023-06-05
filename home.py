import streamlit as st
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt

add_selectbox = st.sidebar.selectbox(
    "Index",
    ("BMI Calculator", "Gap minder", "My page")
)

if add_selectbox == "BMI Calculator":

    st.title('BMI Calculator')

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

elif add_selectbox == "Gap minder":
    st.title("Gap minder data")
    data = pd.read_csv('gapminder.csv')
    st.write(data)
    
    colors = []
    for x in data['continent']:
        if x == 'Asia':
            colors.append('lightcoral')
        elif x == 'Europe':
            colors.append('brown')
        elif x == 'Africa':
            colors.append('olive')
        elif x == 'America':
            colors.append('green')
        else:
            colors.append('orange')
            
    data['colors'] = colors
        
    year = st.slider('연도를 선택하세요.', 1952, 2007, 1952,step = 5)
    st.write("year: ", year)

    data = data[data['year']==year]     # data indexing - user가 선택하는 연도별로 구성되게 함
    
    fig, ax = plt.subplots()
    ax.scatter(data['gdpPercap'], data['lifeExp'], s=data['pop']*0.000002, color = data['colors'])
    ax.set_title('How Does GDP per Capital relate to Life Expectancy?')
    ax.set_xlabel('GDP per Capital')
    ax.set_ylabel('Life Expectancy')    
    st.pyplot(fig)
    
else:
    st.title("My page")