import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import openpyxl
import numpy as np

data = pd.read_csv("zzqz.csv")
data["Date"] = pd.to_datetime(data["Date"])
data1 = pd.read_csv("ATR.csv")
data1["Date"] = pd.to_datetime(data1["Date"])

#定义ATR函数

def to_string(col):
    col = col.str.replace(',', '')
    col = col.astype(float)
    return(col)

low = to_string(data1['Low'])
high= to_string(data1['High'])
close= to_string(data1['Close'])

def TR(T):
    if T>0:
        E= max(high[T]-low[T],abs(high[T]-close[T-1]),abs(close[T-1]-low[T]))/close[T-1]
    else: E=0.012#第一天的真实波幅需要额外设定
    return(E)

def ATR(T):
    def calculate_avg(data):
            total = sum(data)   
            avg = total / len(data) 
            return avg
    if T>60:
        tr60=[]
        for i in range(T-60,T):
            tr60.append(TR(i))
        E= calculate_avg(tr60)
    elif T>0: E= calculate_avg([TR(i) for i in range(T)])
    else: E= 0.012
    return(E)
#print(ATR(500))


#已得到ATR函数，其将日期的编号映射到前60日的平均真实波幅


#接下来利用ATR，进行数据修正

# 1.得到‘每日的ATR’
ATR_data = data['Index'].apply(ATR)
# 读取数据并进行必要的数据处理

data_copy = data.copy()


# 创建图表
plt.rcParams['font.family'] = 'SimHei' 
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.set_yticks(range(0, 10001, 1000))
ax1.set_ylim(0, 10000)
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%y/%m.%d'))
ax1.xaxis.set_major_locator(mdates.DayLocator(interval=260))
ax1.plot(data['Date'], data['Value2'],label='中证全指')

ax1.set_title("ATR60与中证全指",fontsize=24)
ax2 = ax1.twinx() # this is the important function
ax2.set_yticks([0,0.01,0.02,0.03,0.04,0.05,0.06,0.065])
ax2.set_ylim(0, 0.065)
ax2.plot(data['Date'], ATR_data, c='r', alpha=0.6,label='ATR60')

for y_value in range(1000, 10001, 1000):
    ax1.axhline(y=y_value, linestyle='dashed', color='gray', alpha=0.2)
for y_value in [0.01,0.02]:
    ax2.axhline(y=y_value, linestyle='dashed', color='orange')
# 添加图例、坐标轴标签等 
ax1.spines['bottom'].set_color('grey')  
ax1.spines['top'].set_color('none')  
ax1.spines['right'].set_color('none')  
ax1.spines['left'].set_color('none')   
ax2.spines['bottom'].set_color('grey')  
ax2.spines['top'].set_color('none')  
ax2.spines['right'].set_color('grey')  
ax2.spines['left'].set_color('none')  
ax1.legend(fontsize=16,loc=2)
ax2.legend(fontsize=16,loc='best')
#ax2.set_xlim([0, np.e])
  

plt.show()