#  Author: Peter1303
#  Date: 2024/7/26
#  Copyright (c) 2024.

import const
from module.commander import *
from module.logger import *


def copy_script(curr_script_path, script_path):
    out, ok = execute_command(f'docker cp {curr_script_path} {const.safeline_container_name}:{script_path}')
    if not ok:
        logger.error(out)
    return ok


def modify_script_permission(script_path):
    out, ok = execute_command(f'docker exec {const.safeline_container_name} chmod +x {script_path}')
    if not ok:
        logger.error(out)
    return ok


def run_script(script_path, args=''):
    return execute_command(f'docker exec -it {const.safeline_container_name} {script_path} {args}')
