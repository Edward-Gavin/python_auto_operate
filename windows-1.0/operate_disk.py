import os


# 查看某个磁盘的使用状况
def df_disk(command_argv_list):
    try:
        df_result = os.popen("df -h "+command_argv_list[2])
        return df_result
    except Exception as e:
        print(e)
        return e


# 查看某个目录的使用情况
def du_disk(command_argv_list):
    try:
        du_result = os.popen("du -a "+command_argv_list[2])
        return du_result
    except Exception as e:
        print(e)
        return e
