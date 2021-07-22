import urllib.request
import datetime
import csv
import pandas as pd
import time
import json
from config import *
import urllib
from bs4 import BeautifulSoup
import requests

# def get_request_url(url, enc='utf-8'):
#     req = urllib.request.Request(url)
#     try :
#         response = urllib.request.urlopen(req)
#         if response.getcode() == 200:
#             try:
#                 rcv = response.read()
#                 ret = rcv.decode(enc)
#             except UnicodeDecodeError:
#                 ret = rcv.decode(enc,'replace')
#             return ret
#     except Exception as e:
#         print(e)
#         print("[%s] Error for URL: %s" % (datetime.datetime.now(), url))
#         return None
#
# # 오픈API
# def getRHtradeList(LAWD_CD,DEAL_YMD):
#     endPoint = 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcRHTrade'
#     parm = '?_type=json&serviceKey=' + serviceKey
#     parm += '&LAWD_CD=' + LAWD_CD
#     parm += '&DEAL_YMD=' + DEAL_YMD
#     url = endPoint + parm
#     #print(url)
#     retData = get_request_url(url)
#     if retData == None: return None
#     else : return json.loads(retData)
#
# LAWD_CD ='11110'
# DEAL_YMD='202001'
# jsonData = getRHtradeList(LAWD_CD,DEAL_YMD)
# print(jsonData)
#
# # 서울지역 법정동 코드 확인
# with open('data/서울특별시 건축물대장 법정동 코드정보.csv','r',encoding='cp949') as f:
#     csv_data = csv.reader(f)
#     # 2차원 리스트 구조로 변경
#     temp_list = list(csv_data)
#     LAWD_list=[]
#     for CD,b,c,city,gu,dong,g,h,i in temp_list:
#         if city=='서울특별시':
#             LAWD_list.append([CD,city,gu,dong])
# LAWD_CD_list=pd.DataFrame(LAWD_list, columns=('코드','시','구','동'))
# print(LAWD_CD_list)
# print(LAWD_CD_list['코드'])
#
# result=[]
# if jsonData['response']['header']['resultMsg']=='NORMAL SERVICE.':
#     for item in jsonData['response']['body']['items']['item']:
#         if item['지역코드'] in LAWD_CD_list['코드']:
#             pass
#         else:
#             지역코드 = item['지역코드']
#             연립다세대 = item['연립다세대']
#             주소 = str(item['법정동'])+' '+str(item['지번'])
#             층 = str(item['층'])+'층'
#             거래일 = str(item['년'])+' '+str(item['월'])+' '+str(item['일'])
#             거래금액 = item['거래금액']
#             면적 = str(item['대지권면적'])+'/'+str(item['전용면적'])
#             건축년도 = item['건축년도']
#             result.append([지역코드]+[연립다세대]+[주소]+[층]+[거래일]+[거래금액]+[면적]+[건축년도])
# print(result)
#
# seoulRHtrade_table = pd.DataFrame(result, columns=('지역코드','연립다세대','주소','층','거래일','거래금액','면적','건축년도'))
# seoulRHtrade_table.to_csv('data/서울지역 연립다세대 매매 실거래가.csv',index=False,encoding='cp949')

#위도 경도 변환

위도=[]
경도=[]
type = "ROAD"
#PARCEL : 지번주소
#ROAD : 도로명주소
def get_adress():
    with open('data/서울스타벅스.csv', 'r', encoding='cp949') as f:
        csv_data = csv.reader(f)
        result = list(csv_data)
        doro=[]
    for i in result[1:]:
        doro.append(i[2])
    for i in doro:  # 도로주소리스트 하나씩 읽어와서 location에 저장한다.
        location = i
        response = requests.get(f"http://api.vworld.kr/req/address?service=address&request=getcoord&version=2.0&crs=epsg:4326&address={location}%2060&refine=true&simple=false&format=xml&type={type}&key=3D544037-868B-322B-A320-11D7EE4A996C")
        soup = BeautifulSoup(response.text, "xml")
        if soup.find('x') is None or soup.find('y') is None:
            parcel = "PARCEL"
            response = requests.get(f"http://api.vworld.kr/req/address?service=address&request=getcoord&version=2.0&crs=epsg:4326&address={location}%2060&refine=true&simple=false&format=xml&type={parcel}&key=3D544037-868B-322B-A320-11D7EE4A996C")
            soup = BeautifulSoup(response.text,"xml")
            x = soup.find('x').text
            y = soup.find('y').text
        else:
            x = soup.find('x').text
            y = soup.find('y').text
        위도.append(x)
        경도.append(y)
# get_adress()함수는 위도와 경도를 csv에 저장시켜주는 함수다. 1번얻어왓으면 주석처리해주면됌.
get_adress()
mr = pd.read_csv('data/서울스타벅스.csv',encoding='cp949') #이 구문은 주석처리를 안해줘야지 folium을 실행할수있음 왜냐면 csv를 읽어온 토대로 위도 경도 표시를해줘야되서.

#위도, 경도 리스트를 mr이라는 변수=> 즉 파일명.csv에 위도 ,경도 컬럼 생성후 위도, 경도를 전부 넣어주고 to_csv로 파일을 저장시켜준다.
mr['위도'] = 위도
mr['경도'] = 경도
mr.to_csv('data/서울스타벅스.csv', index=False, encoding='cp949')


#---------------------------------------------------------------2021-02-04/남재현 folium 마커 표시
import folium
m = folium.Map(location=[37.566345, 126.977893],zoom_start=12) #초기에 어떤 위치로 잡을지 지정
def add_marker():
    for a,b,c in zip(mr['위도'],mr['경도'],mr['가게']):
        folium.Circle([b,a],
                      radius=20,color="Green",fill_color='#fffggg',popup=c).add_to(m)  #add_to(m) 함수는 folium.map 에 marker를 계속해서 더해준다.
add_marker()  #함수 실행하고
m.save('data/서울스타벅스.html') #파일 저장