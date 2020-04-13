import csv

msisdn_origin = []
msisdn_dest = []
call_duration = []
sms_number = []
number = '968247916'
call_vx_cost = 1
call_isx_cost = 3
sms_cost = 1
summa_vx = 0
summa_isx = 0
summa_sms = 0
summa_all = 0
# сохраняем из csv файла данные нужных столбцов(всех кроме timestamp)
with open('data.csv', "r", newline="") as file:
    reader = csv.DictReader(file, delimiter=',')
    for row in reader:
        cur_arr = row['msisdn_origin']
        msisdn_origin.extend([cur_arr])
        cur_arr = row['msisdn_dest']
        msisdn_dest.extend([cur_arr])
        cur_arr = float(row['call_duration'])
        call_duration.extend([cur_arr])
        cur_arr = int(row['sms_number'])
        sms_number.extend([cur_arr])
# ищем нужный нам по варианту телефонный номер и рассчитываем стоимость различных услуг
i = 0
while i < len(msisdn_dest):
    if msisdn_dest[i] == number:
        summa_vx = summa_vx + call_duration[i]
    i += 1
summa_vx = summa_vx*call_vx_cost
i = 0
while i < len(msisdn_origin):
    if msisdn_origin[i] == number:
        summa_isx = summa_isx + call_duration[i]
    i += 1
summa_isx = summa_isx*call_isx_cost
i = 0
while i < len(sms_number):
    if msisdn_origin[i] == number:
        summa_sms = summa_sms + sms_number[i]
    i += 1
summa_sms = summa_sms*sms_cost
# подсчитываем общую сумму и делаем вывод на экран требуемых значений
print('Duration of incoming calls:', summa_vx/call_vx_cost, 'minutes. Cost:', summa_vx, 'rubles')
print('Duration of outcoming calls:', summa_isx/call_isx_cost, 'minutes. Cost:', summa_isx, 'rubles')
print('Sms number:', summa_sms/sms_cost, 'Cost:', summa_sms, 'rubles')
summa_all = summa_sms + summa_vx + summa_isx
print('Total cost:', summa_all, 'rubles')
