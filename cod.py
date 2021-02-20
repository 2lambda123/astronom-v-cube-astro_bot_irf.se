
# from bs4 import BeautifulSoup
# import requests
# url = 'http://www2.irf.se/Observatory/?link%5BMagnetometers%5D=Data/'
# headers = {
#     "Accept": "*/*",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 OPR/74.0.3911.107"
# }
# req = requests.get(url, headers = headers)
# src = req.text
# soup = BeautifulSoup(src, "lxml")
# title = soup.title
# print(title.text)
