import pandas as pd

from ibapi.client import *
from ibapi.wrapper import *
from time import sleep

fileName = 'qqq_second.csv'
openingHalfHours = ["10:00:00","10:30:00","11:00:00","11:30:00","12:00:00","12:30:00","13:00:00","13:30:00","14:00:00","14:30:00","15:00:00","15:30:00","16:00:00"]
columnNames = ['date','open','high','low','close','vol','avg','bar count']
global df
df = pd.DataFrame(columns=columnNames)
df.to_csv(fileName, mode='w', columns=columnNames, index=False)

global clientId
clientId = 1001

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
    # A Pacing Violation occurs whenever one or more of the following restrictions is not observed:
    # 1. Making identical historical data requests within 15 seconds.
    # 2. Making six or more historical data requests for the same Contract, Exchange and Tick Type within two seconds.
    # 3. Making more than 60 requests within any ten minute period.
    def msgLoopRec(self):
        # sleep(2)
        return
    def nextValidId(self, orderId: int):
        self.nextOrderId = orderId
        print("nextValidId triggered to be: " + str(orderId))

    def historicalData(self, reqId, bar):
        global df
        new_row = pd.DataFrame([[bar.date,bar.open,bar.high,bar.low,bar.close,bar.volume,bar.average,bar.barCount]],columns=columnNames)
        df = pd.concat([df, new_row], ignore_index=True)
        # print(f"Historical Data: {bar}")
    def historicalDataEnd(self, reqId, start, end):
        df.to_csv(fileName, columns=columnNames, index=False)
        print(f"End of HistoricalData")
        print(f"Start: {start}, End: {end}")
        self.disconnect()

def getWeekOf(date: int):
    return [str(date + i) for i in range(0,5)]

def makeHistoricDataRequest(idx, contract, endTime, duration, barSize):
    app = TestApp()
    # TWS uses socket port 7496 for live sessions and 7497 for paper sessions. 
    # IB Gateway by contrast uses 4001 for live sessions and 4002 for paper sessions.
    app.connect('127.0.0.1', 4002, idx)

    sleep(3)
    app.reqHistoricalData(idx, contract, endTime, duration, barSize, "TRADES", 1, 1, 0, [])
    app.run()

def main():

    qqq = Contract()
    qqq.symbol = "QQQ"
    qqq.secType = "STK"
    qqq.exchange = "SMART"
    qqq.currency = "USD"

    datesRequested = getWeekOf(20231002)

    idx = 0
    for date in datesRequested:
        for hour in openingHalfHours:
            makeHistoricDataRequest(idx, qqq, date + ' ' + hour + ' US/Eastern', "1800 S", "1 secs")
            idx += 1

    # Duration setting: S/D/W/M/Y
    # Historical data bar size setting.
    # Legal ones are: 1 secs, 5 secs, 10 secs, 15 secs, 30 secs,
    # 1 min, 2 mins, 3 mins, 5 mins, 10 mins, 15 mins, 20 mins, 30 mins, 
    # 1 hour, 2 hours, 3 hours, 4 hours, 8 hours, 1 day, 1W, 1M
    # app.reqHistoricalData(0, qqq, "20231006 16:00:00 US/Eastern", "1800 S", "1 secs", "TRADES", 1, 1, 0, [])


if __name__ == "__main__":
    main()