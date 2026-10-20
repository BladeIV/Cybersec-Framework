"""Command-line entry point for NetGuardian."""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

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

    c_steps = case_sub.add_parser("steps", help="List a case's checklist with numbers.")
    c_steps.add_argument("name")

    c_check = case_sub.add_parser("check", help="Mark a checklist step done (or undo).")
    c_check.add_argument("name")
    c_check.add_argument("number", type=int, help="Step number from 'case steps'.")
    c_check.add_argument("--undo", action="store_true", help="Mark the step not done.")

    c_note = case_sub.add_parser("note", help="Add a note to a case.")
    c_note.add_argument("name")
    c_note.add_argument("text")

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
    from .triage import Case, CASES_DIR, list_cases, slugify

    if args.case_command == "new":
        case = Case.new(args.name, args.kind)
        try:
            path = case.save(exclusive=True)
        except FileExistsError:
            print(
                f"A case with the slug '{case.slug}' already exists. "
                f"Pick a different name, or edit it with 'case note'/'case check'."
            )
            return 1
        done, total = case.progress
        print(f"Created {args.kind} case '{args.name}' with {total} checklist steps.")
        print(f"Saved to {path}")
        return 0

    if args.case_command == "list":
        paths = list_cases()
        if not paths:
            print("No cases yet. Create one with: netguardian case new <name>")
            return 0
        for p in paths:
            case = Case.load(p)
            done, total = case.progress
            print(f"  {case.name}  [{case.kind}]  {done}/{total} done")
        return 0

    # The remaining commands all act on one existing case, located by slug.
    slug = slugify(args.name)
    path = CASES_DIR / f"{slug}.json"
    if not path.exists():
        print(f"No case named '{args.name}'. Try: netguardian case list")
        return 1
    case = Case.load(path)

    if args.case_command == "show":
        print(case.to_markdown())
        return 0

    if args.case_command == "steps":
        for n, item in enumerate(case.checklist, start=1):
            box = "x" if item.done else " "
            print(f"  {n:>2}. [{box}] {item.function}  {item.text}")
        return 0

    if args.case_command == "check":
        if not 1 <= args.number <= len(case.checklist):
            print(f"Step {args.number} is out of range (1-{len(case.checklist)}).")
            return 1
        item = case.checklist[args.number - 1]
        item.done = not args.undo
        case.save()
        state = "done" if item.done else "not done"
        print(f"Step {args.number} marked {state}: {item.text}")
        return 0

    if args.case_command == "note":
        case.add_note(args.text)
        case.save()
        print(f"Added note to '{case.name}'.")
        return 0

    if args.case_command == "export":
        out = (args.output and Path(args.output)) or Path(f"{slug}.md")
        if out.resolve() == path.resolve():
            print("Refusing to export over the case's own data file.")
            return 1
        try:
            _safe_write(out, case.to_markdown())
        except OSError as e:
            print(f"Could not write {out}: {e} (is it a symlink or protected?)")
            return 1
        print(f"Wrote report to {out}")
        return 0

    return 1


def _safe_write(path: Path, text: str) -> None:
    """Write UTF-8 text without following a symlink at the destination."""
    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags, 0o644)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(text)


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
