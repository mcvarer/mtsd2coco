from addict import Dict
import json
import uuid


def config_reader(path: str) -> Dict:
    with open(path) as f:
        cfg = json.load(f)

    return Dict(cfg)


def id_generator():
    return uuid.uuid1().int % 10000000000

