import tushare as ts

print(ts.__version__)
#ts.get_k_data('600000', ktype='W', autype='hfq')
df = ts.get_tick_data('600848',date='2014-01-09')
print(df.head(10))
print(ts.get_k_data('600000', ktype='W', autype='hfq'))