import urllib.request
import datetime
import csv
import pandas as pd
import time
import json
from config import *
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

# 오픈API
def getRHtradeList(LAWD_CD,DEAL_YMD):
    endPoint = 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcRHTrade'
    parm = '?_type=json&serviceKey=' + serviceKey
    parm += '&LAWD_CD=' + LAWD_CD
    parm += '&DEAL_YMD=' + DEAL_YMD
    url = endPoint + parm
    #print(url)
    retData = get_request_url(url)
    if retData == None: return None
    else : return json.loads(retData)

# LAWD_CD='11110'
# DEAL_YMD='202001'

# 데이터프레임
result=[]
def mk_df():
    if jsonData['response']['header']['resultMsg']=='NORMAL SERVICE.':
        for item in jsonData['response']['body']['items']['item']:
            region = item['지역코드']
            house = item['연립다세대']
            adr = str(item['법정동']) + ' ' + str(item['지번'])
            floor = str(item['층']) + '층'
            date = str(item['년']) + ' ' + str(item['월']) + ' ' + str(item['일'])
            price = item['거래금액']
            size = str(item['대지권면적']) + '/' + str(item['전용면적'])
            year = item['건축년도']
            result.append([region] + [house] + [adr] + [floor] + [date] + [price] + [size] + [year])
    # seoulRHtrade_table = pd.DataFrame(result, columns=('지역코드','연립다세대','주소','층','거래일','거래금액','면적','건축년도'))
    # print(seoulRHtrade_table)
# seoulRHtrade_table.to_csv('data/서울지역 연립다세대 매매 실거래가.csv',encoding='cp949',index=False)

code=set(LAWD_CD_list['코드'])
YMD=['202001','202002','202003','202004','202005','202006','202007','202008','202009','202010','202011','202012']
print(code)
for month in YMD:
    for cd in code:
        LAWD_CD=cd
        DEAL_YMD=month
        jsonData = getRHtradeList(LAWD_CD, DEAL_YMD)
        mk_df()
seoulRHtrade_table = pd.DataFrame(result, columns=('지역코드', '연립다세대', '주소', '층', '거래일', '거래금액', '면적', '건축년도'))
seoulRHtrade_table.to_csv('data/서울지역 연립다세대 매매 실거래가.csv',encoding='cp949',index=False)





