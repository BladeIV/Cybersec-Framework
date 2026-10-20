"""Command-line entry point for NetGuardian."""
from __future__ import annotations

import argparse
import sys

from . import __version__


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="netguardian",
        description="Open-source security tool catalog & triage framework (TUI).",
    )
    parser.add_argument("--version", action="version", version=f"netguardian {__version__}")
    parser.add_argument(
        "--web",
        action="store_true",
        help="Serve the app in a web browser instead of the terminal.",
    )
    parser.add_argument(
        "--port", type=int, default=8000, help="Port for --web mode (default 8000)."
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="Print the catalog as text and exit (no TUI).",
    )

    sub = parser.add_subparsers(dest="command")
    case = sub.add_parser("case", help="Manage triage cases.")
    case_sub = case.add_subparsers(dest="case_command", required=True)

    c_new = case_sub.add_parser("new", help="Start a new case.")
    c_new.add_argument("name")
    c_new.add_argument("--kind", choices=["incident", "pentest"], default="incident")

    case_sub.add_parser("list", help="List saved cases.")

    c_show = case_sub.add_parser("show", help="Print a case as Markdown.")
    c_show.add_argument("name")

    c_export = case_sub.add_parser("export", help="Write a case report to a file.")
    c_export.add_argument("name")
    c_export.add_argument("-o", "--output", help="Output path (default <slug>.md).")

    args = parser.parse_args(argv)

    if args.command == "case":
        return _handle_case(args)

    if args.list:
        return _print_catalog()

    if args.web:
        return _serve_web(args.port)

    from .app import NetGuardianApp

    NetGuardianApp().run()
    return 0


def _handle_case(args) -> int:
    from .triage import Case, CASES_DIR, list_cases

    if args.case_command == "new":
        case = Case.new(args.name, args.kind)
        path = case.save()
        done, total = case.progress
        print(f"Created {args.kind} case '{args.name}' with {total} checklist steps.")
        print(f"Saved to {path}")
        return 0

    if args.case_command == "list":
        paths = list_cases()
        if not paths:
            print(f"No cases yet. Create one with: netguardian case new <name>")
            return 0
        for p in paths:
            case = Case.load(p)
            done, total = case.progress
            print(f"  {case.name}  [{case.kind}]  {done}/{total} done")
        return 0

    # show / export both need to locate the case by slug.
    slug = "".join(c if c.isalnum() else "-" for c in args.name.lower()).strip("-")
    path = CASES_DIR / f"{slug}.json"
    if not path.exists():
        print(f"No case named '{args.name}'. Try: netguardian case list")
        return 1
    case = Case.load(path)

    if args.case_command == "show":
        print(case.to_markdown())
        return 0

    if args.case_command == "export":
        import pathlib

        out = pathlib.Path(args.output or f"{slug}.md")
        out.write_text(case.to_markdown())
        print(f"Wrote report to {out}")
        return 0

    return 1


def _print_catalog() -> int:
    from .loader import load_catalog

    catalog = load_catalog()
    for fn in catalog.functions:
        print(f"\n== {fn.code} · {fn.name} ==")
        for cat in fn.categories:
            print(f"  {cat.name}")
            for tool in cat.tools:
                teams = "/".join(tool.teams)
                print(f"    - {tool.name} [{teams}] — {tool.url}")
    return 0


def _serve_web(port: int) -> int:
    try:
        from textual_serve.server import Server
    except ImportError:
        print(
            "Web mode needs textual-serve. Install it with:\n"
            "    pipx inject netguardian textual-serve\n"
            "or: pip install textual-serve",
            file=sys.stderr,
        )
        return 1

    server = Server("python -m netguardian.app", port=port)
    print(f"Serving NetGuardian at http://localhost:{port}")
    server.serve()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
