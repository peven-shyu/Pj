import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import openpyxl


# 读取数据并进行必要的数据处理
data = pd.read_csv('zzqz.csv')
data['Date'] = pd.to_datetime(data['Date'])
data['Value2'] = data['Value2']
data_copy = data.copy()
dates=pd.read_csv('check.csv')
dates['Date']=pd.to_datetime(dates['Date'])

# 创建图表
plt.rcParams['font.family'] = 'SimHei' 
fig, ax = plt.subplots(figsize=(10, 6))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%y/%m.%d'))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=260))
#plt.xticks(rotation=45)
ax.set_yticks(range(0, 10001, 1000))
ax.set_ylim(0, 10000)
# 绘制曲线
ax.plot(data['Date'], data['Value2'], label='中证全指')

# 信号日
signal_dates = dates['Date'] # 保证 datatime类型
data_copy.set_index('Date', inplace=True)

for signal_date in signal_dates[0:1]:
    ax.axvline(signal_date,0,data_copy['Value2'][signal_date]/10000, c='r', linewidth=0.3, label='信号日')
for signal_date in signal_dates[1:]:
    ax.axvline(signal_date,0,data_copy['Value2'][signal_date]/10000, c='r', linewidth=0.3)

# 添加水平虚线
for y_value in range(1000, 10001, 1000):
    ax.axhline(y=y_value, linestyle='dashed', color='gray', alpha=0.2)

# 添加图例、坐标轴标签等   
ax.legend(fontsize=16,loc=2)
ax.set_title('高位切换信号分布', fontsize=23)


# 显示图表
ax = plt.gca()  
ax.spines['bottom'].set_color('grey')  
ax.spines['top'].set_color('none')  
ax.spines['right'].set_color('none')  
ax.spines['left'].set_color('none')   
plt.show()