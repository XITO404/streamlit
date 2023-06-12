import streamlit as st
import datetime, requests
from plotly import graph_objects as go

st.set_page_config(page_title='Weather Forecast', page_icon="⛅")

st.title("7-DAY WEATHER FORECAST 🌧️🌥️")

city = st.text_input("도시 이름을 입력하세요.")

unit = st.selectbox("온도 단위 선택", ["섭씨", "화씨"])
speed = st.selectbox("풍속 단위 선택", ["m/s", "km/h"])
graph = st.radio("그래프 유형 선택", ["막대 그래프", "선 그래프"])

if unit=="섭씨":
    temp_unit=" °C"
else:
    temp_unit=" °F"
    
if speed=="km/h":
    wind_unit=" km/h"
else:
    wind_unit=" m/s"

if st.button("확인"):
    try:
        api = "9b833c0ea6426b70902aa7a4b1da285c"  # OpenWeatherMap API Key
        cel = 273.15

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}"
        response = requests.get(url)
        x = response.json()

        lon = x["coord"]["lon"]
        lat = x["coord"]["lat"]
        exclude = "current,minutely,hourly"
        url2 = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={exclude}&appid={api}'
        res = requests.get(url2)
        y = res.json()

        maxtemp=[]
        mintemp=[]
        pres=[]
        humd=[]
        wspeed=[]
        desc=[]
        cloud=[]
        rain=[]
        dates=[]
        sunrise=[]
        sunset=[]
        cel=273.15

        for item in y["daily"][:7]:     # 8일간의 데이터에서 7일까지만 받아오도록 슬라이싱
            if unit == "섭씨":
                maxtemp.append(round(item["temp"]["max"] - cel, 1))
                mintemp.append(round(item["temp"]["min"] - cel, 1))
            else:
                maxtemp.append(round((((item["temp"]["max"] - cel) * 1.8) + 32), 1))
                mintemp.append(round((((item["temp"]["min"] - cel) * 1.8) + 32), 1))

            if wind_unit=="m/s":
                wspeed.append(str(round(item["wind_speed"],1))+wind_unit)
            else:
                wspeed.append(str(round(item["wind_speed"]*3.6,1))+wind_unit)

            pres.append(item["pressure"])
            humd.append(str(item["humidity"])+' %')
            
            cloud.append(str(item["clouds"])+' %')
            rain.append(str(int(item["pop"]*100))+'%')

            desc.append(item["weather"][0]["description"].title())
            
            
            d1 = datetime.date.fromtimestamp(item["dt"])
            dates.append(d1.strftime('%d %b'))

        def bargraph():
            fig = go.Figure(data=[
                go.Bar(name="최고 기온", x=dates, y=maxtemp, marker_color='#74afc4'),
                go.Bar(name="최저 기온", x=dates, y=mintemp, marker_color='#bedfeb')
            ])
            fig.update_layout(xaxis_title="날짜", yaxis_title="온도", barmode='group',
                              margin=dict(l=70, r=10, t=80, b=80), font=dict(color="white"))
            st.plotly_chart(fig)

        def linegraph():
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=dates, y=mintemp, name='최저 기온'))
            fig.add_trace(go.Scatter(x=dates, y=maxtemp, name='최고 기온', marker_color='crimson'))
            fig.update_layout(xaxis_title="날짜", yaxis_title="온도", font=dict(color="white"))
            st.plotly_chart(fig)

        st.header(f"{city}의 일주일 일기예보")
        icon=x["weather"][0]["icon"]
        current_weather=x["weather"][0]["description"].title()
        
        if unit=="섭씨":
            temp=str(round(x["main"]["temp"]-cel,2))
        else:
            temp=str(round((((x["main"]["temp"]-cel)*1.8)+32),2))
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("### 현재 기온 ")
        with col2:
            st.image(f"http://openweathermap.org/img/wn/{icon}@2x.png",width=70)

        
        col1, col2= st.columns(2)
        col1.metric("기온",temp+temp_unit)
        col2.metric("날씨",current_weather)
        st.subheader(" ")
        
        if graph=="막대 그래프":
            bargraph()
            
        elif graph=="선 그래프":
            linegraph()

         
        table1=go.Figure(data=[go.Table(header=dict(
                  values = [
                  '<b>날짜</b>',
                  '<b>최고 기온<br>(in'+temp_unit+')</b>',
                  '<b>최저 기온<br>(in'+temp_unit+')</b>',
                  '<b>강수 확률</b>',
                  '<b>운량</b>',
                  '<b>습도</b>'],
                  line_color='black', fill_color='#8f8681',  font=dict(color='white', size=14),height=32),
        cells=dict(values=[dates,maxtemp,mintemp,rain,cloud,humd],
        line_color='black',fill_color=['#c2b6ae',['#f0edeb', '#f0edeb']*7], font_size=14,height=32
            ))])

        table1.update_layout(margin=dict(l=10,r=10,b=10,t=10),height=328)
        st.write(table1)
        
        table2=go.Figure(data=[go.Table(columnwidth=[1,2,1,1,1,1],header=dict(values=['<b>날짜</b>','<b>날씨</b>','<b>풍속</b>','<b>기압<br>(hPa)</b>','<b>일출<br>(in UTC)</b>','<b>일몰<br>(in UTC)</b>']
                  ,line_color='black', fill_color='#8f8681',  font=dict(color='white', size=14),height=36),
        cells=dict(values=[dates,desc,wspeed,pres,sunrise,sunset],
        line_color='black',fill_color=['#c2b6ae',['#f0edeb', '#f0edeb']*7], font_size=14,height=36))])
        
        table2.update_layout(margin=dict(l=10,r=10,b=10,t=10),height=360)
        st.write(table2)
        
        st.header(' ')
        st.header(' ')

    except KeyError:
        st.error("유효하지 않은 도시입니다. 다시 시도해 주세요.")