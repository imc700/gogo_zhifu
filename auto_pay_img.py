import requests

pay_header = {'Host': 'ice.emao99.com',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
              'Accept': 'application/json, text/javascript, */*; q=0.01',
              'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
              'Accept-Encoding': 'gzip, deflate, br',
              'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
              'X-Requested-With': 'XMLHttpRequest',
              'Content-Length': '77',
              'Origin': 'https://ice.emao99.com',
              'Connection': 'keep-alive',
              'Referer': 'https://ice.emao99.com/user/shop.php?cid=181&tid=11466',
              'Cookie': 'PHPSESSID=q0ci4332ioif5tkn2jeldt6nco; mysid=e25c9efd3889dc89b26e8e14e78983a3; _aihecong_chat_visibility=false; _aihecong_chat_visitorlimit=%7B%22limitVisit%22%3Atrue%2C%22limitMarktTime%22%3A1643267004322%7D; op=false; counter=1; user_token=246byvEQq3%2FtXJ9UC905q4LyzRH41xTxVAAGLWOB62exE5fwesr1wgDgPSjU8MDKnGVyqJAI3cPB8rNVpHU9Tdsad0c',
              'Sec-Fetch-Dest': 'empty',
              'Sec-Fetch-Mode': 'cors',
              'Sec-Fetch-Site': 'same-origin'}


def real_pay(trade_no):
    """
    提交订单成功后,默认拿最后一个单子去获取卡密
    :return:
    """
    order_id = 'must be the order'
    res = requests.post('https://ice.emao99.com/ajax.php?act=payrmb', data='orderid={}'.format(trade_no),
                        headers=pay_header)
    if res.status_code == 200 and 'orderid' in res.text:
        json = res.json()
        order_id = json['orderid']
    # todo 此处的page=1有隐患,要测试一下订单量多少后会翻页,翻页后是否还是从第一页拿第一个数据为最新
    res = requests.post('https://ice.emao99.com/ajax.php?act=query', data='qq=&page=1', headers=pay_header)
    if res.status_code == 200 and order_id in res.text:
        json = res.json()
        order = json['data'][0]
        _res = requests.post('https://ice.emao99.com/ajax.php?act=order',
                             data='id={}&skey={}'.format(order['id'], order['skey']), headers=pay_header)
        print(_res.text)
        if _res.status_code == 200 and 'suc' in _res.text:
            print('#########付款成功###########')
            return _res.json()['kminfo'].split('<')[0]
    print('real_pay sth wrong...')
    return None


def auto_pay(tid):
    res = requests.post('https://ice.emao99.com/ajax.php?act=pay',
                        data='tid={}&inputvalue=18836417&num=1&hashsalt=766ee927da4b55aefae105325738fbb0'.format(tid),
                        headers=pay_header)
    if res.status_code == 200 and 'trade_no' in res.text:
        json = res.json()
        if json['need'] > float(json['user_rmb']):
            print('有人下单了,余额不足!!! 需要 {} ,但账户里只有 {} ,请尽快充值')
        else:
            # 拿到订单号了就去下单,获取卡密
            print('余额充足,现在去用ice分站的余额付款...')
            return real_pay(json['trade_no'])
    return None


if __name__ == '__main__':
    auto_pay('11503')
