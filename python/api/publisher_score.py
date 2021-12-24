import requests
import datetime
import hashlib

# 出版社分数接口调用


url = 'http://e.cnipr.com/services/rs/score/loadScoreInfo'
api_key = "nbeval"
api_secret = "2ru3s34pk02r77cy"


def post_score(pn):
    params = {
        'pns': pn,
        'api_key': api_key,
        'sign': sign(pn)
    }
    result = requests.get(url, params=params)
    return result


def sign(pn):
    original_str = pn + api_key + api_secret + datetime.datetime.now().strftime("%Y%m%d%H")
    md = hashlib.md5()
    md.update(original_str.encode('ascii'))
    md_digest = md.digest()
    str2 = ''
    for val in md_digest:
        val = val & 0xFF
        if val <= 15:
            str2 += '0'
        str2 += format(val, 'x')
    return str2.lower()


if __name__ == '__main__':
    request = post_score('CN105730698B')
    print(request.text)
    # score = post_result.json()['score']
    print(request.json()['score'])
