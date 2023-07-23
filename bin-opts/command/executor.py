

class Executor:
    @classmethod
    def pre(cls, args):
        pass

    @classmethod
    def exec(cls, input):
        raise NotImplementedError

    @classmethod
    def post(cls, output):
        pass

    @classmethod
    def do(cls, args):
        input = cls.pre(args)
        output = cls.exec(input)
        cls.post(output)


class LoadExecutor(Executor):
    @classmethod
    def exec(cls, input):
        pass
