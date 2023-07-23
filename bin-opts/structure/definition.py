

from __future__ import annotations
from ast import AnnAssign, Assign, Attribute, Call, ClassDef, Constant, FunctionDef, List, Load, Name, Param, Pass, Store, Subscript, Tuple, arg, arguments

from structure.type import TypeBase, PrimitiveType, ArrayType, StructureType
from structure.type import Uint1, Uint2, Uint4, Uint8, Uint16, Uint32, Uint64


import yaml


class Definition():
    """Represent data structure definition

    TODO: It is needed to change to hold structure classes inside of class variable,
    and each StructureDefinition instance only has a reference to the list.
    each definition should be a singlton instance.
    """
    name: str
    type: TypeBase

    def __init__(self, **kwargs):
        if "type" not in kwargs:
            raise TypeError("type key does not exists")
        if "name" in kwargs:
            self.name = kwargs["name"]
        else:
            self.name = "aaa"

    def to_dict(self):
        print(self.name)
        return {
            "name": self.name
        }

    @classmethod
    def load(cls, **kwargs):
        if "type" not in kwargs:
            raise TypeError("type key does not exists")

        if kwargs["type"] == "object":
            return StructureDefinition(**kwargs)
        elif kwargs["type"] == "array":
            return ArrayDefinition(**kwargs)
        else:
            return PrimitiveDefinition(**kwargs)

    def dump(self):
        print(yaml.dump(self.to_dict()))

    def to_ast_node(self):
        pass


class PrimitiveDefinition(Definition):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if issubclass(globals()[kwargs["type"]], PrimitiveType):
            self.type = globals()[kwargs["type"]]
        else:
            raise TypeError("invalid primitive type")

    def to_dict(self):
        return dict(super().to_dict(), **{
            "type": self.type.__name__
        })

    def instantiate(self):
        return Call(
            func=Name(id=self.type.__name__, ctx=Load()),
            args=[Constant(value=self.name)], keywords=[]
        )


class ArrayDefinition(Definition):
    items: StructureDefinition | ArrayDefinition | PrimitiveDefinition
    size: int

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if kwargs["type"] != 'array':
            raise TypeError("invalid array type")
        else:
            self.type = ArrayType

        if "items" not in kwargs:
            raise TypeError("items key does not exists")

        if "size" not in kwargs:
            raise TypeError("size key does not exists")

        self.items = Definition.load(**kwargs["items"])
        self.size = kwargs["size"]

    def to_dict(self):
        _dict = dict(super().to_dict(), **{
            "type": "array",
            "size": self.size
        })
        _dict["items"] = self.items.to_dict()
        return _dict

    def to_ast_node(self):
        return self.items.to_ast_node()

    def instantiate(self):
        return Call(
            func=Name(id="ArrayType", ctx=Load()),
            args=[
                Attribute(
                    value=Name(id='self', ctx=Load()),
                    attr=self.items.alias, ctx=Load()
                )
                if isinstance(self.items, StructureDefinition)
                else Name(id=self.items.type.__name__, ctx=Load()),
                Constant(value=self.size), Constant(value=self.name)],
            keywords=[]
        )


class StructureDefinition(Definition):
    alias: str
    parameters: list[StructureDefinition | ArrayDefinition | PrimitiveDefinition] = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if kwargs['type'] != 'object':
            raise TypeError('invalid object type')

        if "alias" not in kwargs:
            raise TypeError("alias key does not exists")

        if "parameters" not in kwargs:
            raise TypeError("parameters key does not exists")

        if not isinstance(kwargs['parameters'], list):
            raise TypeError("parameters is not list type")

        self.alias = kwargs["alias"]
        # it is impossible to be forward defining the custom structure class
        # so assing base class of structure.
        self.type = StructureType
        self.parameters = []
        for p in kwargs["parameters"]:
            self.parameters.append(Definition.load(**p))

    def to_dict(self):
        _dict = dict(super().to_dict(), **{
            "type": "object",
            "alias": self.alias,
            "parameters": []
        })
        for parameter in self.parameters:
            _dict["parameters"].append(parameter.to_dict())
        return _dict

    def make_constructor(self):
        return FunctionDef(
            name='__init__',
            args=arguments(
                posonlyargs=[],
                args=[arg(arg='self'), arg(arg='name')],
                kwonlyargs=[],
                kw_defaults=[],
                defaults=[Constant(value=None)]),
            body=[
                Assign(
                    targets=[
                        Attribute(
                            value=Name(id='self', ctx=Load()),
                            attr=p.name,
                            ctx=Store())
                    ],
                    value=p.instantiate()
                ) for p in self.parameters] + [
                Assign(
                    targets=[
                        Attribute(value=Name(id='self', ctx=Load()),
                                  attr='_parameters', ctx=Store())
                    ],
                    value=List(
                        elts=[Attribute(
                            value=Name(id='self', ctx=Load()),
                            attr=p.name,
                            ctx=Load()) for p in self.parameters],
                        ctx=Load()
                    )
                ),
                Assign(
                    targets=[
                        Attribute(value=Name(id='self', ctx=Load()),
                                  attr='__name__', ctx=Store())
                    ],
                    value=Name(id='name', ctx=Load()),
                    ctx=Load()
                )
            ],
            decorator_list=[])

    def to_ast_node(self) -> ClassDef:
        return ClassDef(
            name=self.alias,
            body=[p.to_ast_node() for p in self.parameters if p.to_ast_node()] + [
                self.make_constructor()],
            decorator_list=[],
            bases=[
                Name(id='StructureType', ctx=Load())
            ],
            keywords=[],
        )

    def instantiate(self):
        return Call(
            func=Attribute(
                value=Name(id='self', ctx=Load()),
                attr=self.alias, ctx=Load()),
            args=[Constant(value=self.name)], keywords=[]
        )
