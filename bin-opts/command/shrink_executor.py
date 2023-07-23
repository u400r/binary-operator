import ast

from generator.python_generator import PythonGenerator
from command.executor import Executor


class ShrinkExecutor(Executor):
    @classmethod
    def pre(cls, args):
        return args.structure

    @classmethod
    def post(cls, output):
        PythonGenerator.delete(output)
