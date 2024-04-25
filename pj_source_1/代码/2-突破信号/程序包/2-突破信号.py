import pandas as pd

data1=pd.read_csv('2-sheet1.csv')
data1['Date']=pd.to_datetime(data1['Date'])
data_1=data1.copy()
data_2=data1.copy()
data_2.set_index('Date', inplace=True)

#筛选出当日涨跌幅大于1的日期
filtered_data=data1[data1['Change']>1]

class TimeSeriesAnalyzer:
    def __init__(self, data):
        self.data = data

    def filter_dates(self):
        filtered_dates = []
        for i in range(5, len(self.data)):
            window = self.data[i-5:i]
            if all(-1 <= val <= 1 for val in window['Change']):
                filtered_dates.append(self.data.iloc[i]['Date'])
        return filtered_dates

# 创建 TimeSeriesAnalyzer 的实例，并传入 DataFrame df
analyzer = TimeSeriesAnalyzer(data1)

# 筛选满足条件的日期
filtered_dates = analyzer.filter_dates()
filtered_dates=pd.DataFrame({'Date':filtered_dates})

common_dates = list(set(filtered_dates['Date']) & set(filtered_data['Date']))

#处理数据类型
def to_float(col):
	col = col.str.replace(',', '')
	col = col.astype(float)
	return(col)

low = to_float(data1['Low'])
high= to_float(data1['High'])
close= to_float(data1['Close'])

(data_1['Low'])=low 
(data_1['High'])=high
(data_1['Close'])=close

data_1['rolling_max'] = (data_1['High']).rolling(window=5).max()
data_1['rolling_min'] = (data_1['Close']).rolling(window=5).min()

#收缩函数，将datafrmae映射到满足‘通道收缩’条件的日期的列表
def shrink(data):
	l=[]
	for i in range(7,len(data)):
		#if (data['rolling_min'][i-2]>=data['rolling_min'][i-3]) and(data['rolling_max'][i-2]<=data['rolling_max'][i-3]) and((data['rolling_min'][i-2]>data['rolling_min'][i-3]) or(data['rolling_max'][i-2]<data['rolling_max'][i-3])):
		if (data['rolling_max'][i-2]-data['rolling_min'][i-2])>(data['rolling_max'][i-1]-data['rolling_min'][i-1]) :
			l.append(data['Date'][i])
	return(l)

#得到排序好的日期列表
dates=list(set(common_dates) & set(shrink(data_1)))
sorted_dates = sorted(dates, reverse=False)


#输出检查文件
Dates=pd.DataFrame({'Date':sorted_dates})
def shifting(i):
	a=data_2.copy()
	a=a.shift(i)
	return a['Change'][sorted_dates]
Check={
'Date':sorted_dates,\
'Change':shifting(0),\
'1_day_before':shifting(1),\
'2_day_before':shifting(2),\
'3_day_before':shifting(3),\
'4_day_before':shifting(4),\
'5_day_before':shifting(5)
}
print(Check)
pd.DataFrame(Check).to_csv('check.csv',index=False)


