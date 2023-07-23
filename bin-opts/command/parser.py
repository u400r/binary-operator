# definition敬
# grow -> yamlを読み込んで自身を成長させる
# shrink -> 自分に取り込んでいる定義を削除
# view -> 現在取り込まれているデータ構造の定義をdump
# init -> 初期状態に戻す

# update -> binaryの一部を更新
# dump -> 何かから読み込んだbinaryを標準出力にdump。データ構造 -> binary
# load -> 標準入力から読み込んだbinaryを何かにload。binary -> データ構造

from argparse import ArgumentParser

from command.show_executor import ShowExecutor

from command.view_executor import ViewExecutor
from command.shrink_executor import ShrinkExecutor
from command.grow_executor import GrowExecutor


def define_parser():

    parser = ArgumentParser(prog="Binary Operator")
    subparser = parser.add_subparsers()
    grow = subparser.add_parser("grow")
    shrink = subparser.add_parser("shrink")
    list = subparser.add_parser(name="list")
    show = subparser.add_parser(name="show")
    defs = subparser.add_parser("defs")
    dump = subparser.add_parser("dump")
    load = subparser.add_parser("load")

    grow.set_defaults(handler=GrowExecutor.do)
    shrink.set_defaults(handler=ShrinkExecutor.do)
    list.set_defaults(handler=ViewExecutor.do)
    show.set_defaults(handler=ShowExecutor.do)

    return parser
