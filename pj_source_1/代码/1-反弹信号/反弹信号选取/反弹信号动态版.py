import pandas as pd
#阈值输入
input_str = input("请输入“反弹幅度阈值”与“下跌幅度阈值”（英文逗号分隔）：")
value1, value2 = input_str.split(",")
value1=float(value1)
value2=float(value2)

data = pd.read_csv("zzqz.csv")
data["Date"] = pd.to_datetime(data["Date"])
data_og=data.copy()
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
#2.选出ATR值过小/大的日期的编号
data_steady = ATR_data[(ATR_data <= 0.01)].to_frame()
data_jumpy= ATR_data[(ATR_data >= 0.02)].to_frame()
#3.优化所获取数据格式
def index_trans(df):
	df=df.reset_index()
	df.rename(columns={'Index': 'ATR'}, inplace=True)
	return(df)

data_steady= index_trans(data_steady)
data_jumpy= index_trans(data_jumpy)
#print()输出以查看
#4.定义修正函数
def trans1(t):
	a=data['Value1'][t]
	a=a/(1+((ATR(t)/0.01)-1)*(1/2))
	return a
def trans2(t):
	a=data['Value1'][t]
	a=a/(1+((ATR(t)/0.02)-1)*(1/2))
	return a
#5.得到修正后的涨跌幅序列
modified_steady= data_steady['index'].apply(trans1)
modified_jumpy= data_jumpy['index'].apply(trans2)

data_steady = data_steady.join(modified_steady,lsuffix='_', rsuffix='_ _')
data_steady.columns=['index','ATR','modified_chg']
data_jumpy = data_jumpy.join(modified_jumpy,lsuffix='_', rsuffix='_ _')
data_jumpy.columns=['index','ATR','modified_chg']
#data_steady.to_csv('steady.csv', index=False)
#data_jumpy.to_csv('jumpy.csv', index=False)
#6.将数据整合，得到完整的已修正的涨跌幅序列
chg=data['Value1'].to_frame()
for i in range(len(data_steady['index'])):
	chg.at[data_steady['index'][i],'Value1']=data_steady['modified_chg'][i]
for i in range(len(data_jumpy['index'])):
	chg.at[data_jumpy['index'][i],'Value1']=data_jumpy['modified_chg'][i]
#chg.to_csv('chg.csv',index=False)
data['Value1']=chg['Value1']
#data.to_csv('data_ATR60_modified.csv',index=False)


#data即为已得到的修正数据


filtered_data = data[data["Value1"] > value1]["Date"] #涨跌幅阈值

filtered_data = filtered_data.reset_index()
filtered_data = filtered_data.reset_index()

lis=[]
lis_=[]
i=0
Max=0
Min=0
data['Value2'] = data['Value2'].str.replace(',', '')

data['Value2'] = data['Value2'].astype(float)
while i<len(filtered_data['level_0'])-1:
	Max=data['Value2'][filtered_data['index'][i]:filtered_data['index'][i+1]].max()
	Min=data['Value2'][filtered_data['index'][i]:filtered_data['index'][i+1]].min()
	idMax=data['Value2'][filtered_data['index'][i]:filtered_data['index'][i+1]].idxmax()
	idMin =data['Value2'][filtered_data['index'][i]:filtered_data['index'][i+1]].idxmin()

	if (1-Min/Max)>value2 and idMax<idMin-1:      #下降幅度阈值              
		lis.append(filtered_data['index'][i+1])
		lis_.append(1-Min/Max)
	i=i+1
#lis为信号日日期对应的编号

df={'index': lis,'ATR':[ATR(i) for i in lis],'Date':[data['Date'][i] for i in lis],\
'modified_chg':[data['Value1'][i] for i in lis],'chg':[data_og['Value1'][i] for i in lis],'period_flunc':lis_}
'''index为编号，
  ATR列为当日对应的ATR60值，
  Date列为日期，
  modified_chg为修正后的涨跌幅，！要大于阈值
  chg为原始涨跌幅
  period_flunc为阶段内的跌幅，！要大于阈值
'''
check=pd.DataFrame(df)
#check.to_csv('check.csv',index=False)
print('信号日期为：','\n',check['Date'])








