
import yaml
from command.executor import Executor


class ShowExecutor(Executor):
    @classmethod
    def pre(cls, args):
        return args.structure

    @classmethod
    def exec(cls, input):
        print(yaml.dump(input().to_defs()))
