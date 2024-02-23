import time

from config.constants import SECOND_TO_NANO

def exec_timer(function_execution):
    def wrapper(*args):
        start_time = time.perf_counter_ns()
        result = function_execution(*args)
        time_res = (time.perf_counter_ns() - start_time) / SECOND_TO_NANO
        if time_res < 0.05:
            print(f"\033[34m\033[1m {function_execution.__name__}:\033[0m \033[34m\033[3m Execution time is\033[0m\033[1m\033[32m {time_res:.8f}\033[0m \033[34m\033[3mseconds\033[0m")
        elif time_res < 0.25:
            print(f"\033[34m\033[1m {function_execution.__name__}:\033[0m \033[34m\033[3m Execution time is\033[0m\033[1m\033[33m {time_res:.8f}\033[0m \033[34m\033[3mseconds\033[0m")
        else:
            print(f"\033[34m\033[1m {function_execution.__name__}:\033[0m \033[34m\033[3m Execution time is\033[0m\033[1m\033[31m {time_res:.8f}\033[0m \033[34m\033[3mseconds\033[0m")
        return result
    return wrapper