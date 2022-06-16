# cython: language_level=3
import cython

import json
import typing


@cython.cfunc
@cython.returns(object)
def c_loads_list(l: list, cls: typing.Type):
    res = []
    if type(cls) is typing._GenericAlias:
        origin = cls.__origin__
        if origin is not list:
            return None
        args = cls.__args__
        if len(args) != 1:
            return res
        sub_type: typing.Type = args[0]
        for i in l:
            if type(i) is dict:
                sub_obj = c_loads_dict(i, sub_type)
                res.append(sub_obj)
    return res


@cython.cfunc
@cython.returns(object)
def c_loads_dict(d: dict, cls: typing.Type):
    if type(cls) is typing._GenericAlias:
        origin = cls.__origin__
        if origin is not dict:
            return None
        res = {}
        args = cls.__args__
        if len(args) != 2:
            return res
        key_type = args[0]
        val_type = args[1]
        for key, val in d.items():
            if type(val) is dict:
                res.update({
                    key: c_loads_dict(val, val_type)
                })
        return res
    if not hasattr(cls, "__annotations__"):
        return None
    res = cls.__new__(cls)
    for name, val_type in cls.__annotations__.items():
        value = d.get(name)
        if type(value) is val_type:
            setattr(res, name, value)
        if type(value) is list:
            value = c_loads_list(value, val_type)
            setattr(res, name, value)
        if type(value) is dict:
            value = c_loads_dict(value, val_type)
            setattr(res, name, value)
    return res


def loads(s: str, cls: typing.Type = None):
    list_or_dict = json.loads(s)
    if cls is None or cls is list or cls is dict:
        return list_or_dict
    if type(list_or_dict) is list:
        return c_loads_list(list_or_dict, cls)
    else:
        return c_loads_dict(list_or_dict, cls)
