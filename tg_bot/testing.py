import requests
import time
import schedule
url = "https://www2.irf.se/maggraphs/rt.txt"

def q(url):
    r = requests.get(url, timeout=60)
    data = r.text.split("\n")
    minute_data = data[-900:-1]

    х_deviation = []
    y_deviation = []
    z_deviation = []

    for i in minute_data:
        str(i)
        temp = i.split(' ')
        х_deviation.append(float(temp[-3]))
        y_deviation.append(float(temp[-2]))
        z_deviation.append(float(temp[-1]))

    x_difference = round(max(х_deviation) - min(х_deviation), 3)
    y_difference = round(max(y_deviation) - min(y_deviation), 3)
    z_difference = round(max(z_deviation) - min(z_deviation), 3)

    print(f'Разности: {x_difference}, {y_difference}, {z_difference}')


    def making_q(x_difference, y_difference, z_difference):
        if x_difference >= 15 or y_difference >= 15 or z_difference >= 15:
            return(1)
        elif x_difference >= 30 or y_difference >= 30 or z_difference >= 30:
            return(2)
        elif x_difference >= 60 or y_difference >= 60 or z_difference >= 60:
            return(3)
        elif x_difference >= 120 or y_difference >= 120 or z_difference >= 120:
            return(4)
        elif x_difference >= 210 or y_difference >= 210 or z_difference >= 210:
            return(5)
        elif x_difference >= 360 or y_difference >= 360 or z_difference >= 360:
            return(6)
        elif x_difference >= 600 or y_difference >= 600 or z_difference >= 600:
            return(7)
        elif x_difference >= 990 or y_difference >= 990 or z_difference >= 990:
            return(8)
        elif x_difference >= 1500 or y_difference >= 1500 or z_difference >= 1500:
            return(9)
        else:
            return(0)

    q = making_q(x_difference, y_difference, z_difference)
    print(f"Текущий уровень - {q}")
    return q
""" def test():
    try:
        print(time.localtime())
        schedule.every(1).minutes.do(q(url))
    except:
        print('Connection error')
        time.sleep(1) """
while True:
    
    schedule.every(1).minutes.do(q, url)

