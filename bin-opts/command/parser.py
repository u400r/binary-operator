# definition敬
# grow -> yamlを読み込んで自身を成長させる
# shrink -> 自分に取り込んでいる定義を削除
# view -> 現在取り込まれているデータ構造の定義をdump
# init -> 初期状態に戻す

# update -> binaryの一部を更新
# dump -> 何かから読み込んだbinaryを標準出力にdump。データ構造 -> binary
# load -> 標準入力から読み込んだbinaryを何かにload。binary -> データ構造

from argparse import Action, ArgumentError, ArgumentParser

from command.load_executor import LoadExecutor
from command.dump_executor import DumpExecutor
from command.show_executor import ShowExecutor
from command.view_executor import ViewExecutor
from command.shrink_executor import ShrinkExecutor
from command.grow_executor import GrowExecutor
import generated


class ValidateStructure(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        for structure in generated.structures:
            if structure.__name__ == values:
                setattr(namespace, self.dest, structure)
                break
        else:
            raise ArgumentError(self, "No such structure found.")


def define_parser():

    parser = ArgumentParser(prog="Binary Operator")
    subparser = parser.add_subparsers()
    grow = subparser.add_parser("grow")
    shrink = subparser.add_parser("shrink")
    list = subparser.add_parser(name="list")
    show = subparser.add_parser(name="show")
    dump = subparser.add_parser("dump")
    load = subparser.add_parser("load")

    grow.set_defaults(handler=GrowExecutor.do)
    shrink.add_argument('-s', '--structure', type=str, action=ValidateStructure)
    shrink.set_defaults(handler=ShrinkExecutor.do)
    list.set_defaults(handler=ViewExecutor.do)
    show.add_argument('-s', '--structure', type=str, action=ValidateStructure)
    show.set_defaults(handler=ShowExecutor.do)

    dump.add_argument('-s', '--structure', type=str, action=ValidateStructure)
    dump.set_defaults(handler=DumpExecutor.do)
    load.add_argument('-s', '--structure', type=str, action=ValidateStructure)
    load.set_defaults(handler=LoadExecutor.do)

    return parser
