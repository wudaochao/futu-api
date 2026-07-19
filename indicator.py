from futu import *
from utils import ylog
from group import *

calc_boll_map = {}
calc_bbi_map = {}
indicator_map = dict()
last_indicator_map = dict()

def get_lastest_bbi(code, period):
    code_map = last_indicator_map.get(code)
    if code_map is not None:
        period_map = code_map.get(period)
        if period_map is not None:
            return period_map.get("TIME"), period_map.get("BBI")

    return None, None

def get_lastest_boll(code, period):
    code_map = last_indicator_map.get(code)
    if code_map is not None:
        period_map = code_map.get(period)
        if period_map is not None:
            return period_map.get("TIME"), period_map.get("MID"), period_map.get("UPPER"), period_map.get("LOWER")

    return None, None, None, None

def add_bbi(bbi_map, code, period, time, bbi):
    code_map = bbi_map.get(code)
    if code_map is None:
        code_map = dict()
        bbi_map[code] = code_map

    period_map = code_map.get(period)
    if period_map is None:
        period_map = dict()
        code_map[period] = period_map

    period_map["TIME"] = time
    period_map["BBI"] = bbi

def add_boll(boll_map, code, period, time, mid, upper, lower):
    code_map = boll_map.get(code)
    if code_map is None:
        code_map = dict()
        boll_map[code] = code_map

    period_map = code_map.get(period)
    if period_map is None:
        period_map = dict()
        code_map[period] = period_map

    period_map["TIME"] = time
    period_map["MID"] = mid
    period_map["UPPER"] = upper
    period_map["LOWER"] = lower

def create_indicator_map(group, code):
    hour_period = KLType.K_120M
    if code.startswith(("HK.", "US.")):
        hour_period = KLType.K_240M
    if group == "指标":
        return dict({
            KLType.K_15M: {"BBI": 0.0, "BOLL": {"UPPER": 0.0, "MID": 0.0, "LOWER": 0.0}},
            KLType.K_60M: {"BBI": 0.0, "BOLL": {"UPPER": 0.0, "MID": 0.0, "LOWER": 0.0}},
            hour_period: {"BBI": 0.0, "BOLL": {"UPPER": 0.0, "MID": 0.0, "LOWER": 0.0}},
            KLType.K_WEEK: {"BBI": 0.0, "BOLL": {"UPPER": 0.0, "MID": 0.0, "LOWER": 0.0}},
            KLType.K_MON: {"BBI": 0.0, "BOLL": {"UPPER": 0.0, "MID": 0.0, "LOWER": 0.0}},
            KLType.K_QUARTER: {"BBI": 0.0, "BOLL": {"UPPER": 0.0, "MID": 0.0, "LOWER": 0.0}}
        })
    elif group == "分":
        return dict({
            KLType.K_15M: {"BBI": 0.0, "BOLL": {"UPPER": 0.0, "MID": 0.0, "LOWER": 0.0}},
            hour_period: {"BBI": 0.0},
        })
    elif group == "时":
        return dict({
            hour_period: {"BBI": 0.0, "BOLL": {"UPPER": 0.0, "MID": 0.0, "LOWER": 0.0}},
            KLType.K_WEEK: {"BBI": 0.0},
        })

    elif group == "周":
        return dict({
            KLType.K_WEEK: {"BBI": 0.0, "BOLL": {"UPPER": 0.0, "MID": 0.0, "LOWER": 0.0}},
            KLType.K_MON: {"BBI": 0.0},
        })

    elif group == "月":
        return dict({
            KLType.K_MON: {"BBI": 0.0, "BOLL": {"UPPER": 0.0, "MID": 0.0, "LOWER": 0.0}},
            KLType.K_QUARTER: {"BBI": 0.0},
        })

    elif group == "季":
        return dict({
            KLType.K_QUARTER: {"BBI": 0.0, "BOLL": {"UPPER": 0.0, "MID": 0.0, "LOWER": 0.0}},
        })

    return None


def get_kline_date_range(period):
    end_date = datetime.now().date()
    lookback_days_map = {
        KLType.K_15M: 10,
        KLType.K_60M: 30,
        KLType.K_120M: 45,
        KLType.K_240M: 90,
        KLType.K_WEEK: 260,
        KLType.K_MON: 1100,
        KLType.K_QUARTER: 3000,
    }
    lookback_days = lookback_days_map.get(period, 260)
    start_date = end_date - timedelta(days=lookback_days)
    return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")

def request_indicator_cb(content):
    calc_id = content["calc_id"]
    output_rows = content["output_rows"]
    if len(output_rows) < 2:
        ylog.error(f"indicator output rows too short: calc_id={calc_id}")
        return

    latest = output_rows[-2]
    newest = output_rows[-1]
    time = newest["time"]

    #ylog.debug(f"request_indicator_cb: calc_id={calc_id}, time={time}")
    if calc_id in calc_boll_map:
        code, period = calc_boll_map.pop(calc_id)
        #ylog.debug(f"receive boll: calc_id={calc_id}, period={period} time={time}")
        # 判断指标是否已经最新
        # last_time = last_indicator_map[code][period]["TIME"]
        # last_mid = last_indicator_map[code][period]["BOLL"]["MID"]
        # last_upper = last_indicator_map[code][period]["BOLL"]["UPPER"]
        # last_lower = last_indicator_map[code][period]["BOLL"]["LOWER"]
        last_time, last_mid, last_upper, last_lower = get_lastest_boll(code, period)
        if last_time is not None and last_mid is not None and last_time == time:
            ylog.debug(f"BOLL for '{code} {period}' is already newest: {last_time} {last_mid:.2f} {last_upper:.2f} {last_lower:.2f}")
            return

        mid = 2 * newest["values"][0] - latest["values"][0]
        upper = 2 * newest["values"][1] - latest["values"][1]
        lower = 2 * newest["values"][2] - latest["values"][2]

        add_boll(indicator_map, code, period, time, mid, upper, lower)
        last_time, last_mid, last_upper, last_lower = time, newest["values"][0], newest["values"][1], newest["values"][2]
        add_boll(last_indicator_map, code, period, time, last_mid, last_upper, last_lower)
        # indicator_map[code][period]["BOLL"] = {
        #     "MID": mid,
        #     "UPPER": upper,
        #     "LOWER": lower,
        # }
        # last_indicator_map[code][period]["BOLL"] = {
        #     "TIME": time,
        #     "MID": newest["values"][0],
        #     "UPPER": newest["values"][1],
        #     "LOWER": newest["values"][2],
        # }

        ylog.info(f"BOLL for '{code} {period}' last updated: {last_time} {last_mid:.2f} {last_upper:.2f} {last_lower:.2f}")
        ylog.info(f"BOLL for '{code} {period}' new updated: {time} {mid:.2f} {upper:.2f} {lower:.2f}")

        # self.print_indicator_update(code, period)
        # return

    if calc_id in calc_bbi_map:
        code, period = calc_bbi_map.pop(calc_id)
        #ylog.debug(f"receive bbi: calc_id={calc_id}, period={period} time={time}")
        # last_time = last_indicator_map[code][period]["TIME"]
        # last_bbi = last_indicator_map[code][period]["BBI"]
        last_time, last_bbi = get_lastest_bbi(code, period)
        if last_time is not None and last_bbi is not None and last_time == time:
            ylog.debug(f"BBI for '{code} {period}' is already newest: {last_time} {last_bbi:.2f}")
            return

        bbi = 2 * newest["values"][0] - latest["values"][0]
        add_bbi(indicator_map, code, period, time, bbi)
        last_time, last_bbi = time, newest["values"][0]
        add_bbi(last_indicator_map, code, period, last_time, last_bbi)
        # indicator_map[code][period]["BBI"] = bbi
        # last_indicator_map[code][period]["BBI"] = newest["values"][0]
        # last_indicator_map[code][period]["TIME"] = time
        ylog.info(f"BBI for '{code} {period}' last updated: {last_time} {last_bbi:.2f}")
        ylog.info(f"BBI for '{code} {period}' new updated: {time} {bbi:.2f}")

# def request_indicator(quote_ctx, group, code, period):
#     #code_tasks = code_tasks or self.indicator_tasks.get(code, set())
#     for group_name in group_map:
#         for code in group_map[group_name]:
#             for period in get_periods_by_group_name(code, group_name):
#                 start, end = get_kline_date_range(period)
#                 ret, kl_data, _ = quote_ctx.request_history_kline(
#                     code,
#                     start=start,
#                     end=end,
#                     ktype=period,
#                 )
#                 if ret != RET_OK:
#                     ylog.error(f"request_history_kline error: code={code}, period={period}, msg={kl_data}")
#                     continue
#                 else:
#                     ylog.debug(f"request_history_kline success: {group_name}: {code} -> {period}")
#
#                 if len(kl_data) < 24:
#                     ylog.warning(f"not enough kline data: {group_name}: {code} -> {period}, len={len(kl_data)}")
#                     return
#
#                 #self.close_price_map[period][code] = kl_data["close"].iloc[-1]
#
#                 for indicator_name, calc_map in (
#                         ("BOLL", calc_boll_map),
#                         ("BBI", calc_bbi_map),
#                 ):
#                     #if (period, indicator_name) not in code_tasks:
#                     #    continue
#                     #发起请求
#                     ret, calc_id = quote_ctx.request_indicator_calc_async(
#                         indicator_name, IndicatorLangType.MYLANG, code, period, kl_data
#                     )
#                     if ret == RET_OK:
#                         ylog.debug(f"request {indicator_name} success: code={code}, period={period}, calc_id={calc_id}")
#                         #with self.lock:
#                         calc_map[calc_id] = (code, period)
#                     else:
#                         ylog.error(f"request {indicator_name} error: code={code}, period={period}, error={calc_id}")

def update_indicator(quote_ctx):
    for group_name in group_map:
        for code in group_map[group_name]:
            for period in get_periods_by_group_name(code, group_name):
                start, end = get_kline_date_range(period)
                ret, kl_data, _ = quote_ctx.request_history_kline(
                    code,
                    start=start,
                    end=end,
                    ktype=period,
                )
                if ret != RET_OK:
                    ylog.error(f"request_history_kline error: code={code}, period={period}, msg={kl_data}")
                    continue
                # else:
                #     ylog.debug(f"request_history_kline success: {group_name}: {code} -> {period}")

                if len(kl_data) < 24:
                    ylog.warning(f"not enough kline data: {group_name}: {code} -> {period}, len={len(kl_data)}")
                    return

                #self.close_price_map[period][code] = kl_data["close"].iloc[-1]

                for indicator_name, calc_map in (
                        ("BOLL", calc_boll_map),
                        ("BBI", calc_bbi_map),
                ):
                    #if (period, indicator_name) not in code_tasks:
                    #    continue
                    #发起请求
                    ret, calc_id = quote_ctx.request_indicator_calc_async(
                        indicator_name, IndicatorLangType.MYLANG, code, period, kl_data
                    )
                    if ret == RET_OK:
                        #ylog.debug(f"request {indicator_name} success: code={code}, period={period}, calc_id={calc_id}")
                        #with self.lock:
                        calc_map[calc_id] = (code, period)
                    else:
                        ylog.error(f"request {indicator_name} error: code={code}, period={period}, error={calc_id}")
            time.sleep(1)

def indicator_loop(quote_ctx):
    #time.sleep(60)

    while True:
        ylog.warning("indicator loop start")
        update_indicator(quote_ctx)
        time.sleep(60)


class IndicatorCalcHandler(IndicatorCalcHandlerBase):
    def on_recv_rsp(self, rsp_pb):
        ret_code, content = super(IndicatorCalcHandler, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            print("indicator calc error:", content)
            return ret_code, content

        #self.monitor.on_indicator_result(content)
        #print(content)
        try:
            request_indicator_cb(content)
        except Exception as e:
            ylog.error(f"request_indicator_cb error: {e}")
            ylog.error(traceback.format_exc())
        return RET_OK, content

def indicator_init(quote_ctx):
    quote_ctx.set_handler(IndicatorCalcHandler())
    #update_indicator(quote_ctx)

    thread = threading.Thread(target=indicator_loop, args=(quote_ctx,))
    thread.start()