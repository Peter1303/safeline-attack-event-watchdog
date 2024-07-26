#  Author: Peter1303
#  Date: 2024/7/26
#  Copyright (c) 2024.

import argparse
import os
import time
import requests

import const
import module.config
import module.docker_script as docker_script
from module.commander import *
from module.logger import *
from module.datetime_util import *

interval = 1
max_script_release_count = 10
last_event_id = 0


def log_lines(banner):
    for line in banner.split('\n'):
        logger.info(line)


def log_banner():
    text = '''
     __        __    _       _         _             
 \ \      / /_ _| |_ ___| |__   __| | ___   __ _ 
  \ \ /\ / / _` | __/ __| '_ \ / _` |/ _ \ / _` |
   \ V  V / (_| | || (__| | | | (_| | (_) | (_| |
    \_/\_/ \__,_|\__\___|_| |_|\__,_|\___/ \__, |
                                           |___/ 
    '''
    log_lines(text)
    logger.info('Author: Peter1303')
    logger.info('')


def parse_args():
    # 创建解析器
    parser = argparse.ArgumentParser(description='Watchdog 雷池看门狗')
    # 添加参数
    parser.add_argument('--interval', type=int, help='扫描攻击事件间隔（秒）', default=1)
    # 解析参数
    return parser.parse_args()


def check_docker_installed():
    """
    检查是否安装 Docker
    :return:
    """
    out, ok = execute_command('which docker')
    if not ok:
        logger.error('未安装 Docker')
        exit(1)


def check_safeline_pg_installed():
    """
    检查是否安装雷池
    :return:
    """
    out, ok = execute_command(f'docker inspect {const.safeline_container_name}')
    if not ok:
        logger.error('雷池容器不存在')
        exit(1)
    logger.info('发现雷池 PG 容器')


def get_last_id_from_pg():
    """
    获取最近的攻击事件 ID
    :return:
    """
    out, ok = docker_script.run_script(const.Script.docker_get_last_id_script_path)
    if ok:
        try:
            return int(out)
        except ValueError:
            ok = False
    if not ok:
        logger.error('获取最近的攻击事件 ID 失败')
        exit(1)


def handle_docker_scripts():
    def check_cp_script(script_path, docker_script_path):
        ok = docker_script.copy_script(script_path, docker_script_path)
        if not ok:
            logger.warning(f'复制脚本失败 {script_path}')
        else:
            logger.info(f'复制脚本成功 {script_path}')
        return ok

    def check_modify_permission(docker_script_path):
        ok = docker_script.modify_script_permission(docker_script_path)
        if not ok:
            logger.warning(f'修改权限失败 {docker_script_path}')
        else:
            logger.info(f'修改权限成功 {docker_script_path}')
        return ok

    # 处理获取 ID 脚本
    ok_cp_id = check_cp_script(const.Script.get_last_id_script_path,
                               const.Script.docker_get_last_id_script_path)
    ok_id_mod = check_modify_permission(const.Script.docker_get_last_id_script_path)

    # 处理输出攻击事件脚本
    ok_aec = check_cp_script(const.Script.attack_event_script_path,
                             const.Script.docker_attack_event_script_path)
    ok_aec_mod = check_modify_permission(const.Script.docker_attack_event_script_path)

    # 处理日志脚本
    ok_lsp = check_cp_script(const.Script.logger_script_path,
                             const.Script.docker_logger_script_path)
    ok_mod_lsp = check_modify_permission(const.Script.docker_logger_script_path)
    return ok_cp_id and ok_id_mod and ok_aec and ok_aec_mod and ok_lsp and ok_mod_lsp


def push_events(events):
    global config
    server = config.get(const.Yml.server)
    host = server.get(const.Yml.host, '')
    port = server.get(const.Yml.port, 0)
    path = server.get(const.Yml.path, '')
    header = server.get(const.Yml.header, {})
    if host:
        try:
            url = host
            if port:
                url += f':{port}'
            if path:
                if not path.startswith('/'):
                    path += '/'
                url += path
            logger.info(f'推送攻击事件...')
            resp = requests.post(url, headers=header, json=events)
            if resp.status_code != 200:
                logger.error(f'推送攻击事件失败 [{resp.status_code}] | {resp.text}')
                return False
            logger.info(f'推送攻击事件 {len(events)} 条 [SUCCESS]')
            return True
        except Exception as e:
            logger.error(f'推送攻击事件失败 | {e}')
            return False


def scanning_attack_event():
    """
    扫描攻击事件
    :return:
    """
    global interval, max_script_release_count, last_event_id
    script_release_counter = 0
    while running:
        time.sleep(interval)
        # 获取最近的攻击事件 ID
        pg_last_id = get_last_id_from_pg()
        last_id = config.get(const.Yml.last_id, pg_last_id)
        # 如果没有记录过 ID 位置那么保存
        if not last_id:
            last_id = pg_last_id
            config.set(const.Yml.last_id, last_id)
        total = pg_last_id - last_id
        if total < 0:
            logger.error('请不要使用时间倒流技能')
            exit(1)
        if total:
            if pg_last_id != last_event_id:
                logger.info(f'获取攻击事件 {total} 条')
                last_event_id = pg_last_id
                out, ok = docker_script.run_script(const.Script.docker_attack_event_script_path,
                                                   f'{const.docker_script_path} {last_id}')
                if not ok:
                    if 'no such' in out.lower():
                        if script_release_counter > max_script_release_count:
                            logger.error('脚本释放多次失败')
                            exit(1)
                        script_release_counter += 1
                        handle_docker_scripts()
                        logger.warning(f'重新释放脚本 [{script_release_counter}/{max_script_release_count}]')
                        time.sleep(3)
                        continue
                    else:
                        logger.error('获取攻击事件失败')
                        exit(1)
                lines = out.split('\n')
                lines = [line.strip() for line in lines if line]
                events = []
                # 转换输出为对象
                for line in lines:
                    fields = line.split('|')
                    fields = [field.strip() for field in fields if field]
                    index = 0

                    def increase_and_get():
                        nonlocal index
                        try:
                            return index
                        finally:
                            index += 1

                    item = {
                        'time': format_timestamp(int(fields[increase_and_get()])),
                        'from': fields[increase_and_get()],
                        'ip': fields[increase_and_get()],
                        'target': fields[increase_and_get()],
                        'path': fields[increase_and_get()],
                        'rule_id': fields[increase_and_get()],
                        'id': int(fields[increase_and_get()])
                    }
                    events.append(item)
                if push_events(events):
                    # 记录最近的 ID
                    config.set(const.Yml.last_id, pg_last_id)


if __name__ == '__main__':
    global config
    running = True
    try:
        log_banner()
        args = parse_args()
        check_docker_installed()
        check_safeline_pg_installed()
        curr_path = os.path.dirname(os.path.abspath(__file__))
        config = module.config.Config(f'{curr_path}/config/', 'config.yaml')
        interval = args.interval
        if not handle_docker_scripts():
            logger.error('脚本释放失败')
            exit(1)
        scanning_attack_event()
    except KeyboardInterrupt:
        running = False
        log_lines('''
     / \__
    (    @\___
     /         O
    /   (_____/
    /_____/   U
        ''')
