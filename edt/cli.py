import argparse

from .build import build_project


def main() -> None:
    parser = argparse.ArgumentParser(prog="edt")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("build")
    args = parser.parse_args()
    if args.command in (None, "build"):
        build_project()


if __name__ == "__main__":
    main()
