
import yaml
from command.executor import Executor
import generated


class ShowExecutor(Executor):
    @classmethod
    def exec(cls, input):
        if not generated.structures:
            print("No structure definition found.")
        for structure in generated.structures:
            print(yaml.dump(structure().to_defs()))
