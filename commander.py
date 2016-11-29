#!/usr/bin/python

import sys
import subprocess
import string

args = sys.argv

command = args[1]

executors = {
    'local': 'LocalExecutor',
    'sequential': 'SequentialExecutor'
}

containers = {
    'webserver': 'webserver_1',
    'scheduler': 'scheduler_1',
    'fmeengine': 'fmeengine_1'
}

if command == 'start' or command == 'restart':
    compose_type = args[2] or 'local'
    tmpl = string.Template("Starting $composeType executor.")
    print(tmpl.substitute(composeType=compose_type))
    subprocess.call("docker-compose down && docker-compose -f docker-compose-" \
    + executors[compose_type] + ".yml up -d", shell=True)

elif command == 'ssh':
    cname = args[2] or 'webserver'
    tmpl = string.Template("Opening connection to local $cname container")
    print(tmpl.substitute(cname = cname))
    subprocess.call("docker exec -it dockerairflow_" \
    + containers[cname] + " /bin/bash", shell=True)

elif command == 'rebuild_image':
    print("DID YOU REMOVE THE IMAGE FIRST???")
    subprocess.call("docker build --rm --no-cache -t mrmaksimize/airflow .", shell=True)

elif command == 'remove_image':
    image_id = args[2]
    subprocess.call('docker rmi -f ' + image_id, shell=True)