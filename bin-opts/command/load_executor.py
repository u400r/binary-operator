import sys
from command.executor import Executor


class LoadExecutor(Executor):
    @classmethod
    def pre(cls, args):
        return args.structure

    @classmethod
    def exec(cls, input):
        buf = sys.stdin.buffer.read()
        d = input()
        d.load(buf)
        return d

    @classmethod
    def post(cls, output):
        print(output.to_dict())
