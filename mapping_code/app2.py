from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import pymysql
from haversine import haversine
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
plt.rcParams['font.family']='Gulim'

locat=pd.read_csv('data/location.csv', encoding='cp949')
env=pd.read_csv('data/environment.csv', encoding='cp949')
def scat(n):
    start=(locat.loc[n]['위도'],locat.loc[n]['경도'])
    sur=env[(env.위도<locat.loc[n]['위도']+0.01) & (env.위도>locat.loc[n]['위도']-0.01)
        & (env.경도<locat.loc[n]['경도']+0.013) & (env.경도>locat.loc[n]['경도']-0.013)]
    dis=[]
    for key,value in sur.iterrows():
        goal=(value['위도'],value['경도'])
        dis.append([value['주소'],haversine(start,goal)])
    dis=pd.DataFrame(dis, columns=('주소','거리'))
    distance=pd.merge(sur,dis)
    plt.figure(figsize=(12,8))
    fig1=sns.scatterplot(data=distance, x='경도', y='위도', hue='입지요건', s=400, marker=(5,0))
    plt.figure(figsize=(10,6))
    fig2=sns.scatterplot(data=distance, x='입지요건', y='거리', hue='입지요건', s=400, marker=(5,0))
    print(fig1,fig2)

def search(adr):
    n=locat[locat.주소==adr].index
    print(n)

app=Flask(__name__)

@app.route('/')
@app.route('/<url_answer>')

def hello_world(url_answer=None):
    answer = url_answer
    return render_template('template/main.html',render_answer=answer)

@app.route('/search')
def search():
    input_data1 = request.args.get('input1')
    if search(input_data1).isdigit():
        answer=search(input_data1)
    else:
        return 'wrong adr'

    next_url='/'+str(answer)
    return redirect(next_url)

if __name__=='__main__':
    app.run()



# input_data2 = request.args.get('input2')





