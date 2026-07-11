"""
on_recv_rsp(self, rsp_pb)

实时 K 线回调，异步处理已订阅股票的实时 K 线推送。
在收到实时 K 线数据推送后会回调到该函数，您需要在派生类中覆盖 on_recv_rsp。

参数	类型	说明
ret	RET_CODE	接口调用结果
data	pd.DataFrame	当 ret == RET_OK, 返回 K 线数据数据
str	当 ret != RET_OK, 返回错误描述

K 线数据格式如下：
字段	类型	说明
code	str	股票代码
name	str	股票名称
time_key	str	时间 
open	float	开盘价
close	float	收盘价
high	float	最高价
low	float	最低价
volume	float	成交量
turnover	float	成交额
pe_ratio	float	市盈率
turnover_rate	float	换手率 
last_close	float	昨收价 
k_type	KLType	K 线类型
"""

import time
from futu import *
class CurKlineTest(CurKlineHandlerBase):
    def on_recv_rsp(self, rsp_pb):
        ret_code, data = super(CurKlineTest,self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            print("CurKlineTest: error, msg: %s" % data)
            return RET_ERROR, data
        print("CurKlineTest ", data) # CurKlineTest 自己的处理逻辑
        return RET_OK, data
quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
handler = CurKlineTest()
quote_ctx.set_handler(handler)  # 设置实时K线回调
ret, data = quote_ctx.subscribe(['US.TSLA', 'US.NVDA', "US.AAPL"], [SubType.K_240M], session=Session.ALL)   # 订阅 K 线数据类型，OpenD 开始持续收到服务器的推送
if ret == RET_OK:
    print(data)
else:
    print('error:', data)
time.sleep(15)  # 设置脚本接收 OpenD 的推送持续时间为15秒
quote_ctx.close()   # 关闭当条连接，OpenD 会在1分钟后自动取消相应股票相应类型的订阅    
