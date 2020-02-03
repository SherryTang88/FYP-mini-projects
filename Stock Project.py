import pandas_datareader.data as data
import mpl_finance as mpf
import matplotlib.pyplot as plt
import datetime
import numpy as np
import matplotlib.dates as mdates


#可以出现的数据类型：high,low,open,close,adj close,MA,candle,volume is seperate

def user_input():
    next = '1'
    word = '''
Welcome to Stock Master!

Please select a function to continue:

(1) Search for a stock code by keyword
(2) View stock trend by code

(sample input 1 or 2)
'''
    while next == '1':

        function = str(input(word))

        if function == '1':
            next = check_code()

        else:
            next = view_trend()

def check_code():
    input_keyword = input('Please input keyword for the stock searching for:')
    all_ticker = data.get_nasdaq_symbols(retry_count=3, timeout=30, pause=None)
    all_ticker = all_ticker.drop(columns = ['Nasdaq Traded', 'Listing Exchange',
        'Market Category', 'ETF', 'Round Lot Size', 'Test Issue',
        'Financial Status', 'CQS Symbol', 'NASDAQ Symbol', 'NextShares'])

    name_list = all_ticker['Security Name'].values.tolist()
    name_list = [x.lower() for x in name_list]

    l= []
    num = 0

    for item in name_list:
        if input_keyword in item:
            l.insert(num,item)
            num = num + 1

    all_ticker = all_ticker.reset_index()
    all_ticker = all_ticker.set_index('Security Name')
    code_dic = all_ticker.to_dict()
    new_dic = code_dic.get('Symbol')
    new_dic = {k.lower(): v for k, v in new_dic.items()}

    print('\nBelow are code for security name containing: '+ input_keyword +'\n')

    for item in l:
        p = str(item) + ' ---- ' + str(new_dic.get(item))
        print(p)

    next = next_request()
    return next


def view_trend():

    code = str(input('Please input the code of the stock requested:\n'))
    input_start = str(input('please enter start date (eg. 2019-1-1):'))
    start = input_to_date(input_start)
    input_end = str(input('please enter end date (eg. 2019-1-1):'))
    end = input_to_date(input_end)

    df = data.DataReader(code,'yahoo',start,end)
    df = df.reset_index()
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
    graph_choice = str(input('''
Please select type of graph.
(1) Candle Stick
(2) High
(3) Low
(4) Open
(5) Close
(6) Adj Close
(7) Moving Average
(8) Volume

You may select mutiple choices, seperate each choice by comma.

Sample input for candle stick + High + Volume:
1,2,8

'''))
    choice_list = graph_choice.split(',')

    choice_dic = {'2':'High',
                '3':'Low',
                '4':'Open',
                '5':'Close',
                '6':'Adj Close',
                '7':'MA'}

    freq = (len(df['Date']))//20

    if '8' in choice_list:
        choice_list.remove('8')


        if len(choice_list) != 0:

            ax2 = plt.subplot2grid((8,1),(6,0),rowspan = 3,colspan =1)
            ax2.set_xticks(range(0, len(df['Date']), freq))
            ax2.set_xticklabels(df['Date'][::freq], rotation=35, fontsize = 'x-small')
            ax2.bar(df['Date'], df['Volume'])
            ax2.legend(loc='best')

            ax1 = plt.subplot2grid((8,1),(0,0),rowspan = 5,colspan =1)
            ax1.legend(loc='best')
            ax1.set_xticks(range(0, len(df['Date']), freq))
            ax1.set_xticklabels(df['Date'][::freq], rotation=35,fontsize = 'x-small')

            if '1' in choice_list:
                mpf.candlestick2_ochl(ax1, df.Open, df.Close, df.High, df.Low, width=0.5,
                                  colorup='r', colordown='g')
                choice_list.remove('1')

            if '7' in choice_list:
                ma = int(input('''

Please input the frequency for the moving average.

Sample input for 100 days moving average:
100
'''))
                df['average'] = df.Close.rolling(window=ma).mean()
                ax1.plot(np.arange(0, len(df['Date'])), df['average'],label= 'M'+str(ma), lw=1.0)
                choice_list.remove('7')

            for item in choice_list:
                ax1.plot(np.arange(0, len(df['Date'])), df[choice_dic.get(item)],label = choice_dic.get(item),lw=1.0)
                #ax1.set_xlim(0, len(df['Date']))
                #ax1.set_xticklabels(df['Date'])

            ax1.legend(loc='best')
            plt.show()

        else:
            ax2 = plt.subplot2grid((1,1),(0,0),rowspan = 1,colspan =1)
            ax2.set_xticks(range(0, len(df['Date']), freq))
            ax2.set_xticklabels(df['Date'][::freq], rotation=35, fontsize = 'x-small')
            ax2.bar(df['Date'], df['Volume'])
            ax2.legend(loc='best')
            plt.show()

    else:
        ax1 = plt.subplot2grid((1,1),(0,0),rowspan = 1,colspan =1)
        ax1.set_xticks(range(0, len(df['Date']), freq))
        ax1.set_xticklabels(df['Date'][::freq], rotation=35,fontsize = 'x-small')

        if '1' in choice_list:
            mpf.candlestick2_ochl(ax1, df.Open, df.Close, df.High, df.Low, width=0.5,
                                          colorup='r', colordown='g')
            choice_list.remove('1')

        if '7' in choice_list:
            ma = int(input('''

Please input the frequency for the moving average.

Sample input for 100 days moving average:
100
'''))
            df['average'] = df.Close.rolling(window=ma).mean()
            ax1.plot(np.arange(0, len(df['Date'])), df['average'],label= 'M'+str(ma), lw=1.0)
            choice_list.remove('7')

        for item in choice_list:
            ax1.plot(np.arange(0, len(df['Date'])), df[choice_dic.get(item)],label = choice_dic.get(item),lw=1.0)

        ax1.legend(loc='best')
        plt.show()

    next = next_request()
    return next

def next_request():

    next_word = '''
Would you like to
1. return to menu
2. exit program
(sample input : 1 or 2)
'''

    next = str(input(next_word))

    return next

def plot_others(choice_list,df,choice_dic):
    ax1 = plt.subplot2grid((6,1),(0,0),rowspan = 6,colspan =1)
    if '1' in choice_list:
        mpf.candlestick2_ochl(ax1, df.Open, df.Close, df.High, df.Low, width=0.5,
                      colorup='r', colordown='g')
        choice_list.remove('1')

    if '7' in choice_list:
        ma = int(input('''

Please input the frequency for the moving average.

Sample input for 100 days moving average:
100

'''))
        df['average'] = df.Close.rolling(window=ma).mean()
        ax1.plot(np.arange(0, len(df.index)), df['average'],label= 'M'+str(ma), lw=1.0)
        #ax1.plot(df.index, df['average'])
        choice_list.remove('7')

    for item in choice_list:
        ax1.plot(np.arange(0, len(df.index)), df[choice_dic.get(item)],label = choice_dic.get(item),lw=1.0)
        #ax1.plot(df.index, df[choice_dic.get(item)])
        ax1.set_xlim(0, len(df.index))
        ax1.set_xticklabels(df.index)
    plt.show()


def input_to_date(input_date):

    temp = input_date.split('-',2)
    year = int(temp[0])
    month = int(temp[1])
    day = int(temp[2])
    date = datetime.datetime(year,month,day)

    return date

user_input()
