import pandas as pd


data1=pd.read_csv('north.csv')
data1['Date']=pd.to_datetime(data1['Date'])
data_1=data1.copy()
data2 = pd.read_csv('zzqz.csv')
data2["Date"] = pd.to_datetime(data2['Date'])


date_Change_more_than_1=set(data2[data2['Value1']>1.3]['Date'])


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

date_North_larger_than_Value=data_1[data_1['North']>data_1['Value']]['Date']


dates=list(set(date_North_larger_than_Value) & date_Change_more_than_1)
sorted_dates = sorted(dates, reverse=False)
Dates=pd.DataFrame({'Date':sorted_dates})
a1=data_1.copy()
a1.set_index('Date', inplace=True)
a2=data2.copy()
a2.set_index('Date', inplace=True)
Check=pd.DataFrame({'Date':sorted_dates,\
	'North':a1['North'][sorted_dates],\
	'Value':a1['Value'][sorted_dates],\
	'Change':a2['Value1'][sorted_dates]})
#输出检查文件
Check.to_csv('check.csv',index=False)

