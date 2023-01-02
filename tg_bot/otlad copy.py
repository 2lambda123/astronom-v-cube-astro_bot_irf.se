import urllib3

url = "https://www2.irf.se/maggraphs/rt.txt"
http = urllib3.PoolManager()
response = http.request('GET', url, headers={'Range':'bytes=-35000'})
q_data = response.data.decode("utf-8").splitlines()[-901:-1]
print(len(q_data))

# х_deviation = []
# y_deviation = []
# z_deviation = []

# for i in q_data:
#     str(i)
#     temp = i.split(' ')
#     х_deviation.append(float(temp[-3]))
#     y_deviation.append(float(temp[-2]))
#     z_deviation.append(float(temp[-1]))

# x_difference = round(max(х_deviation) - min(х_deviation), 3)
# y_difference = round(max(y_deviation) - min(y_deviation), 3)
# z_difference = round(max(z_deviation) - min(z_deviation), 3)

# print(f'Разности: {x_difference}, {y_difference}, {z_difference}')