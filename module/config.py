#  Author: Peter1303
#  Date: 2024/7/26
#  Copyright (c) 2024.

import yaml
import os

import const


class Config:
    default_config = {
        const.Yml.last_id: None,
        const.Yml.server: {
            const.Yml.host: None,
            const.Yml.port: None,
            const.Yml.path: None
        }
    }

    def __init__(self, config_path, name):
        self.file_path = config_path + name
        # 如果路径不存在那么新建
        if not os.path.exists(config_path):
            os.mkdir(config_path)
        # 如果文件不存在那么创建
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                yaml.dump(self.default_config, f)
        self.data = {}
        self.load()

    def load(self):
        with open(self.file_path, 'r') as f:
            self.data = yaml.safe_load(f)

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        with open(self.file_path, 'w') as f:
            yaml.dump(self.data, f)
