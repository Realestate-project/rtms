from flask import Flask, send_file, render_template, make_response

from io import BytesIO, StringIO
import numpy as np

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# remove cache
from functools import wraps, update_wrapper
from datetime import datetime

def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
    return update_wrapper(no_cache, view)

app = Flask(__name__, static_url_path='/static')

@app.route('/normal/<m_v>')
@nocache
def normal(m_v):
    m, v = m_v.split("_")
    m, v = int(m), int(v)
    return render_template("random_gen.html", mean=m, var=v, width=800, height=600)

@app.route('/fig/<int:mean>_<int:var>')
@nocache
def fig(mean, var):
    plt.figure(figsize=(4,3))
    xs = np.random.normal(mean,var,100)
    ys = np.random.normal(mean,var,100)
    plt.scatter(xs,ys, s=100, marker='h', color='red', alpha=0.3)

    # binary object
    img=BytesIO()
    plt.savefig(img, format='png', dpi=300)
    img.seek(0)
    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)





















