#  Author: Peter1303
#  Date: 2024/7/26
#  Copyright (c) 2024.

import subprocess


def execute_command(command):
    try:
        result = subprocess.run(command,
                                shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                universal_newlines=True)
        # 检查命令执行是否成功
        if result.returncode == 0:
            return result.stdout.strip(), True
        else:
            out = result.stderr.strip()
            if not out:
                out = result.stdout.strip()
            return out, False
    except Exception as e:
        return str(e), False
