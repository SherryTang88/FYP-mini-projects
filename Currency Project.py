#I am just trying push.

import pandas_datareader as data
import datetime
import matplotlib.pyplot as plt
import requests

def main_menu():
    next = '1'
    while next == '1':
        mode = int(input('''
Welcome to CURRENCY EXPERT!

Please select a function to continue:
1. money exchange calculation
2. view currency trend

(sample input : 1 or 2)
'''))

        if mode == 1:
            next = mode_calculate()
        elif mode == 2:
            next = mode_trend()

def mode_calculate():

    flag = False

    while flag == False:
        input_code = str(input('''
________________________________________
Currently Supported and Respective Code:

Brazilian Real : BRL
Canadaian Dollar : CAD
Chinese Yuan : CNY
Denish Krone : DKK
Hong Kong Dollar : HKD
Indian Rupee : INR
Japanese Yen : JPY
South Korean Won : KRW
Malaysian Ringgit : MYR
Mexican Peso : MXN
Norwegian Krone: NOK
Swedish Krona : SEK
South African Rand: ZAR
Singapore Dollar : SGD
Sri Lankan Rupee: LKR
Swiss Franc : CHF
New Taiwan Dollar : TWD
Thai Baht : THB
Australian Dollar : AUD
Euro : EUR
New Zealand Dollar : NZD
British Pound : GBP
Venezuelan Bolivar : VEF
________________________________________

Would you like to exchange money from ___ ?
(sample input : SGD/CNY/JPY)
'''))
        input_code = input_code.upper()
        in_code = input_to_code(input_code)
        output_code= str(input('''
________________________________________
Currently Supported and Respective Code:
Brazilian Real : BRL
Canadaian Dollar : CAD
Chinese Yuan : CNY
Denish Krone : DKK
Hong Kong Dollar : HKD
Indian Rupee : INR
Japanese Yen : JPY
South Korean Won : KRW
Malaysian Ringgit : MYR
Mexican Peso : MXN
Norwegian Krone: NOK
Swedish Krona : SEK
South African Rand: ZAR
Singapore Dollar : SGD
Sri Lankan Rupee: LKR
Swiss Franc : CHF
New Taiwan Dollar : TWD
Thai Baht : THB
Australian Dollar : AUD
Euro : EUR
New Zealand Dollar : NZD
British Pound : GBP
Venezuelan Bolivar : VEF
________________________________________

To ___?
(sample input : SGD/CNY/JPY)
'''))
        output_code = output_code.upper()
        out_code = input_to_code(output_code)

        input_amount = float(input('\nHow much '+input_code+' would you like to exchange?\n'))
        input_date = str(input('''
Exchange date requested (sample input : 2019-1-1):
(kindly skip this portion if the date requested is today)
''' ))

        if input_date =='':
            url = 'https://api.exchangerate-api.com/v4/latest/USD'
            response = requests.get(url)
            result = response.json()
            get_dates = result.get('rates')
            in_currency = float(get_dates.get(input_code))
            out_currency = float(get_dates.get(output_code))
            input_date = ' today'

        else:
            end = input_to_date(input_date)
            df = data.get_data_fred([in_code,out_code],end,end)
            df = df.reset_index()
            check = df.loc[df['DATE']==input_date]
            if check.shape[0]==0 or check.isnull().values.any():
                print('Sorry. The rate on the date requested is unavailable.')
                continue
            else:
                in_currency = float(df.loc[df['DATE']== input_date][in_code])
                out_currency = float(df.loc[df['DATE']== input_date][out_code])
                input_date = ' on ' + input_date

        rate = 1/in_currency*out_currency
        rate = float("{0:.2f}".format(rate))
        out_amount = input_amount*rate
        out_amount = float("{0:.2f}".format(out_amount))

        print('''
------------------------|RESULT|------------------------
''')
        print(str(input_amount) + ' ' + input_code  + ' can be exchanged into ' +str(out_amount)+ ' '+output_code + input_date)
        print('The exchange rate is ' + str(rate))

        print('''
--------------------------------------------------------
''')

        flag = True

    next = next_request()

    return next

def mode_trend():
    input_code_num = str(input('''
Would you like to view
(1) Absolute trend for one currency
(2) Relative trend for two currencies

Sample input : 1 or 2
'''))
    if input_code_num == '2':
        input_code = str(input('''
________________________________________
Currently Supported and Respective Code:
Brazilian Real : BRL
Canadaian Dollar : CAD
Chinese Yuan : CNY
Denish Krone : DKK
Hong Kong Dollar : HKD
Indian Rupee : INR
Japanese Yen : JPY
South Korean Won : KRW
Malaysian Ringgit : MYR
Mexican Peso : MXN
Norwegian Krone: NOK
Swedish Krona : SEK
South African Rand: ZAR
Singapore Dollar : SGD
Sri Lankan Rupee: LKR
Swiss Franc : CHF
New Taiwan Dollar : TWD
Thai Baht : THB
Australian Dollar : AUD
Euro : EUR
New Zealand Dollar : NZD
British Pound : GBP
Venezuelan Bolivar : VEF
________________________________________
Please enter two currency codes, seperate them with comma:

Sample input : CNY,SGD
'''))
        input_code = input_code.upper()
        temp_code = input_code.split(',',2)

        input_start = str(input('please enter start date (eg. 2019-1-1):'))
        start = input_to_date(input_start)
        input_end = str(input('please enter end date (eg. 2019-1-1):'))
        end = input_to_date(input_end)

        real_code0 = input_to_code(temp_code[0])
        real_code1 = input_to_code(temp_code[1])
        df = data.get_data_fred([real_code0,real_code1],start,end)
        df['float0'] = [float(x) for x in df[real_code0]]
        df['float1'] = [float(x) for x in df[real_code1]]
        df['ratio'] = df['float0']/df['float1']
        df['ratio'].plot.line(figsize = (15,8))
        plt.show()

    else:
        input_code = str(input('''
________________________________________
Currently Supported and Respective Code:
Brazilian Real : BRL
Canadaian Dollar : CAD
Chinese Yuan : CNY
Denish Krone : DKK
Hong Kong Dollar : HKD
Indian Rupee : INR
Japanese Yen : JPY
South Korean Won : KRW
Malaysian Ringgit : MYR
Mexican Peso : MXN
Norwegian Krone: NOK
Swedish Krona : SEK
South African Rand: ZAR
Singapore Dollar : SGD
Sri Lankan Rupee: LKR
Swiss Franc : CHF
New Taiwan Dollar : TWD
Thai Baht : THB
Australian Dollar : AUD
Euro : EUR
New Zealand Dollar : NZD
British Pound : GBP
Venezuelan Bolivar : VEF
________________________________________

Please enter money code to view currency trend:
(sample input : SGD/CNY/JPY)
'''))

        input_code = input_code.upper()
        code = input_to_code(input_code)
        input_start = str(input('please enter start date (eg. 2019-1-1):'))
        start = input_to_date(input_start)
        input_end = str(input('please enter end date (eg. 2019-1-1):'))
        end = input_to_date(input_end)

        df = data.get_data_fred(code,start,end)
        name = input_code + ' Currency Trend'
        df = df.rename(columns={code:name})
        df.plot.line(figsize = (15,8))
        plt.show()

    next = next_request()
    return next

def input_to_date(input_date):

    temp = input_date.split('-',2)
    year = int(temp[0])
    month = int(temp[1])
    day = int(temp[2])
    date = datetime.datetime(year,month,day)

    return date

def input_to_code(input_code):

    code_dic = {'BRL':'DEXBZUS',
                'CAD':'DEXCAUS',
                'CNY':'DEXCHUS',
                'DKK':'DEXDNUS',
                'HKD':'DEXHKUS',
                'INR':'DEXINUS',
                'JPY':'DEXJPUS',
                'KRW':'DEXKOUS',
                'MYR':'DEXMAUS',
                'MXN':'DEXMXUS',
                'NOK':'DEXNOUS',
                'SEK':'DEXSDUS',
                'ZAR':'DEXSFUS',
                'SGD':'DEXSIUS',
                'LKR':'DEXSLUS',
                'CHF':'DEXSZUS',
                'TWD':'DEXTAUS',
                'THB':'DEXTHUS',
                'AUD':'DEXUSAL',
                'EUR':'DEXUSEU',
                'NZD':'DEXUSNZ',
                'GBP':'DEXUSUK',
                'VEF':'DEXVZUS'}

    input_cap = input_code.upper()
    code = code_dic[input_cap]

    return code

def next_request():

    next_word = '''
Would you like to
1. return to menu
2. exit program
(sample input : 1 or 2)
'''

    next = str(input(next_word))

    return next

main_menu()
