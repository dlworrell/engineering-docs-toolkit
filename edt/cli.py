import argparse
from pathlib import Path

from .build import build_project
from .init_project import init_project


def main() -> None:
    parser = argparse.ArgumentParser(prog="edt")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("build")
    sub.add_parser("init")
    args = parser.parse_args()
    if args.command in (None, "build"):
        build_project()
    elif args.command == "init":
        init_project(Path.cwd())


if __name__ == "__main__":
    main()
