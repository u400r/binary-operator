import sys
from .executor import Executor
from structure.definition import Definition
from generator.python_generator import PythonGenerator

import yaml


class GrowExecutor(Executor):
    @classmethod
    def pre(cls):
        buf = sys.stdin.read()
        return yaml.safe_load(buf)

    @classmethod
    def exec(cls, input):
        defs = []
        if isinstance(input, list) or isinstance(input, tuple):
            for element in input:
                defs.append(Definition.load(**element))
        else:
            defs.append(Definition.load(**input))
        return defs

    @classmethod
    def post(cls, output):
        for klass in output:
            PythonGenerator.generate(klass)
