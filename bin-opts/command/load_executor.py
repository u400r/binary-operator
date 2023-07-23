from command.executor import Executor


class LoadExecutor(Executor):
    @classmethod
    def pre(cls, args):
        return args.structure

    @classmethod
    def exec(cls, input):
        d = input()
        d.load((0x0).to_bytes(length=248))
        return d

    @classmethod
    def post(cls, output):
        print(output.to_dict())
