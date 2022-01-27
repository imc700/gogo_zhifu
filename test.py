import requests

def sorted_img_sales(datas):
    s = sorted(datas, key=lambda x: x['sales'])
    s.reverse()
    print(s)
def test_getImages():
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
        sorted_imgs = sorted_img_sales(json['data'])
        return json
    return ''


if __name__ == '__main__':
    test_getImages()
