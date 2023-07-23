from _ast import Assign, ImportFrom
import ast
from multiprocessing.util import is_exiting
import os
from pathlib import Path
from .generator import Generator


class InitAllTransformer(ast.NodeTransformer):

    def __init__(self, class_name, is_generate) -> None:
        self.class_name = class_name
        self.import_from = None
        self.is_generate = is_generate
        super().__init__()

    def visit_Assign(self, node: Assign):
        is_structures_assign = False
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "structures":
                is_structures_assign = True
        if not is_structures_assign:
            return node

        if not isinstance(node.value, ast.List):
            raise RuntimeError("generated.__init__ might be corrupted")
        class_elt = None
        for elt in node.value.elts:
            if elt.id == self.class_name:
                class_elt = elt

        if self.is_generate and not class_elt:
            node.value.elts.append(ast.Name(id=self.class_name, ctx=ast.Load()))
        elif not self.is_generate and class_elt:
            node.value.elts.remove(class_elt)

        return node

    def visit_ImportFrom(self, node: ImportFrom):
        if node.module == self.class_name:
            for name in node.names:
                if name.name == self.class_name:
                    self.import_from = node
        return node


class PythonGenerator(Generator):
    base_path = Path(__file__).parent.joinpath("../generated/")

    @classmethod
    def dumpast(cls, class_ast, path, debug=True):
        if debug:
            print(ast.dump(class_ast, indent=4))
        with open(path, "w") as f:
            f.write(ast.unparse(class_ast))

    @classmethod
    def loadast(cls, path):
        with open(file=path, mode="r") as f:
            return ast.parse(f.read())

    @classmethod
    def generate(cls, klass):
        # generate python script according to definition
        classdefs = klass.to_ast_node()
        class_ast = ast.Module(
            body=[
                ast.ImportFrom(
                    module='structure.type', names=[ast.alias(name='StructureType'), ast.alias(name='ArrayType')], level=0),
                ast.ImportFrom(
                    module='structure.definition', names=[ast.alias(name='*')], level=0),
                classdefs],
            type_ignores=[]
        )
        ast.fix_missing_locations(class_ast)
        path = cls.base_path.joinpath(f"{klass.alias}.py")
        cls.dumpast(class_ast, path)

        # update __init__.py
        init_file_path = cls.base_path.joinpath("__init__.py")
        init_ast = cls.loadast(init_file_path)
        trans = InitAllTransformer(klass.alias, True)

        # update structures
        trans.visit(init_ast)
        # insert import sentense if not exists
        if not trans.import_from:
            init_ast.body.insert(0, ast.ImportFrom(
                module=klass.alias, names=[ast.alias(name=klass.alias)], level=1))
        cls.dumpast(init_ast, init_file_path)

    @classmethod
    def delete(cls, klass_name):
        path = cls.base_path.joinpath("__init__.py")
        init_ast = cls.loadast(path)
        trans = InitAllTransformer(klass_name, False)
        trans.visit(node=init_ast)

        if trans.import_from:
            init_ast.body.remove(trans.import_from)
        cls.dumpast(init_ast, path)
        os.remove(cls.base_path.joinpath(f"{klass_name}.py"))
