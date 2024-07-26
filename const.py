#  Author: Peter1303
#  Date: 2024/7/26
#  Copyright (c) 2024.

safeline_container_name = 'safeline-pg'
script_path = './script/'
docker_script_path = '/run/'


class Script:
    attack_event_script = 'attack_event.sh'
    get_last_id_script = 'get_last_id.sh'
    watchdog_script = 'watchdog.sh'
    logger_script = 'logger.sh'

    attack_event_script_path = script_path + attack_event_script
    docker_attack_event_script_path = docker_script_path + attack_event_script

    get_last_id_script_path = script_path + get_last_id_script
    docker_get_last_id_script_path = docker_script_path + get_last_id_script

    watchdog_script_path = script_path + watchdog_script
    docker_watchdog_script_path = docker_script_path + watchdog_script

    logger_script_path = script_path + logger_script
    docker_logger_script_path = docker_script_path + logger_script


class Yml:
    last_id = 'last-id'
    server = 'server'
    host = 'host'
    port = 'port'
    path = 'path'
    header = 'header'
