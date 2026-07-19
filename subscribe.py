from futu import *
from group import *

def on_realtime_price(code, cur_price):
    print("code: %s, cur_price: %f" % (code, cur_price))

class DynamicRTDataHandler(RTDataHandlerBase):
    def on_recv_rsp(self, rsp_pb):
        ret_code, data = super(DynamicRTDataHandler, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            print("RTData error, msg: %s" % data)
            return RET_ERROR, data
        for _, row in data.iterrows():
            on_realtime_price(row["code"], row["cur_price"])
        return RET_OK, data

def subscribe_loop(quote_ctx):
    while True:
        sub_list = []

        code_list = sorted(get_all_groups())
        # ret, data = quote_ctx.subscribe(code_list, [SubType.RT_DATA], session=Session.ALL)
        # if ret != RET_OK:
        #     print("subscribe error:", data)

        ret, data = quote_ctx.query_subscription()
        if ret == RET_OK:
            if data["sub_list"].get("RT_DATA") is not None:
                sub_list = sorted(data["sub_list"]["RT_DATA"])
                ylog.debug(data["sub_list"]["RT_DATA"])
        else:
            ylog.error(data)

        for code in code_list:
            if code not in sub_list:
                ylog.info(f"'{code}' need to be subscribed")

        for code in sub_list:
            if code not in code_list:
                ylog.info(f"'{code}' need to be unsubscribed")

        if sub_list != code_list:
            ylog.info(f"sub_list: {sub_list}, code_list: {code_list}")
            ret, data = quote_ctx.subscribe(sorted(code_list), [SubType.RT_DATA], session=Session.ALL)
            if ret != RET_OK:
                print("subscribe error:", data)
            else:
                ylog.info(f"subscribe success, code_list: {code_list}")

        time.sleep(60)

def subscribe_init(quote_ctx):
    quote_ctx.set_handler(DynamicRTDataHandler())

    thread = threading.Thread(target=subscribe_loop, args=(quote_ctx, ))
    thread.start()
    return thread