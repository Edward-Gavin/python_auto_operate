import os


def create_dir(command_argv_list):
    try:
        os.mkdir(command_argv_list[2])
        return command_argv_list[2] + ", Create successfully! "
    except Exception as e:
        print(e)
        return e


def delete_dir(command_argv_list):
    try:
        os.rmdir(command_argv_list[2])
        return command_argv_list[2] + ", Delete successfully! "
    except Exception as e:
        print(e)
        return e


def attrib_file(command_argv_list):
    try:
        os.system("attrib " + command_argv_list[2] + " " + command_argv_list[3])
        return command_argv_list[3] + ", Attribute is changed! "
    except Exception as e:
        print(e)
        return e


def create_file(command_argv_list):
    try:
        # os.mknod(command_argv_list[2])
        f = open(command_argv_list[1], mode='w', )
        f.write('')
        f.close()
        return command_argv_list[2] + ", Create file successfully! "
    except Exception as e:
        print(e)
        return e


def delete_file(command_argv_list):
    try:
        os.remove(command_argv_list[2])
        return command_argv_list[2] + ", Delete file successfully! "
    except Exception as e:
        print(e)
        return e
