import argparse
from pathlib import Path

from .build import build_project
from .check import check_project
from .doctor import doctor_project
from .init_project import init_project
from .pdf_import import import_pdf
from .project_import import import_project
from .translation_memory import add_term


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="edt",
        description="Engineering Documents Toolkit",
    )
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("build", help="build the current EDT project")
    sub.add_parser("check", help="check generated project output")
    sub.add_parser("doctor", help="check configured external dependencies")
    sub.add_parser("init", help="initialize an EDT project")
    project_import = sub.add_parser("import", help="run the project import pipeline")
    project_import.add_argument("--manifest", default="edt/project.yml")
    imp = sub.add_parser("import-pdf", help="write PDF import notes")
    imp.add_argument("source")
    imp.add_argument("output")
    mem = sub.add_parser("tm-add", help="add a translation-memory term")
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
    elif args.command == "doctor":
        report = doctor_project(Path.cwd())
        print(report.to_text(), end="")
        raise SystemExit(0 if report.ready else 3)
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
