    # Copyright (C) 2019  ab-trader

    # This program is free software: you can redistribute it and/or modify
    # it under the terms of the GNU General Public License as published by
    # the Free Software Foundation, either version 3 of the License, or
    # (at your option) any later version.

    # This program is distributed in the hope that it will be useful,
    # but WITHOUT ANY WARRANTY; without even the implied warranty of
    # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    # GNU General Public License for more details.

    # You should have received a copy of the GNU General Public License
    # along with this program.  If not, see <https://www.gnu.org/licenses/>.

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import backtrader as bt
import backtrader_addons as bta
import os.path
import sys


class DataTest(bt.Strategy):

    # simple strategy to print the data feed for test needs

    params = (('dt', None),)

    def __init__(self):

        pass
    

    def next(self):
 
        adjclose = self.data.adjclose[0] if 'ADJUSTED' in self.p.dt else 0.0
        div = self.data.div[0] if 'ADJUSTED' in self.p.dt else 0.0
        split = self.data.split[0] if 'ADJUSTED' in self.p.dt else 0.0

        print('%s %s o: %0.5f, h: %0.5f, l: %0.5f, c: %0.5f, ' % (
            self.data.datetime.date().isoformat(),
            self.data.datetime.time().isoformat(), self.data.open[0],
            self.data.high[0], self.data.low[0], self.data.close[0]) + 
            'ac: %0.5f, v: %0.1f, d: %0.5f, s: %0.3f ' % (
            adjclose, self.data.volume[0], div, split))


if __name__ == '__main__':

    # get script agrments: 1st - datatype, 2nd - interval in min for intraday
    # data (see Alphavantage API)
    datatype = str(sys.argv[1])
    interval = int(sys.argv[2]) if len(sys.argv) > 2 else 0

    # alphavantage data types and related bt parameters
    alphavantage_datas = {
        'INTRADAY': ['intraday_%dmin' % interval, bt.TimeFrame.Minutes,
                     interval],
        'DAILY': ['daily', bt.TimeFrame.Days, 1],
        'DAILY_ADJUSTED': ['daily_adjusted', bt.TimeFrame.Days, 1],
        'WEEKLY': ['weekly', bt.TimeFrame.Weeks, 1],
        'WEEKLY_ADJUSTED': ['weekly_adjusted', bt.TimeFrame.Weeks, 1],
        'MONTHLY': ['monthly', bt.TimeFrame.Months, 1],
        'MONTHLY_ADJUSTED': ['monthly_adjusted', bt.TimeFrame.Months, 1],
    }
    
    d = alphavantage_datas[datatype]
    modpath = os.path.dirname(os.path.abspath(__file__))
    dataspath = '../datas'
    ticker = d[0] + '_MSFT.csv'

    datapath = os.path.join(modpath, dataspath, ticker)

    # --- use case for Alphavantage CSV data feed ---
    data = bta.datafeeds.AlphavantageCSV(dataname=datapath, plot=True,
                                         name=ticker,
                                         timeframe=d[1],
                                         compression=d[2],
                                         datatype=datatype)
    # --- use case for Alphavantage CSV data feed ---
    
    cerebro = bt.Cerebro()
    cerebro.addstrategy(DataTest, dt=datatype)
    cerebro.adddata(data)
    cerebro.run(stdstats=False)

    cerebro.plot(style='candle', numfigs=1, volup = 'green', voldown = 'red',
                 voltrans = 75.0, voloverlay = False)