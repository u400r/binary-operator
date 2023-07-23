import sys
from .executor import Executor
from structure.definition import Definition
from generator.python_generator import PythonGenerator

import yaml


class GrowExecutor(Executor):

    @classmethod
    def exec(cls, input):
        buf = yaml.safe_load(sys.stdin.read())
        defs = []
        if isinstance(buf, list) or isinstance(buf, tuple):
            for element in buf:
                defs.append(Definition.load(**element))
        else:
            defs.append(Definition.load(**buf))
        return defs

    @classmethod
    def post(cls, output):
        for klass in output:
            PythonGenerator.generate(klass)
