import argparse
from pathlib import Path

from .build import build_project
from .check import check_project
from .init_project import init_project
from .pdf_import import import_pdf
from .project_import import import_project
from .translation_memory import add_term


def main() -> None:
    parser = argparse.ArgumentParser(prog="edt")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("build")
    sub.add_parser("check")
    sub.add_parser("init")
    project_import = sub.add_parser("import")
    project_import.add_argument("--manifest", default="edt/project.yml")
    imp = sub.add_parser("import-pdf")
    imp.add_argument("source")
    imp.add_argument("output")
    mem = sub.add_parser("tm-add")
    mem.add_argument("database")
    mem.add_argument("source")
    mem.add_argument("target")
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
    elif args.command == "import":
        result = import_project(Path.cwd(), Path(args.manifest))
        print(f"wrote {result.report_path}")
    elif args.command == "import-pdf":
        import_pdf(Path(args.source), Path(args.output))
    elif args.command == "tm-add":
        add_term(Path(args.database), args.source, args.target)


if __name__ == "__main__":
    main()
