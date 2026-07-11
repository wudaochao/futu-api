"""

介绍

获取已订阅股票的实时 K 线数据，必须要先订阅。

参数

参数	类型	说明
code	str	股票代码
name	str	股票名称
num	int	K 线数据个数 
ktype	KLType	K 线类型
autype	AuType	复权类型
返回

参数	类型	说明
ret	RET_CODE	接口调用结果
data	pd.DataFrame	当 ret == RET_OK，返回 K 线数据数据
str	当 ret != RET_OK，返回错误描述


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
"""

"""
接口限制

此接口为获取实时 K 线接口，最多能获取最近的 1000 根。如需获取历史 K 线，请参考 获取历史 K 线
市盈率和换手率字段，只有日 K 及以上周期的正股才有数据
期权, 仅提供日K, 1分K, 5分K, 15分K, 60分K。

"""

from futu import *
quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)

ret_sub, err_message = quote_ctx.subscribe(['SH.000852'], [SubType.K_120M], subscribe_push=False, session=Session.ALL)
# 先订阅 K 线类型。订阅成功后 OpenD 将持续收到服务器的推送，False 代表暂时不需要推送给脚本
if ret_sub == RET_OK:  # 订阅成功
    ret, data = quote_ctx.get_cur_kline('SH.000852', 20, KLType.K_120M, AuType.QFQ)  # 获取美股AAPL最近2个 K 线数据
    if ret == RET_OK:
        print(data)
        print(data['turnover_rate'][0])   # 取第一条的换手率
        print(data['turnover_rate'].values.tolist())   # 转为 list
    else:
        print('error:', data)
else:
    print('subscription failed', err_message)
quote_ctx.close()  # 关闭当条连接，OpenD 会在1分钟后自动取消相应股票相应类型的订阅
