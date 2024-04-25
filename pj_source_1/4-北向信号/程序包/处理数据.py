import pandas as pd


data1=pd.read_csv('3-.csv',low_memory=False)
data1['Date']=pd.to_datetime(data1['Date'])


valid_index=[]
for i in range(len(data1)):
	if data1['North'][i] != 0 :
		valid_index.append(i)
data_tm=pd.DataFrame({'Date':[data1['Date'][i] for i in valid_index],\
	'North':[data1['North'][i] for i in valid_index]})
data_tm.to_csv('north.csv',index=False)
