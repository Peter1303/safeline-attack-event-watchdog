#  Author: Peter1303
#  Date: 2024/7/26
#  Copyright (c) 2024.

from datetime import datetime


def format_timestamp(timestamp):
    dt_object = datetime.utcfromtimestamp(timestamp)
    formatted_date_string = dt_object.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_date_string
