"""
accinfo_query(trd_env=TrdEnv.REAL, acc_id=0, acc_index=0, refresh_cache=False, currency=Currency.HKD, asset_category=AssetCategory.NONE)

介绍

查询交易业务账户的资产净值、证券市值、现金、购买力等资金数据。

参数

参数	类型	说明
trd_env	TrdEnv	交易环境
acc_id	int	交易业务账户 ID 
acc_index	int	交易业务账户列表中的账户序号 
refresh_cache	bool	是否刷新缓存 
currency	Currency	计价货币 
asset_category	AssetCategory	资产类别 
返回

参数	类型	说明
ret	RET_CODE	接口调用结果
data	pd.DataFrame	当 ret == RET_OK 时，返回资金数据
str	当 ret != RET_OK 时，返回错误描述
资金数据格式如下：
字段	类型	说明
power	float	最大购买力 
max_power_short	float	卖空购买力 
net_cash_power	float	现金购买力
total_assets	float	总资产净值
securities_assets	float	证券资产净值
fund_assets	float	基金资产净值
bond_assets	float	债券资产净值
cash	float	现金
market_val	float	证券市值 
long_mv	float	多头市值
short_mv	float	空头市值
pending_asset	float	在途资产
interest_charged_amount	float	计息金额
frozen_cash	float	冻结资金
avl_withdrawal_cash	float	现金可提 
max_withdrawal	float	最大可提 
currency	Currency	计价货币 
available_funds	float	可用资金 
unrealized_pl	float	未实现盈亏 
realized_pl	float	已实现盈亏 
risk_level	CltRiskLevel	风控状态 
risk_status	CltRiskStatus	风险状态 
initial_margin	float	初始保证金
margin_call_margin	float	Margin Call 保证金
maintenance_margin	float	维持保证金
hk_cash	float	港元现金 
hk_avl_withdrawal_cash	float	港元可提 
hkd_net_cash_power	float	港元现金购买力 
hkd_assets	float	港股资产净值 
us_cash	float	美元现金 
us_avl_withdrawal_cash	float	美元可提 
usd_net_cash_power	float	美元现金购买力 
usd_assets	float	美股资产净值 
cn_cash	float	人民币现金 
cn_avl_withdrawal_cash	float	人民币可提 
cnh_net_cash_power	float	人民币现金购买力 
cnh_assets	float	A股资产净值 
jp_cash	float	日元现金 
jp_avl_withdrawal_cash	float	日元可提 
jpy_net_cash_power	float	日元现金购买力 
jpy_assets	float	日股资产净值 
sg_cash	float	新元现金 
sg_avl_withdrawal_cash	float	新元可提 
sgd_net_cash_power	float	新元现金购买力 
sgd_assets	float	新股资产净值 
au_cash	float	澳元现金 
au_avl_withdrawal_cash	float	澳元可提 
aud_net_cash_power	float	澳元现金购买力 
aud_assets	float	澳股资产净值 
ca_cash	float	加元现金 
ca_avl_withdrawal_cash	float	加元可提 
cad_net_cash_power	float	加元现金购买力 
cad_assets	float	加元资产净值 
my_cash	float	令吉现金 
my_avl_withdrawal_cash	float	令吉可提 
myr_net_cash_power	float	令吉现金购买力 
myr_assets	float	令吉资产净值 
is_pdt	bool	是否为 PDT 账户 
pdt_seq	string	剩余日内交易次数 
beginning_dtbp	float	初始日内交易购买力 
remaining_dtbp	float	剩余日内交易购买力 
dt_call_amount	float	日内交易待缴金额 
dt_status	DtStatus	日内交易限制情况 
crypto_mv	float	加密货币市值
exposure_level	ExposureLevel	持仓限额状态 
exposure_limit	float	持仓限额（单位 USD） 
used_limit	float	已用持仓限额（单位 USD） 
remaining_limit	float	剩余持仓限额（单位 USD） 

"""

from futu import *
trd_ctx = OpenSecTradeContext(filter_trdmarket=TrdMarket.HK, host='127.0.0.1', port=11111, security_firm=SecurityFirm.FUTUSECURITIES)
ret, data = trd_ctx.accinfo_query()
if ret == RET_OK:
    print(data)
    print(data['power'][0])  # 取第一行的购买力
    print(data['power'].values.tolist())  # 转为 list
else:
    print('accinfo_query error: ', data)
trd_ctx.close()  # 关闭当条连接
