import pandas as pd

data1 = pd.read_csv("ATR.csv")

data1["Date"] = pd.to_datetime(data1["Date"])

#print(data)
#转换为浮点类型
def to_string(col):
	col = col.str.replace(',', '')
	col = col.astype(float)
	return(col)

low = to_string(data1['Low'])
high= to_string(data1['High'])
close= to_string(data1['Close'])

def TR(T):
	E= max(high[T]-low[T],abs(high[T]-close[T-1]),abs(close[T-1]-low[T]))/close[T-1]
	return(E)

def ATR(T):
	def calculate_avg(data):
		total = sum(data)   
		avg = total / len(data) 
		return avg
	tr60=[]
	for i in range(T-60,T):
		tr60.append(TR(i))
	E= calculate_avg(tr60)
	return(E)
#print(ATR(89))


