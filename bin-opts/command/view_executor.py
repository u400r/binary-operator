
from command.executor import Executor
import generated


class ViewExecutor(Executor):
    @classmethod
    def exec(cls, input):
        if not generated.structures:
            print("No structure definition found.")
        for structure in generated.structures:
            print(structure.__name__)
