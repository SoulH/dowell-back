import os
import re


def from_database_url(conn_str: str):
    pattern = r'(\w+)://((\w+):(\w+)@)*(\w+):(\d+)(/(\w+))*'
    res = re.findall(pattern, conn_str)[0]
    return {k: v for k, v in {
        'ENGINE': res[0],
        'NAME': res[7],
        'ENFORCE_SCHEMA': False,
        'CLIENT': {
            'username': res[2],
            'password': res[3],
            'host': res[4],
            'port': res[5],
        }
    }.items() if v}


def get_environ_databases(suffix: str = None):
    names = (k for k in os.environ.keys() if k.endswith(suffix))

    def db_name(name: str):
        return name.replace(suffix, '').lower()

    def db_cfg(name: str):
        return from_database_url(os.environ[name])
    # return {}
    return {db_name(k): db_cfg(k) for k in names}
