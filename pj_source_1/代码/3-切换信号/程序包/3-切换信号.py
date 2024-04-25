import pandas as pd


#数据读取处理
def file_trans(file_name):
	data = pd.read_csv(file_name)
	data['Date'] = pd.to_datetime(data['Date'])
	return data
data1 = file_trans("ATR.csv")
data2 = file_trans('hyzs_new.csv')
data2.set_index('Date', inplace=True)
data3 = file_trans("zzqz.csv")


code_list=['801010.SL',	'801030.SL',	'801040.SL',	'801050.SL',	'801080.SL',
	'801110.SL',	'801120.SL',	'801130.SL',	'801140.SL',	'801150.SL',
	'801160.SL',	'801170.SL',	'801180.SL',	'801200.SL',	'801210.SL',
	'801230.SL',	'801710.SL',	'801720.SL',	'801730.SL',	'801740.SL',
	'801750.SL',	'801760.SL',	'801770.SL',	'801780.SL',	'801790.SL',
	'801880.SL',	'801890.SL',	'801950.SL',	'801960.SL',	'801970.SL',
	'801980.SL']

#定义ATR函数
def to_float(col):
	col = col.str.replace(',', '')
	col = col.astype(float)
	return(col)

low = to_float(data1['Low'])
high= to_float(data1['High'])
close= to_float(data1['Close'])

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


#已得到ATR函数（中证全指），该函数将日期的编号映射到前60日的平均真实波幅
def ATR_multiply_100(x):
	a=ATR(x)*100
	return a


#定义处理日期加减的函数
def date_minus(d1,days):
	d3 = d1 - datetime.timedelta(days)
	return d3
def date_add(d1,days):
	d3 = d1 + datetime.timedelta(days)
	return d3


#得到中证全指当日跌幅超过ATR60的日期
ATR60_col=data3['Index'].apply(ATR_multiply_100)
data3['ATR_col']=ATR60_col
filtered_data=data3[data3['Value1']<0]
data3_copy=data3.copy()
data3_copy.set_index('Date', inplace=True)
filtered_data = filtered_data.copy()
filtered_data['distance'] = filtered_data['Value1'] + filtered_data['ATR_col']
filtered_data=filtered_data[filtered_data['distance']<0]


# 使用rolling函数获取前250天的最大值
rolling_max = data2.rolling(window=245).max()
result_df = data2 == rolling_max
row_sum = result_df.sum(axis=1)

#print(row_sum)

# 将日期列转换为datetime64类型的日期索引
row_sum.index = pd.to_datetime(row_sum.index)

# 获取信号日期列表
previous_day_data = row_sum.shift(1)
greater_dates = row_sum.index[row_sum < previous_day_data-2]
A=greater_dates.copy()
B=filtered_data.copy()
common_data = list(set(A) & set(B['Date']))
sorted_dates = sorted(common_data, reverse=False)


# 显示结果，输出文件
a=row_sum.copy()
a=a.shift(1)
Check=pd.DataFrame({'Date':sorted_dates,\
	'industry_hits_newhigh':row_sum[sorted_dates],\
	'former_newhigh':a[sorted_dates],\
	'change':data3_copy['Value1'][sorted_dates],\
	'ATR60':data3_copy['ATR_col'][sorted_dates]})
print(Check)
#Check.to_csv('check.csv',index=False)







