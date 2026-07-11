"""
接口限制

每 30 秒内最多请求 60 次快照。
每次请求，接口参数 股票代码列表 支持传入的标的数量上限是 400 个。
港股 BMP 权限下，单次请求的香港证券（含窝轮、牛熊、界内证）快照数量上限是 20 个。
港股期权期货 BMP 权限下，单次请求的香港期货和期权的快照数量上限是 20 个。
"""

from futu import *
quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)

ret, data = quote_ctx.get_market_snapshot(['HK.00700', 'US.AAPL'])
if ret == RET_OK:
    print(data)
    print(data['code'][0])    # 取第一条的股票代码
    print(data['code'].values.tolist())   # 转为 list
else:
    print('error:', data)
quote_ctx.close() # 结束后记得关闭当条连接，防止连接条数用尽

