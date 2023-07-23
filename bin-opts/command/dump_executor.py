from command.executor import Executor
import generated


class DumpExecutor(Executor):
    @classmethod
    def pre(cls):
        return "Data"

    @classmethod
    def exec(cls, input):
        for data in generated.structures:
            if data.__name__ == input:
                return data().dump()

    @classmethod
    def post(cls, output):
        print(output)
