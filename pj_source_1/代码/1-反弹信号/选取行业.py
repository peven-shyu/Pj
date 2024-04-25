while True:
	v=(input('请输入要查询行业分组的信号日的序号\n\
		（例如，想要查询第二个信号日的行业分组，输入2）\n\
		（退出输入stop）：'))
	if v=='stop': break
	else:v=int(v)

	import pandas as pd
	import matplotlib.pyplot as plt

	code_list=['801010.SL',	'801030.SL',	'801040.SL',	'801050.SL',	'801080.SL',
	'801110.SL',	'801120.SL',	'801130.SL',	'801140.SL',	'801150.SL',
	'801160.SL',	'801170.SL',	'801180.SL',	'801200.SL',	'801210.SL',
	'801230.SL',	'801710.SL',	'801720.SL',	'801730.SL',	'801740.SL',
	'801750.SL',	'801760.SL',	'801770.SL',	'801780.SL',	'801790.SL',
	'801880.SL',	'801890.SL',	'801950.SL',	'801960.SL',	'801970.SL',
	'801980.SL']

	name_list=[
	'农林牧渔',	'基础化工',	'钢铁',	'有色金属',	'电子',	
	'家用电器' ,'食品饮料','纺织服饰',	'轻工制造',	'医药生物',	
	'公用事业' ,'交通运输',	'房地产',	'商贸零售',	'社会服务',	
	'综合'	,'建筑材料',	'建筑装饰',	'电力设备',	'国防军工',	
	'计算机', '传媒',	'通信'	,'银行',	'非银金融',	
	'汽车'	,'机械设备','煤炭','石油石化',	'环保',	
	'美容护理',
	]

	name_map={}
	for i in range(len(code_list)):
		name_map[code_list[i]]=name_list[i]

	data1 = pd.read_csv("hy.csv")#data1包含行业在大区间内每天的涨跌幅
	data1["Date"] = pd.to_datetime(data1["Date"])
	#data_og=data.copy()
	data2 = pd.read_csv("check.csv")#data2包含信号数据
	data2["Date"] = pd.to_datetime(data2["Date"])

	def calculate_avg(data):
		total = sum(data)   
		avg = total / len(data) 
		return avg
	#定义域为各信号日的日期的编号的序号，从序号t先映射到第t个信号日的日期的编号data2['index'][t]
	def momentum_Frame(t):
		chg20=[]
		s=[momentum_industry(h) for h in range(len(code_list))]
		def momentum_industry(j):
			for i in range(data2['index'][t]-20,data2['index'][t]):
				chg20.append(data1[code_list[j]][i])
			avg20=calculate_avg(chg20)
			mmt=data2['chg'][t]-avg20
			return(mmt)
		ss={'index':[i for i in range(len(s))],
		'industry':code_list,
		'name':name_list
		,'momentum':s}
		df=pd.DataFrame(ss)
		return(df)


	def sort(df):
		ser=df['momentum'].sort_values(ascending=True)
		fra=ser.to_frame()
		fra=fra.reset_index()
		return(fra)


	def group(dfe,k):
		name=[]
		industry=[]
		if k==1 or k==2 or k==3 or k== 4 :
			for i in range(1+k*6,7+k*6):
				name.append(dfe['name'][sort(dfe)['index'][i]])
				industry.append(dfe['industry'][sort(dfe)['index'][i]])
			ss={
			'industry':industry,
			'name':name}
			df=pd.DataFrame(ss)
			return(df)
		elif k==0: 
			for i in range(7):
				name.append(dfe['name'][sort(dfe)['index'][i]])
				industry.append(dfe['industry'][sort(dfe)['index'][i]])
			ss={#'index':[i for i in range(7)],
			'industry':industry,
			'name':name}
			df=pd.DataFrame(ss)
			return(df)
		else: return('wrong argument')
	a = momentum_Frame(v-1)
	print('第一组','\n',group(a,0),'\n','第二组','\n',group(a,1),'\n',\
	'第三组','\n',group(a,2),'\n','第四组','\n',group(a,3),'\n','第五组','\n',group(a,4))



