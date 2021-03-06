from functools import reduce

import numpy as np
from flask import json, jsonify, render_template, request
from flask_babel import lazy_gettext as _l
from flask_babel import _
from flask_login import current_user, login_user, logout_user

from app.data import bp
from app.models import Ngrok
from ext import cache, desc

ord_data = []

def gen_vibration(t, sampling_rate, fft_size):
    x = np.sin(2*np.pi*156.25*t)+1 + 2*np.sin(2*np.pi*234.375*t)+2
    xs = x[:fft_size]
    # xf = np.fft.rfft(xs)/fft_size
    # freqs = np.linspace(0, sampling_rate/2, fft_size/2+1)
    # xfp = 20*np.log10(np.clip(np.abs(xf), 1e-20, 1e100))
    # xfp2 = np.clip(np.abs(xf), 1e-20, 1e100)
    return xs      


def gen_speed(t, sampling_rate, fft_size):
    A = [round(np.random.random_sample()*100, 2) for i in range(3)]
    W = [round(np.random.random_sample()*1000, 2) for i in range(3)]
    ys = [i*np.sin(2*np.pi*j*t)+i for i, j in zip(A, W)]
    x = reduce((lambda x, y: x + y), ys)
    xs = x[:fft_size]
    return xs                                            

@cache.cached(timeout=50)
@bp.route('/', methods=['GET', 'POST'])
def  index():
    data_set=dict()
    sampling_rate = 4000
    fft_size = 256
    t = np.arange(0, 20.0, 1.0/sampling_rate)
    tr = [round(i, 4) for i in t]
    x = np.linspace(0, 300, 256)
    xr = [round(i, 2) for i in x]

    y1 = [round(i, 2) for i in gen_speed(t, sampling_rate, fft_size)]
    y2 = [round(i, 2) for i in gen_vibration(t, sampling_rate, fft_size)]
    # fft_data = [round(i, 2) for i in fy]

    y = [y1,y2]
    fy = [20*np.log10(np.clip(np.abs(abs(np.fft.fft(i)) /
                         len(x)), 1e-20, 1e100)) for i in y]
    fft_data = [[round(i, 2) for i in p] for p in fy]

    data_set['orig'] = [{'i': i, 't': ts, 'y1': j1, 'y2': j2}
                        for i,(ts, j1,j2) in enumerate(zip(tr, y1,y2))]
    # data_set['ana'] = [{'i': i, 'x': x, 'y': x}
    #                    for i, (x, y) in enumerate(zip(xr, fft_data))]

    if request.method == 'POST':
        return jsonify({
            'x':    xr,
            't':    tr,
            'y1':   y1,
            'y2':   y2,
            'fy':   fft_data
        })
        
    if request.method == 'GET':
        return render_template('data/index.html', title=_('Data'), data='active', data_set=data_set)
    


@bp.route('/fft', methods=['GET', 'POST'])
def fft():
    # global ord_data
    if request.method == 'POST':
        x = json.loads(request.form['x'])
        y = np.asarray(json.loads(request.form['y']), dtype=float)
        # print(y.shape)
        fy = [np.clip(np.abs(abs(np.fft.fft(i)) /
                                         len(x)), 1e-20, 1e100) for i in y]
        fft_data = [[round(i, 2) for i in p] for p in fy]
        
        # ord_data = fft_data
        return jsonify(
            {
                'x': x,
                'y': fft_data
            }
        )


@bp.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        x = request.form['x']
        y = request.form['y']
        fy = abs(np.fft.fft(y))/len(x)
        fft_data = [round(i, 2) for i in fy]
        return jsonify(
            {
                'x':x,
                'fft': fft_data
            }
        )


@cache.cached(timeout=50)
@bp.route('/save', methods=['GET', 'POST'])
def save():
    if request.method == 'POST':
        x = request.form['x']
        y = request.form['y']
        fy = abs(np.fft.fft(y))/len(x)
        fft_data = [round(i, 2) for i in fy]
        return jsonify(
            {
                'x':x,
                'fft': fft_data
            }
        )
