from futu import *
from group import group_init
from indicator import indicator_init
from utils import ylog

def main_loop(quote_ctx):
    while True:
        ylog.warning("main loop start")
        time.sleep(5)

if __name__ == '__main__':
    ylog.init()

    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    group_init(quote_ctx)
    indicator_init(quote_ctx)

    thread = threading.Thread(target=main_loop, args=(quote_ctx,))
    thread.start()
    thread.join()
