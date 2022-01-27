import hashlib
import logging
import time

import flask
import requests
from flask import Flask, session

from auto_pay_img import auto_pay

app = Flask(__name__)
app.config['SECRET_KEY'] = 'imc700'
# ctx = app.app_context()
# ctx.push()
app_id = 'b593949004c10e02'
app_secret = 'b593949004c10e028c596ef29db10680'
wayId = 7246
type = 1  # 1wx,2zfb
app_sign = hashlib.md5((app_id + app_secret).encode(encoding='utf-8')).hexdigest()
go_header = {'App-Id': app_id, 'App-Sign': app_sign}
go_url = 'https://www.gogozhifu.com/createOrder'
notify_url = 'http://q1.afanxyz.xyz:39110/notify'
return_url = 'http://q1.afanxyz.xyz:39110/result'


# https://www.gogozhifu.com/shop/user/index#//way/my/index.html
@app.route('/createOrder', methods=['GET', 'POST'])
def createOrder():
    """
    传入title和price
    :return:
    """
    print('---createOrder---')
    payId = str(int(time.time()))
    price = flask.request.args.get('price')
    param = flask.request.args.get('id')
    if price is None or param is None:
        return 'param missing.'
    sign = hashlib.md5((app_id + payId + param + str(type) + price + app_secret).encode(encoding='utf-8')).hexdigest()
    go_data = {'payId': payId, 'type': type, 'price': price, 'param': param, 'sign': sign, 'isHtml': 1,
               'returnParam': 0, 'wayId': wayId,
               'notifyUrl': notify_url}
    res = requests.post(go_url, data=go_data, headers=go_header)
    if res.status_code == 200:
        html = res.text
        print(html)
        return html.split("= '")[1].split("'")[0] if 'href' in html else ''
    return ''


@app.route('/notify', methods=['GET', 'POST'])
def notify():
    print('---notify---')
    param = flask.request.json.get('param')
    price = flask.request.json.get('price')
    reallyPrice = flask.request.json.get('reallyPrice')
    print('notify get all param: ', param, price, reallyPrice)
    print('---go to order now---')
    pay_result = auto_pay(str(param))
    if pay_result is None:
        return 'order ice failed...please check your money in ice...'
    session['final_key'] = pay_result
    print('---go to order close---')
    print('---notify_close---')
    if reallyPrice >= price:
        return 'success'
    print('sth price wrong...it looks like reallyPrice < price')
    return ''


@app.route('/result', methods=['GET', 'POST'])
def result():
    # 根据param去db拿个序列号,方案2
    print('---result---')
    # param = flask.request.args.get('param')
    # print('result param is : ', param)
    print('---result_close---')
    return session.get('final_key')


def sorted_img_sales(datas, page_index):
    should_remove = ["11560", "11582", "10769", "11304"]
    datas = [x for x in datas if x['tid'] not in should_remove and '0' != x['stock']]
    s = sorted(datas, key=lambda x: x['sales'])
    s.reverse()
    for x in s:
        x['price'] = round(x['price'] + 2, 2)
    return s[(page_index - 1) * 10: page_index * 10]


@app.route('/getImages', methods=['GET', 'POST'])
def getImages():
    page_index = flask.request.args.get('pageIndex')
    img_header = {'Host': 'ice.emao99.com',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
                  'Accept': 'application/json, text/javascript, */*; q=0.01',
                  'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                  'Accept-Encoding': 'gzip, deflate',
                  'X-Requested-With': 'XMLHttpRequest',
                  'Connection': 'keep-alive',
                  'Referer': 'http://ice.emao99.com/?cid=181',
                  'Cookie': 'PHPSESSID=q0ci4332ioif5tkn2jeldt6nco; mysid=e25c9efd3889dc89b26e8e14e78983a3; _aihecong_chat_visibility=false; _aihecong_chat_visitorlimit=%7B%22limitVisit%22%3Atrue%2C%22limitMarktTime%22%3A1643267004322%7D; op=false; counter=1; user_token=246byvEQq3%2FtXJ9UC905q4LyzRH41xTxVAAGLWOB62exE5fwesr1wgDgPSjU8MDKnGVyqJAI3cPB8rNVpHU9Tdsad0c',
                  'Cache-Control': 'max-age=0'}
    res = requests.get('http://ice.emao99.com/ajax.php?act=gettool&cid=181&info=1', headers=img_header)
    if res.status_code == 200 and 'suc' in res.text:
        json = res.json()
        sorted_imgs = sorted_img_sales(json['data'], int(page_index))
        json['data'] = sorted_imgs
        return json
    return ''


if __name__ == '__main__':
    LOG_FORMAT = '{"time":"%(asctime)s","msg":"%(message)s"}'
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, filename='./app.log')
    logging.info('zhifu start...')
    app.run(host='0.0.0.0', port=5000)