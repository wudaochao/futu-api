import threading
import time


PRINT_SECONDS = {0, 15, 30, 45}


def run_timer():
    last_print_second = None

    while True:
        current_second = time.localtime().tm_sec
        if current_second in PRINT_SECONDS and current_second != last_print_second:
            print(f"current second: {current_second:02d}")
            last_print_second = current_second

        time.sleep(0.2)


thread = threading.Thread(target=run_timer)
thread.start()
thread.join()
