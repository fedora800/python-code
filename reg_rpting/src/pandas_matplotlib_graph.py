'''
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from time import sleep


chart_data=pd.read_csv('C:\mytmp\grafana_stats\im_internal_queue_latency_20191114_TEST.csv', index_col='Date')

print(chart_data)
chart_data.plot(kind='bar')
plt.legend()


ts = pd.Series(np.random.randn(1000),index=pd.date_range('1/1/2000', periods=1000))
print(ts)
ts = ts.cumsum()
ts.plot.bar()



from pandas import DataFrame

import matplotlib.pyplot as mplot
mplot.switch_backend("TkAgg")

   
Data = {'Unemployment_Rate': [6.1,5.8,5.7,5.7,5.8,5.6,5.5,5.3,5.2,5.2],
        'Stock_Index_Price': [1500,1520,1525,1523,1515,1540,1545,1560,1555,1565]
       }
  
df = DataFrame(Data,columns=['Unemployment_Rate','Stock_Index_Price'])
print (df)

df.plot(x ='Unemployment_Rate', y='Stock_Index_Price', kind = 'scatter')    


from pandas import DataFrame
   
Data = {'Unemployment_Rate': [6.1,5.8,5.7,5.7,5.8,5.6,5.5,5.3,5.2,5.2],
        'Stock_Index_Price': [1500,1520,1525,1523,1515,1540,1545,1560,1555,1565]
       }
  
df = DataFrame(Data,columns=['Unemployment_Rate','Stock_Index_Price'])
df.plot(x ='Unemployment_Rate', y='Stock_Index_Price', kind = 'scatter')


import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame({
    'name':[
        'john','lisa','peter','carl','linda','betty'
    ],
    'date_of_birth':[
        '01/21/1988','03/10/1977','07/25/1999','01/22/1977','09/30/1968','09/15/1970'
    ]
})

df['date_of_birth'] = pd.to_datetime(df['date_of_birth'],infer_datetime_format=True)

plt.clf()
df['date_of_birth'].map(lambda d: d.month).plot(kind='hist')
plt.show()



import matplotlib.pyplot as plt
import pandas as pd

df = pd.DataFrame({
    'name':['john','mary','peter','jeff','bill','lisa','jose'],
    'age':[23,78,22,19,45,33,20],
    'gender':['M','F','M','M','M','F','M'],
    'state':['california','dc','california','dc','california','texas','texas'],
    'num_children':[2,0,0,3,2,1,4],
    'num_pets':[5,1,0,5,2,2,3]
})
'''

import matplotlib.pyplot as plt
import pandas as pd

df=pd.read_csv('C:\mytmp\grafana_stats\im_internal_queue_latency_20191114_TEST.csv')

print(df.groupby('Process'))

# a scatter plot comparing num_children and num_pets
df.groupby('Process').plot(kind='line',x='Date',y='q_latency')
plt.show()






















