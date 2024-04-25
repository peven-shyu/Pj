import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import openpyxl
import pandas as pd


data1=pd.read_csv('north.csv')
data1['Date']=pd.to_datetime(data1['Date'])
data_1=data1.copy()

def A120(T):
    def calculate_avg(data):
            total = sum(data)   
            avg = total / len(data) 
            return avg
    if T>120:
        tr120=[]
        for i in range(T-120,T):
            tr120.append(data1['North'][i])
        E= calculate_avg(tr120)
    elif T>0: E= calculate_avg([data1['North'][i] for i in range(T)])
    else: E= 0
    return(E)
def std120(T):
    if T>120:
        tr120=[]
        for i in range(T-120,T):
            tr120.append(data1['North'][i])
        E= pd.Series(tr120).var()
    elif T>0: E= pd.Series([data1['North'][i] for i in range(T)]).var()
    else: E= 0
    return(E**(1/2))

A120_data = pd.Series([i for i in range(len(data1))]).apply(A120)
Std120_data=pd.Series([i for i in range(len(data1))]).apply(std120)
data_1['A120']=A120_data
data_1['Value']=A120_data+Std120_data+Std120_data

plt.rcParams['font.family'] = 'SimHei' 
plt.rcParams['axes.unicode_minus'] = False
fig, ax = plt.subplots()  # 创建图表和轴
ax.xaxis.set_major_formatter(mdates.DateFormatter('%y/%m.%d')) 
ax.xaxis.set_major_locator(mdates.DayLocator(interval=130))  
ax.tick_params(axis='y', which='major', labelsize=12)
ax.set_yticks(list(range(-200,251,50)))
plt.bar(data1['Date'], data1['North'].values,label='北向资金净买入')

ax.plot(data_1['Date'], data_1['Value'], color='red',linewidth=2,alpha=0.5,label='120日均值+2倍标准差')

ax.legend(fontsize=15,loc=2)  # 添加图例

ax.set_title('北向资金',fontsize=23)  # 设置图表标题

for y_value in range(-200, 251, 50):
    ax.axhline(y=y_value, linestyle='dashed', color='gray', alpha=0.2)
#7. 显示图表：
ax = plt.gca()  
ax.spines['bottom'].set_color('grey')  
ax.spines['top'].set_color('none')  
ax.spines['right'].set_color('none')  
ax.spines['left'].set_color('none')   
plt.show()