from command.executor import Executor


class DumpExecutor(Executor):
    @classmethod
    def pre(cls, args):
        return args.structure

    @classmethod
    def exec(cls, input):
        return input().dump()

    @classmethod
    def post(cls, output):
        print(output)
