import csv
import matplotlib
import matplotlib.pyplot as plt


ip = '217.15.20.194'
traffic_price = 1
# 1000 Kb бесплатно т.к. требуется тарификация после 1000Мб, а у абонента меньше 1000
free_traffic = 1
with open('data.csv', "r", newline="") as file:
    reader = csv.DictReader(file, delimiter=',')
    summ_bits = 0
    to_check = []
    # Обрабатываем входные данные
    for row in reader:
        if row['sa'] == ip or row['da'] == ip:
            bits_length = int(row['ibyt'])
            summ_bits += bits_length
            to_check.append(('Income:' if row['sa'] == ip else 'Outcome:') + f'{bits_length} bytes')
    # Тарифицируем абонента
    summ_mb = summ_bits / 2 ** 20
    price = (summ_mb - free_traffic) * traffic_price if summ_mb > free_traffic else 0

file_name = 'graph.png'
import datetime
import itertools
with open('data.csv', "r", newline="") as file:
    reader = csv.DictReader(file, delimiter=',')
    dates_lens = []
    for row in reader:
        if row['sa'] == ip or row['da'] == ip:
            dates_lens.append((datetime.datetime.strptime(row['ts'], "%Y-%m-%d %H:%M:%S"), int(row['ibyt']) / 1024))

    # Делаем группировку трафика по минутам
    def group_filter(x):

        return datetime.datetime.strptime(x[0].strftime('%Y-%m-%d %H:%M:0'), '%Y-%m-%d %H:%M:%S')


    dates_lens = itertools.groupby(sorted(dates_lens, key=group_filter), group_filter)

    dates_lens = [(key, sum([x[1] for x in group])) for key, group in dates_lens]

    dates = [x[0] for x in dates_lens]
    kb_len = [x[1] for x in dates_lens]

    dates = matplotlib.dates.date2num(dates)
    ax = plt.subplot(111)
    ax.plot(dates, kb_len)
    ax.xaxis_date()
    plt.xlabel('Time')
    xformatter = matplotlib.dates.DateFormatter('%H:%M')
    plt.gcf().axes[0].xaxis.set_major_formatter(xformatter)
    plt.ylabel('kB')
    plt.savefig(file_name)

# Выводим информацию
print('Mb used:', summ_mb)
print('Price is', price, 'rubles')
print(f'Graphic image saved to current directory as: {file_name}')
