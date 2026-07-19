from futu import *
import threading
import time
from datetime import datetime

from utils.ylog import setup_logger


log = setup_logger(name="timer", log_dir="logs", level="DEBUG")

PRINT_SECONDS = {0, 15, 30, 45}

code_list = ["SH.688981", "SH.000001"]

calc_boll_map = dict()
calc_bbi_map = dict()


indicator_map = dict({
    "SH.688981": dict({"BBI": 0, "BOLL":{}}),
    "SH.000001": dict({"BBI": 0, "BOLL":{}})
}
)

#bbi: float
#mid: float
#upper: float
#lower: float


class IndicatorCalcHandler(IndicatorCalcHandlerBase):
    def on_recv_rsp(self, rsp_pb):
        ret_code, content = super(IndicatorCalcHandler, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            log.error("indicator calc error: %s", content)
            return ret_code, content
        #print('calc result:', content)

        calc_id = content["calc_id"]
        lastest = content["output_rows"][-2]
        newest = content["output_rows"][-1]
        if calc_id in calc_boll_map:
            code = calc_boll_map[calc_id]
            mid = 2 * newest["values"][0] - lastest["values"][0]
            upper = 2 * newest["values"][1] - lastest["values"][1]
            lower = 2 * newest["values"][2] - lastest["values"][2]

            indicator_map[code]["BOLL"] = dict({"MID": mid, "UPPER": upper, "LOWER": lower})
            del calc_boll_map[calc_id]

        if calc_id in calc_bbi_map:
            code = calc_bbi_map[calc_id]
            bbi = 2 * newest["values"][0] - lastest["values"][0]
            indicator_map[code]["BBI"] = bbi
            del calc_bbi_map[calc_id]

        log.info("indicator map: %s", indicator_map)

        return RET_OK, content

def run_timer():
    last_print_second = None
    last_print_minute = None

    while True:
        current_second = time.localtime().tm_sec
        if current_second in PRINT_SECONDS and current_second != last_print_second:
            log.info("current second: %02d", current_second)
            log.debug("current time: %s", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            last_print_second = current_second

            for code in code_list:
                ret, kl_data, _ = quote_ctx.request_history_kline(code, start='2026-07-01', end='2026-07-13',
                                                                  ktype=KLType.K_15M)
                # ret, kl_data, _ = quote_ctx.get_cur_kline('SH.688981', 50, KLType.K_120M, AuType.QFQ)
                # ret, kl_data = quote_ctx.get_cur_kline('SH.688981', 25, KLType.K_DAY, AuType.QFQ)

                if ret != RET_OK:
                    log.warning("request history kline failed for %s: %s", code, kl_data)
                    continue

                ret, calc_id = quote_ctx.request_indicator_calc_async(
                    'BOLL', IndicatorLangType.MYLANG, code, KLType.K_15M, kl_data)
                if ret == RET_OK:
                    #print(f"calc_id for '{code}' is: {calc_id}(boll)")
                    calc_boll_map[calc_id] = code
                else:
                    log.error("request BOLL indicator failed for %s: %s", code, calc_id)

                ret, calc_id = quote_ctx.request_indicator_calc_async(
                    'BBI', IndicatorLangType.MYLANG,
                    code, KLType.K_15M, kl_data)
                if ret == RET_OK:
                    #print(f"calc_id for '{code}' is: {calc_id}(bbi)")
                    calc_bbi_map[calc_id] = code
                else:
                    log.error("request BBI indicator failed for %s: %s", code, calc_id)


        current_minute = time.localtime().tm_hour
        if (current_minute == 12 or current_minute == 15 or current_minute == 16) and current_minute != last_print_minute:
            log.info("current minute: %02d", current_minute)
            log.debug("current time: %s", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            last_print_minute = current_minute

        time.sleep(0.2)

if __name__ == "__main__":
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)

    quote_ctx.set_handler(IndicatorCalcHandler())

    thread = threading.Thread(target=run_timer)
    thread.start()
    thread.join()
