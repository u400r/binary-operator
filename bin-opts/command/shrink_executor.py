import ast

from generator.python_generator import PythonGenerator
from command.executor import Executor


class ShrinkExecutor(Executor):
    @classmethod
    def exec(cls, input):
        return "Data"

    @classmethod
    def post(cls, output):
        PythonGenerator.delete(output)
