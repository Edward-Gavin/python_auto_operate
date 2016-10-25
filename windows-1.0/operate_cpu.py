import psutil
import time

com_dic = {'cputime': 'cpu_time', 'cpucount': 'cpu_count',
           'cpucountl': 'cpu_count_logical', 'virmem': 'virtual_memory',
           'swapmem': 'swap_memory', 'users': 'users', 'boottime': 'boot_time'}


def cpu_time():
    try:
        cputime = list(psutil.cpu_times())
        usertime = time.ctime(cputime[0])
        systemtime = time.ctime(cputime[1])
        idle = time.ctime(cputime[2])
        return "usertime: " + usertime + " systemtime: " + systemtime + " idle: " + idle
    except Exception as e:
        print(e)
        return e


def cpu_count():
    try:
        cpucount = psutil.cpu_count()
        return "CPU count is: " + str(cpucount)
    except Exception as e:
        print(e)
        return e


def cpu_count_logical():
    try:
        cpu_count_lo = psutil.cpu_count(logical=False)
        return "CPU logical is: " + str(cpu_count_lo)
    except Exception as e:
        print(e)
        return e


def virtual_memory():
    try:
        memory_byte = list(psutil.virtual_memory())
        memory = []
        for i in memory_byte:
            memory.append(float(i / 1024 / 1024 / 1024))
        print(memory)
        return "Total memory: " + str(round(memory[0])) + " Available memory: " + str(
            round(memory[1])) + " Used memory: " + str(round(memory[3])) + " Free memory: " + str(round(memory[4]))
    except Exception as e:
        print(e)
        return e


def swap_memory():
    try:
        memory_swap_byte = list(psutil.swap_memory())
        memory_swap = []
        for i in memory_swap_byte:
            memory_swap.append(float(i / 1024 / 1024 / 1024))
        return "Total memory: " + str(round(memory_swap[0])) + " Available memory: " + str(
            round(memory_swap[1])) + " Used memory: " + str(round(memory_swap[2]))
    except Exception as e:
        print(e)
        return e


def users():
    try:
        psutil.users()
        return psutil.users()
    except Exception as e:
        print(e)
        return e


def boot_time():
    try:
        psutil.boot_time()
        return time.ctime(psutil.boot_time())
    except Exception as e:
        print(e)
        return e
