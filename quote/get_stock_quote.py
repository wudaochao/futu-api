"""
提示

此接口提供了一次性获取实时数据的功能，如需持续获取推送数据，请参考 实时报价回调 接口
获取实时数据 和 实时数据回调 的差别，请参考 如何通过订阅接口获取实时行情？
"""

from futu import *
quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)

ret_sub, err_message = quote_ctx.subscribe(['US.TSLA'], [SubType.QUOTE], subscribe_push=False)
# 先订阅 K 线类型。订阅成功后 OpenD 将持续收到服务器的推送，False 代表暂时不需要推送给脚本
if ret_sub == RET_OK:  # 订阅成功
    ret, data = quote_ctx.get_stock_quote(['US.TSLA'])  # 获取订阅股票报价的实时数据
    if ret == RET_OK:
        print(data)
        print(data['code'][0])   # 取第一条的股票代码
        print(data['code'].values.tolist())   # 转为 list
    else:
        print('error:', data)
else:
    print('subscription failed', err_message)
quote_ctx.close()  # 关闭当条连接，OpenD 会在1分钟后自动取消相应股票相应类型的订阅


