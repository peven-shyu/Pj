import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import openpyxl
import matplotlib as mpl

data0=pd.read_csv('check.csv')
data0['Date'] = pd.to_datetime(data0['Date'])

# 提取每一年的年份
data0['Year'] = data0['Date'].dt.year

# 统计每一年的时间数量
year_counts = data0['Year'].value_counts().sort_index()

l_1=[i for i in range(2013,2024)]
def function(t):
	if t not in year_counts.index:
		return 0
	else: return year_counts[t]
l_2=[function(i) for i in range(2013,2024)]

year_count=dict(zip(l_1,l_2))
year_count=pd.Series(year_count)

#绘制
plt.rcParams['font.family'] = 'SimHei' 
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_yticks(range(0, 8, 1))
year_count.plot(kind='bar')


# 添加标题和标签
plt.title('信号数量分布',fontsize=23)


# 添加水平虚线
for y_value in range(0,8,1):
	ax.axhline(y=y_value, linestyle='dashed', color='gray', alpha=0.2)

ax.set_xticklabels(ax.get_xticklabels(), rotation=0,fontsize=36)
ax.set_yticklabels(ax.get_yticklabels(), rotation=0,fontsize=32)


# 显示图表
ax = plt.gca()  
ax.spines['bottom'].set_color('none') 
ax.spines['top'].set_color('none')  
ax.spines['right'].set_color('none')  
ax.spines['left'].set_color('none')  
plt.show()