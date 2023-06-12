import streamlit as st      # streamlit 라이브러리 가져오기
import datetime, requests   # datetime과 requests 모듈 가져오기
from plotly import graph_objects as go  # plotly의 graph_objects 모듈 가져오기

# 탭의 이름과 아이콘 설정
st.set_page_config(page_title='Weather Forecast', page_icon="⛅",)

# 웹앱 제목 출력 - title
st.title("7-DAY WEATHER FORECAST 🌧️🌥️")

# 사용자로부터 도시 이름 입력받는 입력 박스 생성; 영어만 가능
city = st.text_input("도시 이름을 입력하세요.")

# 온도 단위 선택하는 셀렉트 박스 생성
unit = st.selectbox("온도 단위 선택", ["섭씨", "화씨"])

# 풍속 단위 선택하는 셀렉트 박스 생성
speed = st.selectbox("풍속 단위 선택", ["m/s", "km/h"])

# 그래프 유형 선택하는 라디오 버튼 생성
graph = st.radio("그래프 유형 선택", ["막대 그래프", "선 그래프"])

# 선택된 온도 단위에 따라 온도 단위 문자열 설정하기
if unit=="섭씨":            # 섭씨이면
    temp_unit=" °C"         # °C
else:                       # 화씨이면
    temp_unit=" °F"         # °F      
    
if speed=="km/h":           # km/h
    wind_unit=" km/h"       # km/h
else:                       # m/s
    wind_unit=" m/s"        # m/s

# 확인 버튼 생성
if st.button("확인"):       # 확인 버튼을 클릭하면
    try:
        api = "9b833c0ea6426b70902aa7a4b1da285c"    # OpenWeatherMap API Key
        cel = 273.15        # [K] = [°C] + 273.15
        
        # API를 통해 유저가 선택한 도시의 실시간 날씨 정보 가져오기
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}"
        response = requests.get(url)                # URL에 GET 요청을 보내고, 응답 받아오기     
        x = response.json()                         # 받아온 API 응답을 JSON 형식으로 반환, x에 저장

        lon = x["coord"]["lon"]     # 경도
        lat = x["coord"]["lat"]     # 위도
        exclude = "current,minutely,hourly"
        
        # 선택한 도시의 7일간 일기예보 데이터 가져오기
        url2 = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={exclude}&appid={api}'
        res = requests.get(url2)
        y = res.json()

        maxtemp = []    # 최고 기온 리스트
        mintemp = []    # 최저 기온 리스트
        pres = []    # 기압 리스트
        humd = []    # 습도 리스트
        wspeed = []    # 풍속 리스트
        desc = []    # 날씨 설명 리스트
        cloud = []    # 운량 리스트
        rain = []    # 강수 확률 리스트
        dates = []    # 날짜 리스트
        sunrise = []    # 일출 시간 리스트
        sunset = []    # 일몰 시간 리스트
        cel = 273.15    # 섭씨 변환을 위한 상수

        # 8일간의 데이터에서 7일까지만 받아오도록 슬라이싱, 각 변수에 저장
        for item in y["daily"][:7]:     
            # 온도 단위에 따라 최고 기온과 최저 기온을 변환하여 리스트에 추가
            if unit == "섭씨":  # 섭씨이면
                maxtemp.append(round(item["temp"]["max"] - cel, 1)) # 계산 후 소수점 첫째 자리까지 반올림, maxtemp 리스트에 추가
                mintemp.append(round(item["temp"]["min"] - cel, 1)) # 계산 후 소수점 첫째 자리까지 반올림, mintemp 리스트에 추가
            else:               # 화씨이면
                maxtemp.append(round((((item["temp"]["max"] - cel) * 1.8) + 32), 1)) # 섭씨->화씨 변환 후 같은 방식으로 반올림, 리스트 추가
                mintemp.append(round((((item["temp"]["min"] - cel) * 1.8) + 32), 1)) # 섭씨->화씨 변환 후 같은 방식으로 반올림, 리스트 추가

            # 풍속 단위에 따라 풍속을 변환하여 리스트에 추가
            if wind_unit=="m/s":
                wspeed.append(str(round(item["wind_speed"],1))+wind_unit)
            else:
                wspeed.append(str(round(item["wind_speed"]*3.6,1))+wind_unit)
                
            # 기압, 습도, 운량, 강수 확률, 날씨 설명을 각각의 리스트에 추가합니다.
            pres.append(item["pressure"])
            humd.append(str(item["humidity"])+' %')
            cloud.append(str(item["clouds"])+' %')
            rain.append(str(int(item["pop"]*100))+'%')
            desc.append(item["weather"][0]["description"].title())
            
            # 날짜를 datetime 객체로 변환하여 리스트에 추가합니다.
            d1 = datetime.date.fromtimestamp(item["dt"])
            dates.append(d1.strftime('%d %b'))

        # 막대 그래프 출력 함수
        def bargraph():
            fig = go.Figure(data=[
                go.Bar(name="최고 기온", x=dates, y=maxtemp, marker_color='#74afc4'),
                go.Bar(name="최저 기온", x=dates, y=mintemp, marker_color='#bedfeb')
            ])
            fig.update_layout(xaxis_title="날짜", yaxis_title="온도", barmode='group',
                              margin=dict(l=70, r=10, t=80, b=80), font=dict(color="white"))
            st.plotly_chart(fig)

        # 선 그래프 출력 함수
        def linegraph():
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=dates, y=mintemp, name='최저 기온'))
            fig.add_trace(go.Scatter(x=dates, y=maxtemp, name='최고 기온', marker_color='crimson'))
            fig.update_layout(xaxis_title="날짜", yaxis_title="온도", font=dict(color="white"))
            st.plotly_chart(fig)

        # 선택한 도시의 일주일 일기예보 출력
        st.header(f"{city}의 일주일 일기예보")
        icon=x["weather"][0]["icon"]
        current_weather=x["weather"][0]["description"].title()
        
        # 현재 기온을 온도 단위에 맞게 설정
        if unit=="섭씨":
            temp=str(round(x["main"]["temp"]-cel,2))
        else:
            temp=str(round((((x["main"]["temp"]-cel)*1.8)+32),2))
        
        # 현재 기온과 날씨 아이콘 출력
        col1, col2 = st.columns(2)
        with col1:
            st.write("### 현재 기온 ")
        with col2:
            st.image(f"http://openweathermap.org/img/wn/{icon}@2x.png",width=70)

        # 현재 기온 및 날씨 정보 출력
        col1, col2= st.columns(2)
        col1.metric("기온",temp+temp_unit)
        col2.metric("날씨",current_weather)
        st.subheader(" ")
        
        # 선택한 그래프 유형에 따라 그래프 출력
        if graph=="막대 그래프":
            bargraph()
            
        elif graph=="선 그래프":
            linegraph()

        # 일기예보 테이블 중 표1 생성 및 출력
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

        # 표1의 레이아웃 조정
        table1.update_layout(margin=dict(l=10,r=10,b=10,t=10),height=328)
        
        # 표1 출력
        st.write(table1)
        
        # 표2 생성
        table2=go.Figure(data=[go.Table(columnwidth=[1,2,1,1,1,1],header=dict(values=['<b>날짜</b>','<b>날씨</b>','<b>풍속</b>','<b>기압<br>(hPa)</b>','<b>일출<br>(in UTC)</b>','<b>일몰<br>(in UTC)</b>']
                  ,line_color='black', fill_color='#8f8681',  font=dict(color='white', size=14),height=36),
        cells=dict(values=[dates,desc,wspeed,pres,sunrise,sunset],
        line_color='black',fill_color=['#c2b6ae',['#f0edeb', '#f0edeb']*7], font_size=14,height=36))])
        
        # 표2 레이아웃 조정
        table2.update_layout(margin=dict(l=10,r=10,b=10,t=10),height=360)
        
        # 표2 출력
        st.write(table2)
        
        # 빈 헤더 추가
        st.header(' ')
        st.header(' ')

    # 유저의 키 입력에 대한 예외 처리
    except KeyError:
        st.error("유효하지 않은 도시입니다. 다시 시도해 주세요.")
