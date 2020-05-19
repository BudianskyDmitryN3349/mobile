import csv
import fpdf
import os
# 1 Лабораторная
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
summa_vx = summa_vx * call_vx_cost
i = 0
while i < len(msisdn_origin):
    if msisdn_origin[i] == number:
        summa_isx = summa_isx + call_duration[i]
    i += 1
summa_isx = summa_isx * call_isx_cost
i = 0
while i < len(sms_number):
    if msisdn_origin[i] == number:
        summa_sms = summa_sms + sms_number[i]
    i += 1
summa_sms = summa_sms * sms_cost
# подсчитываем общую сумму

summa_all = summa_sms + summa_vx + summa_isx

# 2 Лабораторная
ip = '217.15.20.194'
traffic_price = 1
# 1000 Kb бесплатно т.к. требуется тарификация после 1000Мб, а у абонента меньше 1000
free_traffic = 1
with open('datai.csv', "r", newline="") as file:
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

summa_vsego = price + summa_all

# создание пдф файла


def to_pdf(name_of_file, name_of_bank, inn, kpp, bik, recipient, num1, num2,
           bill_number, bill_date, provider, customer, cause, summa_vsego):
    # Массив для заполнения таблицы со списком услуг и их цен
    data = [['Входящие звонки', str(summa_vx / call_vx_cost), 'Минуты', str(call_vx_cost), str(summa_vx)],
            ['Исходящие звонки', str(summa_isx / call_isx_cost), 'Минуты', str(call_isx_cost), str(summa_isx)],
            ['СМС', str(summa_sms / sms_cost), 'Штуки', str(sms_cost), str(summa_sms)],
            ['Сетевой трафик', str('%.2f' % summ_mb), 'Мегабайты', str(traffic_price), str('%.2f' % price)]]
    pdf = fpdf.FPDF()
    pdf.set_right_margin(15)
    pdf.set_left_margin(15)
    pdf.add_page()
    # Добавляем шрифт
    pdf.add_font('DejaVu', '', os.path.join('.', 'Font_Dejavu_spacebefore', 'DejaVuSansCondensed.ttf'), uni=True)
    pdf.add_font('DejaVu', 'B', os.path.join('.', 'Font_Dejavu_spacebefore', 'DejaVuSansCondensed-Bold.ttf'), uni=True)

    pdf.set_font('DejaVu', '', 10)
    headers = [[f'Банк получателя: {name_of_bank}', f'БИК: {bik}'],
               [f'ИНН: {inn}', f'КПП: {kpp}', f'Сч. № {num1}'],
               [f'Получатель: {recipient}', f'Сч. № {num2}']]
    col_width = (pdf.w - 30) / 2
    row_height = pdf.font_size * 2
    for rows in headers:
        for col in rows:
            pdf.cell(col_width / 2 if 'ИНН' in col or 'КПП' in col else col_width, row_height,
                     txt=col, border=1)
        pdf.ln(row_height)

    pdf.set_font('DejaVu', 'B', 14)
    s = f'Счёт №{bill_number} от {bill_date} г.'
    margins = int((pdf.w - pdf.get_string_width(s) - 30) / 2 / pdf.get_string_width(' ')) * ' '
    pdf.write(14, margins + s)
    pdf.ln(5)
    pdf.write(14, '_' * int((pdf.w - 30) / pdf.get_string_width('_')))

    pdf.set_font('DejaVu', '', 10)
    pdf.ln(10)
    pdf.write(10, 'Поставщик')
    pdf.ln(5)
    pdf.write(10, f'(Исполнитель): {provider}')
    pdf.ln(10)
    pdf.write(10, 'Покупатель')
    pdf.ln(5)
    pdf.write(10, f'(Заказчик): {customer}')
    pdf.ln(10)
    pdf.write(10, f'Основание: {cause}')
    pdf.ln(10)

    row_height = pdf.font_size * 2
    pdf.cell(10, row_height, txt='№', border=1)  # №
    pdf.cell(70, row_height, txt='Наименование работ, услуг', border=1)  # Наименование
    pdf.cell(15, row_height, txt='Кол-вo', border=1)  # Кол-во
    pdf.cell(30, row_height, txt='Ед.', border=1)  # Ед.
    pdf.cell(25, row_height, txt='Цена', border=1)  # Ценна
    pdf.cell(25, row_height, txt='Сумма', border=1)  # Сумма*
    pdf.ln(row_height)
    for rows in data:
        row_num = 0
        pdf.cell(10, row_height, txt=str(row_num + 1), border=1)  # №
        pdf.cell(70, row_height, txt=rows[0], border=1)  # Наименование
        pdf.cell(15, row_height, txt=rows[1], border=1)  # Кол-во
        pdf.cell(30, row_height, txt=rows[2], border=1)  # Ед.
        pdf.cell(25, row_height, txt=rows[3], border=1)  # Ценна
        pdf.cell(25, row_height, txt=rows[4], border=1)  # Сумма*
        pdf.ln(row_height)

    summa_vsego = float("{0:.2f}".format(summa_vsego))
    strings = [f'Итого: {summa_vsego } руб.', f'В том числе НДС: 0 руб.', f'Всего к оплате: {summa_vsego} руб.']
    pdf.set_font('DejaVu', 'B', 10)
    for s in strings:
        margins = int((pdf.w - pdf.get_string_width(s) - 36) / pdf.get_string_width(' ')) * ' '
        pdf.write(10, margins + s)
        pdf.ln(5)
    pdf.ln(5)

    pdf.set_font('DejaVu', '', 10)
    strings = ['*Сумма была расчитана с учетом цены и количества первых бесплатных единиц по вашему тарифу', 'Внимание!', 'Оплата данного счета означает согласие с условиями поставки товара.',
               'Уведомление об оплате обязательно, в противном случае не гарантируется наличие товара на складе.',
               'Товар отпускается по факту прихода денег на р/с Поставщика, самовывозом, при наличии',
               'доверенности и паспорта.']
    for s in strings:
        pdf.write(10, s)
        pdf.ln(5)
    pdf.set_font('DejaVu', 'B', 14)
    pdf.write(14, '_' * int((pdf.w - 30) / pdf.get_string_width('_')))
    pdf.ln(20)
    pdf.set_font('DejaVu', '', 10)
    margins = int((pdf.w - pdf.get_string_width('РуководительБухгалтер') - 30) / 2 / pdf.get_string_width('_')) * '_'
    pdf.write(10, f'Руководитель{margins}Бухгалтер{margins}')

    pdf.output(name=name_of_file)


to_pdf('Bill.pdf', 'MMMS', '316451354', '3451', '3154', 'Пржевальскый', '1254', '2245',
       '14523', '19.05.2020', 'ОАО АОА', 'Пржевальскый', 'Мое желание', summa_vsego)
print('Счет был успешно сформирован.')
