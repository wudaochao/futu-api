from futu import *
from group import group_init
from indicator import indicator_init
from subscribe import subscribe_init
from utils import ylog

trade_time_15m = {
    "09:30",
    "09:45",
    "10:00",
    "10:15",
    "10:30",
    "10:45",
    "11:00",
    "11:15",
    "11:30",
    "13:00",
    "13:15",
    "13:30",
    "13:45",
    "14:15",
    "14:30",
    "14:45",
    "15:00",
}

trade_time_2h = {
    "09:26",
    "11:25",
    "14:55"
}

def main_loop(quote_ctx):
    ylog.info("main loop start")
    while True:
        #ylog.debug("main loop")
        time.sleep(5)

if __name__ == '__main__':
    ylog.init()

    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    group_init(quote_ctx)
    indicator_init(quote_ctx)
    subscribe_init(quote_ctx)

    thread = threading.Thread(target=main_loop, args=(quote_ctx,))
    thread.start()
    thread.join()
