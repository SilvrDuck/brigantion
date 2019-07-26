from requests
from box import Box
import json
import cfg




post('http://localhost:5000/monitor/', json={'input': 'this is a test'})


def report_error(hosts, msg):
    post(f'{hosts.monitor}/{cfg.rte.report_error}', json=TODO_HERE)

if __name__ == '__main__':
    hosts = Box({'server': server_host, 'monitor': monitor_host})

    while True:
        try:

        except Exception as e:
            report_error(hosts, e)
