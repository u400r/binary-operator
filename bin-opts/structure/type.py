from __future__ import annotations
from abc import ABC
from typing import Callable, Sized


class TypeBase(ABC):

    def __init__(self, name=None):
        self.__name__ = name

    def raw(self) -> bytearray:
        pass

    def load(self, data: bytes, pos: int = 0):
        pass

    def dump(self) -> bytearray:
        pass

    def to_defs(self):
        if self.__name__:
            return {"name": self.__name__}
        else:
            return {}

    def __len__(self):
        pass

    def __str__(self):
        pass


class PrimitiveType(TypeBase):
    _size: int
    _format: Callable[[PrimitiveType, bytearray], str]
    _start: int
    _end: int

    def __init__(self, name=None):
        self.__name__ = name
        self._data = bytearray((0).to_bytes(self._size))

    def to_dict(self):
        return {self.__name__: self._format(self._data)} \
            if self.__name__ else self._format(self._data)

    def raw(self) -> bytearray:
        return self._data

    def load(self,  data: bytes, pos: int = 0):
        self._data[:] = data[pos:pos+self._size]

    def dump(self) -> bytearray:
        return self._data

    def to_defs(self):
        return {**super().to_defs(), **{"type": self.__class__.__name__}}

    def __len__(self):
        return self._size

    def __str__(self):
        return self.__class__.__name__


def singed_fromatter(t: PrimitiveType, data: bytearray):
    return data.hex()


def unsinged_fromatter(t: PrimitiveType, data: bytearray):
    return data.hex()


# builtin type definition
class Uint1(PrimitiveType):
    _size = 1
    _format = unsinged_fromatter


class Uint2(PrimitiveType):
    _size = 2
    _format = unsinged_fromatter


class Uint4(PrimitiveType):
    _size = 4
    _format = unsinged_fromatter


class Uint8(PrimitiveType):
    _size = 8
    _format = unsinged_fromatter


class Uint16(PrimitiveType):
    _size = 16
    _format = unsinged_fromatter


class Uint32(PrimitiveType):
    _size = 32
    _format = unsinged_fromatter


class Uint64(PrimitiveType):
    _size = 64
    _format = unsinged_fromatter


class ArrayType(TypeBase, Sized):

    def __init__(self, item, size, name=None):
        self.__name__ = name
        self._size = size
        # todo: must consider recursive tuple definition
        self._items = tuple(item() for i in range(self._size))

    def to_dict(self):
        children = []

        for item in self._items:
            children.append(item.to_dict())
        if self.__name__:
            return {self.__name__: children}
        else:
            return children

    def load(self, data: bytes, pos: int = 0):
        for item in self._items:
            item.load(data, pos)
            pos += len(item)

    def dump(self) -> bytearray:
        return b"".join([item.dump() for item in self._items])

    def raw(self):
        pass

    def to_defs(self):
        return {**super().to_defs(), **{
            "type": "array",
            "size": self._size,
            "items": self._items[0].to_defs()
        }}

    def __len__(self):
        return sum([len(item) for item in self._items])

    def __str__(self):
        return ""


class StructureType(TypeBase, Sized):
    _parameters: list[StructureType | ArrayType | PrimitiveType] = []

    def __init__(self, name=None):
        self.__name__ = name

    def load(self, data: bytes, pos: int = 0):
        for parameter in self._parameters:
            parameter.load(data, pos)
            pos += len(parameter)

    def dump(self):
        return b"".join([p.dump() for p in self._parameters])

    def raw(self):
        return b""

    def to_dict(self):
        children = {}
        for parameter in self._parameters:
            children.update(parameter.to_dict())
        if self.__name__:
            _dict = {self.__name__: children}
        else:
            _dict = children
        return _dict

    def to_defs(self):
        defs = {**super().to_defs(), **{
            "type": "object",
            "alias": self.__class__.__name__,
            "parameters": []
        }}
        for parameter in self._parameters:
            defs["parameters"].append(parameter.to_defs())
        return defs

    def __len__(self):
        return sum([len(p) for p in self._parameters])

    def __str__(self):
        return ""
    # binary -> instance: load
    # instance -> binary: dump
    # class -> yaml: definition
    # yaml -> class: ast.compile?
