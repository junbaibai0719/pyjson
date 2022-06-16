import json
import typing

import pyjson, pyjson1
from utils import timer


class Test:
    id: int
    name: str
    num: int


test_json_str = json.dumps({
    "o": {
        "id": 1,
        "name": "dsad",
        "num": 123
    },
    "2": {
        "id": 1,
        "name": "dsad",
        "num": 123
    },
    "o3": {
        "id": 1,
        "name": "dsad",
        "num": 123
    }
})

test_json_str1 = json.dumps([
    {
        "id": 1,
        "name": "dsad",
        "num": 123
    },
    {
        "id": 1,
        "name": "dsad",
        "num": 123
    },
    {
        "id": 1,
        "name": "dsad",
        "num": 123
    }
])


@timer.repeat(10 ** 6)
def test():
    t = pyjson.loads(test_json_str, typing.Dict[str, Test])


@timer.repeat(10 ** 6)
def test1():
    t = pyjson1.loads(test_json_str, typing.Dict[str, Test])


@timer.repeat(10 ** 6)
def test_json():
    t = json.loads(test_json_str1)


t = test()
test1()
test_json()


@timer.repeat(10 ** 6)
def test():
    t = pyjson.loads(test_json_str1, typing.List[Test])


@timer.repeat(10 ** 6)
def test1():
    t = pyjson1.loads(test_json_str1, typing.List[Test])


@timer.repeat(10 ** 6)
def test_json():
    t = json.loads(test_json_str1)


test()
test1()
test_json()
