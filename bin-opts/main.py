
from command.parser import define_parser
from command.shrink_executor import ShrinkExecutor
from command.grow_executor import GrowExecutor
from command.view_executor import ViewExecutor


def main():

    parser = define_parser()
    args = parser.parse_args()
    if hasattr(args, 'handler'):
        args.handler(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
