from futu import *
quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)

ret, data = quote_ctx.get_price_reminder(code='US.AAPL')
if ret == RET_OK:
    print(data)
    print(data['key'].values.tolist())   # 转为 list
else:
    print('error:', data)
print('******************************************')
ret, data = quote_ctx.get_price_reminder(code=None, market=Market.US)
if ret == RET_OK:
    print(data)
    if data.shape[0] > 0:  # 如果到价提醒列表不为空
        print(data['code'][0])    # 取第一条的股票代码
        print(data['code'].values.tolist())   # 转为 list
else:
    print('error:', data)
quote_ctx.close() # 结束后记得关闭当条连接，防止连接条数用尽
