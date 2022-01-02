import requests
import numpy as np
url = "https://www2.irf.se/maggraphs/rt.txt"
r = requests.get(url)
data = r.text
minute_data = str(data[-33855:])
х_deviation = []
y_deviation = []
z_deviation = []

item_start = 0
item_finish = 36


for i in np.arange(1, 900, 1):
    work_string = minute_data[item_start:item_finish]

xxx = list(map(float, minute_data.split()))
print(xxx)
print(minute_data)
""" for i in xxx:
    print(float(i)) """

""" 
    х_deviation.append(float(work_string[16:22]))
    y_deviation.append(float(work_string[23:29]))
    z_deviation.append(float(work_string[30:37]))
    item_start += 37
    item_finish += 37

x_difference = max(х_deviation) - min(х_deviation)
y_difference = max(y_deviation) - min(y_deviation)
z_difference = max(z_deviation) - min(z_deviation)

print(f'Разности: {x_difference}, {y_difference}, {z_difference}')

def making_q(x_difference, y_difference, z_difference):
    if x_difference > 15 or y_difference > 15 or z_difference > 15:
        return(1)
    elif x_difference > 30 or y_difference > 30 or z_difference > 30:
        return(2)
    elif x_difference > 60 or y_difference > 60 or z_difference > 60:
        return(3)
    elif x_difference > 120 or y_difference > 120 or z_difference > 120:
        return(4)
    elif x_difference > 210 or y_difference > 210 or z_difference > 210:
        return(5)
    elif x_difference > 360 or y_difference > 360 or z_difference > 360:
        return(6)
    elif x_difference > 600 or y_difference > 600 or z_difference > 600:
        return(7)
    elif x_difference > 990 or y_difference > 990 or z_difference > 990:
        return(8)
    elif x_difference > 1500 or y_difference > 1500 or z_difference > 1500:
        return(9)
    else: 
        return(0)

q = making_q(x_difference, y_difference, z_difference)
print(f"Текущий уровень - {q}")
 """
