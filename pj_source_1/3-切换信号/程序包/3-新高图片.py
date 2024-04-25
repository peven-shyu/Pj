import pandas as pd
import datetime


def file_trans(file_name):
    data = pd.read_csv(file_name)
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)
    return data
data2 = file_trans('hyzs_new.csv')

rolling_max = data2.rolling(window=250).max()
result_df = data2 == rolling_max
row_sum = result_df.sum(axis=1)
'''
放到row_sum后运行

'''
#1. 导入所需的库：


import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import openpyxl

#3. 创建图表，并设置日期格式：
plt.rcParams['font.family'] = 'SimHei' 
fig, ax = plt.subplots()  # 创建图表和轴
ax.xaxis.set_major_formatter(mdates.DateFormatter('%y/%m.%d')) 
ax.xaxis.set_major_locator(mdates.DayLocator(interval=260))  
ax.set_yticks([0,4,8,12,16,20,24,28])
plt.bar(row_sum.index, row_sum.values,label='新高行业数量')


#6. 添加图例、坐标轴标签等：

ax.legend(fontsize=15,loc=2)  # 添加图例

ax.set_title('创52周新高行业数量形势',fontsize=23)  # 设置图表标题

for y_value in range(4, 29, 4):
    ax.axhline(y=y_value, linestyle='dashed', color='gray', alpha=0.2)
#7. 显示图表：
ax = plt.gca()  
ax.spines['bottom'].set_color('grey')  
ax.spines['top'].set_color('none')  
ax.spines['right'].set_color('none')  
ax.spines['left'].set_color('none')   
plt.show()