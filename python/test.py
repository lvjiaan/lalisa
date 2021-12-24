import requests











if __name__ == '__main__':
    url = "http://image.zldsj.com/H/PID/CNA0/2005/0914/00000000001666/0FCE14NKRU014F57/CLA/CLA_ZH.html"

    result = requests.get(url)

    print(result.text)
