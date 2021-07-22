import os
import numpy as np
import pandas  as pd
import folium
import branca
from folium.plugins import MarkerCluster
from folium.features import CustomIcon
from folium import plugins

bike = pd.read_excel('data/따릉이.xlsx')
bike_x = bike['위도']
bike_y = bike['경도']
lat = bike['위도'].mean()
long = bike['경도'].mean()

dh=pd.read_csv('data/price_grading_deposit_high.csv', encoding='cp949')
mh=pd.read_csv('data/price_grading_monthly_high.csv', encoding='cp949')
pp=pd.read_csv('data/price_grading_proper.csv', encoding='cp949')

m_2=folium.Map(location=[37.566345, 126.977893], zoom_start=12)

main = folium.FeatureGroup(name='전/월세')
m_2.add_child(main)
env = folium.FeatureGroup(name= '전체 입지요건')
m_2.add_child(env)
g1 = plugins.FeatureGroupSubGroup(env, '따릉이 대여소')
m_2.add_child(g1)
g2 = plugins.FeatureGroupSubGroup(env, '스타벅스')
m_2.add_child(g2)
g3 = plugins.FeatureGroupSubGroup(env, '대형마트')
m_2.add_child(g3)
g4 = plugins.FeatureGroupSubGroup(env, '맥도널드')
m_2.add_child(g4)
g5 = plugins.FeatureGroupSubGroup(env, '병원')
m_2.add_child(g5)
g6 = plugins.FeatureGroupSubGroup(env, '스터디룸')
m_2.add_child(g6)
g7 = plugins.FeatureGroupSubGroup(env, '영화관')
m_2.add_child(g7)
g8 = plugins.FeatureGroupSubGroup(env, '코인노래방')
m_2.add_child(g8)
g9 = plugins.FeatureGroupSubGroup(env, '코인세탁소')
m_2.add_child(g9)

marker_cluster = MarkerCluster().add_to(main)

for key, value in mh.iterrows():
    name = value['건물명']
    adr = value['주소'] + ' ' + value['층']
    price = value['거래금액']
    size = str(value['면적']) + '(' + str(value['평']) + ')'
    year = value['건축년도']
    date = value['거래일']
    kind = value['건물형태']

    html = """
    <div class="name">
        <h2> {name} </h2>
        <div class="adr" data-testid="기본정보_1title" style="font-size: 12px; font-style: italic;"> {adr} </div>
    </div>
    <hr size="2px;" noshade size="20px;">
    <div class="line1" style></div>
    <div class="brief-info" data-testid="기본정보">
        <div class="biref-info-sub>
            <div class="first-info" style="padding-top: 13px; width: 200;">
                <div dir="auto" class="first-info-title" data-testid="기본정보_1title" style="font-size: 12px; font-weight: bold;">전세ᆞ월세</div>
                <div dir="auto" class="first-info-sub" data-testid="기본정보_1sub" style="color: reb(45, 96, 163); font-size: 25px;
                line-height:26px; color: #4169E1; font-weight: bold;"> {price} </div>
            <div class="second-info" style="padding-top: 18px; width: 200;">
                <div dir="auto" class="second-info-title" data-testid="기본정보_2title" style="font-size: 12px;">전용면적(평)</div>
                <div dir="auto" class="second-info-sub" data-testid="기본정보_2sub" style="color: reb(45, 96, 163); font-size: 19px;
                line-height:26px; color: #4169E1; font-weight: bold;"> {size} 평 </div>
            <div class="third-info" style="padding-top: 18px; width: 200;">
                <div dir="auto" class="third-info-title" data-testid="기본정보_3title" style="font-size: 12px;">건물 형태</div>
                <div dir="auto" class="third-info-sub" data-testid="기본정보_3sub" style="color: reb(45, 96, 163); font-size: 18px;
                line-height:26px; color: #4169E1; font-weight: bold;"> {kind} </div>
        </div>
    </div>

    <hr size="2px;" noshade size="20px;">
    <br>
    <div class="detailed-title">
        <div class="detailed-info-title" data-testid="상세정보_view" style="min-height: 50px;">
    <div dir="auto" class="detailed-info-title" data-testid="상세정보_title" style="font-size: 17px; line-height:23px; font-weight: bold;">상세정보</div>

    </div>
    <div class="detailed-sub">
        <div class="detailed-info-sub" data-testid="상세정보_table">
    <div class="line1" style="min-height: 35px;">
        <div class="detailed-info-sub" style="padding-top: 18px; width: 200;">
            <div dir="auto" class="detailed-info-title2" data-testid="상세정보_2title" style="font-size: 12px;">거래일</div>
            <div dir="auto" class="fifth-info-sub" data-testid="상세정보_4sub" style="color: reb(45, 96, 163); font-size: 18px;
            line-height:26px;"> {date} </div>
        <div class="detailed-info-sub" style="padding-top: 18px; width: 200;">
            <div dir="auto" class="detailed-info-title1" data-testid="상세정보_1title" style="font-size: 12px;">건축년도</div>
            <div dir="auto" class="fourth-info-sub" data-testid="상세정보_3sub" style="color: reb(45, 96, 163); font-size: 18px;
            line-height:26px;"> {year} </div>
    </div>

    """.format(name=name, adr=adr, price=price, size=size, kind=kind, year=year, date=date)

    iframe = branca.element.IFrame(html=html, width=300, height=400)
    popup = folium.Popup(iframe, max_width=300)
    icon2 = folium.features.CustomIcon('https://user-images.githubusercontent.com/74045426/'
                                       '108214344-684d3480-7173-11eb-8533-a7eb385d751b.png', icon_size=(54, 37.2))  # 휘발성!!!!!!!!!!!!11
    folium.Marker([value['위도'], value['경도']], popup=popup, icon=icon2).add_to(marker_cluster)

for key, value in pp.iterrows():
    name = value['건물명']
    adr = value['주소'] + ' ' + value['층']
    price = value['거래금액']
    size = str(value['면적']) + '(' + str(value['평']) + ')'
    year = value['건축년도']
    date = value['거래일']
    kind = value['건물형태']

    html = """
    <div class="name">
        <h2> {name} </h2>
        <div class="adr" data-testid="기본정보_1title" style="font-size: 12px; font-style: italic;"> {adr} </div>
    </div>
    <hr size="2px;" noshade size="20px;">
    <div class="line1" style></div>
    <div class="brief-info" data-testid="기본정보">
        <div class="biref-info-sub>
            <div class="first-info" style="padding-top: 13px; width: 200;">
                <div dir="auto" class="first-info-title" data-testid="기본정보_1title" style="font-size: 12px; font-weight: bold;">전세ᆞ월세</div>
                <div dir="auto" class="first-info-sub" data-testid="기본정보_1sub" style="color: reb(45, 96, 163); font-size: 25px;
                line-height:26px; color: #4169E1; font-weight: bold;"> {price} </div>
            <div class="second-info" style="padding-top: 18px; width: 200;">
                <div dir="auto" class="second-info-title" data-testid="기본정보_2title" style="font-size: 12px;">전용면적(평)</div>
                <div dir="auto" class="second-info-sub" data-testid="기본정보_2sub" style="color: reb(45, 96, 163); font-size: 19px;
                line-height:26px; color: #4169E1; font-weight: bold;"> {size} 평 </div>
            <div class="third-info" style="padding-top: 18px; width: 200;">
                <div dir="auto" class="third-info-title" data-testid="기본정보_3title" style="font-size: 12px;">건물 형태</div>
                <div dir="auto" class="third-info-sub" data-testid="기본정보_3sub" style="color: reb(45, 96, 163); font-size: 18px;
                line-height:26px; color: #4169E1; font-weight: bold;"> {kind} </div>
        </div>
    </div>

    <hr size="2px;" noshade size="20px;">
    <br>
    <div class="detailed-title">
        <div class="detailed-info-title" data-testid="상세정보_view" style="min-height: 50px;">
    <div dir="auto" class="detailed-info-title" data-testid="상세정보_title" style="font-size: 17px; line-height:23px; font-weight: bold;">상세정보</div>

    </div>
    <div class="detailed-sub">
        <div class="detailed-info-sub" data-testid="상세정보_table">
    <div class="line1" style="min-height: 35px;">
        <div class="detailed-info-sub" style="padding-top: 18px; width: 200;">
            <div dir="auto" class="detailed-info-title2" data-testid="상세정보_2title" style="font-size: 12px;">거래일</div>
            <div dir="auto" class="fifth-info-sub" data-testid="상세정보_4sub" style="color: reb(45, 96, 163); font-size: 18px;
            line-height:26px;"> {date} </div>
        <div class="detailed-info-sub" style="padding-top: 18px; width: 200;">
            <div dir="auto" class="detailed-info-title1" data-testid="상세정보_1title" style="font-size: 12px;">건축년도</div>
            <div dir="auto" class="fourth-info-sub" data-testid="상세정보_3sub" style="color: reb(45, 96, 163); font-size: 18px;
            line-height:26px;"> {year} </div>
    </div>

    """.format(name=name, adr=adr, price=price, size=size, kind=kind, year=year, date=date)

    iframe = branca.element.IFrame(html=html, width=300, height=400)
    popup = folium.Popup(iframe, max_width=300)
    icon1 = folium.features.CustomIcon('https://user-images.githubusercontent.com/74045426/'
                                       '108214349-6a16f800-7173-11eb-93db-2a61f44ec07c.png', icon_size=(55.4, 36.4))  # 휘발성!!!!!!!!!!!!11
    folium.Marker([value['위도'], value['경도']], popup=popup, icon=icon1).add_to(marker_cluster)

for key, value in dh.iterrows():
    name = value['건물명']
    adr = value['주소'] + ' ' + value['층']
    price = value['거래금액']
    size = str(value['면적']) + '(' + str(value['평']) + ')'
    year = value['건축년도']
    date = value['거래일']
    kind = value['건물형태']

    html = """
    <div class="name">
        <h2> {name} </h2>
        <div class="adr" data-testid="기본정보_1title" style="font-size: 12px; font-style: italic;"> {adr} </div>
    </div>
    <hr size="2px;" noshade size="20px;">
    <div class="line1" style></div>
    <div class="brief-info" data-testid="기본정보">
        <div class="biref-info-sub>
            <div class="first-info" style="padding-top: 13px; width: 200;">
                <div dir="auto" class="first-info-title" data-testid="기본정보_1title" style="font-size: 12px; font-weight: bold;">전세ᆞ월세</div>
                <div dir="auto" class="first-info-sub" data-testid="기본정보_1sub" style="color: reb(45, 96, 163); font-size: 25px;
                line-height:26px; color: #4169E1; font-weight: bold;"> {price} </div>
            <div class="second-info" style="padding-top: 18px; width: 200;">
                <div dir="auto" class="second-info-title" data-testid="기본정보_2title" style="font-size: 12px;">전용면적(평)</div>
                <div dir="auto" class="second-info-sub" data-testid="기본정보_2sub" style="color: reb(45, 96, 163); font-size: 19px;
                line-height:26px; color: #4169E1; font-weight: bold;"> {size} 평 </div>
            <div class="third-info" style="padding-top: 18px; width: 200;">
                <div dir="auto" class="third-info-title" data-testid="기본정보_3title" style="font-size: 12px;">건물 형태</div>
                <div dir="auto" class="third-info-sub" data-testid="기본정보_3sub" style="color: reb(45, 96, 163); font-size: 18px;
                line-height:26px; color: #4169E1; font-weight: bold;"> {kind} </div>
        </div>
    </div>

    <hr size="2px;" noshade size="20px;">
    <br>
    <div class="detailed-title">
        <div class="detailed-info-title" data-testid="상세정보_view" style="min-height: 50px;">
    <div dir="auto" class="detailed-info-title" data-testid="상세정보_title" style="font-size: 17px; line-height:23px; font-weight: bold;">상세정보</div>

    </div>
    <div class="detailed-sub">
        <div class="detailed-info-sub" data-testid="상세정보_table">
    <div class="line1" style="min-height: 35px;">
        <div class="detailed-info-sub" style="padding-top: 18px; width: 200;">
            <div dir="auto" class="detailed-info-title2" data-testid="상세정보_2title" style="font-size: 12px;">거래일</div>
            <div dir="auto" class="fifth-info-sub" data-testid="상세정보_4sub" style="color: reb(45, 96, 163); font-size: 18px;
            line-height:26px;"> {date} </div>
        <div class="detailed-info-sub" style="padding-top: 18px; width: 200;">
            <div dir="auto" class="detailed-info-title1" data-testid="상세정보_1title" style="font-size: 12px;">건축년도</div>
            <div dir="auto" class="fourth-info-sub" data-testid="상세정보_3sub" style="color: reb(45, 96, 163); font-size: 18px;
            line-height:26px;"> {year} </div>
    </div>

    """.format(name=name, adr=adr, price=price, size=size, kind=kind, year=year, date=date)

    iframe = branca.element.IFrame(html=html, width=300, height=400)
    popup = folium.Popup(iframe, max_width=300)
    icon3 = folium.features.CustomIcon('https://user-images.githubusercontent.com/74045426/'
                                       '108214348-697e6180-7173-11eb-94e1-dab5fa9db771.png', icon_size=(41.6, 35.6))  # 휘발성!!!!!!!!!!!!11
    folium.Marker([value['위도'], value['경도']], popup=popup, icon=icon3).add_to(marker_cluster)

coords = []
for i in range(len(bike)-1):
    x = bike_x[i]
    y = bike_y[i]
    coords.append([x, y])
for i in range(len(coords)):
    folium.Circle(
        location = coords[i],
        radius = 50,
        color = 'blue',
        fill = 'crimson',
    ).add_to(g1)
# m.save('2020따릉이 대여소지도.html')

mr = pd.read_csv('data/스타벅스.csv',encoding='cp949') #이 구문은 주석처리를 안해줘야지 folium을 실행할수있음 왜냐면 csv를 읽어온 토대로 위도 경도 표시를해줘야되서.

def add_marker():
    for a,b,c in zip(mr['위도'],mr['경도'],mr['가게']):
        folium.Circle([a,b],
                      radius=20,color="Green",fill_color='#fffggg',popup=c).add_to(g2)  #add_to(m) 함수는 folium.map 에 marker를 계속해서 더해준다.
add_marker()  #함수 실행하고

mr = pd.read_csv('data/대형마트.csv',encoding='cp949') #이 구문은 주석처리를 안해줘야지 folium을 실행할수있음 왜냐면 csv를 읽어온 토대로 위도 경도 표시를해줘야되서.
def add_marker():
    for a,b,c in zip(mr['위도'],mr['경도'],mr['가게']):
        folium.Circle([a,b],
                      radius=20,color="Yellow",fill_color='#fffggg',popup=c).add_to(g3)  #add_to(m) 함수는 folium.map 에 marker를 계속해서 더해준다.
add_marker()  #함수 실행하고

mr = pd.read_csv('data/맥도널드.csv',encoding='cp949') #이 구문은 주석처리를 안해줘야지 folium을 실행할수있음 왜냐면 csv를 읽어온 토대로 위도 경도 표시를해줘야되서.
def add_marker():
    for a,b,c in zip(mr['위도'],mr['경도'],mr['가게']):
        folium.Circle([a,b],
                      radius=20,color="Red",fill_color='#fffggg',popup=c).add_to(g4)  #add_to(m) 함수는 folium.map 에 marker를 계속해서 더해준다.
add_marker()  #함수 실행하고

mr = pd.read_csv('data/병원.csv',encoding='cp949') #이 구문은 주석처리를 안해줘야지 folium을 실행할수있음 왜냐면 csv를 읽어온 토대로 위도 경도 표시를해줘야되서.
def add_marker():
    for a,b,c in zip(mr['위도'],mr['경도'],mr['가게']):
        folium.Circle([a,b],
                      radius=20,color="White",fill_color='#fffggg',popup=c).add_to(g5)  #add_to(m) 함수는 folium.map 에 marker를 계속해서 더해준다.
add_marker()  #함수 실행하고

mr = pd.read_csv('data/스터디룸.csv',encoding='cp949') #이 구문은 주석처리를 안해줘야지 folium을 실행할수있음 왜냐면 csv를 읽어온 토대로 위도 경도 표시를해줘야되서.
def add_marker():
    for a,b,c in zip(mr['위도'],mr['경도'],mr['가게']):
        folium.Circle([a,b],
                      radius=20,color="Gray",fill_color='#fffggg',popup=c).add_to(g6)  #add_to(m) 함수는 folium.map 에 marker를 계속해서 더해준다.
add_marker()  #함수 실행하고

mr = pd.read_csv('data/영화관.csv',encoding='cp949') #이 구문은 주석처리를 안해줘야지 folium을 실행할수있음 왜냐면 csv를 읽어온 토대로 위도 경도 표시를해줘야되서.
def add_marker():
    for a,b,c in zip(mr['위도'],mr['경도'],mr['가게']):
        folium.Circle([a,b],
                      radius=20,color="Black",fill_color='#fffggg',popup=c).add_to(g7)  #add_to(m) 함수는 folium.map 에 marker를 계속해서 더해준다.
add_marker()  #함수 실행하고

mr = pd.read_csv('data/코인노래방.csv',encoding='cp949') #이 구문은 주석처리를 안해줘야지 folium을 실행할수있음 왜냐면 csv를 읽어온 토대로 위도 경도 표시를해줘야되서.
def add_marker():
    for a,b,c in zip(mr['위도'],mr['경도'],mr['가게']):
        folium.Circle([a,b],
                      radius=20,color="Silver",fill_color='#fffggg',popup=c).add_to(g8)  #add_to(m) 함수는 folium.map 에 marker를 계속해서 더해준다.
add_marker()  #함수 실행하고

mr = pd.read_csv('data/코인세탁소.csv',encoding='cp949') #이 구문은 주석처리를 안해줘야지 folium을 실행할수있음 왜냐면 csv를 읽어온 토대로 위도 경도 표시를해줘야되서.
def add_marker():
    for a,b,c in zip(mr['위도'],mr['경도'],mr['가게']):
        folium.Circle([a,b],
                      radius=20,color="Purple",fill_color='#fffggg',popup=c).add_to(g9)  #add_to(m) 함수는 folium.map 에 marker를 계속해서 더해준다.
add_marker()  #함수 실행하고

folium.LayerControl(collapsed=False).add_to(m_2)

m_2.save('map_RE.html')





