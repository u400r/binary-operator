

class Executor:
    @classmethod
    def pre(cls):
        pass

    @classmethod
    def exec(cls, input):
        raise NotImplementedError

    @classmethod
    def post(cls, output):
        pass

    @classmethod
    def do(cls):
        input = cls.pre()
        output = cls.exec(input)
        cls.post(output)


class LoadExecutor(Executor):
    @classmethod
    def exec(cls, input):
        pass
