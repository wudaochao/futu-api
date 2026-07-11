"""
get_acc_list()

获取交易业务账户列表。
要调用其他交易接口前，请先获取此列表，确认要操作的交易业务账户无误  
"""

from futu import *
trd_ctx = OpenSecTradeContext(filter_trdmarket=TrdMarket.HK, host='127.0.0.1', port=11111, security_firm=SecurityFirm.FUTUSECURITIES)
ret, data = trd_ctx.get_acc_list()
if ret == RET_OK:
    print(data)
    print(data['acc_id'][0])  # 取第一个账号
    print(data['acc_id'].values.tolist())  # 转为 list
else:
    print('get_acc_list error: ', data)
trd_ctx.close()