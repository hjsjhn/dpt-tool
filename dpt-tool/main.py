from time import sleep
from datetime import datetime
from constant import default_choice, default_server, choice_to_func, choice_to_name, RETRIES, TOTAL_RETRIES, TIMEOUT

def run(choice, arg):
    for _ in range(RETRIES):
        try:
            func = choice_to_func[choice]
            ret = func(arg)
            if isinstance(ret, bool):
                ret = "Yes" if ret else "No"
            print(f"{choice}: {ret}")
            return
        except:
            sleep(TIMEOUT)
            pass
    print(f"{choice}: FAILED")
