import pandas as pd


fileName = 'qqq_second.csv'
columnNames = ['date','open','high','low','close','vol','avg','bar count']

global df
df = pd.DataFrame(columns=columnNames)
df.to_csv(fileName, mode='w', columns=columnNames, index=False)
