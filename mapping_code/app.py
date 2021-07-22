import io
from io import BytesIO, StringIO
from flask import Flask,render_template,Response
from flask.globals import request
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
import random
import pandas as pd
from haversine import haversine
import seaborn as sns
import matplotlib.font_manager as fm
plt.rcParams['font.family']='Gulim'

locat=pd.read_csv('data/location.csv', encoding='cp949')
env=pd.read_csv('data/environment.csv', encoding='cp949')

app = Flask(__name__)
@app.route("/")
def index():
    adr = str(request.args.get('adr', '가락동 169-2'))
    n=int(request.args.get('n',49772))
    num_x = int(request.args.get('num_x', 49772))
    spec = locat.loc[num_x]['주소']
    return render_template('index.html', adr=adr, num_x = num_x, n=n, spec=spec)

@app.route('/code')
def code():
    adr=request.args.get("adr")
    n=locat[locat.주소==adr].index
    return render_template('index.html', n=n, adr=adr)

@app.route('/matplot-imag-<int:num_x>.png')
def plot_png2(num_x):
    fig2 = Figure()
    start=(locat.loc[num_x]['위도'],locat.loc[num_x]['경도'])
    sur=env[(env.위도<locat.loc[num_x]['위도']+0.01) & (env.위도>locat.loc[num_x]['위도']-0.01)
        & (env.경도<locat.loc[num_x]['경도']+0.013) & (env.경도>locat.loc[num_x]['경도']-0.013)]
    dis=[]
    for key,value in sur.iterrows():
        goal=(value['위도'],value['경도'])
        dis.append([value['주소'],haversine(start,goal)])
    dis=pd.DataFrame(dis, columns=('주소','거리'))
    distance=pd.merge(sur,dis)
    plt.figure(figsize=(14,6))
    ax = plt.subplot(1, 2, 1)
    sns.scatterplot(data=distance, x='경도', y='위도', hue='입지요건', s=400, marker=(5,0))
    ax = plt.subplot(1, 2, 2)
    sns.scatterplot(data=distance, x='입지요건', y='거리', hue='입지요건', s=400, marker=(5,0))

    # binary object
    img=BytesIO()
    plt.savefig(img, format='png', dpi=300)
    img.seek(0)
    return Response(img, mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=True)