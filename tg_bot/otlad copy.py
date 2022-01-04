import urllib3

url = "https://www2.irf.se/maggraphs/rt.txt"
http = urllib3.PoolManager()
response = http.request('GET', url, headers={'Range':'bytes=-3600'})
print(response.data)