import streamlit as st
import requests
from datetime import datetime
import pandas as pd

city_code_list = {
    '東京都':'130010',
    '大阪':'270000',
    '北海道':'016010',
    '愛知':'230010',
    '福岡':'400010',
    '那覇':'471010',
}

city_code_index = '東京都'

st.title('天気アプリ')
st.write('調べたい地域を選んでください。')
city_code_index = st.selectbox('地域を選んでください。', city_code_list.keys())
city_code = city_code_list[city_code_index]
current_city_code = st.empty()
current_city_code.write('**選択中の地域**：' + city_code_index)

url = 'https://weather.tsukumijima.net/api/forecast/city/' + city_code

response = requests.get(url)

weather_json = response.json()
now_hour = datetime.now().hour

weather_today = weather_json['forecasts'][0]['telop']
weather_today_image = weather_json['forecasts'][0]['image']['url']


weather_today_text = '**今日の天気**：' + weather_today
st.write(weather_today_text)
st.image(weather_today_image)

if 0 <= now_hour and now_hour <6:
    weather_now = weather_json['forecasts'][0]['chanceOfRain']['T00_06']
elif 6 <= now_hour and now_hour < 12:
    weather_now = weather_json['forecasts'][0]['chanceOfRain']['T06_12']
elif 12 <= now_hour and now_hour < 18:
    weather_now = weather_json['forecasts'][0]['chanceOfRain']['T12_18']
else:
    weather_now = weather_json['forecasts'][0]['chanceOfRain']['T18_24']


weather_now_text = '**現在の降水確率**：' + weather_now
st.write(weather_now_text)

df1 = pd.DataFrame(weather_json['forecasts'][0]['chanceOfRain'],index=['今日'])
df2 = pd.DataFrame(weather_json['forecasts'][1]['chanceOfRain'],index=['明日'])
df3 = pd.DataFrame(weather_json['forecasts'][2]['chanceOfRain'],index=['明後日'])

df = pd.concat([df1, df2, df3])
df.columns = ['0-6時', '6-12時', '12-18時', '18-24時']
st.dataframe(df)

st.write('**今日の降水確率の移り変わり**')

# % を取り除いて数値に変換（文字列 → int）
df_numeric = df.applymap(lambda x: int(x.strip('%')))

st.bar_chart(df_numeric.loc['今日'])