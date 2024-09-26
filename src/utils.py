import time

def get_now_ftime(format="%Y%m%d_%H%M%S"):
    return time.strftime(format, time.localtime())

def convert_str_to_time(str_time, format="%Y%m%d_%H%M%S"):
    return time.strptime(str_time, format)
