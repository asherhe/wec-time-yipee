import argparse

from control import Control
from server import Server
from testing import Testing


def main():
    parser = argparse.ArgumentParser(
        prog="WEC2026",
        description="hip hip hooray!",
    )

    parser.add_argument(
        "--test", action=argparse.BooleanOptionalAction, help="run in test mode"
    )

    args = parser.parse_args()

    control = Control()

    if args.test:
        t = Testing(control)
        t.run()
    else:
        s = Server("127.0.0.1", 8800, control)
        s.run()


if __name__ == "__main__":
    main()
