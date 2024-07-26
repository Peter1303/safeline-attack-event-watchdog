#  Author: Peter1303
#  Date: 2024/7/26
#  Copyright (c) 2024.

import logging

# 创建一个日志记录器
logger = logging.getLogger('Watchdog')
# 设置日志记录等级
logger.setLevel(logging.INFO)
# 创建一个控制台日志处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
# 定义日志格式
formatter = logging.Formatter('%(asctime)s [%(levelname)s] | %(message)s',
                              datefmt='%Y/%m/%d %H:%M:%S')
# 设置日志格式
console_handler.setFormatter(formatter)
# 将日志处理器添加到日志记录器
logger.addHandler(console_handler)
