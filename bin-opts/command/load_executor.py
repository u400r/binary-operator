from command.executor import Executor
import generated


class LoadExecutor(Executor):
    @classmethod
    def pre(cls):
        return "Data"

    @classmethod
    def exec(cls, input):
        for data in generated.structures:
            if data.__name__ == input:
                d = data()
                d.load((0x0).to_bytes(length=248))
                return d

    @classmethod
    def post(cls, output):
        print(output.to_dict())
