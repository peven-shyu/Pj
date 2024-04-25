import pandas as pd

code_list=[
'801010.SL',	'801030.SL',	'801040.SL',	'801050.SL',	'801080.SL',
'801110.SL',	'801120.SL',	'801130.SL',	'801140.SL',	'801150.SL',
'801160.SL',	'801170.SL',	'801180.SL',	'801200.SL',	'801210.SL',
'801230.SL',	'801710.SL',	'801720.SL',	'801730.SL',	'801740.SL',
'801750.SL',	'801760.SL',	'801770.SL',	'801780.SL',	'801790.SL',
'801880.SL',	'801890.SL',	'801950.SL',	'801960.SL',	'801970.SL',
'801980.SL'
]


data1 = pd.read_csv("hy.csv",parse_dates=['Date'])
#data1包含行业在大区间内每天的涨跌幅
#data_og=data.copy()
data2 = pd.read_csv("check.csv",parse_dates=['Date'])#data2包含信号数据


def calculate_avg(data):
	total = sum(data)   
	avg = total / len(data) 
	return avg
#定义域为各信号日的日期的编号的序号，从序号t先映射到第t个信号日的日期的编号data2['index'][t]
def momentum_Frame(t):
	chg20=[]
	s=[]
	def momentum_industry(j):
		for i in range(data2['index'][t]-20,data2['index'][t]):
			chg20.append(data1[code_list[j]][i])
		avg20=calculate_avg(chg20)
		mmt=data1[code_list[j]][data2['index'][t]]-avg20
		return(mmt)
	for h in range(len(code_list)):
		s.append(momentum_industry(h))
	ss={'index':[i for i in range(len(s))],
	'industry':code_list,
	#'name':name_list,
	'momentum':s}
	df=pd.DataFrame(ss)
	return(df)


def sort(df):
	ser=df['momentum'].sort_values(ascending=True)
	fra=ser.to_frame()
	fra=fra.reset_index()
	return(fra)


def group(dfe,k):
	#name=[]
	industry=[]
	
	if k==1 or k==2 or k==3 or k== 4 :
		for i in range(1+k*6,7+k*6):
			#name.append(dfe['name'][sort(dfe)['index'][i]])
			industry.append(dfe['industry'][sort(dfe)['index'][i]])
		return(industry)
	
	elif k==0: 
		for i in range(7):
			#name.append(dfe['name'][sort(dfe)['index'][i]])
			industry.append(dfe['industry'][sort(dfe)['index'][i]])
		return(industry)

	else: return('wrong argument')

num_list=['i' for i in range(len(data2))]
result_list=[list(group(momentum_Frame(i),4)) for i in range(len(data2))]
industry_result_every_signal=pd.DataFrame(dict(zip(num_list, result_list)))


data_hyzs = pd.read_csv("hyzs.csv", parse_dates=["Date"])
data_zzqz =pd.read_csv('zzqz.csv', parse_dates=['Date'])
def profit(i):
	num=0
	
	for j in range(6):
		a1=data_hyzs[industry_result_every_signal['i'][j]][data2['index'][i]+19]
		a2=data_hyzs[industry_result_every_signal['i'][j]][data2['index'][i]]
		a3=data_zzqz['Value2'][data2['index'][i]+19]
		a4=data_zzqz['Value2'][data2['index'][i]]
		a=(float(a1)-float(a2))/float(a2)-(float(a3)-float(a4))/float(a4)
		num=num+a
	return(num/6)
	
print(calculate_avg([profit(i) for i in range(len(data2))]))
profit_=pd.DataFrame({'pro_rate':[profit(i) for i in range(len(data2))]})
win=profit_[profit_['pro_rate']>0]
print(len(win)/len(data2))











