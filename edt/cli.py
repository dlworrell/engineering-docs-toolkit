import argparse
from pathlib import Path

from .build import build_project
from .check import check_project
from .init_project import init_project
from .pdf_import import import_pdf


def main() -> None:
    parser = argparse.ArgumentParser(prog="edt")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("build")
    sub.add_parser("check")
    sub.add_parser("init")
    imp = sub.add_parser("import-pdf")
    imp.add_argument("source")
    imp.add_argument("output")
    args = parser.parse_args()
    if args.command in (None, "build"):
        build_project()
    elif args.command == "check":
        issues = check_project(Path.cwd())
        for issue in issues:
            print(issue)
        raise SystemExit(1 if issues else 0)
    elif args.command == "init":
        init_project(Path.cwd())
    elif args.command == "import-pdf":
        import_pdf(Path(args.source), Path(args.output))


if __name__ == "__main__":
    main()
