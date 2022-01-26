import hashlib
import logging
import time

import flask
import requests
from flask import Flask

app = Flask(__name__)
app_id = 'b593949004c10e02'
app_secret = 'b593949004c10e028c596ef29db10680'
wayId = 7246
type = 1  # 1wx,2zfb
app_sign = hashlib.md5((app_id + app_secret).encode(encoding='utf-8')).hexdigest()
go_header = {'App-Id': app_id, 'App-Sign': app_sign}
go_url = 'https://www.gogozhifu.com/createOrder'
notify_url = 'http://q1.afanxyz.xyz:39110/notify'
return_url = 'http://q1.afanxyz.xyz:39110/result'

#https://www.gogozhifu.com/shop/user/index#//way/my/index.html
@app.route('/createOrder', methods=['GET', 'POST'])
def createOrder():
    """
    传入title和price
    :return:
    """
    print('---createOrder---')
    payId = str(int(time.time()))
    price = '0.1'
    param = 'any_img_id'
    sign = hashlib.md5((app_id + payId + param + str(type) + price + app_secret).encode(encoding='utf-8')).hexdigest()
    go_data = {'payId': payId, 'type': type, 'price': price, 'param': param, 'sign': sign, 'isHtml': 1,
               'returnParam': 1, 'wayId': wayId,
               'notifyUrl': notify_url}
    res = requests.post(go_url, data=go_data, headers=go_header)
    if res.status_code == 200:
        html = res.text
        print(html)
        return html.split("= '")[1].split("'")[0] if 'href' in html else ''
    return ''


@app.route('/notify', methods=['GET', 'POST'])
def notify():
    # 根据param去db拿个序列号
    print('---notify---')
    param = flask.request.json.get('param')
    price = flask.request.json.get('price')
    reallyPrice = flask.request.json.get('reallyPrice')
    print(param, price, reallyPrice)
    print('---notify_close---')
    if reallyPrice >= price:
        return 'success'
    print('sth price wrong...')
    return ''


@app.route('/result', methods=['GET', 'POST'])
def result():
    # 根据param去db拿个序列号
    print('---result---')
    param = flask.request.args.get('param')
    print('result param is : ', param)
    print('---result_close---')
    print('ready to select db and return sth...')
    return 'from db'


if __name__ == '__main__':
    LOG_FORMAT = '{"time":"%(asctime)s","msg":"%(message)s"}'
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, filename='./app.log')
    logging.info('zhifu start...')
    app.run(host='0.0.0.0', port=5000)
