import urllib.request
import datetime
import csv
import pandas as pd
import time
import json
from config import *

# 서울지역 법정동 코드 확인
with open('data/서울특별시 건축물대장 법정동 코드정보.csv','r',encoding='cp949') as f:
    csv_data = csv.reader(f)
    # 2차원 리스트 구조로 변경
    temp_list = list(csv_data)
    LAWD_list=[]
    for CD,b,c,city,gu,dong,g,h,i in temp_list:
        if city=='서울특별시':
            LAWD_list.append([CD,city,gu,dong])
LAWD_CD_list=pd.DataFrame(LAWD_list, columns=('코드','시','구','동'))
print(LAWD_CD_list)
print(LAWD_CD_list['코드'])

def get_request_url(url, enc='utf-8'):
    req = urllib.request.Request(url)
    try :
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            try:
                rcv = response.read()
                ret = rcv.decode(enc)
            except UnicodeDecodeError:
                ret = rcv.decode(enc,'replace')
            return ret
    except Exception as e:
        print(e)
        print("[%s] Error for URL: %s" % (datetime.datetime.now(), url))
        return None

# # 연립다세대
# # 오픈API
# def getRHtradeList(LAWD_CD,DEAL_YMD):
#     endPoint = '	http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcRHRent'
#     parm = '?_type=json&serviceKey=' + serviceKey
#     parm += '&LAWD_CD=' + LAWD_CD
#     parm += '&DEAL_YMD=' + DEAL_YMD
#     url = endPoint + parm
#     #print(url)
#     retData = get_request_url(url)
#     if retData == None: return None
#     else : return json.loads(retData)
#
# # 데이터프레임
# result=[]
# def mk_df():
#     if jsonData['response']['header']['resultMsg']=='NORMAL SERVICE.' :
#         print(jsonData)
#         print("="*20)
#         if jsonData['response']['body']['totalCount'] == 0:
#             return None
#
#         for item in jsonData['response']['body']['items']['item']:
#             if '지번' not in item.keys(): break
#             elif '건축년도' not in item.keys():break
#             region = item['지역코드']
#             house = item['연립다세대']
#             adr = str(item['법정동']) + ' ' + str(item['지번'])
#             floor = str(item['층']) + '층'
#             date = str(item['년']) + ' ' + str(item['월']) + ' ' + str(item['일'])
#             price = str(item['보증금액']) + '/' + str(item['월세금액'])
#             size = item['전용면적']
#             year = item['건축년도']
#             result.append([region] + [house] + [adr] + [floor] + [date] + [price] + [size] + [year])
#     # seoulRHtrade_table = pd.DataFrame(result, columns=('지역코드','연립다세대','주소','층','거래일','거래금액','면적','건축년도'))
#     # print(seoulRHtrade_table)
# # seoulRHtrade_table.to_csv('data/서울지역 연립다세대 매매 실거래가.csv',encoding='cp949',index=False)
#
# code=set(LAWD_CD_list['코드'])
# YMD=['202001','202002','202003','202004','202005','202006','202007','202008','202009','202010','202011','202012']
# print(code)
# for month in YMD:
#     for cd in code:
#         LAWD_CD=cd
#         DEAL_YMD=month
#         jsonData = getAPTtradeList(LAWD_CD, DEAL_YMD)
#         mk_df()
# seoulAPTtrade_table = pd.DataFrame(result, columns=('지역코드', '건물명', '주소', '층', '거래일', '거래금액', '면적', '건축년도'))
# seoulAPTtrade_table.to_csv('data/서울지역 연립다세대 전월세.csv',encoding='cp949',index=False)

# 좌표값
# 좌표출력 오픈API
def getLocation(location):
    endPoint = 'http://api.vworld.kr/req/address?service=address&request=getcoord&version=2.0&crs=epsg:4326'
    parm = '&address='+urllib.parse.quote(location)
    parm += '&refine=false&simple=false&format=json&type=parcel'
    parm += '&key=A32C414E-511C-38A4-B53C-215AE9AC3B0C'
    url = endPoint + parm
    print(url)
    retData = get_request_url(url)
    if retData == None:
        return None
    else:
        return json.loads(retData)

rh_list=pd.read_csv('data/서울지역 연립다세대 전월세.csv', encoding='cp949')
rh_list

# adr_list1=set(rh_list['주소'][:2500])
# print(len(adr_list1))
# lat_list1=[]
# long_list1=[]
# for adr in adr_list1:
#     loca_json=getLocation(adr)
#     if loca_json['response']['status'] == 'OK':
#         lat_list1.append([adr,loca_json['response']['result']['point']['y']])
#         long_list1.append([adr,loca_json['response']['result']['point']['x']])
#     else:
#         pass
#
# lat_df1 = pd.DataFrame(lat_list1, columns=('주소','위도'))
# long_df1 = pd.DataFrame(long_list1, columns=('주소','경도'))
# loca_df1=pd.merge(lat_df1,long_df1)
# loca_df1.to_csv('data/전월세 위치값_연립다세대1.csv', encoding='cp949', index=False)
# loca_df1

adr_list2=set(rh_list['주소'][2500:5000])
print(len(adr_list2))
lat_list2=[]
long_list2=[]
for adr in adr_list2:
    loca_json=getLocation(adr)
    if loca_json['response']['status'] == 'OK':
        lat_list2.append([adr,loca_json['response']['result']['point']['y']])
        long_list2.append([adr,loca_json['response']['result']['point']['x']])
    else:
        pass

lat_df2 = pd.DataFrame(lat_list2, columns=('주소','위도'))
long_df2 = pd.DataFrame(long_list2, columns=('주소','경도'))
loca_df2=pd.merge(lat_df2,long_df2)
loca_df2.to_csv('data/전월세 위치값_연립다세대2.csv', encoding='cp949', index=False)
loca_df2









