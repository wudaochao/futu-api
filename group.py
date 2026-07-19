import threading
from futu import *
from utils import ylog

GROUP_NAMES = ("指标", "分", "时", "周", "月", "季")

group_map = dict({"指标": [], "分": [], "时": [], "周": [], "月": [], "季": []})

def new_group():
    return dict({"指标": [], "分": [], "时": [], "周": [], "月": [], "季": []})

def get_periods_by_group_name(code, group_name):
    hour_period = KLType.K_120M
    if code.startswith(("HK.", "US.")):
        hour_period = KLType.K_240M
    if group_name == "指标":
        return [KLType.K_15M, hour_period, KLType.K_WEEK, KLType.K_MON, KLType.K_QUARTER]
    elif group_name == "分":
        return [KLType.K_15M, hour_period]
    elif group_name == "时":
        return [hour_period, KLType.K_WEEK]
    elif group_name == "周":
        return [KLType.K_WEEK, KLType.K_MON]
    elif group_name == "月":
        return [KLType.K_MON, KLType.K_QUARTER]
    elif group_name == "季":
        return [KLType.K_QUARTER]

    return None

def compare_group(group, new_groups, old_groups):
    flag = True

    for code in new_groups:
        if code not in old_groups:
            ylog.info(f"'{code}' is added into group['{group}']")
            flag = False

    for code in old_groups:
        if code not in new_groups:
            ylog.info(f"'{code}' is removed from group['{group}']")
            flag = False

    return flag

def update_group(quote_ctx):
    new_group_map = new_group()

    for group in GROUP_NAMES:
        ret, data = quote_ctx.get_user_security(group_name=group)
        if ret == RET_OK:
            code_list = data["code"].dropna().unique().tolist()
            new_group_map[group] = code_list
            ylog.debug(f"{group}: {code_list}")
        else:
            ylog.warning(data)
            return

    """
    比较新旧分组，更新group_map
    """
    global group_map
    for group in GROUP_NAMES:
        if not compare_group(group, new_group_map[group], group_map[group]):
            ylog.info(f"'{group}' has changed: new={new_group_map[group]}, old={group_map[group]}")
        else:
            ylog.debug(f"'{group}' has not changed: code_list={group_map[group]}")

    ylog.info(f"new_group_map: {new_group_map}")

    ylog.info(f"group_map: {group_map}")
    #group_map = new_group_map
    group_map.update(new_group_map)
    ylog.info(f"group_map: {group_map}")


def group_loop(quote_ctx):
    time.sleep(300)
    while True:
        update_group(quote_ctx)
        time.sleep(300)

def group_init(quote_ctx):
    update_group(quote_ctx)

    thread = threading.Thread(target=group_loop, args=(quote_ctx,))
    thread.start()