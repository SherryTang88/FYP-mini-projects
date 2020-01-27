import pandas_datareader.data as data
import mpl_finance as mpf
import matplotlib.pyplot as plt
import datetime
import numpy as np

def input_to_date(input_date):

    temp = input_date.split('-',2)
    year = int(temp[0])
    month = int(temp[1])
    day = int(temp[2])
    date = datetime.datetime(year,month,day)

    return date

code = str(input('Please input the code of the stock requested:\n'))
input_start = str(input('please enter start date (eg. 2019-1-1):'))
start = input_to_date(input_start)
input_end = str(input('please enter end date (eg. 2019-1-1):'))
end = input_to_date(input_end)
ave = str(input('Would you like to view n-days average? (input Y/N):'))
if ave=='Y' or ave=='y':
    freq = int(input('Please input n, while n is the n-days average:\n'))

df = data.DataReader(code,'yahoo',start , end)
df['average'] = df.Close.rolling(window=freq).mean()

fig = plt.figure(figsize=(8, 6), dpi=100, facecolor="white")
fig.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)
ave_line = fig.add_subplot(1, 1, 1)
mpf.candlestick2_ochl(ave_line, df.Open, df.Close, df.High, df.Low, width=0.5,
                      colorup='r', colordown='g')

ave_line.plot(np.arange(0, len(df.index)), df['average'], 'black', label= 'M'+str(ave), lw=1.0)

ave_line.set_title(code)
ave_line.set_xlabel("date")
ave_line.set_ylabel(u"price")
#ave_line.set_xlim(0, len(df.index))
ave_line.set_xticks(range(0, len(df.index), 10))
ave_line.set_xticklabels([df.index.strftime('%Y-%m-%d')[index] for index in ave_line.get_xticks()])

for label in ave_line.xaxis.get_ticklabels():
    label.set_rotation(30)

plt.show()


#fig2 = fig.add_subplot(2,1,2)
#fig2.set_size_inches(20,5)
#df_stockload['Volume'].plot(kind = 'bar')
#plt.show()
