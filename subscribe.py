import time
from futu import *
from group import *
from indicator import *
from urllib import request
from urllib.error import HTTPError, URLError

last_price_map = {}

period_names = {
    KLType.K_15M: "15分钟",
    KLType.K_60M: "1小时",
    KLType.K_120M: "2小时",
    KLType.K_240M: "4小时",
    KLType.K_WEEK: "周线",
    KLType.K_MON: "月线",
    KLType.K_QUARTER: "季线",
}

DEFAULT_FEISHU_WEBHOOK_URL = (
    "https://open.feishu.cn/open-apis/bot/v2/hook/"
    "0f2015b5-6d16-4f3b-b8c6-e0df7853db37"
)

sent_feishu_period_keys = set()

def should_suppress_feishu(suppress_key):
    if suppress_key is None:
        return False
    if suppress_key in sent_feishu_period_keys:
        return True
    sent_feishu_period_keys.add(suppress_key)
    return False

def get_feishu_suppress_key(code, action_type):
    now = datetime.now()
    return code, action_type, now.year, now.month, now.day, now.hour, now.minute // 15

def send_feishu_message(text, suppress_key=None):
    if should_suppress_feishu(suppress_key):
        return

    print(text)
    payload = {
        "msg_type": "text",
        "content": {
            "text": text,
        },
    }
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(
        DEFAULT_FEISHU_WEBHOOK_URL,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=5) as resp:
            if resp.status >= 300:
                print(f"feishu webhook error: status={resp.status}")
    except HTTPError as exc:
        print(f"feishu webhook http error: status={exc.code}, msg={exc.reason}")
    except URLError as exc:
        print(f"feishu webhook url error: msg={exc.reason}")
    except TimeoutError:
        print("feishu webhook timeout")


def check_period_alert(code, period, indicator_name, last_price, current_price):
    period_name = period_names[period]

    if "BOLL" == indicator_name:
        #ylog.info(f"check_period_alert for boll {code} {period}: last_price={last_price:.2f}, current_price={current_price:.2f}")
        t, last_close = get_lastest_close(code, period)
        t, last_mid, last_upper, last_lower = get_lastest_boll(code, period)
        t, mid, upper, lower = get_boll(code, period)
        if last_mid is not None and mid is not None and last_close is not None:
            ylog.info(f"{code} {period:<10}: upper={upper:.2f} lower={lower:.2f} last_mid={last_mid:.2f} last_close={last_close:.2f} mid={mid:.2f} current={current_price:.2f}")
            if last_mid < last_close < last_upper:
                if current_price >= upper > last_price:
                    action = f"{code}涨到{period_name}BOLL上轨"
                    message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {action}(新): upper={upper:.2f}, last_price={last_price:.2f} current={current_price:.2f}"
                    print(message)
                    send_feishu_message(message, suppress_key=get_feishu_suppress_key(code, action))
                elif current_price < mid < last_price:
                    action = f"{code}跌到{period_name}BOLL中轨"
                    message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {action}(新): mid={mid:.2f}, last_price={last_price:.2f} current={current_price:.2f}"
                    print(message)
                    send_feishu_message(message, suppress_key=get_feishu_suppress_key(code, action))
            elif last_mid > last_close > last_lower:
                if current_price >= mid > last_price:
                    action = f"{code}涨到{period_name}BOLL中轨"
                    message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {action}(新): mid={mid:.2f}, last_price={last_price:.2f} current={current_price:.2f}"
                    print(message)
                    send_feishu_message(message, suppress_key=get_feishu_suppress_key(code, action))
                elif current_price <= lower < last_price:
                    action = f"{code}跌到{period_name}BOLL下轨"
                    message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {action}(新): lower={lower:.2f}, last_price={last_price:.2f} current={current_price:.2f}"
                    print(message)
                    send_feishu_message(message, suppress_key=get_feishu_suppress_key(code, action))
    if "BBI" == indicator_name:
        #ylog.info(f"check_period_alert for bbi {code} {period}: last_price={last_price:.2f}, current_price={current_price:.2f}")
        t, last_close = get_lastest_close(code, period)
        _, last_bbi = get_lastest_bbi(code, period)
        t, last_mid, last_upper, last_lower = get_lastest_boll(code, period)
        _, bbi = get_bbi(code, period)
        if last_mid is not None and last_bbi is not None and bbi is not None and last_close is not None:
            ylog.info(f"{code} {period:<10}: last_bbi={last_bbi:.2f} last_close={last_close:.2f} bbi={bbi:.2f} current={current_price:.2f}")
            if last_close > last_bbi > last_mid:
                if current_price <= bbi < last_price:
                    action = f"{code}跌到{period_name}BBI"
                    message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {action}(新): bbi={bbi:.2f}, last_price={last_price:.2f} current={current_price:.2f}"
                    print(message)
                    send_feishu_message(message, suppress_key=get_feishu_suppress_key(code, action))
            elif last_close < last_bbi < last_mid:
                if current_price >= bbi > last_price:
                    action = f"{code}涨到{period_name}BBI"
                    message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {action}(新): bbi={bbi:.2f}, last_price={last_price:.2f} current={current_price:.2f}"
                    print(message)
                    send_feishu_message(message, suppress_key=get_feishu_suppress_key(code, action))

def on_realtime_price(code, cur_price):
    ylog.info(f"{code} {cur_price}")

    if code not in last_price_map:
        last_price_map[code] = cur_price
        return

    last_price = last_price_map[code]
    for group_name in group_map:
        if code in group_map[group_name]:
            for period, indicator_names in get_periods_by_group_name(code, group_name).items():
                if "BOLL" in indicator_names:
                    check_period_alert(code, period, "BOLL", last_price, cur_price)

            for period, indicator_names in get_periods_by_group_name(code, group_name).items():
                if "BBI" in indicator_names:
                    check_period_alert(code, period, "BBI", last_price, cur_price)

    last_price_map[code] = cur_price

    # periods = {period for period, _ in self.indicator_tasks.get(code, set())}
    # for period in periods:
    #     self.check_period_alert(code, period, last_price, current_price)

class DynamicRTDataHandler(RTDataHandlerBase):
    def on_recv_rsp(self, rsp_pb):
        ret_code, data = super(DynamicRTDataHandler, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            print("RTData error, msg: %s" % data)
            return RET_ERROR, data

        for _, row in data.iterrows():
            try :
                on_realtime_price(row["code"], row["cur_price"])
            except Exception as e:
                ylog.error(f"on_realtime_price error: {e}")
                ylog.error(traceback.format_exc())
        return RET_OK, data

def subscribe_loop(quote_ctx):
    time.sleep(5)

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